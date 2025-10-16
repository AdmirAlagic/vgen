#!/usr/bin/env python3
"""
AudioBlender Video Generator Crew
================================

Optimized CrewAI implementation following latest standards for autonomous
development of high-fidelity audio-reactive video generation.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.llm import LLM

# Import custom tools
try:
    from audioblender_video_generator.tools.audio_analysis_tool import AudioAnalysisTool
    from audioblender_video_generator.tools.blender_optimization_tool import BlenderOptimizationTool
    from audioblender_video_generator.tools.rendering_optimization_tool import RenderingOptimizationTool
    from audioblender_video_generator.tools.quality_assessment_tool import QualityAssessmentTool
except ImportError:
    # Fallback to local tools if not in package structure
    from tools.audio_analysis_tool import AudioAnalysisTool
    from tools.blender_optimization_tool import BlenderOptimizationTool
    from tools.rendering_optimization_tool import RenderingOptimizationTool
    from tools.quality_assessment_tool import QualityAssessmentTool

@CrewBase
class AudioBlenderVideoGeneratorCrew:
    """AudioBlender Video Generator crew for autonomous development"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @before_kickoff
    def before_kickoff_function(self, inputs):
        """Initialize the system before crew execution."""
        print(f"🚀 Initializing AudioBlender Video Generator Crew")
        print(f"📋 Input parameters: {inputs}")
        
        # Validate inputs
        if 'topic' not in inputs:
            inputs['topic'] = 'Audio-Reactive Video Generation'
        
        # Set up output directory
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        return inputs

    @after_kickoff
    def after_kickoff_function(self, result):
        """Process results after crew execution."""
        print(f"✅ AudioBlender Crew execution completed")
        print(f"📊 Results summary: {len(result)} tasks completed")
        
        # Save comprehensive results
        self._save_comprehensive_results(result)
        
        return result

    @agent
    def audio_analysis_specialist(self) -> Agent:
        """Audio Analysis Specialist agent."""
        return Agent(
            config=self.agents_config['audio_analysis_specialist'],  # type: ignore[index]
            verbose=True,
            tools=[AudioAnalysisTool()],
            llm=self._get_optimized_llm()
        )

    @agent
    def blender_animation_expert(self) -> Agent:
        """Blender Animation Expert agent."""
        return Agent(
            config=self.agents_config['blender_animation_expert'],  # type: ignore[index]
            verbose=True,
            tools=[BlenderOptimizationTool()],
            llm=self._get_optimized_llm()
        )

    @agent
    def rendering_performance_specialist(self) -> Agent:
        """Rendering Performance Specialist agent."""
        return Agent(
            config=self.agents_config['rendering_performance_specialist'],  # type: ignore[index]
            verbose=True,
            tools=[RenderingOptimizationTool()],
            llm=self._get_optimized_llm()
        )

    @agent
    def quality_assurance_manager(self) -> Agent:
        """Quality Assurance Manager agent."""
        return Agent(
            config=self.agents_config['quality_assurance_manager'],  # type: ignore[index]
            verbose=True,
            tools=[QualityAssessmentTool()],
            llm=self._get_optimized_llm()
        )

    @agent
    def project_orchestrator(self) -> Agent:
        """Project Orchestrator agent."""
        return Agent(
            config=self.agents_config['project_orchestrator'],  # type: ignore[index]
            verbose=True,
            tools=[
                AudioAnalysisTool(),
                BlenderOptimizationTool(),
                RenderingOptimizationTool(),
                QualityAssessmentTool()
            ],
            llm=self._get_optimized_llm(),
            allow_delegation=True
        )

    @task
    def audio_optimization_task(self) -> Task:
        """Audio optimization task."""
        return Task(
            config=self.tasks_config['audio_optimization_task'],  # type: ignore[index]
            output_file='output/audio_optimization_report.md'
        )

    @task
    def blender_enhancement_task(self) -> Task:
        """Blender enhancement task."""
        return Task(
            config=self.tasks_config['blender_enhancement_task'],  # type: ignore[index]
            output_file='output/blender_enhancement_report.md'
        )

    @task
    def rendering_optimization_task(self) -> Task:
        """Rendering optimization task."""
        return Task(
            config=self.tasks_config['rendering_optimization_task'],  # type: ignore[index]
            output_file='output/rendering_optimization_report.md'
        )

    @task
    def quality_assessment_task(self) -> Task:
        """Quality assessment task."""
        return Task(
            config=self.tasks_config['quality_assessment_task'],  # type: ignore[index]
            output_file='output/quality_assessment_report.md'
        )

    @task
    def orchestration_task(self) -> Task:
        """Orchestration task."""
        return Task(
            config=self.tasks_config['orchestration_task'],  # type: ignore[index]
            output_file='output/orchestration_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AudioBlender Video Generator crew."""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            manager_llm=self._get_manager_llm()
        )

    def _get_optimized_llm(self) -> LLM:
        """Get optimized LLM configuration for agents."""
        # Check for available API keys and use the best available model
        if os.getenv("OPENAI_API_KEY"):
            return LLM(
                model="gpt-4o",
                temperature=0.1,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif os.getenv("ANTHROPIC_API_KEY"):
            return LLM(
                model="claude-3-5-sonnet-20241022",
                temperature=0.1,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            # Fallback to default
            return LLM(
                model="gpt-3.5-turbo",
                temperature=0.1
            )

    def _get_manager_llm(self) -> LLM:
        """Get LLM configuration for crew manager."""
        # Use Claude for management decisions if available
        if os.getenv("ANTHROPIC_API_KEY"):
            return LLM(
                model="claude-3-5-sonnet-20241022",
                temperature=0.05,  # Lower temperature for consistent management
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            return self._get_optimized_llm()

    def _save_comprehensive_results(self, result):
        """Save comprehensive results from crew execution."""
        import json
        from datetime import datetime
        
        output_dir = Path("output/autonomous")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        results_file = output_dir / f"crew_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "status": "completed",
                "results": str(result),
                "crew_type": "AudioBlender Video Generator",
                "version": "2.0"
            }, f, indent=2)
        
        print(f"💾 Comprehensive results saved to: {results_file}")

    def run_autonomous_development(self, audio_file: str = None, target_quality: str = "commercial") -> Dict[str, Any]:
        """Run autonomous development process with optimized crew."""
        print("🤖 Starting AudioBlender Autonomous Development Process")
        print("=" * 70)
        
        # Prepare inputs
        inputs = {
            'topic': 'Audio-Reactive Video Generation',
            'audio_file': audio_file,
            'target_quality': target_quality,
            'project_path': str(Path(__file__).parent.parent.parent),
            'output_path': str(Path(__file__).parent.parent.parent / "output"),
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Execute the crew
            result = self.crew().kickoff(inputs=inputs)
            
            print("✅ Autonomous Development Complete")
            print("=" * 70)
            
            return {
                "status": "success",
                "result": result,
                "inputs": inputs,
                "improvements_applied": True,
                "crew_version": "2.0_optimized"
            }
            
        except Exception as e:
            print(f"❌ Error in autonomous development: {e}")
            return {
                "status": "error",
                "error": str(e),
                "inputs": inputs,
                "crew_version": "2.0_optimized"
            }
