"""
项目技术路线图生成脚本
用于项目申报书的技术路线图绘制
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os
import platform

def setup_chinese_font():
    """设置中文字体"""
    system = platform.system()
    
    if system == 'Windows':
        font_list = ['SimHei', 'Microsoft YaHei', 'Microsoft JhengHei', 'Arial Unicode MS']
    elif system == 'Darwin':
        font_list = ['Arial Unicode MS', 'PingFang TC', 'Heiti TC', 'SimHei']
    else:
        font_list = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
    
    plt.rcParams['font.sans-serif'] = font_list
    plt.rcParams['axes.unicode_minus'] = False
    print(f"已设置中文字体：{font_list}")

def draw_rounded_box(ax, x, y, width, height, facecolor, edgecolor, linewidth=2, radius=0.02):
    """绘制圆角矩形"""
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                         boxstyle=f"round,pad=0,rounding_size={radius}",
                         facecolor=facecolor, edgecolor=edgecolor,
                         linewidth=linewidth, zorder=2)
    ax.add_patch(box)
    return box

def draw_arrow(ax, x1, y1, x2, y2, color='#666666', lw=2):
    """绘制箭头连接"""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                              connectionstyle='arc3,rad=0'),
                zorder=1)

def create_roadmap():
    """创建技术路线图"""
    # 设置中文字体
    setup_chinese_font()
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 22), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(-3.5, 20)
    ax.axis('off')
    
    # 配色方案（学术风格）
    colors = {
        'phase1': '#E3F2FD',  # 浅蓝
        'phase2': '#E8F5E9',  # 浅绿
        'phase3': '#FFF3E0',  # 浅橙
        'phase4': '#F3E5F5',  # 浅紫
        'phase5': '#E0F7FA',  # 浅青
        'border1': '#1976D2',
        'border2': '#388E3C',
        'border3': '#F57C00',
        'border4': '#7B1FA2',
        'border5': '#00838F',
        'title_bg': '#1565C0',
        'text': '#333333',
        'subtext': '#555555'
    }
    
    # 标题
    ax.text(6, 19.3, 'ABM消费决策仿真研究技术路线图', 
            fontsize=20, fontweight='bold', ha='center', va='center', color='#1565C0')
    ax.text(6, 18.8, '基于Ising-DIB混合模型的AI依赖行为研究', 
            fontsize=12, ha='center', va='center', color='#666666')
    
    # ========== 第一阶段：理论框架构建 ==========
    y_phase1 = 16.5
    # 阶段标题框
    draw_rounded_box(ax, 6, y_phase1, 10, 1.2, colors['phase1'], colors['border1'], radius=0.05)
    ax.text(6, y_phase1, '第一阶段：理论框架构建', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['border1'])
    ax.text(10.5, y_phase1, '[计划]', fontsize=10, ha='center', va='center', 
            color=colors['border1'], style='italic')
    
    # 内容框
    y_content1 = 14.8
    content1_items = [
        '文献综述与理论整合',
        '  - Ising模型（统计物理方法）',
        '  - D-I-B决策框架（消费者行为）',
        '  - 人机信任理论（AI依赖研究）',
        '',
        '提出L1-L5消费者依赖等级分类',
        '  L1自主型(10%) / L2参考型(25%) / L3半委托型(30%)',
        '  L4依赖型(25%) / L5完全委托型(10%)',
        '',
        '构建Ising-DIB混合理论模型'
    ]
    draw_rounded_box(ax, 6, y_content1, 9.5, 2.8, '#FAFAFA', colors['border1'], linewidth=1.5, radius=0.03)
    content_text = '\n'.join(content1_items)
    ax.text(6, y_content1, content_text, fontsize=9.5, ha='center', va='center', 
            color=colors['text'], linespacing=1.4)
    
    # 箭头1
    draw_arrow(ax, 6, 13.5, 6, 12.8, color='#666666', lw=2)
    
    # ========== 第二阶段：预实验与模型验证 ==========
    y_phase2 = 12.2
    draw_rounded_box(ax, 6, y_phase2, 10, 1.2, colors['phase2'], colors['border2'], radius=0.05)
    ax.text(6, y_phase2, '第二阶段：预实验与模型验证', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['border2'])
    ax.text(10.5, y_phase2, '[已完成]', fontsize=10, ha='center', va='center', 
            color=colors['border2'], fontweight='bold')
    
    y_content2 = 10.3
    content2_items = [
        '基于经验假设的初始比例设定',
        '  L1:10% / L2:25% / L3:30% / L4:25% / L5:10%',
        '',
        'ABM仿真系统开发',
        '  - 消费者代理（7维人格特质建模）',
        '  - AI代理（3能力等级 × 6种错误类型）',
        '  - 市场环境与社交网络构建',
        '',
        '基线实验运行与参数校准'
    ]
    draw_rounded_box(ax, 6, y_content2, 9.5, 2.6, '#FAFAFA', colors['border2'], linewidth=1.5, radius=0.03)
    content_text2 = '\n'.join(content2_items)
    ax.text(6, y_content2, content_text2, fontsize=9.5, ha='center', va='center', 
            color=colors['text'], linespacing=1.4)
    
    # 箭头2
    draw_arrow(ax, 6, 9.1, 6, 8.4, color='#666666', lw=2)
    
    # ========== 第三阶段：量表开发与问卷调查 ==========
    y_phase3 = 7.8
    draw_rounded_box(ax, 6, y_phase3, 10, 1.2, colors['phase3'], colors['border3'], radius=0.05)
    ax.text(6, y_phase3, '第三阶段：量表开发与问卷调查', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['border3'])
    ax.text(10.5, y_phase3, '[进行中]', fontsize=10, ha='center', va='center', 
            color=colors['border3'], fontweight='bold')
    
    y_content3 = 5.7
    content3_items = [
        '基于经典量表改编',
        '  Huang et al. 2020 | Parasuraman & Manzey 2010',
        '  Lee & See 2004 | Davis 1989',
        '',
        '10题项量表开发（7点Likert量表）',
        '  - 算法决策接受度维度',
        '  - 自动化信任与过度依赖维度',
        '  - 感知风险 vs 感知收益维度',
        '',
        '预测试（n=30-50）→ 信效度检验（Cronbach\'s α > 0.7）',
        '正式问卷调查（n≥300）→ 数据分析 → 确定L1-L5真实比例'
    ]
    draw_rounded_box(ax, 6, y_content3, 9.5, 3.2, '#FAFAFA', colors['border3'], linewidth=1.5, radius=0.03)
    content_text3 = '\n'.join(content3_items)
    ax.text(6, y_content3, content_text3, fontsize=9.5, ha='center', va='center', 
            color=colors['text'], linespacing=1.4)
    
    # 箭头3
    draw_arrow(ax, 6, 4.3, 6, 3.6, color='#666666', lw=2)
    
    # ========== 第四阶段：正式实验 ==========
    y_phase4 = 3.0
    draw_rounded_box(ax, 6, y_phase4, 10, 1.2, colors['phase4'], colors['border4'], radius=0.05)
    ax.text(6, y_phase4, '第四阶段：正式实验', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['border4'])
    ax.text(10.5, y_phase4, '[计划]', fontsize=10, ha='center', va='center', 
            color=colors['border4'], style='italic')
    
    y_content4 = 1.6
    content4_items = [
        '用真实比例替换经验假设，重新校准模型',
        '',
        '10组实验设计：',
        '  - 基线模型 / 消费者记忆 / AI进化 / 信息干预 / 网络结构',
        '  - 代际动态 / AI竞争 / 情境敏感性 / 过滤气泡 / 系统性风险'
    ]
    draw_rounded_box(ax, 6, y_content4, 9.5, 1.8, '#FAFAFA', colors['border4'], linewidth=1.5, radius=0.03)
    content_text4 = '\n'.join(content4_items)
    ax.text(6, y_content4, content_text4, fontsize=9.5, ha='center', va='center', 
            color=colors['text'], linespacing=1.4)
    
    # ========== 第五阶段：政策建议与成果输出 ==========
    # 箭头4
    draw_arrow(ax, 6, 0.7, 6, 0.0, color='#666666', lw=2)
    
    y_phase5 = -0.6
    draw_rounded_box(ax, 6, y_phase5, 10, 1.0, colors['phase5'], colors['border5'], radius=0.05)
    ax.text(6, y_phase5, '第五阶段：政策建议与成果输出', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['border5'])
    ax.text(10.5, y_phase5, '[计划]', fontsize=10, ha='center', va='center', 
            color=colors['border5'], style='italic')
    
    y_content5 = -1.8
    content5_items = [
        '实验结果分析与理论贡献',
        '消费者保护政策建议',
        '学术论文撰写与发表'
    ]
    draw_rounded_box(ax, 6, y_content5, 9.5, 1.4, '#FAFAFA', colors['border5'], linewidth=1.5, radius=0.03)
    content_text5 = '\n'.join(content5_items)
    ax.text(6, y_content5, content_text5, fontsize=9.5, ha='center', va='center', 
            color=colors['text'], linespacing=1.5)
    
    # 添加图例说明
    legend_y = -2.9
    ax.text(6, legend_y, '图例：[已完成]  [进行中]  [计划]', 
            fontsize=10, ha='center', va='center', color='#666666',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5F5F5', edgecolor='#CCCCCC'))
    
    # 保存图片
    output_dir = r'c:\Users\admin\WPSDrive\2197502\WPS云盘\【科研】\【论文】ABM消费决策代理\abm_simulation\results'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'technical_roadmap.png')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"技术路线图已保存至: {output_path}")
    
    plt.show()
    return fig, ax

if __name__ == '__main__':
    create_roadmap()
