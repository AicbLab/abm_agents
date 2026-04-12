"""
统一输出路径配置
所有实验结果集中存储到 abm_simulation/results/ 下各自子目录
"""
import os

# 项目根目录（即本文件所在的 abm_simulation/ 目录）
_HERE = os.path.dirname(os.path.abspath(__file__))

# 所有实验结果的统一输出根目录
RESULTS_ROOT = os.path.join(_HERE, "results")

# 各实验的输出目录（由 run_*.py 引用，不要在 visualization_*.py 里硬编码路径）
RESULTS = {
    "baseline":      os.path.join(RESULTS_ROOT, "baseline_exp1"),
    "exp2":          os.path.join(RESULTS_ROOT, "exp2_consumer_memory"),
    "exp3":          os.path.join(RESULTS_ROOT, "exp3_ai_evolution"),
    "exp4":          os.path.join(RESULTS_ROOT, "exp4_information_intervention"),
    "exp5":          os.path.join(RESULTS_ROOT, "exp5_network_structure"),
    "exp6":          os.path.join(RESULTS_ROOT, "exp6_generational_dynamics"),
    "exp7":          os.path.join(RESULTS_ROOT, "exp7_ai_competition"),
    "exp8":          os.path.join(RESULTS_ROOT, "exp8_context_sensitivity"),
    "exp9":          os.path.join(RESULTS_ROOT, "exp9_filter_bubble"),
    "exp10":         os.path.join(RESULTS_ROOT, "exp10_systemic_risk"),
}
