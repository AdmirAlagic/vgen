#!/usr/bin/env python3
"""
Revolutionary Advanced Particle Systems
Implements SPH fluid dynamics, cloth simulation, smoke, and advanced physics
"""

import numpy as np
import numba
from numba import jit, cuda
import math
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
import threading
import queue
from scipy.spatial import cKDTree
import moderngl as mgl

# Try to import GPU acceleration libraries
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False

try:
    import taichi as ti
    TAICHI_AVAILABLE = True
except ImportError:
    TAICHI_AVAILABLE = False

class ParticleType(Enum):
    """Types of particles in the system"""
    FLUID = "fluid"
    SMOKE = "smoke"
    FIRE = "fire"
    CLOTH = "cloth"
    SPARK = "spark"
    ENERGY = "energy"
    PLASMA = "plasma"

@dataclass
class ParticleProperties:
    """Physical properties of a particle"""
    mass: float = 1.0
    radius: float = 0.1
    density: float = 1000.0
    viscosity: float = 0.01
    surface_tension: float = 0.0728
    restitution: float = 0.8
    friction: float = 0.1
    temperature: float = 293.15  # Kelvin
    color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    life_span: float = 10.0
    audio_reactivity: float = 1.0

@dataclass 
class SimulationSettings:
    """Simulation configuration"""
    max_particles: int = 100000
    time_step: float = 0.016  # 60 FPS
    gravity: Tuple[float, float, float] = (0.0, -9.81, 0.0)
    boundary_min: Tuple[float, float, float] = (-10.0, -10.0, -10.0)
    boundary_max: Tuple[float, float, float] = (10.0, 10.0, 10.0)
    use_spatial_hashing: bool = True
    grid_cell_size: float = 0.5
    neighbor_radius: float = 1.0
    use_gpu: bool = True
    gpu_threads_per_block: int = 256

class SpatialHashGrid:
    """Spatial hashing for efficient neighbor finding"""
    
    def __init__(self, cell_size: float, bounds: Tuple[Tuple[float, float, float], Tuple[float, float, float]]):
        self.cell_size = cell_size
        self.inv_cell_size = 1.0 / cell_size
        self.bounds_min = np.array(bounds[0])
        self.bounds_max = np.array(bounds[1])
        self.grid_size = ((self.bounds_max - self.bounds_min) / cell_size + 1).astype(int)
        self.clear()
    
    def clear(self):
        """Clear the grid"""
        self.grid = {}
        self.particle_to_cell = {}
    
    def hash_position(self, position: np.ndarray) -> Tuple[int, int, int]:
        """Hash a position to grid coordinates"""
        grid_pos = ((position - self.bounds_min) * self.inv_cell_size).astype(int)
        grid_pos = np.clip(grid_pos, 0, self.grid_size - 1)
        return tuple(grid_pos)
    
    def insert_particle(self, particle_id: int, position: np.ndarray):
        """Insert particle into spatial hash"""
        cell = self.hash_position(position)
        
        if cell not in self.grid:
            self.grid[cell] = []
        
        self.grid[cell].append(particle_id)
        self.particle_to_cell[particle_id] = cell
    
    def get_neighbors(self, position: np.ndarray, radius: float) -> List[int]:
        """Get all particles within radius of position"""
        neighbors = []
        
        # Calculate grid cell range to check
        min_cell = self.hash_position(position - radius)
        max_cell = self.hash_position(position + radius)
        
        for x in range(min_cell[0], max_cell[0] + 1):
            for y in range(min_cell[1], max_cell[1] + 1):
                for z in range(min_cell[2], max_cell[2] + 1):
                    cell = (x, y, z)
                    if cell in self.grid:
                        neighbors.extend(self.grid[cell])
        
        return neighbors

class FluidParticle:
    """Fluid particle for SPH simulation"""
    
    def __init__(self, particle_id: int, position: np.ndarray, properties: ParticleProperties):
        self.id = particle_id
        self.position = position.copy()
        self.velocity = np.zeros(3, dtype=np.float32)
        self.acceleration = np.zeros(3, dtype=np.float32)
        self.force = np.zeros(3, dtype=np.float32)
        
        self.density = properties.density
        self.pressure = 0.0
        self.mass = properties.mass
        self.radius = properties.radius
        self.viscosity = properties.viscosity
        self.surface_tension = properties.surface_tension
        
        self.color = np.array(properties.color, dtype=np.float32)
        self.temperature = properties.temperature
        self.life = properties.life_span
        self.audio_reactivity = properties.audio_reactivity
        
        self.neighbors = []
        self.neighbor_distances = []

@numba.jit(nopython=True, parallel=True)
def sph_kernel_poly6(r: float, h: float) -> float:
    """Poly6 SPH kernel function"""
    if r >= 0.0 and r <= h:
        factor = 315.0 / (64.0 * math.pi * h**9)
        return factor * (h*h - r*r)**3
    return 0.0

@numba.jit(nopython=True, parallel=True)
def sph_kernel_spiky_gradient(r_vec: np.ndarray, h: float) -> np.ndarray:
    """Spiky gradient kernel for pressure forces"""
    r = np.linalg.norm(r_vec)
    if r > 0.0 and r <= h:
        factor = -45.0 / (math.pi * h**6)
        return factor * (h - r)**2 * (r_vec / r)
    return np.zeros(3, dtype=np.float32)

@numba.jit(nopython=True, parallel=True)
def sph_kernel_viscosity_laplacian(r: float, h: float) -> float:
    """Viscosity laplacian kernel"""
    if r >= 0.0 and r <= h:
        factor = 45.0 / (math.pi * h**6)
        return factor * (h - r)
    return 0.0

class SPHFluidSimulator:
    """Smoothed Particle Hydrodynamics fluid simulator"""
    
    def __init__(self, settings: SimulationSettings):
        self.settings = settings
        self.particles = []
        self.spatial_grid = SpatialHashGrid(
            settings.grid_cell_size,
            (settings.boundary_min, settings.boundary_max)
        )
        
        # SPH constants
        self.rest_density = 1000.0
        self.gas_constant = 2000.0
        self.viscosity_constant = 250.0
        self.surface_tension_constant = 0.0728
        self.smoothing_radius = 0.8
        
        # Audio reactivity
        self.audio_energy = 0.0
        self.audio_frequencies = np.zeros(512, dtype=np.float32)
        
        # Performance tracking
        self.last_update_time = 0.0
        
    def add_particle(self, position: np.ndarray, properties: ParticleProperties) -> int:
        """Add a new particle to the simulation"""
        if len(self.particles) >= self.settings.max_particles:
            return -1
        
        particle_id = len(self.particles)
        particle = FluidParticle(particle_id, position, properties)
        self.particles.append(particle)
        
        return particle_id
    
    def update(self, dt: float, audio_energy: float = 0.0, audio_frequencies: np.ndarray = None):
        """Update fluid simulation"""
        start_time = time.time()
        
        self.audio_energy = audio_energy
        if audio_frequencies is not None:
            self.audio_frequencies = audio_frequencies
        
        # Update spatial hash
        self._update_spatial_hash()
        
        # Find neighbors
        self._find_neighbors()
        
        # Calculate densities
        self._calculate_densities()
        
        # Calculate pressures
        self._calculate_pressures()
        
        # Calculate forces
        self._calculate_forces()
        
        # Apply audio reactivity
        self._apply_audio_forces()
        
        # Integrate
        self._integrate(dt)
        
        # Handle boundaries
        self._handle_boundaries()
        
        # Update particle life
        self._update_particle_life(dt)
        
        self.last_update_time = time.time() - start_time
    
    def _update_spatial_hash(self):
        """Update spatial hash grid"""
        self.spatial_grid.clear()
        
        for particle in self.particles:
            if particle.life > 0:
                self.spatial_grid.insert_particle(particle.id, particle.position)
    
    def _find_neighbors(self):
        """Find neighbors for each particle"""
        for particle in self.particles:
            if particle.life <= 0:
                continue
                
            neighbors = self.spatial_grid.get_neighbors(particle.position, self.smoothing_radius)
            
            particle.neighbors = []
            particle.neighbor_distances = []
            
            for neighbor_id in neighbors:
                if neighbor_id != particle.id and neighbor_id < len(self.particles):
                    neighbor = self.particles[neighbor_id]
                    if neighbor.life > 0:
                        distance = np.linalg.norm(particle.position - neighbor.position)
                        if distance < self.smoothing_radius:
                            particle.neighbors.append(neighbor_id)
                            particle.neighbor_distances.append(distance)
    
    def _calculate_densities(self):
        """Calculate particle densities using SPH"""
        for particle in self.particles:
            if particle.life <= 0:
                continue
            
            density = 0.0
            
            # Self contribution
            density += particle.mass * sph_kernel_poly6(0.0, self.smoothing_radius)
            
            # Neighbor contributions
            for i, neighbor_id in enumerate(particle.neighbors):
                distance = particle.neighbor_distances[i]
                neighbor = self.particles[neighbor_id]
                density += neighbor.mass * sph_kernel_poly6(distance, self.smoothing_radius)
            
            particle.density = max(density, self.rest_density)
    
    def _calculate_pressures(self):
        """Calculate pressure from density"""
        for particle in self.particles:
            if particle.life <= 0:
                continue
                
            # Ideal gas law
            particle.pressure = self.gas_constant * (particle.density - self.rest_density)
    
    def _calculate_forces(self):
        """Calculate SPH forces"""
        for particle in self.particles:
            if particle.life <= 0:
                continue
            
            force = np.zeros(3, dtype=np.float32)
            
            # Pressure force
            for i, neighbor_id in enumerate(particle.neighbors):
                neighbor = self.particles[neighbor_id]
                r_vec = particle.position - neighbor.position
                
                if np.linalg.norm(r_vec) > 0:
                    pressure_force = sph_kernel_spiky_gradient(r_vec, self.smoothing_radius)
                    pressure_force *= -(particle.pressure + neighbor.pressure) / (2.0 * neighbor.density)
                    pressure_force *= particle.mass
                    force += pressure_force
            
            # Viscosity force
            for i, neighbor_id in enumerate(particle.neighbors):
                neighbor = self.particles[neighbor_id]
                distance = particle.neighbor_distances[i]
                
                velocity_diff = neighbor.velocity - particle.velocity
                viscosity_force = velocity_diff * self.viscosity_constant
                viscosity_force *= particle.mass * sph_kernel_viscosity_laplacian(distance, self.smoothing_radius)
                viscosity_force /= neighbor.density
                force += viscosity_force
            
            # Gravity
            gravity_force = np.array(self.settings.gravity, dtype=np.float32) * particle.mass
            force += gravity_force
            
            particle.force = force
    
    def _apply_audio_forces(self):
        """Apply audio-reactive forces"""
        if self.audio_energy <= 0:
            return
        
        for particle in self.particles:
            if particle.life <= 0:
                continue
            
            # Audio-reactive turbulence
            freq_idx = min(int(particle.position[0] * 10) % len(self.audio_frequencies), len(self.audio_frequencies) - 1)
            audio_amplitude = self.audio_frequencies[freq_idx] if freq_idx >= 0 else 0.0
            
            # Create swirling motion based on audio
            time_factor = time.time() * 2.0
            audio_force = np.array([
                math.sin(particle.position[0] * 0.1 + time_factor) * audio_amplitude,
                math.cos(particle.position[2] * 0.1 + time_factor) * audio_amplitude,
                math.sin(particle.position[1] * 0.1 + time_factor) * audio_amplitude
            ], dtype=np.float32)
            
            audio_force *= self.audio_energy * particle.audio_reactivity * 100.0
            particle.force += audio_force
    
    def _integrate(self, dt: float):
        """Integrate particle motion"""
        for particle in self.particles:
            if particle.life <= 0:
                continue
            
            # Verlet integration
            particle.acceleration = particle.force / particle.mass
            
            particle.velocity += particle.acceleration * dt
            particle.position += particle.velocity * dt
            
            # Apply damping
            particle.velocity *= 0.999
    
    def _handle_boundaries(self):
        """Handle boundary conditions"""
        boundary_min = np.array(self.settings.boundary_min, dtype=np.float32)
        boundary_max = np.array(self.settings.boundary_max, dtype=np.float32)
        
        for particle in self.particles:
            if particle.life <= 0:
                continue
            
            # Check boundaries and apply collision response
            for i in range(3):
                if particle.position[i] < boundary_min[i]:
                    particle.position[i] = boundary_min[i]
                    particle.velocity[i] *= -0.5  # Energy loss on collision
                elif particle.position[i] > boundary_max[i]:
                    particle.position[i] = boundary_max[i]
                    particle.velocity[i] *= -0.5
    
    def _update_particle_life(self, dt: float):
        """Update particle life and remove dead particles"""
        active_particles = []
        
        for particle in self.particles:
            particle.life -= dt
            if particle.life > 0:
                active_particles.append(particle)
        
        # Update particle IDs
        for i, particle in enumerate(active_particles):
            particle.id = i
        
        self.particles = active_particles
    
    def get_particle_data(self) -> Dict[str, np.ndarray]:
        """Get particle data for rendering"""
        if not self.particles:
            return {
                'positions': np.array([]).reshape(0, 3),
                'velocities': np.array([]).reshape(0, 3),
                'colors': np.array([]).reshape(0, 4),
                'sizes': np.array([]),
                'densities': np.array([])
            }
        
        positions = np.array([p.position for p in self.particles if p.life > 0], dtype=np.float32)
        velocities = np.array([p.velocity for p in self.particles if p.life > 0], dtype=np.float32)
        colors = np.array([p.color for p in self.particles if p.life > 0], dtype=np.float32)
        sizes = np.array([p.radius for p in self.particles if p.life > 0], dtype=np.float32)
        densities = np.array([p.density for p in self.particles if p.life > 0], dtype=np.float32)
        
        return {
            'positions': positions,
            'velocities': velocities, 
            'colors': colors,
            'sizes': sizes,
            'densities': densities
        }

class ClothParticle:
    """Particle for cloth simulation"""
    
    def __init__(self, position: np.ndarray, mass: float = 1.0, pinned: bool = False):
        self.position = position.copy()
        self.old_position = position.copy()
        self.acceleration = np.zeros(3, dtype=np.float32)
        self.mass = mass
        self.pinned = pinned
        self.audio_reactivity = 1.0

class ClothConstraint:
    """Distance constraint between cloth particles"""
    
    def __init__(self, particle1_id: int, particle2_id: int, rest_length: float, stiffness: float = 1.0):
        self.particle1_id = particle1_id
        self.particle2_id = particle2_id
        self.rest_length = rest_length
        self.stiffness = stiffness

class ClothSimulator:
    """Position-based cloth simulation"""
    
    def __init__(self, width: int, height: int, cloth_size: float = 5.0):
        self.width = width
        self.height = height
        self.cloth_size = cloth_size
        
        self.particles = []
        self.constraints = []
        
        self.gravity = np.array([0.0, -9.81, 0.0], dtype=np.float32)
        self.damping = 0.01
        self.constraint_iterations = 3
        
        self.audio_energy = 0.0
        
        self._create_cloth()
    
    def _create_cloth(self):
        """Create cloth mesh"""
        # Create particles
        for y in range(self.height):
            for x in range(self.width):
                pos_x = (x / (self.width - 1) - 0.5) * self.cloth_size
                pos_y = 5.0  # Start height
                pos_z = (y / (self.height - 1) - 0.5) * self.cloth_size
                
                position = np.array([pos_x, pos_y, pos_z], dtype=np.float32)
                
                # Pin top row
                pinned = (y == 0)
                
                particle = ClothParticle(position, mass=1.0, pinned=pinned)
                self.particles.append(particle)
        
        # Create constraints
        for y in range(self.height):
            for x in range(self.width):
                particle_id = y * self.width + x
                
                # Horizontal constraints
                if x < self.width - 1:
                    neighbor_id = y * self.width + (x + 1)
                    rest_length = self.cloth_size / (self.width - 1)
                    constraint = ClothConstraint(particle_id, neighbor_id, rest_length)
                    self.constraints.append(constraint)
                
                # Vertical constraints
                if y < self.height - 1:
                    neighbor_id = (y + 1) * self.width + x
                    rest_length = self.cloth_size / (self.height - 1)
                    constraint = ClothConstraint(particle_id, neighbor_id, rest_length)
                    self.constraints.append(constraint)
                
                # Diagonal constraints for stability
                if x < self.width - 1 and y < self.height - 1:
                    neighbor_id = (y + 1) * self.width + (x + 1)
                    rest_length = self.cloth_size * math.sqrt(2) / (self.width - 1)
                    constraint = ClothConstraint(particle_id, neighbor_id, rest_length, stiffness=0.5)
                    self.constraints.append(constraint)
                
                if x > 0 and y < self.height - 1:
                    neighbor_id = (y + 1) * self.width + (x - 1)
                    rest_length = self.cloth_size * math.sqrt(2) / (self.width - 1)
                    constraint = ClothConstraint(particle_id, neighbor_id, rest_length, stiffness=0.5)
                    self.constraints.append(constraint)
    
    def update(self, dt: float, audio_energy: float = 0.0):
        """Update cloth simulation"""
        self.audio_energy = audio_energy
        
        # Apply forces
        for particle in self.particles:
            if not particle.pinned:
                # Gravity
                particle.acceleration = self.gravity.copy()
                
                # Audio reactivity (wind effect)
                if audio_energy > 0.1:
                    wind_force = np.array([
                        math.sin(time.time() * 2.0 + particle.position[0] * 0.1) * audio_energy,
                        0.0,
                        math.cos(time.time() * 1.5 + particle.position[2] * 0.1) * audio_energy
                    ], dtype=np.float32) * 20.0
                    
                    particle.acceleration += wind_force * particle.audio_reactivity
        
        # Verlet integration
        for particle in self.particles:
            if not particle.pinned:
                temp = particle.position.copy()
                particle.position = particle.position * 2.0 - particle.old_position + particle.acceleration * dt * dt
                particle.old_position = temp
                
                # Apply damping
                velocity = particle.position - particle.old_position
                particle.position = particle.position - velocity * self.damping
        
        # Satisfy constraints
        for _ in range(self.constraint_iterations):
            for constraint in self.constraints:
                self._satisfy_constraint(constraint)
    
    def _satisfy_constraint(self, constraint: ClothConstraint):
        """Satisfy distance constraint"""
        p1 = self.particles[constraint.particle1_id]
        p2 = self.particles[constraint.particle2_id]
        
        delta = p1.position - p2.position
        distance = np.linalg.norm(delta)
        
        if distance > 0:
            difference = (constraint.rest_length - distance) / distance
            translate = delta * difference * 0.5 * constraint.stiffness
            
            if not p1.pinned:
                p1.position += translate
            if not p2.pinned:
                p2.position -= translate
    
    def get_mesh_data(self) -> Dict[str, np.ndarray]:
        """Get cloth mesh data for rendering"""
        positions = np.array([p.position for p in self.particles], dtype=np.float32)
        
        # Generate indices for triangles
        indices = []
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                # Two triangles per quad
                top_left = y * self.width + x
                top_right = y * self.width + (x + 1)
                bottom_left = (y + 1) * self.width + x
                bottom_right = (y + 1) * self.width + (x + 1)
                
                # Triangle 1
                indices.extend([top_left, bottom_left, top_right])
                # Triangle 2
                indices.extend([top_right, bottom_left, bottom_right])
        
        indices = np.array(indices, dtype=np.uint32)
        
        return {
            'positions': positions,
            'indices': indices,
            'width': self.width,
            'height': self.height
        }

class SmokeParticle:
    """Particle for smoke simulation"""
    
    def __init__(self, position: np.ndarray, velocity: np.ndarray, temperature: float = 400.0):
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.temperature = temperature
        self.density = 1.0
        self.life = 5.0
        self.size = 0.5
        self.color = np.array([0.8, 0.8, 0.8, 1.0], dtype=np.float32)

class SmokeSimulator:
    """Smoke and fire particle system with thermal dynamics"""
    
    def __init__(self, max_particles: int = 10000):
        self.max_particles = max_particles
        self.particles = []
        
        self.ambient_temperature = 293.15  # 20°C in Kelvin
        self.buoyancy_strength = 10.0
        self.cooling_rate = 50.0  # K/s
        self.diffusion_rate = 0.1
        
        self.audio_energy = 0.0
        
        # Emitter properties
        self.emitter_position = np.array([0.0, -2.0, 0.0], dtype=np.float32)
        self.emission_rate = 50.0  # particles per second
        self.emission_timer = 0.0
    
    def update(self, dt: float, audio_energy: float = 0.0):
        """Update smoke simulation"""
        self.audio_energy = audio_energy
        
        # Emit new particles
        self._emit_particles(dt)
        
        # Update existing particles
        for particle in self.particles[:]:
            # Temperature cooling
            particle.temperature -= self.cooling_rate * dt
            particle.temperature = max(particle.temperature, self.ambient_temperature)
            
            # Buoyancy force based on temperature
            temperature_diff = particle.temperature - self.ambient_temperature
            buoyancy = np.array([0.0, 1.0, 0.0], dtype=np.float32) * temperature_diff * self.buoyancy_strength * dt
            particle.velocity += buoyancy
            
            # Audio reactivity (turbulence)
            if audio_energy > 0.1:
                turbulence = np.array([
                    math.sin(time.time() * 3.0 + particle.position[0] * 0.2) * audio_energy,
                    0.0,
                    math.cos(time.time() * 2.0 + particle.position[2] * 0.2) * audio_energy
                ], dtype=np.float32) * 5.0
                particle.velocity += turbulence * dt
            
            # Update position
            particle.position += particle.velocity * dt
            
            # Update appearance based on temperature
            self._update_particle_appearance(particle)
            
            # Update life
            particle.life -= dt
            
            # Grow and fade
            particle.size += dt * 0.5
            particle.color[3] *= 0.995  # Fade alpha
            
            # Remove dead particles
            if particle.life <= 0 or particle.color[3] < 0.01:
                self.particles.remove(particle)
    
    def _emit_particles(self, dt: float):
        """Emit new smoke particles"""
        self.emission_timer += dt
        
        # Audio-reactive emission
        effective_rate = self.emission_rate * (1.0 + self.audio_energy * 2.0)
        
        particles_to_emit = int(effective_rate * dt)
        
        for _ in range(particles_to_emit):
            if len(self.particles) >= self.max_particles:
                break
            
            # Random position around emitter
            offset = np.random.normal(0.0, 0.2, 3).astype(np.float32)
            position = self.emitter_position + offset
            
            # Initial velocity with randomness
            velocity = np.array([
                np.random.normal(0.0, 1.0),
                np.random.uniform(2.0, 5.0),
                np.random.normal(0.0, 1.0)
            ], dtype=np.float32)
            
            # Audio-reactive temperature
            temperature = 400.0 + self.audio_energy * 200.0
            
            particle = SmokeParticle(position, velocity, temperature)
            self.particles.append(particle)
    
    def _update_particle_appearance(self, particle: SmokeParticle):
        """Update particle color based on temperature"""
        # Temperature to color mapping (blackbody radiation)
        temp = particle.temperature
        
        if temp > 1000.0:  # Hot - orange/red
            r = 1.0
            g = 0.5 + (temp - 1000.0) / 1000.0 * 0.5
            b = 0.0
        elif temp > 600.0:  # Warm - red/orange
            r = 1.0
            g = (temp - 600.0) / 400.0 * 0.5
            b = 0.0
        else:  # Cool - gray smoke
            intensity = 0.3 + (temp - self.ambient_temperature) / 300.0 * 0.5
            r = g = b = intensity
        
        particle.color[:3] = [r, g, b]
    
    def get_particle_data(self) -> Dict[str, np.ndarray]:
        """Get smoke particle data for rendering"""
        if not self.particles:
            return {
                'positions': np.array([]).reshape(0, 3),
                'colors': np.array([]).reshape(0, 4),
                'sizes': np.array([])
            }
        
        positions = np.array([p.position for p in self.particles], dtype=np.float32)
        colors = np.array([p.color for p in self.particles], dtype=np.float32)
        sizes = np.array([p.size for p in self.particles], dtype=np.float32)
        
        return {
            'positions': positions,
            'colors': colors,
            'sizes': sizes
        }

class AdvancedParticleManager:
    """Manages all particle systems"""
    
    def __init__(self, settings: SimulationSettings):
        self.settings = settings
        
        # Initialize subsystems
        self.fluid_sim = SPHFluidSimulator(settings)
        self.cloth_sim = ClothSimulator(20, 20, 4.0)
        self.smoke_sim = SmokeSimulator(5000)
        
        # Performance monitoring
        self.performance_stats = {
            'fluid_time': 0.0,
            'cloth_time': 0.0,
            'smoke_time': 0.0,
            'total_particles': 0
        }
        
        # Audio data
        self.current_audio_energy = 0.0
        self.current_audio_frequencies = np.zeros(512, dtype=np.float32)
    
    def update(self, dt: float, audio_energy: float = 0.0, audio_frequencies: np.ndarray = None):
        """Update all particle systems"""
        self.current_audio_energy = audio_energy
        if audio_frequencies is not None:
            self.current_audio_frequencies = audio_frequencies
        
        # Update fluid simulation
        start_time = time.time()
        self.fluid_sim.update(dt, audio_energy, audio_frequencies)
        self.performance_stats['fluid_time'] = time.time() - start_time
        
        # Update cloth simulation
        start_time = time.time()
        self.cloth_sim.update(dt, audio_energy)
        self.performance_stats['cloth_time'] = time.time() - start_time
        
        # Update smoke simulation
        start_time = time.time()
        self.smoke_sim.update(dt, audio_energy)
        self.performance_stats['smoke_time'] = time.time() - start_time
        
        # Update stats
        self.performance_stats['total_particles'] = (
            len(self.fluid_sim.particles) +
            len(self.cloth_sim.particles) +
            len(self.smoke_sim.particles)
        )
    
    def add_fluid_emitter(self, position: np.ndarray, particle_count: int = 100):
        """Add fluid particles at position"""
        properties = ParticleProperties(
            mass=1.0,
            radius=0.1,
            density=1000.0,
            viscosity=0.01,
            color=(0.3, 0.6, 1.0, 0.8),
            life_span=10.0,
            audio_reactivity=1.0
        )
        
        for i in range(particle_count):
            offset = np.random.normal(0.0, 0.3, 3).astype(np.float32)
            particle_pos = position + offset
            self.fluid_sim.add_particle(particle_pos, properties)
    
    def get_all_render_data(self) -> Dict[str, Any]:
        """Get all particle data for rendering"""
        return {
            'fluid': self.fluid_sim.get_particle_data(),
            'cloth': self.cloth_sim.get_mesh_data(),
            'smoke': self.smoke_sim.get_particle_data(),
            'performance': self.performance_stats
        }
    
    def create_audio_reactive_explosion(self, position: np.ndarray, intensity: float):
        """Create an audio-reactive particle explosion"""
        # Fluid explosion
        properties = ParticleProperties(
            mass=0.5,
            radius=0.05,
            density=500.0,
            color=(1.0, 0.5 + intensity * 0.5, 0.0, 0.9),
            life_span=3.0 + intensity * 2.0,
            audio_reactivity=2.0
        )
        
        particle_count = int(50 + intensity * 100)
        for i in range(particle_count):
            # Spherical distribution
            phi = np.random.uniform(0, 2 * math.pi)
            costheta = np.random.uniform(-1, 1)
            theta = math.acos(costheta)
            
            radius = np.random.uniform(0.1, 1.0)
            
            offset = np.array([
                radius * math.sin(theta) * math.cos(phi),
                radius * math.sin(theta) * math.sin(phi),
                radius * costheta
            ], dtype=np.float32) * intensity
            
            particle_pos = position + offset
            particle_id = self.fluid_sim.add_particle(particle_pos, properties)
            
            if particle_id >= 0:
                # Add initial velocity
                explosion_velocity = offset * (10.0 + intensity * 20.0)
                self.fluid_sim.particles[particle_id].velocity = explosion_velocity

if __name__ == "__main__":
    # Test the advanced particle systems
    settings = SimulationSettings(
        max_particles=10000,
        time_step=0.016,
        use_gpu=False  # Set to True if GPU acceleration is available
    )
    
    particle_manager = AdvancedParticleManager(settings)
    
    # Add some initial particles
    particle_manager.add_fluid_emitter(np.array([0.0, 2.0, 0.0]), 200)
    
    print("🎆 Advanced Particle Systems Test")
    print("=" * 40)
    
    # Simulate for a few steps
    for step in range(10):
        audio_energy = 0.5 + 0.5 * math.sin(step * 0.1)
        particle_manager.update(0.016, audio_energy)
        
        stats = particle_manager.performance_stats
        print(f"Step {step}: {stats['total_particles']} particles, "
              f"Fluid: {stats['fluid_time']:.3f}s, "
              f"Cloth: {stats['cloth_time']:.3f}s, "
              f"Smoke: {stats['smoke_time']:.3f}s")
    
    print("✅ Advanced particle systems test completed!")