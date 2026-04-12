"""
可视化模块
生成仿真结果图表
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # 必须在 import pyplot 之前设置，否则在图形环境中可能使用错误后端
import matplotlib.pyplot as plt
from typing import List, Dict, Optional
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class SimulationVisualizer:
    """仿真结果可视化器"""
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_level_distribution_evolution(self, metrics_history: List, save: bool = True):
        """绘制依赖等级分布演化"""
        steps = [m.step for m in metrics_history]
        
        # 提取各级别数量
        levels_data = {i: [] for i in range(1, 6)}
        for m in metrics_history:
            for level in range(1, 6):
                levels_data[level].append(m.level_distribution.get(level, 0))
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        labels = ['L1 自主型', 'L2 信息辅助', 'L3 半委托', 'L4 高度依赖', 'L5 完全代理']
        
        for level, color, label in zip(range(1, 6), colors, labels):
            ax.plot(steps, levels_data[level], label=label, color=color, linewidth=2)
        
        ax.set_xlabel('仿真步数', fontsize=12)
        ax.set_ylabel('智能体数量', fontsize=12)
        ax.set_title('AI依赖等级分布演化', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        if save:
            plt.savefig(f"{self.output_dir}/level_distribution_evolution.png", dpi=150, bbox_inches='tight')
        plt.close()
    
    def plot_magnetization(self, metrics_history: List, save: bool = True):
        """绘制磁化强度演化"""
        steps = [m.step for m in metrics_history]
        magnetizations = [m.magnetization for m in metrics_history]
        temperatures = [m.temperature for m in metrics_history]
        couplings = [m.coupling_strength for m in metrics_history]
        
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        
        # 磁化强度
        ax = axes[0]
        ax.plot(steps, magnetizations, 'b-', linewidth=2)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax.set_ylabel('磁化强度 M', fontsize=11)
        ax.set_title('Ising序参量演化', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 温度
        ax = axes[1]
        ax.plot(steps, temperatures, 'r-', linewidth=2)
        ax.set_ylabel('温度 T', fontsize=11)
        ax.set_title('社会温度演化', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 耦合强度
        ax = axes[2]
        ax.plot(steps, couplings, 'g-', linewidth=2)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('耦合强度 J', fontsize=11)
        ax.set_title('社会影响强度演化', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save:
            plt.savefig(f"{self.output_dir}/ising_dynamics.png", dpi=150, bbox_inches='tight')
        plt.close()
    
    def plot_performance_metrics(self, metrics_history: List, save: bool = True):
        """绘制性能指标"""
        steps = [m.step for m in metrics_history]
        
        satisfactions = [m.avg_satisfaction for m in metrics_history]
        decision_times = [m.avg_decision_time for m in metrics_history]
        ai_usage = [m.ai_usage_rate for m in metrics_history]
        error_rates = [m.error_rate for m in metrics_history]
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 满意度
        ax = axes[0, 0]
        ax.plot(steps, satisfactions, 'b-', linewidth=2)
        ax.set_ylabel('平均满意度', fontsize=11)
        ax.set_title('消费者满意度演化', fontsize=12, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        
        # 决策时间
        ax = axes[0, 1]
        ax.plot(steps, decision_times, 'g-', linewidth=2)
        ax.set_ylabel('平均决策时间', fontsize=11)
        ax.set_title('决策效率演化', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # AI使用率
        ax = axes[1, 0]
        ax.plot(steps, ai_usage, 'r-', linewidth=2)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('AI使用率', fontsize=11)
        ax.set_title('AI代理采用率演化', fontsize=12, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        
        # 错误率
        ax = axes[1, 1]
        ax.plot(steps, error_rates, 'orange', linewidth=2)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('错误率', fontsize=11)
        ax.set_title('消费决策错误率演化', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save:
            plt.savefig(f"{self.output_dir}/performance_metrics.png", dpi=150, bbox_inches='tight')
        plt.close()
    
    def plot_final_distribution(self, metrics_history: List, save: bool = True):
        """绘制最终分布"""
        if not metrics_history:
            return
        
        final = metrics_history[-1]
        distribution = final.level_distribution
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # 柱状图
        levels = list(range(1, 6))
        counts = [distribution.get(l, 0) for l in levels]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        labels = ['L1\n自主型', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理']
        
        bars = ax1.bar(labels, counts, color=colors, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('智能体数量', fontsize=12)
        ax1.set_title('最终依赖等级分布', fontsize=13, fontweight='bold')
        ax1.grid(True, axis='y', alpha=0.3)
        
        # 添加数值标签
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{count}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # 饼图
        total = sum(counts)
        if total > 0:
            percentages = [c/total*100 for c in counts]
            explode = (0.02, 0.02, 0.05, 0.02, 0.02)
            
            ax2.pie(percentages, labels=labels, colors=colors, autopct='%1.1f%%',
                   explode=explode, shadow=True, startangle=90)
            ax2.set_title('依赖等级占比', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        if save:
            plt.savefig(f"{self.output_dir}/final_distribution.png", dpi=150, bbox_inches='tight')
        plt.close()
    
    def plot_phase_diagram(self, sim, save: bool = True):
        """绘制相图（耦合强度vs磁化强度）"""
        # 需要运行参数扫描
        J_values = np.linspace(0.1, 1.5, 30)
        
        magnetizations = []
        for J in J_values:
            sim.network.J = J
            # 热化
            for _ in range(50):
                sim.network.monte_carlo_step()
            # 测量
            mags = []
            for _ in range(20):
                sim.network.monte_carlo_step()
                mags.append(abs(sim.network.get_magnetization()))
            magnetizations.append(np.mean(mags))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(J_values, magnetizations, 'bo-', linewidth=2, markersize=6)
        ax.set_xlabel('耦合强度 J', fontsize=12)
        ax.set_ylabel('|磁化强度| |M|', fontsize=12)
        ax.set_title('相变图：社会影响强度 vs 系统有序度', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 标记临界点
        Jc = sim.network.get_critical_J()
        ax.axvline(x=Jc, color='r', linestyle='--', label=f'理论临界值 Jc={Jc:.3f}')
        ax.legend(fontsize=10)
        
        if save:
            plt.savefig(f"{self.output_dir}/phase_diagram.png", dpi=150, bbox_inches='tight')
        plt.close()
        
        # 恢复原始值
        sim.network.J = self._get_original_J(sim)
    
    def _get_original_J(self, sim):
        """获取原始耦合强度"""
        if sim.metrics_history:
            return sim.metrics_history[-1].coupling_strength
        return 0.5
    
    def generate_all_plots(self, sim):
        """生成所有图表"""
        print("\n生成可视化图表...")
        
        self.plot_level_distribution_evolution(sim.metrics_history)
        self.plot_magnetization(sim.metrics_history)
        self.plot_performance_metrics(sim.metrics_history)
        self.plot_final_distribution(sim.metrics_history)
        
        print(f"图表已保存到: {self.output_dir}/")
        print("  - level_distribution_evolution.png")
        print("  - ising_dynamics.png")
        print("  - performance_metrics.png")
        print("  - final_distribution.png")


def quick_visualize(sim, output_dir: str = "results"):
    """快速可视化入口"""
    viz = SimulationVisualizer(output_dir)
    viz.generate_all_plots(sim)
    return viz


if __name__ == "__main__":
    # 测试可视化
    print("可视化模块已加载")
