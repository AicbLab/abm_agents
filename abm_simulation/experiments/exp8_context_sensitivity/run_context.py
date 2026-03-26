"""
实验8运行脚本: 情境敏感性
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from experiments.exp8_context_sensitivity.contexts import (
    ContextExperimentRunner, ConsumptionContext
)
from experiments.exp8_context_sensitivity.visualization_context import visualize_context_results


def run_experiment8():
    """运行实验8: 情境敏感性"""
    print("="*70)
    print("【实验8】情境敏感性实验")
    print("研究问题: 不同消费场景下依赖行为差异？")
    print("="*70)
    
    print(f"\n仿真配置:")
    print(f"  - 消费者数量: 500")
    print(f"  - 测试情境: 6种")
    print(f"  - 每情境轮数: 50")
    
    # 创建实验运行器
    runner = ContextExperimentRunner(n_consumers=500)
    
    # 运行所有情境实验
    print("\n运行各情境实验...")
    results = runner.run_all_contexts()
    
    # 输出结果
    print("\n【各情境实验结果】")
    print(f"\n{'情境':<25} {'AI使用率':<12} {'满意度':<12} {'调整后等级':<12}")
    print("-" * 65)
    
    for context_name, result in results.items():
        print(f"{context_name:<25} {result['ai_usage_rate']*100:<12.1f} "
              f"{result['avg_satisfaction']:<12.3f} {result['avg_adjusted_level']:<12.2f}")
    
    # 跨情境分析
    print("\n【跨情境分析】")
    analysis = runner.get_cross_context_analysis()
    
    print("\nAI使用率排名:")
    for ctx, rate in analysis['context_ranking_by_ai_usage']:
        print(f"  {ctx}: {rate*100:.1f}%")
    
    print("\n满意度排名:")
    for ctx, sat in analysis['context_ranking_by_satisfaction']:
        print(f"  {ctx}: {sat:.3f}")
    
    # 生成可视化
    print("\n" + "="*70)
    print("生成可视化...")
    visualize_context_results(runner, output_dir="experiments/exp8_context_sensitivity/results")
    
    print("\n" + "="*70)
    print("实验8完成!")
    print("="*70)
    
    return runner, results


if __name__ == "__main__":
    runner, results = run_experiment8()
