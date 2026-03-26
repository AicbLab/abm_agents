"""
实验 5 运行脚本：网络结构对比
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import SimulationConfig
from experiments.exp5_network_structure.simulation_network import NetworkStructureSimulation
from experiments.exp5_network_structure.network_variants import NetworkTopology
from experiments.exp5_network_structure.visualization_network import visualize_network_comparison


def run_experiment5():
    """运行实验 5: 网络结构对比"""
    print("="*70)
    print("【实验 5】异质性社交网络结构")
    print("研究问题：不同网络拓扑如何影响依赖扩散？")
    print("="*70)
    print("\n提示：实验 5 需要扩展 IsingSocialNetwork 以支持多种网络拓扑")
    print("当前框架已准备好，需要实现以下功能:")
    print("1. NetworkGenerator 生成不同类型的网络")
    print("2. 将生成的网络集成到 IsingSocialNetwork 中")
    print("3. 对比不同网络下的仿真结果")
    print("\n已创建的核心组件:")
    print("- network_variants.py: 网络生成器")
    print("- simulation_network.py: 网络结构仿真引擎")
    print("- visualization_network.py: 可视化模块")
    print("\n" + "="*70)
    print("实验 5 框架已完成，待实现完整功能!")
    print("="*70)


if __name__ == "__main__":
    run_experiment5()
