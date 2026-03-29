"""
交互式运行 ABM 仿真 - 手动输入初始人群比例

使用方法:
    python run_interactive.py
    
功能:
    1. 提示用户输入 L1-L5 各等级的初始比例
    2. 验证输入的有效性（总和必须为 1）
    3. 使用自定义比例启动完整仿真
    4. 输出结果汇总和可视化
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'abm_simulation'))

from simulation import ABMSimulation, SimulationConfig
try:
    from visualization.plots import quick_visualize
    has_viz = True
except ImportError:
    has_viz = False
    print("  可视化模块未找到，将跳过图表生成")

def main():
    print("="*70)
    print("ABM 消费决策代理仿真系统 - 交互式版本")
    print("模型：Ising-D-I-B (Desire-Intention-Behavior)")
    print("="*70)
    print()
    
    # 方式 1: 完全交互式（推荐）
    print("正在启动交互式配置...")
    print()
    
    try:
        # 创建交互式仿真对象
        sim = ABMSimulation(interactive=True)
        
        print("\n" + "="*70)
        print(" 仿真初始化完成！")
        print("="*70)
        print(f"\n当前配置:")
        print(f"   消费者数量：{sim.config.n_consumers}")
        print(f"   商家数量：{sim.config.n_merchants}")
        print(f"   AI 代理数量：{sim.config.n_ai_agents}")
        print(f"   仿真步数：{sim.config.n_steps}")
        print(f"   网络类型：{sim.config.network_type}")
        print(f"   初始耦合强度：{sim.config.initial_coupling}")
        print(f"   初始温度：{sim.config.initial_temperature}")
        print()
        
        # 显示初始分布
        print("初始依赖等级分布:")
        dist = sim.config.initial_level_distribution
        level_names = {
            1: 'L1 自主',
            2: 'L2 信息辅助',
            3: 'L3 半委托',
            4: 'L4 高度依赖',
            5: 'L5 完全代理'
        }
        for level in range(1, 6):
            ratio = dist.get(level, 0)
            bar = '' * int(ratio * 20)
            print(f"  {level_names[level]:<12}: {ratio*100:5.1f}% {bar}")
        print()
        
        # 询问是否开始仿真
        print("是否开始运行仿真？(Y/n): ", end='')
        response = input().strip().lower()
        
        if response == '' or response == 'y':
            print("\n 开始仿真...\n")
            print("="*70)
            
            # 运行仿真
            metrics = sim.run()
            
            # 输出汇总结果
            summary = sim.get_summary_statistics()
            
            print("\n" + "="*70)
            print("仿真结果汇总")
            print("="*70)
            
            print("\n【依赖等级分布演化】")
            init_dist = sim.metrics_history[0].level_distribution if sim.metrics_history else {}
            final_dist = summary['final_level_distribution']
            
            print(f"{'等级':<12} {'初始':<10} {'最终':<10} {'变化'}")
            print("-" * 45)
            for level in range(1, 6):
                init = init_dist.get(level, 0)
                final = final_dist.get(level, 0)
                change = final - init
                change_str = f"+{change}" if change > 0 else str(change)
                print(f"{level_names[level]:<12} {init:<10} {final:<10} {change_str}")
            
            print("\n【Ising 动力学】")
            mag_trend = summary['magnetization_trend']
            print(f"  磁化强度：{mag_trend['initial']:.3f}  {mag_trend['final']:.3f} (变化：{mag_trend['change']:+.3f})")
            print(f"  临界耦合强度：{sim.network.get_critical_J():.4f}")
            
            print("\n【消费者行为】")
            print(f"  平均满意度：{summary['satisfaction']['mean']:.3f}")
            print(f"  AI 使用率：{summary['ai_usage']:.3f}")
            print(f"  错误率：{summary['error_rate']:.3f}")
            
            print("\n【网络拓扑】")
            net_metrics = summary['network_metrics']
            print(f"  平均聚类系数：{net_metrics.get('avg_clustering', 0):.3f}")
            print(f"  平均路径长度：{net_metrics.get('avg_path_length', 0):.2f}")
            
            # 生成可视化
            if has_viz:
                print("\n" + "="*70)
                print("生成可视化图表...")
                print("="*70)
                viz = quick_visualize(sim, output_dir="results/interactive")
                print("\n 图表已保存至 results/interactive/ 目录")
            
            print("\n" + "="*70)
            print(" 仿真完成!")
            print("="*70)
            
        else:
            print("\n已取消仿真运行")
            
    except KeyboardInterrupt:
        print("\n\n  用户中断")
    except Exception as e:
        print(f"\n  发生错误：{e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print("程序结束")
    print("="*70)

if __name__ == "__main__":
    main()
