"""
实验5仿真引擎: 网络结构对比
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict, List
from dataclasses import dataclass

from simulation import ABMSimulation, SimulationConfig
from models.ising_network import IsingSocialNetwork
from experiments.exp5_network_structure.network_variants import (
    NetworkTopology, NetworkGenerator, NetworkMetricsAnalyzer
)


@dataclass
class NetworkComparisonMetrics:
    """网络对比指标"""
    topology: str
    network_metrics: Dict
    simulation_metrics: Dict
    convergence_step: int
    final_polarization: float


class NetworkStructureSimulation(ABMSimulation):
    """
    实验5: 网络结构仿真
    
    使用不同网络拓扑运行仿真
    """
    
    def __init__(self, 
                 config: SimulationConfig,
                 topology: NetworkTopology = NetworkTopology.SMALL_WORLD):
        """
        初始化网络结构仿真
        
        Args:
            config: 仿真配置
            topology: 网络拓扑类型
        """
        self.topology = topology
        self.network_metrics = {}
        
        # 先保存配置，然后手动初始化
        self.config = config
        self.current_step = 0
        self.metrics_history = []
        
        # 生成指定拓扑的网络
        self._generate_network_with_topology()
        
        # 初始化消费者（使用生成的网络）
        self._init_consumers_with_network()
        
        # 初始化其他组件
        from agents.ai_agent import AIAgentPopulation
        from environment.market import MarketEnvironment
        
        self.ai_population = AIAgentPopulation(n_agents=config.n_ai_agents)
        self.market = MarketEnvironment(n_merchants=config.n_merchants)
        
        # 分析网络指标
        self.network_metrics = NetworkMetricsAnalyzer.analyze(self.network.graph)
    
    def _generate_network_with_topology(self):
        """生成指定拓扑的网络"""
        generator = NetworkGenerator(n_nodes=self.config.n_consumers)
        graph = generator.generate(self.topology)
        
        # 创建 Ising 网络（继承原有功能）
        self.network = IsingSocialNetwork(
            n_agents=self.config.n_consumers,
            network_type='small_world'  # 使用 small_world，但会被下面的 graph 替换
        )
        # 替换底层图
        self.network.graph = graph
        self.network.adjacency = nx.to_numpy_array(graph)
        
        # 初始化自旋状态
        self.network.initialize_spins()
    
    def _init_consumers_with_network(self):
        """使用网络初始化消费者"""
        from agents.consumer_dib import ConsumerAgentDIB, ConsumerTraits
        
        self.consumers = []
        for i in range(self.config.n_consumers):
            # 根据自旋状态确定初始依赖等级
            spin = self.network.get_node_spin(i)
            initial_level = self.network.spin_to_level(spin)
            
            traits = ConsumerTraits()
            consumer = ConsumerAgentDIB(
                consumer_id=i,
                initial_dependency_level=initial_level,
                traits=traits
            )
            self.consumers.append(consumer)
    
    def run(self) -> Dict:
        """运行仿真并收集网络特定指标"""
        results = super().run()
        
        # 添加网络指标
        results['network_topology'] = self.topology.value
        results['network_metrics'] = self.network_metrics
        
        return results
    
    def get_network_summary(self) -> Dict:
        """获取网络结构汇总"""
        return {
            'topology': self.topology.value,
            'network_metrics': self.network_metrics,
            'n_nodes': self.network_metrics.get('n_nodes', 0),
            'avg_degree': self.network_metrics.get('avg_degree', 0),
            'clustering': self.network_metrics.get('avg_clustering', 0),
            'path_length': self.network_metrics.get('avg_path_length', 0),
            'modularity': self.network_metrics.get('modularity', 0),
        }
    
    def get_summary_statistics(self) -> Dict:
        """获取完整统计"""
        base_summary = super().get_summary_statistics()
        network_summary = self.get_network_summary()
        
        return {**base_summary, **network_summary}


import networkx as nx


def run_network_comparison():
    """运行网络结构对比实验"""
    print("="*70)
    print("【实验5】异质性社交网络结构")
    print("研究问题: 不同网络拓扑如何影响依赖扩散？")
    print("="*70)
    
    config = SimulationConfig(
        n_consumers=500,
        n_merchants=20,
        n_ai_agents=3,
        n_steps=300,
        initial_coupling=0.2,
        initial_temperature=2.0,
        enable_adaptive_coupling=True,
    )
    
    topologies = [
        NetworkTopology.SMALL_WORLD,
        NetworkTopology.SCALE_FREE,
        NetworkTopology.COMMUNITY,
        NetworkTopology.RANDOM,
        NetworkTopology.REGULAR,
    ]
    
    results = {}
    
    for topology in topologies:
        print(f"\n{'='*70}")
        print(f"运行 {topology.value} 网络拓扑...")
        print("="*70)
        
        sim = NetworkStructureSimulation(config, topology=topology)
        sim.run()
        
        summary = sim.get_summary_statistics()
        results[topology.value] = (sim, summary)
        
        # 输出网络指标
        print(f"\n网络指标:")
        print(f"  平均度: {summary.get('avg_degree', 0):.2f}")
        print(f"  聚类系数: {summary.get('clustering', 0):.3f}")
        print(f"  平均路径长度: {summary.get('path_length', 0):.2f}")
        print(f"  模块度: {summary.get('modularity', 0):.3f}")
        
        # 输出仿真结果
        print(f"\n仿真结果:")
        final_dist = summary['final_level_distribution']
        for level in range(1, 6):
            count = final_dist.get(level, 0)
            pct = count / config.n_consumers * 100
            print(f"  L{level}: {pct:.1f}%")
    
    # 对比分析
    print("\n" + "="*70)
    print("【网络拓扑对比分析】")
    print("="*70)
    
    print(f"\n{'拓扑':<15} {'L5%':<8} {'满意度':<8} {'聚类':<8} {'路径长':<8}")
    print("-" * 55)
    
    for topo_name, (sim, summary) in results.items():
        l5_pct = summary['final_level_distribution'].get(5, 0) / 500 * 100
        sat = summary.get('satisfaction', {}).get('mean', 0)
        clust = summary.get('clustering', 0)
        path = summary.get('path_length', 0)
        print(f"{topo_name:<15} {l5_pct:<8.1f} {sat:<8.3f} {clust:<8.3f} {path:<8.2f}")
    
    # 生成可视化
    print("\n" + "="*70)
    print("生成可视化...")
    
    from experiments.exp5_network_structure.visualization_network import visualize_network_comparison
    visualize_network_comparison(results, output_dir="experiments/exp5_network_structure/results")
    
    print("\n" + "="*70)
    print("实验5完成!")
    print("="*70)
    
    return results


if __name__ == "__main__":
    results = run_network_comparison()
