"""
实验5可视化: 网络结构对比
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Dict


def visualize_network_comparison(results: Dict, output_dir: str):
    """可视化网络结构对比结果"""
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(18, 12))
    
    # 1. 网络拓扑可视化示例
    for i, (topo_name, (sim, summary)) in enumerate(list(results.items())[:4]):
        ax = plt.subplot(3, 4, i+1)
        _plot_network_structure(ax, sim, topo_name)
    
    # 2. 依赖等级分布对比
    ax5 = plt.subplot(3, 4, 5)
    _plot_level_distribution_comparison(ax5, results)
    
    # 3. 网络指标雷达图
    ax6 = plt.subplot(3, 4, 6, projection='polar')
    _plot_network_metrics_radar(ax6, results)
    
    # 4. 满意度vs网络指标
    ax7 = plt.subplot(3, 4, 7)
    _plot_satisfaction_vs_metrics(ax7, results)
    
    # 5. 收敛速度对比
    ax8 = plt.subplot(3, 4, 8)
    _plot_convergence_comparison(ax8, results)
    
    # 6. 相变临界点分析
    ax9 = plt.subplot(3, 4, 9)
    _plot_phase_transition(ax9, results)
    
    # 7. 磁化强度演化
    ax10 = plt.subplot(3, 4, 10)
    _plot_magnetization_evolution(ax10, results)
    
    # 8. 网络指标热力图
    ax11 = plt.subplot(3, 4, 11)
    _plot_metrics_heatmap(ax11, results)
    
    # 9. 综合排名
    ax12 = plt.subplot(3, 4, 12)
    _plot_topology_ranking(ax12, results)
    
    plt.suptitle('实验5: 网络结构对比分析', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/network_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ 网络对比图已保存: {output_dir}/network_comparison.png")


def _plot_network_structure(ax, sim, topo_name):
    """绘制网络结构示例"""
    import networkx as nx
    
    G = sim.network.graph
    
    # 选择前100个节点进行可视化
    if G.number_of_nodes() > 100:
        nodes = list(G.nodes())[:100]
        G = G.subgraph(nodes)
    
    # 布局
    if topo_name in ['scale_free', 'star']:
        pos = nx.spring_layout(G, k=0.5, iterations=50)
    else:
        pos = nx.spring_layout(G, k=0.3)
    
    # 根据度设置节点大小
    degrees = dict(G.degree())
    node_sizes = [degrees.get(n, 1) * 20 + 20 for n in G.nodes()]
    
    # 绘制
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=node_sizes, 
                          node_color='steelblue', alpha=0.7)
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.3, width=0.5)
    
    ax.set_title(f'{topo_name}\n(n={G.number_of_nodes()}, e={G.number_of_edges()})')
    ax.axis('off')


def _plot_level_distribution_comparison(ax, results):
    """绘制依赖等级分布对比"""
    topologies = list(results.keys())
    levels = range(1, 6)
    
    x = np.arange(len(topologies))
    width = 0.15
    
    for level in levels:
        percentages = []
        for topo_name, (sim, summary) in results.items():
            pct = summary['final_level_distribution'].get(level, 0) / 500 * 100
            percentages.append(pct)
        
        ax.bar(x + (level-3) * width, percentages, width, label=f'L{level}')
    
    ax.set_xlabel('网络拓扑')
    ax.set_ylabel('百分比 (%)')
    ax.set_title('依赖等级分布对比')
    ax.set_xticks(x)
    ax.set_xticklabels([t[:8] for t in topologies], rotation=45, ha='right')
    ax.legend()


def _plot_network_metrics_radar(ax, results):
    """绘制网络指标雷达图"""
    metrics = ['clustering', 'path_length', 'modularity', 'avg_degree']
    metric_labels = ['聚类系数', '路径长度', '模块度', '平均度']
    
    # 归一化指标值
    angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(results)))
    
    for i, (topo_name, (sim, summary)) in enumerate(results.items()):
        values = []
        for metric in metrics:
            val = summary.get(metric, 0)
            # 归一化到0-1
            if metric == 'path_length':
                val = 1 / (1 + val)  # 路径长度越短越好
            elif metric == 'avg_degree':
                val = min(1, val / 10)
            values.append(val)
        
        values += values[:1]
        ax.plot(angles, values, 'o-', linewidth=2, label=topo_name[:8], color=colors[i])
        ax.fill(angles, values, alpha=0.1, color=colors[i])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metric_labels)
    ax.set_ylim(0, 1)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.set_title('网络指标雷达图')


def _plot_satisfaction_vs_metrics(ax, results):
    """绘制满意度vs网络指标"""
    clusterings = []
    satisfactions = []
    labels = []
    
    for topo_name, (sim, summary) in results.items():
        clusterings.append(summary.get('clustering', 0))
        satisfactions.append(summary.get('satisfaction', {}).get('mean', 0))
        labels.append(topo_name[:6])
    
    ax.scatter(clusterings, satisfactions, s=100, alpha=0.6)
    
    for i, label in enumerate(labels):
        ax.annotate(label, (clusterings[i], satisfactions[i]), 
                   xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    ax.set_xlabel('聚类系数')
    ax.set_ylabel('平均满意度')
    ax.set_title('满意度 vs 聚类系数')
    ax.grid(True, alpha=0.3)


def _plot_convergence_comparison(ax, results):
    """绘制收敛速度对比"""
    for topo_name, (sim, summary) in results.items():
        if sim.metrics_history:
            steps = [m.step for m in sim.metrics_history]
            # 使用磁化强度的变化作为收敛指标
            mags = []
            for m in sim.metrics_history:
                dist = m.level_distribution
                mag = (dist.get(5, 0) + dist.get(4, 0) - dist.get(1, 0) - dist.get(2, 0)) / 500
                mags.append(mag)
            
            ax.plot(steps, mags, label=topo_name[:8], linewidth=2)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('高依赖偏向度')
    ax.set_title('收敛速度对比')
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_phase_transition(ax, results):
    """绘制相变分析"""
    topologies = list(results.keys())
    final_l5 = []
    
    for topo_name, (sim, summary) in results.items():
        l5_pct = summary['final_level_distribution'].get(5, 0) / 500
        final_l5.append(l5_pct)
    
    colors = ['green' if x > 0.3 else 'orange' if x > 0.15 else 'red' for x in final_l5]
    ax.bar(range(len(topologies)), final_l5, color=colors, alpha=0.6)
    ax.set_xticks(range(len(topologies)))
    ax.set_xticklabels([t[:8] for t in topologies], rotation=45, ha='right')
    ax.set_ylabel('L5比例')
    ax.set_title('高依赖相变结果')
    ax.axhline(y=0.2, color='gray', linestyle='--', alpha=0.5, label='临界点')


def _plot_magnetization_evolution(ax, results):
    """绘制磁化强度演化"""
    for topo_name, (sim, summary) in results.items():
        if sim.metrics_history:
            steps = [m.step for m in sim.metrics_history]
            mags = []
            for m in sim.metrics_history:
                dist = m.level_distribution
                # 计算磁化强度（L5=2, L4=1, L3=0, L2=-1, L1=-2）
                mag = (2*dist.get(5, 0) + 1*dist.get(4, 0) - 1*dist.get(2, 0) - 2*dist.get(1, 0)) / 500
                mags.append(mag)
            
            ax.plot(steps, mags, label=topo_name[:8], linewidth=2)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('磁化强度')
    ax.set_title('磁化强度演化')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)


def _plot_metrics_heatmap(ax, results):
    """绘制指标热力图"""
    metrics = ['clustering', 'path_length', 'modularity', 'avg_degree']
    metric_labels = ['聚类', '路径长', '模块度', '平均度']
    
    data = []
    topo_labels = []
    
    for topo_name, (sim, summary) in results.items():
        row = []
        for metric in metrics:
            val = summary.get(metric, 0)
            # 归一化
            if metric == 'path_length':
                val = 1 / (1 + val)
            elif metric == 'avg_degree':
                val = min(1, val / 10)
            row.append(val)
        data.append(row)
        topo_labels.append(topo_name[:8])
    
    data = np.array(data)
    
    im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    ax.set_xticks(range(len(metric_labels)))
    ax.set_xticklabels(metric_labels)
    ax.set_yticks(range(len(topo_labels)))
    ax.set_yticklabels(topo_labels)
    ax.set_title('网络指标热力图')
    
    # 添加数值标注
    for i in range(len(topo_labels)):
        for j in range(len(metric_labels)):
            text = ax.text(j, i, f'{data[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=8)
    
    plt.colorbar(im, ax=ax)


def _plot_topology_ranking(ax, results):
    """绘制拓扑综合排名"""
    # 计算综合得分
    scores = []
    labels = []
    
    for topo_name, (sim, summary) in results.items():
        # 综合得分 = 满意度 * 0.4 + (1-错误率) * 0.3 + 收敛速度 * 0.3
        sat = summary.get('satisfaction', {}).get('mean', 0)
        err = summary.get('error_rate', 0)
        
        score = sat * 0.5 + (1 - err) * 0.5
        scores.append(score)
        labels.append(topo_name)
    
    # 排序
    sorted_indices = np.argsort(scores)[::-1]
    sorted_scores = [scores[i] for i in sorted_indices]
    sorted_labels = [labels[i][:10] for i in sorted_indices]
    
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(scores)))
    ax.barh(range(len(scores)), sorted_scores, color=colors)
    ax.set_yticks(range(len(scores)))
    ax.set_yticklabels(sorted_labels)
    ax.set_xlabel('综合得分')
    ax.set_title('拓扑综合排名')
    ax.invert_yaxis()


from typing import Dict
