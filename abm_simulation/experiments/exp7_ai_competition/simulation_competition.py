"""
实验7仿真引擎: AI竞争
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict, List
from dataclasses import dataclass

from simulation import ABMSimulation, SimulationConfig
from experiments.exp7_ai_competition.ai_competition import CompetitiveAIMarket


@dataclass
class CompetitionMetrics:
    """竞争实验特有指标"""
    step: int
    market_concentration: float
    competition_intensity: float
    avg_consumer_satisfaction: float
    market_leader_id: int


class CompetitionSimulation(ABMSimulation):
    """
    实验7: AI竞争仿真
    
    研究多AI市场竞争对消费者选择的影响
    """
    
    def __init__(self,
                 config: SimulationConfig,
                 n_ai_agents: int = 4):
        """
        初始化竞争仿真
        
        Args:
            config: 仿真配置
            n_ai_agents: AI代理数量
        """
        super().__init__(config)
        
        # 替换为竞争性AI市场
        self.ai_market = CompetitiveAIMarket(n_agents=n_ai_agents)
        
        self.competition_metrics_history: List[CompetitionMetrics] = []
    
    def run_step(self) -> Dict:
        """运行单步仿真（包含竞争）"""
        step_metrics = {
            'competitions': 0,
            'satisfaction_sum': 0,
        }
        
        # 1. 消费者决策和AI竞争
        for consumer in self.consumers:
            if consumer.dependency_level == 1:
                continue
            
            # AI竞争
            winner, choice_details = self.ai_market.compete_for_consumer(
                consumer_id=consumer.id,
                consumer_level=consumer.dependency_level,
                consumer_traits={
                    'quality_preference': 0.5 + consumer.traits.satisfaction_sensitivity * 0.3,
                    'price_sensitivity': 0.3,
                    'reputation_preference': consumer.traits.trust_tendency
                }
            )
            
            # 模拟服务结果
            offer = None
            for agent in self.ai_market.agents:
                if agent.id == winner.id:
                    offer = agent.make_competitive_offer(
                        consumer.id, consumer.dependency_level, []
                    )
                    break
            
            if offer:
                # 计算满意度
                error_occurred = np.random.random() < offer['error_prob']
                if error_occurred:
                    satisfaction = 0.3
                else:
                    satisfaction = 0.5 + offer['quality'] * 0.5
                
                # 更新AI
                winner.update_from_outcome(
                    consumer_id=consumer.id,
                    won=True,
                    satisfaction=satisfaction
                )
                
                step_metrics['competitions'] += 1
                step_metrics['satisfaction_sum'] += satisfaction
        
        # 2. 更新市场份额
        self.ai_market.update_market_shares(len(self.consumers))
        
        # 3. Ising步骤
        self.network.monte_carlo_step(self.current_step)
        
        # 4. 更新消费者
        for consumer in self.consumers:
            new_spin = self.network.get_node_spin(consumer.id)
            new_level = self.network.spin_to_level(new_spin)
            consumer.update_dependency_level(new_level)
        
        # 5. 收集指标
        self._collect_competition_metrics(step_metrics)
        
        self.current_step += 1
        return step_metrics
    
    def _collect_competition_metrics(self, step_metrics: Dict):
        """收集竞争指标"""
        market_metrics = self.ai_market.get_market_metrics()
        
        # 找出市场领导者
        agent_metrics = market_metrics['agent_metrics']
        leader = max(agent_metrics, key=lambda x: x['market_share']) if agent_metrics else {'agent_id': -1}
        
        avg_sat = (step_metrics['satisfaction_sum'] / max(1, step_metrics['competitions'])) if step_metrics['competitions'] > 0 else 0.5
        
        metric = CompetitionMetrics(
            step=self.current_step,
            market_concentration=market_metrics['market_concentration'],
            competition_intensity=market_metrics['competition_intensity'],
            avg_consumer_satisfaction=avg_sat,
            market_leader_id=leader['agent_id']
        )
        self.competition_metrics_history.append(metric)
    
    def get_competition_summary(self) -> Dict:
        """获取竞争实验汇总"""
        market_metrics = self.ai_market.get_market_metrics()
        
        # 计算竞争效果
        if len(self.competition_metrics_history) >= 2:
            initial = self.competition_metrics_history[0]
            final = self.competition_metrics_history[-1]
            
            competition_evolution = {
                'initial_concentration': initial.market_concentration,
                'final_concentration': final.market_concentration,
                'concentration_change': final.market_concentration - initial.market_concentration,
                'avg_competition_intensity': np.mean([m.competition_intensity for m in self.competition_metrics_history])
            }
        else:
            competition_evolution = {}
        
        return {
            'market_metrics': market_metrics,
            'competition_evolution': competition_evolution,
            'final_market_shares': {m['agent_id']: m['market_share'] for m in market_metrics['agent_metrics']},
            'strategy_performance': self._analyze_strategy_performance()
        }
    
    def _analyze_strategy_performance(self) -> Dict:
        """分析各策略表现"""
        strategy_performance = {}
        
        for agent in self.ai_market.agents:
            strategy = agent.strategy.value
            if strategy not in strategy_performance:
                strategy_performance[strategy] = {
                    'count': 0,
                    'total_market_share': 0,
                    'total_reputation': 0
                }
            
            strategy_performance[strategy]['count'] += 1
            strategy_performance[strategy]['total_market_share'] += agent.profile.market_share
            strategy_performance[strategy]['total_reputation'] += agent.profile.reputation
        
        # 计算平均
        for strategy in strategy_performance:
            count = strategy_performance[strategy]['count']
            if count > 0:
                strategy_performance[strategy]['avg_market_share'] = (
                    strategy_performance[strategy]['total_market_share'] / count
                )
                strategy_performance[strategy]['avg_reputation'] = (
                    strategy_performance[strategy]['total_reputation'] / count
                )
        
        return strategy_performance
    
    def get_summary_statistics(self) -> Dict:
        """获取完整统计"""
        base_summary = super().get_summary_statistics()
        competition_summary = self.get_competition_summary()
        
        return {**base_summary, **competition_summary}


def run_experiment7():
    """运行实验7: AI竞争"""
    print("="*70)
    print("【实验7】竞争AI代理市场")
    print("研究问题: 多AI竞争如何影响消费者选择？")
    print("="*70)
    
    config = SimulationConfig(
        n_consumers=500,
        n_merchants=20,
        n_ai_agents=4,
        network_type='small_world',
        n_steps=300,
        initial_coupling=0.2,
        initial_temperature=2.0,
    )
    
    print(f"\n仿真配置:")
    print(f"  - 消费者数量: {config.n_consumers}")
    print(f"  - AI代理数量: {config.n_ai_agents}")
    print(f"  - 竞争策略: 价格竞争、质量溢价、差异化、协作")
    
    sim = CompetitionSimulation(config, n_ai_agents=4)
    sim.run()
    
    summary = sim.get_summary_statistics()
    
    print("\n【市场竞争结果】")
    if 'market_metrics' in summary:
        market = summary['market_metrics']
        print(f"  市场竞争强度: {market.get('competition_intensity', 0):.3f}")
        print(f"  市场集中度(HHI): {market.get('market_concentration', 0):.3f}")
        
        print(f"\n  各AI市场份额:")
        for agent_metric in market.get('agent_metrics', []):
            print(f"    AI-{agent_metric['agent_id']} ({agent_metric['strategy']}): "
                  f"{agent_metric['market_share']*100:.1f}%")
    
    if 'strategy_performance' in summary:
        print(f"\n  策略表现:")
        for strategy, perf in summary['strategy_performance'].items():
            print(f"    {strategy}: 平均份额 {perf.get('avg_market_share', 0)*100:.1f}%, "
                  f"声誉 {perf.get('avg_reputation', 0):.3f}")
    
    print("\n【最终依赖等级分布】")
    final_dist = summary['final_level_distribution']
    for level in range(1, 6):
        count = final_dist.get(level, 0)
        pct = count / config.n_consumers * 100
        print(f"  L{level}: {count} ({pct:.1f}%)")
    
    # 生成可视化
    print("\n" + "="*70)
    print("生成可视化...")
    
    from experiments.exp7_ai_competition.visualization_competition import visualize_competition_results
    visualize_competition_results(sim, output_dir="experiments/exp7_ai_competition/results")
    
    print("\n" + "="*70)
    print("实验7完成!")
    print("="*70)
    
    return sim, summary


if __name__ == "__main__":
    sim, summary = run_experiment7()
