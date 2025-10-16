#!/usr/bin/env python3
"""
Test script for the distributed AudioBlenderVideo system
Verifies all components are working correctly
"""

import os
import sys
import time
import requests
import json
from pathlib import Path

def test_coordinator_health():
    """Test render coordinator health."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Coordinator healthy: {data['status']}")
            print(f"   Workers: {data['worker_count']}")
            print(f"   Active jobs: {data['active_jobs']}")
            return True
        else:
            print(f"❌ Coordinator unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Coordinator unreachable: {e}")
        return False

def test_workers():
    """Test worker health."""
    try:
        response = requests.get("http://localhost:8000/workers", timeout=5)
        if response.status_code == 200:
            workers = response.json()
            healthy_workers = 0
            for worker_name, worker_info in workers.items():
                if worker_info['status'] == 'healthy':
                    healthy_workers += 1
                    print(f"✅ {worker_name}: {worker_info['status']} ({worker_info['current_jobs']}/{worker_info['max_jobs']} jobs)")
                else:
                    print(f"❌ {worker_name}: {worker_info['status']}")
            
            print(f"   Total healthy workers: {healthy_workers}")
            return healthy_workers > 0
        else:
            print(f"❌ Failed to get worker status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to check workers: {e}")
        return False

def test_audio_processor():
    """Test audio processor health."""
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Audio processor healthy: {data['status']}")
            print(f"   GPU available: {data['gpu_available']}")
            print(f"   Cache size: {data['cache_size']} files")
            return True
        else:
            print(f"❌ Audio processor unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Audio processor unreachable: {e}")
        return False

def test_ai_optimizer():
    """Test AI optimizer health."""
    try:
        response = requests.get("http://localhost:8002/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI optimizer healthy: {data['status']}")
            print(f"   OpenAI available: {data['openai_available']}")
            print(f"   Anthropic available: {data['anthropic_available']}")
            print(f"   Models loaded: {data['models_loaded']}")
            return True
        else:
            print(f"❌ AI optimizer unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI optimizer unreachable: {e}")
        return False

def test_redis():
    """Test Redis connection."""
    try:
        import redis
        r = redis.from_url("redis://localhost:6379")
        r.ping()
        print("✅ Redis connection healthy")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def test_distributed_renderer():
    """Test distributed renderer integration."""
    try:
        sys.path.insert(0, 'src')
        from distributed_renderer import get_best_renderer
        
        renderer = get_best_renderer()
        system_info = renderer.get_system_info()
        
        print(f"✅ Distributed renderer integration working")
        print(f"   System type: {system_info['type']}")
        print(f"   Available: {system_info['available']}")
        
        if system_info['type'] == 'distributed':
            print(f"   Workers: {len(system_info['workers'])}")
            print(f"   Status: {system_info['status']['status']}")
        
        return True
    except Exception as e:
        print(f"❌ Distributed renderer test failed: {e}")
        return False

def test_audio_analysis():
    """Test audio analysis with sample data."""
    try:
        # Create a simple test audio file (1 second of silence)
        import numpy as np
        import soundfile as sf
        
        test_audio_path = "test_audio.wav"
        sample_rate = 44100
        duration = 1.0  # 1 second
        
        # Generate a simple sine wave
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = 0.1 * np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
        
        sf.write(test_audio_path, audio_data, sample_rate)
        
        # Test audio processor
        response = requests.post(
            "http://localhost:8001/analyze",
            json={'audio_path': test_audio_path, 'fps': 60},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Audio analysis working")
            print(f"   Duration: {data['duration']:.2f}s")
            print(f"   Frames: {data['total_frames']}")
            print(f"   Processing time: {data['processing_time']:.2f}s")
            
            # Clean up
            os.unlink(test_audio_path)
            return True
        else:
            print(f"❌ Audio analysis failed: {response.status_code}")
            os.unlink(test_audio_path)
            return False
            
    except Exception as e:
        print(f"❌ Audio analysis test failed: {e}")
        return False

def test_ai_optimization():
    """Test AI optimization with sample data."""
    try:
        sample_audio_features = {
            'duration': 60.0,
            'fps': 60,
            'total_frames': 3600,
            'bass_energy': [0.5] * 100,
            'mid_energy': [0.5] * 100,
            'high_energy': [0.5] * 100,
            'onset_strength': [0.5] * 100
        }
        
        sample_hardware_specs = {
            'gpu_memory': 16,
            'cpu_cores': 16,
            'system_memory': 32,
            'gpu_compute_capability': 8.6
        }
        
        response = requests.post(
            "http://localhost:8002/optimize",
            json={
                'audio_features': sample_audio_features,
                'hardware_specs': sample_hardware_specs,
                'target_quality': 'balanced',
                'target_speed': 'fast'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI optimization working")
            print(f"   Engine: {data['optimized_parameters']['engine']}")
            print(f"   Samples: {data['optimized_parameters']['samples']}")
            print(f"   Quality score: {data['quality_score']:.1f}/100")
            print(f"   Estimated time: {data['estimated_render_time']:.1f}s")
            return True
        else:
            print(f"❌ AI optimization failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI optimization test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Distributed AudioBlenderVideo System")
    print("=" * 50)
    
    tests = [
        ("Redis Connection", test_redis),
        ("Render Coordinator", test_coordinator_health),
        ("Worker Health", test_workers),
        ("Audio Processor", test_audio_processor),
        ("AI Optimizer", test_ai_optimizer),
        ("Distributed Renderer", test_distributed_renderer),
        ("Audio Analysis", test_audio_analysis),
        ("AI Optimization", test_ai_optimization),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"   ⚠️ {test_name} test failed")
        except Exception as e:
            print(f"   ❌ {test_name} test error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Distributed system is ready!")
        print("\n🚀 You can now run: python src/main.py")
        print("   The system will automatically use distributed rendering!")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure Docker is running: docker ps")
        print("   2. Check if services are up: docker-compose ps")
        print("   3. View logs: docker-compose logs")
        print("   4. Restart system: docker-compose restart")

if __name__ == "__main__":
    main()
