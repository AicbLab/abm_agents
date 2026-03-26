"""
统一可视化生成器
将所有实验的可视化图表集中到一个文件夹，并修复中文显示
"""

import sys
import os
import shutil
from pathlib import Path

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入中文字体配置
from visualization.chinese_font import setup_chinese_font
setup_chinese_font()

def collect_all_figures():
    """收集所有实验的图表到统一文件夹"""
    
    # 创建统一的输出目录
    output_dir = Path("results/all_figures")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    experiments_dir = Path("experiments")
    
    collected_count = 0
    
    # 遍历所有实验文件夹
    for exp_folder in experiments_dir.iterdir():
        if not exp_folder.is_dir():
            continue
        
        # 查找 results 子文件夹
        results_folder = exp_folder / "results"
        if not results_folder.exists():
            continue
        
        # 复制所有 PNG 文件
        for png_file in results_folder.glob("**/*.png"):
            # 构建新的文件名（包含实验名称）
            new_name = f"{exp_folder.name}_{png_file.name}"
            dest_path = output_dir / new_name
            
            # 复制文件
            shutil.copy2(png_file, dest_path)
            print(f"已复制：{png_file.name} -> {new_name}")
            collected_count += 1
    
    print(f"\n完成！共收集 {collected_count} 张图表到：{output_dir}")
    return output_dir


if __name__ == "__main__":
    collect_all_figures()
