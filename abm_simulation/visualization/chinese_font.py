"""
中文字体配置模块
为所有可视化提供统一的中文字体支持
"""

import matplotlib.pyplot as plt
import matplotlib

def setup_chinese_font():
    """
    设置中文字体
    在 Windows 上使用 SimHei，在 Mac 上使用 Arial Unicode MS
    """
    import platform
    
    system = platform.system()
    
    if system == 'Windows':
        # Windows 使用黑体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    elif system == 'Darwin':
        # Mac 使用 Arial Unicode MS
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
    else:
        # Linux 尝试使用文泉驿
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'Arial Unicode MS']
    
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False
    
    return True

# 自动应用中文字体
setup_chinese_font()
