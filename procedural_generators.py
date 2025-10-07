#!/usr/bin/env python3
"""
Revolutionary Procedural Geometry Generation
L-systems, fractals, and advanced mathematical structures for audio visualization
"""

import numpy as np
import math
import random
import time
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Callable, Any
from enum import Enum
import networkx as nx
import scipy.spatial.distance as distance
from scipy.spatial import ConvexHull, Voronoi
import sympy as sp
from sympy import symbols, lambdify, sin, cos, exp, log, sqrt
import threading
import queue

class GeometryType(Enum):
    """Types of procedural geometry"""
    L_SYSTEM = "l_system"
    FRACTAL = "fractal"
    CELLULAR_AUTOMATA = "cellular_automata"
    PERLIN_NOISE = "perlin_noise"
    VORONOI = "voronoi"
    DELAUNAY = "delaunay"
    PARAMETRIC = "parametric"
    NEURAL_GENERATED = "neural_generated"

@dataclass
class LSystemRule:
    """L-System production rule"""
    predecessor: str
    successor: str
    probability: float = 1.0
    condition: Optional[Callable] = None

@dataclass
class ProceduralSettings:
    """Settings for procedural generation"""
    geometry_type: GeometryType = GeometryType.L_SYSTEM
    iterations: int = 5
    complexity: float = 1.0
    audio_reactivity: float = 1.0
    seed: int = 42
    animation_speed: float = 1.0
    color_scheme: str = "rainbow"
    scale_factor: float = 1.0

class LSystemGenerator:
    """Advanced L-System generator with audio reactivity"""
    
    def __init__(self, axiom: str, rules: List[LSystemRule], interpretation: Dict[str, Any]):
        self.axiom = axiom
        self.rules = rules
        self.interpretation = interpretation
        self.current_string = axiom
        self.generation = 0
        
        # Audio-reactive parameters
        self.audio_energy = 0.0
        self.audio_frequencies = np.zeros(512, dtype=np.float32)
        
        # Turtle graphics state
        self.turtle_state = {
            'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
            'direction': np.array([0.0, 1.0, 0.0], dtype=np.float32),
            'up': np.array([0.0, 0.0, 1.0], dtype=np.float32),
            'angle': 25.0,  # degrees
            'step_size': 1.0,
            'thickness': 0.1
        }
        
        self.state_stack = []
        self.geometry = {
            'vertices': [],
            'edges': [],
            'faces': [],
            'colors': [],
            'normals': []
        }
    
    def iterate(self, iterations: int = 1, audio_energy: float = 0.0, audio_frequencies: np.ndarray = None):
        """Perform L-System iterations with audio reactivity"""
        self.audio_energy = audio_energy
        if audio_frequencies is not None:
            self.audio_frequencies = audio_frequencies
        
        for _ in range(iterations):
            new_string = ""
            
            for char in self.current_string:
                # Find applicable rules
                applicable_rules = [rule for rule in self.rules if rule.predecessor == char]
                
                if applicable_rules:
                    # Choose rule based on probability and conditions
                    chosen_rule = self._choose_rule(applicable_rules, char)
                    if chosen_rule:
                        new_string += self._apply_audio_modulation(chosen_rule.successor)
                    else:
                        new_string += char
                else:
                    new_string += char
            
            self.current_string = new_string
            self.generation += 1
    
    def _choose_rule(self, rules: List[LSystemRule], context_char: str) -> Optional[LSystemRule]:
        """Choose rule based on probability and audio reactivity"""
        if not rules:
            return None
        
        # Modify probabilities based on audio
        total_prob = 0.0
        modified_rules = []
        
        for rule in rules:
            # Audio-reactive probability modification
            audio_influence = 1.0 + self.audio_energy * 0.5
            modified_prob = rule.probability * audio_influence
            
            modified_rules.append((rule, modified_prob))
            total_prob += modified_prob
        
        # Weighted random selection
        r = random.random() * total_prob
        cumulative_prob = 0.0
        
        for rule, prob in modified_rules:
            cumulative_prob += prob
            if r <= cumulative_prob:
                return rule
        
        return rules[0]  # Fallback
    
    def _apply_audio_modulation(self, string: str) -> str:
        """Apply audio-reactive modulation to generated string"""
        # Add audio-reactive elements
        if self.audio_energy > 0.7:
            # High energy: add more branching
            string = string.replace('F', 'F[+F][-F]')
        elif self.audio_energy > 0.4:
            # Medium energy: add some variation
            string = string.replace('F', 'FF')
        
        return string
    
    def generate_geometry(self) -> Dict[str, np.ndarray]:
        """Generate 3D geometry from L-System string"""
        self._reset_turtle()
        self.geometry = {
            'vertices': [],
            'edges': [],
            'faces': [],
            'colors': [],
            'normals': []
        }
        
        vertex_count = 0
        
        for i, char in enumerate(self.current_string):
            if char in self.interpretation:
                command = self.interpretation[char]
                
                if command == 'forward':
                    vertex_count = self._turtle_forward(vertex_count)
                elif command == 'turn_left':
                    self._turtle_turn(self.turtle_state['angle'])
                elif command == 'turn_right':
                    self._turtle_turn(-self.turtle_state['angle'])
                elif command == 'pitch_up':
                    self._turtle_pitch(self.turtle_state['angle'])
                elif command == 'pitch_down':
                    self._turtle_pitch(-self.turtle_state['angle'])
                elif command == 'roll_left':
                    self._turtle_roll(self.turtle_state['angle'])
                elif command == 'roll_right':
                    self._turtle_roll(-self.turtle_state['angle'])
                elif command == 'push':
                    self._turtle_push()
                elif command == 'pop':
                    self._turtle_pop()
                elif command == 'increase_angle':
                    self.turtle_state['angle'] *= 1.1
                elif command == 'decrease_angle':
                    self.turtle_state['angle'] *= 0.9
        
        return self._finalize_geometry()
    
    def _reset_turtle(self):
        """Reset turtle to initial state"""
        self.turtle_state = {
            'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
            'direction': np.array([0.0, 1.0, 0.0], dtype=np.float32),
            'up': np.array([0.0, 0.0, 1.0], dtype=np.float32),
            'angle': 25.0 + self.audio_energy * 15.0,  # Audio-reactive angle
            'step_size': 1.0 + self.audio_energy * 0.5,
            'thickness': 0.1 + self.audio_energy * 0.05
        }
        self.state_stack = []
    
    def _turtle_forward(self, vertex_count: int) -> int:
        """Move turtle forward and create geometry"""
        start_pos = self.turtle_state['position'].copy()
        
        # Audio-reactive step size
        step = self.turtle_state['step_size'] * (0.8 + self.audio_energy * 0.4)
        
        self.turtle_state['position'] += self.turtle_state['direction'] * step
        end_pos = self.turtle_state['position'].copy()
        
        # Create geometry for the segment
        self._create_segment(start_pos, end_pos, vertex_count)
        
        return vertex_count + 8  # 8 vertices per segment (cylinder)
    
    def _create_segment(self, start: np.ndarray, end: np.ndarray, vertex_count: int):
        """Create cylindrical segment geometry"""
        direction = end - start
        length = np.linalg.norm(direction)
        
        if length < 1e-6:
            return
        
        direction = direction / length
        
        # Create perpendicular vectors
        if abs(direction[1]) < 0.9:
            right = np.cross(direction, np.array([0, 1, 0]))
        else:
            right = np.cross(direction, np.array([1, 0, 0]))
        
        right = right / np.linalg.norm(right)
        up = np.cross(direction, right)
        
        # Audio-reactive thickness and color
        thickness = self.turtle_state['thickness'] * (0.5 + self.audio_energy)
        
        # Create cylinder vertices
        segments = 4  # Simplified cylinder
        vertices = []
        
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            
            # Start circle
            offset = right * math.cos(angle) * thickness + up * math.sin(angle) * thickness
            vertices.append(start + offset)
            
            # End circle
            vertices.append(end + offset)
        
        # Add vertices to geometry
        start_idx = len(self.geometry['vertices'])
        self.geometry['vertices'].extend(vertices)
        
        # Audio-reactive color
        freq_idx = min(int(self.generation * 10) % len(self.audio_frequencies), len(self.audio_frequencies) - 1)
        audio_val = self.audio_frequencies[freq_idx] if freq_idx >= 0 else 0.0
        
        color = np.array([
            0.5 + audio_val * 0.5,
            0.3 + self.audio_energy * 0.7,
            0.8 - audio_val * 0.3,
            1.0
        ], dtype=np.float32)
        
        for _ in vertices:
            self.geometry['colors'].append(color)
        
        # Create faces (simplified)
        for i in range(segments):
            next_i = (i + 1) % segments
            
            # Side faces (quads as two triangles)
            v1 = start_idx + i * 2
            v2 = start_idx + i * 2 + 1
            v3 = start_idx + next_i * 2 + 1
            v4 = start_idx + next_i * 2
            
            self.geometry['faces'].extend([[v1, v2, v3], [v1, v3, v4]])
    
    def _turtle_turn(self, angle: float):
        """Turn turtle around up axis"""
        angle_rad = math.radians(angle * (1.0 + self.audio_energy * 0.3))
        
        # Rotation matrix around up axis
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        right = np.cross(self.turtle_state['direction'], self.turtle_state['up'])
        new_direction = self.turtle_state['direction'] * cos_a + right * sin_a
        self.turtle_state['direction'] = new_direction / np.linalg.norm(new_direction)
    
    def _turtle_pitch(self, angle: float):
        """Pitch turtle around right axis"""
        angle_rad = math.radians(angle * (1.0 + self.audio_energy * 0.3))
        
        right = np.cross(self.turtle_state['direction'], self.turtle_state['up'])
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        new_direction = self.turtle_state['direction'] * cos_a + self.turtle_state['up'] * sin_a
        new_up = -self.turtle_state['direction'] * sin_a + self.turtle_state['up'] * cos_a
        
        self.turtle_state['direction'] = new_direction / np.linalg.norm(new_direction)
        self.turtle_state['up'] = new_up / np.linalg.norm(new_up)
    
    def _turtle_roll(self, angle: float):
        """Roll turtle around direction axis"""
        angle_rad = math.radians(angle * (1.0 + self.audio_energy * 0.3))
        
        right = np.cross(self.turtle_state['direction'], self.turtle_state['up'])
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        new_up = self.turtle_state['up'] * cos_a + right * sin_a
        self.turtle_state['up'] = new_up / np.linalg.norm(new_up)
    
    def _turtle_push(self):
        """Push current state onto stack"""
        state_copy = {
            'position': self.turtle_state['position'].copy(),
            'direction': self.turtle_state['direction'].copy(),
            'up': self.turtle_state['up'].copy(),
            'angle': self.turtle_state['angle'],
            'step_size': self.turtle_state['step_size'],
            'thickness': self.turtle_state['thickness']
        }
        self.state_stack.append(state_copy)
    
    def _turtle_pop(self):
        """Pop state from stack"""
        if self.state_stack:
            self.turtle_state = self.state_stack.pop()
    
    def _finalize_geometry(self) -> Dict[str, np.ndarray]:
        """Convert geometry to numpy arrays"""
        return {
            'vertices': np.array(self.geometry['vertices'], dtype=np.float32) if self.geometry['vertices'] else np.array([]).reshape(0, 3),
            'faces': np.array(self.geometry['faces'], dtype=np.uint32) if self.geometry['faces'] else np.array([]).reshape(0, 3),
            'colors': np.array(self.geometry['colors'], dtype=np.float32) if self.geometry['colors'] else np.array([]).reshape(0, 4)
        }

class FractalGenerator:
    """Advanced fractal geometry generator"""
    
    def __init__(self):
        self.audio_energy = 0.0
        self.audio_frequencies = np.zeros(512, dtype=np.float32)
        
    def generate_mandelbrot_surface(self, resolution: int = 256, iterations: int = 100) -> Dict[str, np.ndarray]:
        """Generate 3D Mandelbrot set surface"""
        # Create coordinate grid
        x = np.linspace(-2, 2, resolution)
        y = np.linspace(-2, 2, resolution)
        X, Y = np.meshgrid(x, y)
        
        # Audio-reactive parameters
        zoom = 1.0 + self.audio_energy * 0.5
        offset_x = self.audio_energy * 0.1 * math.sin(time.time())
        offset_y = self.audio_energy * 0.1 * math.cos(time.time())
        
        # Calculate Mandelbrot
        C = (X + offset_x) / zoom + 1j * (Y + offset_y) / zoom
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)
        
        for i in range(iterations):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            M[mask] = i
        
        # Create 3D surface
        vertices = []
        faces = []
        colors = []
        
        height_scale = 0.5 + self.audio_energy * 2.0
        
        for i in range(resolution - 1):
            for j in range(resolution - 1):
                # Height based on iteration count
                h1 = M[i, j] / iterations * height_scale
                h2 = M[i+1, j] / iterations * height_scale
                h3 = M[i, j+1] / iterations * height_scale
                h4 = M[i+1, j+1] / iterations * height_scale
                
                # Vertices for quad
                v1 = [X[i, j], Y[i, j], h1]
                v2 = [X[i+1, j], Y[i+1, j], h2]
                v3 = [X[i, j+1], Y[i, j+1], h3]
                v4 = [X[i+1, j+1], Y[i+1, j+1], h4]
                
                start_idx = len(vertices)
                vertices.extend([v1, v2, v3, v4])
                
                # Create triangular faces
                faces.extend([[start_idx, start_idx+1, start_idx+2],
                             [start_idx+1, start_idx+3, start_idx+2]])
                
                # Audio-reactive colors
                freq_idx = int((i + j) * 0.5) % len(self.audio_frequencies)
                audio_val = self.audio_frequencies[freq_idx]
                
                color = [
                    0.5 + audio_val * 0.5,
                    h1 * 2.0,
                    0.8 - audio_val * 0.3,
                    1.0
                ]
                
                for _ in range(4):
                    colors.append(color)
        
        return {
            'vertices': np.array(vertices, dtype=np.float32),
            'faces': np.array(faces, dtype=np.uint32),
            'colors': np.array(colors, dtype=np.float32)
        }
    
    def generate_julia_set(self, c_real: float = -0.7, c_imag: float = 0.27015, resolution: int = 256) -> Dict[str, np.ndarray]:
        """Generate Julia set geometry"""
        # Audio-reactive parameters
        c_real += self.audio_energy * 0.1 * math.sin(time.time() * 2.0)
        c_imag += self.audio_energy * 0.1 * math.cos(time.time() * 1.5)
        
        x = np.linspace(-2, 2, resolution)
        y = np.linspace(-2, 2, resolution)
        X, Y = np.meshgrid(x, y)
        
        c = complex(c_real, c_imag)
        Z = X + 1j * Y
        M = np.zeros(Z.shape)
        
        iterations = int(50 + self.audio_energy * 50)
        
        for i in range(iterations):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + c
            M[mask] = i
        
        # Convert to 3D points
        points = []
        colors = []
        
        height_scale = self.audio_energy * 0.5
        
        for i in range(0, resolution, 2):  # Skip some points for performance
            for j in range(0, resolution, 2):
                if M[i, j] < iterations - 1:  # Only include points in the set
                    height = M[i, j] / iterations * height_scale
                    points.append([X[i, j], Y[i, j], height])
                    
                    # Color based on iteration count and audio
                    freq_idx = (i + j) % len(self.audio_frequencies)
                    audio_val = self.audio_frequencies[freq_idx]
                    
                    colors.append([
                        M[i, j] / iterations,
                        audio_val,
                        0.8 - M[i, j] / iterations * 0.5,
                        1.0
                    ])
        
        return {
            'vertices': np.array(points, dtype=np.float32),
            'colors': np.array(colors, dtype=np.float32),
            'type': 'points'  # Render as points instead of mesh
        }
    
    def generate_ifs_fractal(self, transformations: List[np.ndarray], iterations: int = 100000) -> Dict[str, np.ndarray]:
        """Generate Iterated Function System fractal"""
        points = []
        colors = []
        
        # Starting point
        point = np.array([0.0, 0.0, 1.0], dtype=np.float32)  # Homogeneous coordinates
        
        # Audio-reactive iteration scaling
        effective_iterations = int(iterations * (0.5 + self.audio_energy * 0.5))
        
        for i in range(effective_iterations):
            # Choose random transformation
            transform_idx = random.randint(0, len(transformations) - 1)
            transform = transformations[transform_idx]
            
            # Apply transformation
            point = transform @ point
            
            # Skip first few iterations (settling)
            if i > 100:
                # Convert back to 3D
                if point[2] != 0:
                    x, y = point[0] / point[2], point[1] / point[2]
                    
                    # Audio-reactive height
                    freq_idx = i % len(self.audio_frequencies)
                    height = self.audio_frequencies[freq_idx] * self.audio_energy * 2.0
                    
                    points.append([x, y, height])
                    
                    # Color based on transformation and audio
                    color_factor = transform_idx / len(transformations)
                    audio_factor = self.audio_frequencies[freq_idx]
                    
                    colors.append([
                        color_factor + audio_factor * 0.3,
                        0.5 + audio_factor * 0.5,
                        0.8 - color_factor * 0.3,
                        0.8
                    ])
        
        return {
            'vertices': np.array(points, dtype=np.float32),
            'colors': np.array(colors, dtype=np.float32),
            'type': 'points'
        }

class ParametricSurfaceGenerator:
    """Generates parametric surfaces with audio reactivity"""
    
    def __init__(self):
        self.audio_energy = 0.0
        self.audio_frequencies = np.zeros(512, dtype=np.float32)
        
    def generate_torus(self, major_radius: float = 2.0, minor_radius: float = 1.0, 
                      u_res: int = 50, v_res: int = 50) -> Dict[str, np.ndarray]:
        """Generate audio-reactive torus"""
        # Audio-reactive parameters
        R = major_radius * (0.8 + self.audio_energy * 0.4)
        r = minor_radius * (0.5 + self.audio_energy * 0.5)
        
        vertices = []
        faces = []
        colors = []
        
        for i in range(u_res):
            for j in range(v_res):
                u = 2 * math.pi * i / u_res
                v = 2 * math.pi * j / v_res
                
                # Audio-reactive distortion
                freq_u = int(i * len(self.audio_frequencies) / u_res) % len(self.audio_frequencies)
                freq_v = int(j * len(self.audio_frequencies) / v_res) % len(self.audio_frequencies)
                
                audio_distort_u = self.audio_frequencies[freq_u] * self.audio_energy * 0.2
                audio_distort_v = self.audio_frequencies[freq_v] * self.audio_energy * 0.2
                
                # Torus equations with audio distortion
                x = (R + (r + audio_distort_u) * math.cos(v)) * math.cos(u)
                y = (R + (r + audio_distort_u) * math.cos(v)) * math.sin(u)
                z = (r + audio_distort_v) * math.sin(v)
                
                vertices.append([x, y, z])
                
                # Audio-reactive color
                color = [
                    0.5 + self.audio_frequencies[freq_u] * 0.5,
                    0.3 + self.audio_energy * 0.7,
                    0.8 - self.audio_frequencies[freq_v] * 0.3,
                    1.0
                ]
                colors.append(color)
                
                # Create faces
                if i < u_res - 1 and j < v_res - 1:
                    v1 = i * v_res + j
                    v2 = (i + 1) * v_res + j
                    v3 = i * v_res + (j + 1)
                    v4 = (i + 1) * v_res + (j + 1)
                    
                    faces.extend([[v1, v2, v3], [v2, v4, v3]])
        
        return {
            'vertices': np.array(vertices, dtype=np.float32),
            'faces': np.array(faces, dtype=np.uint32),
            'colors': np.array(colors, dtype=np.float32)
        }
    
    def generate_klein_bottle(self, u_res: int = 50, v_res: int = 50) -> Dict[str, np.ndarray]:
        """Generate Klein bottle with audio reactivity"""
        vertices = []
        faces = []
        colors = []
        
        for i in range(u_res):
            for j in range(v_res):
                u = 2 * math.pi * i / u_res
                v = 2 * math.pi * j / v_res
                
                # Audio-reactive parameters
                freq_idx = (i + j) % len(self.audio_frequencies)
                audio_factor = self.audio_frequencies[freq_idx] * self.audio_energy
                
                # Klein bottle parametric equations with audio modulation
                if u < math.pi:
                    x = 3 * math.cos(u) * (1 + math.sin(u)) + 2 * (1 - math.cos(u) / 2) * math.cos(u) * math.cos(v)
                    y = 8 * math.sin(u) + 2 * (1 - math.cos(u) / 2) * math.sin(u) * math.cos(v)
                else:
                    x = 3 * math.cos(u) * (1 + math.sin(u)) + 2 * (1 - math.cos(u) / 2) * math.cos(v + math.pi)
                    y = 8 * math.sin(u)
                
                z = 2 * (1 - math.cos(u) / 2) * math.sin(v)
                
                # Apply audio distortion
                x += audio_factor * math.sin(u * 2 + time.time()) * 0.5
                y += audio_factor * math.cos(v * 2 + time.time()) * 0.5
                z += audio_factor * math.sin((u + v) + time.time()) * 0.3
                
                vertices.append([x, y, z])
                
                # Audio-reactive color
                colors.append([
                    0.6 + audio_factor * 0.4,
                    0.4 + math.sin(u) * 0.3 + audio_factor * 0.3,
                    0.8 + math.cos(v) * 0.2 - audio_factor * 0.2,
                    0.9
                ])
                
                # Create faces
                if i < u_res - 1 and j < v_res - 1:
                    v1 = i * v_res + j
                    v2 = (i + 1) * v_res + j
                    v3 = i * v_res + (j + 1)
                    v4 = (i + 1) * v_res + (j + 1)
                    
                    faces.extend([[v1, v2, v3], [v2, v4, v3]])
        
        return {
            'vertices': np0.array(vertices, dtype=np.float32),
            'faces': np.array(faces, dtype=np.uint32),
            'colors': np.array(colors, dtype=np.float32)
        }

class CellularAutomataGenerator:
    """Generates 3D structures using cellular automata"""
    
    def __init__(self, size: int = 64):
        self.size = size
        self.grid = np.zeros((size, size, size), dtype=np.uint8)
        self.rules = {}
        self.audio_energy = 0.0
        
    def set_rules(self, survival: List[int], birth: List[int]):
        """Set cellular automata rules (3D version of Conway's Game of Life)"""
        self.rules = {
            'survival': survival,
            'birth': birth
        }
    
    def seed_random(self, density: float = 0.3):
        """Randomly seed the grid"""
        # Audio-reactive seeding
        effective_density = density * (0.5 + self.audio_energy * 0.5)
        self.grid = (np.random.random((self.size, self.size, self.size)) < effective_density).astype(np.uint8)
    
    def iterate(self, steps: int = 10):
        """Run cellular automata for specified steps"""
        for step in range(steps):
            new_grid = np.zeros_like(self.grid)
            
            for x in range(1, self.size - 1):
                for y in range(1, self.size - 1):
                    for z in range(1, self.size - 1):
                        # Count living neighbors
                        neighbors = 0
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                for dz in [-1, 0, 1]:
                                    if dx == 0 and dy == 0 and dz == 0:
                                        continue
                                    neighbors += self.grid[x + dx, y + dy, z + dz]
                        
                        # Apply rules
                        if self.grid[x, y, z] == 1:  # Currently alive
                            if neighbors in self.rules.get('survival', [4, 5, 6]):
                                new_grid[x, y, z] = 1
                        else:  # Currently dead
                            if neighbors in self.rules.get('birth', [5]):
                                new_grid[x, y, z] = 1
            
            self.grid = new_grid
    
    def generate_geometry(self) -> Dict[str, np.ndarray]:
        """Generate geometry from cellular automata grid"""
        vertices = []
        faces = []
        colors = []
        
        # Create cube for each living cell
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    if self.grid[x, y, z] == 1:
                        # Create cube vertices
                        cube_vertices = [
                            [x, y, z],
                            [x+1, y, z],
                            [x+1, y+1, z],
                            [x, y+1, z],
                            [x, y, z+1],
                            [x+1, y, z+1],
                            [x+1, y+1, z+1],
                            [x, y+1, z+1]
                        ]
                        
                        start_idx = len(vertices)
                        vertices.extend(cube_vertices)
                        
                        # Cube faces
                        cube_faces = [
                            [0, 1, 2], [0, 2, 3],  # Bottom
                            [4, 7, 6], [4, 6, 5],  # Top
                            [0, 4, 5], [0, 5, 1],  # Front
                            [2, 6, 7], [2, 7, 3],  # Back
                            [0, 3, 7], [0, 7, 4],  # Left
                            [1, 5, 6], [1, 6, 2]   # Right
                        ]
                        
                        # Offset face indices
                        for face in cube_faces:
                            faces.append([face[0] + start_idx, face[1] + start_idx, face[2] + start_idx])
                        
                        # Color based on position and audio
                        color = [
                            x / self.size + self.audio_energy * 0.2,
                            y / self.size + self.audio_energy * 0.3,
                            z / self.size + self.audio_energy * 0.1,
                            0.8
                        ]
                        
                        for _ in range(8):  # 8 vertices per cube
                            colors.append(color)
        
        return {
            'vertices': np.array(vertices, dtype=np.float32),
            'faces': np.array(faces, dtype=np.uint32),
            'colors': np.array(colors, dtype=np.float32)
        }

class ProceduralGeometryManager:
    """Manages all procedural geometry generation"""
    
    def __init__(self):
        # L-System presets
        self.lsystem_presets = {
            'tree': {
                'axiom': 'F',
                'rules': [
                    LSystemRule('F', 'FF+[+F-F-F]-[-F+F+F]', 0.7),
                    LSystemRule('F', 'F[+F][-F]', 0.3)
                ],
                'interpretation': {
                    'F': 'forward',
                    '+': 'turn_left',
                    '-': 'turn_right',
                    '[': 'push',
                    ']': 'pop'
                }
            },
            'crystal': {
                'axiom': 'F+F+F+F',
                'rules': [
                    LSystemRule('F', 'F+F-F-F+F', 1.0)
                ],
                'interpretation': {
                    'F': 'forward',
                    '+': 'turn_left',
                    '-': 'turn_right'
                }
            },
            'organic': {
                'axiom': 'F',
                'rules': [
                    LSystemRule('F', 'F[+F]F[-F]F', 0.6),
                    LSystemRule('F', 'FF', 0.4)
                ],
                'interpretation': {
                    'F': 'forward',
                    '+': 'turn_left',
                    '-': 'turn_right',
                    '[': 'push',
                    ']': 'pop'
                }
            }
        }
        
        # Initialize generators
        self.fractal_gen = FractalGenerator()
        self.parametric_gen = ParametricSurfaceGenerator()
        self.cellular_gen = CellularAutomataGenerator()
        
        # Current audio state
        self.audio_energy = 0.0
        self.audio_frequencies = np.zeros(512, dtype=np.float32)
        
    def update_audio(self, energy: float, frequencies: np.ndarray):
        """Update audio data for all generators"""
        self.audio_energy = energy
        self.audio_frequencies = frequencies
        
        self.fractal_gen.audio_energy = energy
        self.fractal_gen.audio_frequencies = frequencies
        
        self.parametric_gen.audio_energy = energy
        self.parametric_gen.audio_frequencies = frequencies
        
        self.cellular_gen.audio_energy = energy
    
    def generate_lsystem(self, preset_name: str, iterations: int = 5) -> Dict[str, np.ndarray]:
        """Generate L-System geometry"""
        if preset_name not in self.lsystem_presets:
            preset_name = 'tree'  # Default
        
        preset = self.lsystem_presets[preset_name]
        
        lsystem = LSystemGenerator(
            preset['axiom'],
            preset['rules'],
            preset['interpretation']
        )
        
        lsystem.iterate(iterations, self.audio_energy, self.audio_frequencies)
        return lsystem.generate_geometry()
    
    def generate_fractal(self, fractal_type: str = 'mandelbrot') -> Dict[str, np.ndarray]:
        """Generate fractal geometry"""
        if fractal_type == 'mandelbrot':
            return self.fractal_gen.generate_mandelbrot_surface(resolution=128)
        elif fractal_type == 'julia':
            return self.fractal_gen.generate_julia_set()
        elif fractal_type == 'sierpinski':
            # Sierpinski triangle IFS
            transforms = [
                np.array([[0.5, 0, 0], [0, 0.5, 0], [0, 0, 1]]),
                np.array([[0.5, 0, 0.5], [0, 0.5, 0], [0, 0, 1]]),
                np.array([[0.5, 0, 0.25], [0, 0.5, 0.5], [0, 0, 1]])
            ]
            return self.fractal_gen.generate_ifs_fractal(transforms)
        else:
            return self.fractal_gen.generate_mandelbrot_surface()
    
    def generate_parametric_surface(self, surface_type: str = 'torus') -> Dict[str, np.ndarray]:
        """Generate parametric surface"""
        if surface_type == 'torus':
            return self.parametric_gen.generate_torus()
        elif surface_type == 'klein_bottle':
            return self.parametric_gen.generate_klein_bottle()
        else:
            return self.parametric_gen.generate_torus()
    
    def generate_cellular_automata(self, iterations: int = 10) -> Dict[str, np.ndarray]:
        """Generate cellular automata structure"""
        self.cellular_gen.set_rules(survival=[4, 5, 6], birth=[5])
        self.cellular_gen.seed_random(density=0.3)
        self.cellular_gen.iterate(iterations)
        return self.cellular_gen.generate_geometry()
    
    def generate_audio_reactive_geometry(self, geometry_type: GeometryType = GeometryType.L_SYSTEM) -> Dict[str, np.ndarray]:
        """Generate geometry that reacts to current audio state"""
        if geometry_type == GeometryType.L_SYSTEM:
            # Choose L-system based on audio characteristics
            if self.audio_energy > 0.7:
                return self.generate_lsystem('organic', 6)
            elif self.audio_energy > 0.4:
                return self.generate_lsystem('tree', 5)
            else:
                return self.generate_lsystem('crystal', 4)
        
        elif geometry_type == GeometryType.FRACTAL:
            # Choose fractal based on audio
            dominant_freq = np.argmax(self.audio_frequencies) / len(self.audio_frequencies)
            
            if dominant_freq < 0.3:
                return self.generate_fractal('sierpinski')
            elif dominant_freq < 0.7:
                return self.generate_fractal('julia')
            else:
                return self.generate_fractal('mandelbrot')
        
        elif geometry_type == GeometryType.PARAMETRIC:
            # Audio-reactive surface choice
            if self.audio_energy > 0.5:
                return self.generate_parametric_surface('klein_bottle')
            else:
                return self.generate_parametric_surface('torus')
        
        elif geometry_type == GeometryType.CELLULAR_AUTOMATA:
            iterations = int(5 + self.audio_energy * 10)
            return self.generate_cellular_automata(iterations)
        
        else:
            return self.generate_lsystem('tree', 5)  # Default

if __name__ == "__main__":
    # Test procedural generators
    manager = ProceduralGeometryManager()
    
    # Simulate audio data
    manager.update_audio(0.7, np.random.random(512).astype(np.float32))
    
    print("🌿 Procedural Geometry Generation Test")
    print("=" * 50)
    
    # Test L-System
    lsystem_geo = manager.generate_lsystem('tree', 4)
    print(f"L-System Tree: {lsystem_geo['vertices'].shape[0]} vertices, {lsystem_geo['faces'].shape[0]} faces")
    
    # Test Fractal
    mandelbrot_geo = manager.generate_fractal('mandelbrot')
    print(f"Mandelbrot: {mandelbrot_geo['vertices'].shape[0]} vertices, {mandelbrot_geo['faces'].shape[0]} faces")
    
    # Test Parametric
    torus_geo = manager.generate_parametric_surface('torus')
    print(f"Torus: {torus_geo['vertices'].shape[0]} vertices, {torus_geo['faces'].shape[0]} faces")
    
    # Test Cellular Automata
    cellular_geo = manager.generate_cellular_automata(5)
    print(f"Cellular: {cellular_geo['vertices'].shape[0]} vertices, {cellular_geo['faces'].shape[0]} faces")
    
    print("✅ Procedural generation test completed!")