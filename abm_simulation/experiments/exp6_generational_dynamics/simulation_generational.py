"""
实验6仿真引擎: 代际演化
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict, List
from dataclasses import dataclass

from simulation import ABMSimulation, SimulationConfig
from experiments.exp6_generational_dynamics.generations import GenerationalDynamics


@dataclass
class GenerationalMetrics:
    """代际实验特有指标"""
    step: int
    generation_composition: Dict
    avg_dependency_by_generation: Dict
    generation_transitions: int


class GenerationalSimulation(ABMSimulation):
    """
    实验6: 代际演化仿真
    
    研究长期代际更替对AI依赖文化的影响
    """
    
    def __init__(self,
                 config: SimulationConfig,
                 generation_duration: int = 100,
                 n_generations: int = 5):
        """
        初始化代际仿真
        
        Args:
            config: 仿真配置
            generation_duration: 每代持续时间
            n_generations: 总代数
        """
        # 调整仿真步数以适应多代
        adjusted_config = SimulationConfig(
            **{**config.__dict__, 'n_steps': generation_duration * n_generations}
        )
        
        super().__init__(adjusted_config)
        
        # 初始化代际动力学
        self.generational_dynamics = GenerationalDynamics(
            initial_population=config.n_consumers,
            generation_duration=generation_duration,
            n_generations=n_generations
        )
        
        self.generational_metrics_history: List[GenerationalMetrics] = []
        self.generation_duration = generation_duration
        self.n_generations = n_generations
    
    def run_step(self) -> Dict:
        """运行单步仿真（包含代际更替）"""
        # 1. 执行代际步骤
        gen_events = self.generational_dynamics.step(self.current_step)
        
        # 2. 如果发生代际更替，更新消费者
        if gen_events['new_generation']:
            self._update_consumers_after_turnover()
        
        # 3. 消费者与AI交互
        for consumer in self.consumers:
            if consumer.dependency_level == 1:
                continue
            
            # 简化的交互模拟
            ai_recommendation = {
                'quality': np.random.beta(5, 2),
                'error': np.random.random() < 0.1
            }
            
            satisfaction = ai_recommendation['quality'] * 0.8 + 0.2
            if ai_recommendation['error']:
                satisfaction *= 0.5
            
            # 更新消费者
            if hasattr(consumer, 'update_from_experience'):
                consumer.update_from_experience(satisfaction, used_ai=True)
            
            # 同步依赖等级到网络
            self.network.set_node_spin(consumer.id, self.network.level_to_spin(consumer.dependency_level))
        
        # 4. Ising步骤（社会影响）
        self.network.monte_carlo_step(self.current_step)
        
        # 5. 同步网络状态回消费者
        for consumer in self.consumers:
            new_spin = self.network.get_node_spin(consumer.id)
            new_level = self.network.spin_to_level(new_spin)
            consumer.dependency_level = new_level
        
        # 6. 收集指标
        self._collect_generational_metrics(gen_events)
        
        self.current_step += 1
        return gen_events
    
    def _update_consumers_after_turnover(self):
        """代际更替后更新消费者列表"""
        # 获取新的代际消费者
        new_consumers = list(self.generational_dynamics.consumers.values())
        
        # 更新仿真中的消费者列表
        self.consumers = new_consumers
        
        # 同步网络状态
        for consumer in self.consumers:
            self.network.set_node_spin(consumer.id, self.network.level_to_spin(consumer.dependency_level))
    
    def _collect_generational_metrics(self, gen_events: Dict):
        """收集代际指标"""
        gen_summary = self.generational_dynamics.get_summary()
        
        # 计算各代平均依赖等级
        avg_dep_by_gen = {}
        for gen_type, levels in gen_summary['dependency_by_generation'].items():
            total = sum(levels.values())
            if total > 0:
                weighted_sum = sum(level * count for level, count in levels.items())
                avg_dep_by_gen[gen_type] = weighted_sum / total
            else:
                avg_dep_by_gen[gen_type] = 3.0
        
        metric = GenerationalMetrics(
            step=self.current_step,
            generation_composition=gen_summary['generation_composition'],
            avg_dependency_by_generation=avg_dep_by_gen,
            generation_transitions=len(gen_events.get('generation_transitions', []))
        )
        self.generational_metrics_history.append(metric)
    
    def get_generational_summary(self) -> Dict:
        """获取代际实验汇总"""
        gen_summary = self.generational_dynamics.get_summary()
        
        # 计算长期趋势
        if len(self.generational_metrics_history) >= 2:
            initial = self.generational_metrics_history[0]
            final = self.generational_metrics_history[-1]
            
            # 计算各代依赖等级的变化
            dependency_trends = {}
            for gen_type in initial.avg_dependency_by_generation.keys():
                init_val = initial.avg_dependency_by_generation.get(gen_type, 3.0)
                final_val = final.avg_dependency_by_generation.get(gen_type, 3.0)
                dependency_trends[gen_type] = {
                    'initial': init_val,
                    'final': final_val,
                    'change': final_val - init_val
                }
        else:
            dependency_trends = {}
        
        return {
            'generational_summary': gen_summary,
            'dependency_trends': dependency_trends,
            'final_generation_composition': gen_summary['generation_composition'],
            'total_generations_completed': self.generational_dynamics.current_generation + 1
        }
    
    def get_summary_statistics(self) -> Dict:
        """获取完整统计"""
        base_summary = super().get_summary_statistics()
        generational_summary = self.get_generational_summary()
        
        return {**base_summary, **generational_summary}


def run_experiment6():
    """运行实验6: 代际演化"""
    print("="*70)
    print("【实验6】多代际演化（长期动态）")
    print("研究问题: 代际更替如何改变AI依赖文化？")
    print("="*70)
    
    config = SimulationConfig(
        n_consumers=500,
        n_merchants=20,
        n_ai_agents=3,
        network_type='small_world',
        initial_coupling=0.2,
        initial_temperature=2.0,
    )
    
    print(f"\n仿真配置:")
    print(f"  - 每代持续时间: 100步")
    print(f"  - 总代数: 5代")
    print(f"  - 总仿真步数: 500步")
    
    sim = GenerationalSimulation(
        config=config,
        generation_duration=100,
        n_generations=5
    )
    
    sim.run()
    
    summary = sim.get_summary_statistics()
    
    print("\n【代际演化结果】")
    if 'generational_summary' in summary:
        gen = summary['generational_summary']
        print(f"  完成的代数: {summary.get('total_generations_completed', 0)}")
        print(f"\n  最终代际构成:")
        for gen_type, count in summary.get('final_generation_composition', {}).items():
            pct = count / 500 * 100
            print(f"    {gen_type}: {count} ({pct:.1f}%)")
        
        print(f"\n  各代依赖等级趋势:")
        for gen_type, trend in summary.get('dependency_trends', {}).items():
            print(f"    {gen_type}: {trend['initial']:.2f} -> {trend['final']:.2f} "
                  f"({trend['change']:+.2f})")
    
    print("\n【最终依赖等级分布】")
    final_dist = summary['final_level_distribution']
    for level in range(1, 6):
        count = final_dist.get(level, 0)
        pct = count / 500 * 100
        print(f"  L{level}: {count} ({pct:.1f}%)")
    
    # 生成可视化
    print("\n" + "="*70)
    print("生成可视化...")
    
    from experiments.exp6_generational_dynamics.visualization_generational import visualize_generational_results
    visualize_generational_results(sim, output_dir="experiments/exp6_generational_dynamics/results")
    
    print("\n" + "="*70)
    print("实验6完成!")
    print("="*70)
    
    return sim, summary


if __name__ == "__main__":
    sim, summary = run_experiment6()
