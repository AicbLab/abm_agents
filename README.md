# ABM 消费决策代理模拟系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)](LICENSE)

##  快速开始

### 运行仿真平台

**克隆仓库并启动:**

`ash
# 1. 克隆仓库
git clone https://github.com/YinMengjiao/abm_agents.git
cd abm_agents/abm_simulation

# 2. 创建虚拟环境 (推荐)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 安装依赖
pip install numpy matplotlib networkx pandas

# 4. 运行基线实验
python experiments/baseline_exp1/run_baseline.py

# 5. 启动 Web 交互界面 (可选)
python frontend/start_server.py
# 然后在浏览器打开 http://localhost:8000
`

### 运行其他实验

`ash
# 消费者记忆实验
python experiments/exp2_consumer_memory/run_comparison.py

# AI 进化实验
python experiments/exp3_ai_evolution/run_evolution.py

# 信息干预实验
python experiments/exp4_information_intervention/run_intervention.py

# 网络结构实验
python experiments/exp5_network_structure/run_network.py

# 代际动态实验
python experiments/exp6_generational_dynamics/run_generational.py

# AI 竞争实验
python experiments/exp7_ai_competition/run_competition.py

# 情境敏感性实验
python experiments/exp8_context_sensitivity/run_context.py

# 信息茧房实验
python experiments/exp9_filter_bubble/run_filter_bubble.py

# 系统性风险实验
python experiments/exp10_systemic_risk/run_systemic_risk.py
`

---

##  项目简介

本项目是一个基于 **Agent-Based Modeling (ABM)** 的消费决策代理模拟系统，融合了 **Ising 模型**、**D-I-B 框架**和**多智能体系统**,用于研究消费者行为、AI 智能体与市场环境的复杂交互作用。

### 核心特色

-  **三层耦合建模**: Ising-D-I-B 框架整合社会影响、决策机制与行为演化
-  **AI 智能体**: 支持 AI 代理与人类消费者的混合仿真
-  **网络动力学**: 基于 Ising 模型的社交网络传播机制
-  **可视化分析**: 自动生成实验结果图表和分析报告
-  **交互界面**: Web 前端支持实时参数调整和结果查看

---

##  项目结构

`
abm_simulation/
 agents/                 # 智能体模块
    ai_agent.py        # AI 智能体实现
    consumer_dib.py    # D-I-B 框架消费者智能体
 environment/            # 环境模块
    market.py          # 市场环境模拟
 models/                 # 模型模块
    ising_network.py   # Ising 网络模型
 experiments/            # 实验模块 (10 个子实验)
    baseline_exp1/           # 基线实验
    exp2_consumer_memory/    # 消费者记忆机制
    exp3_ai_evolution/       # AI 进化机制
    exp4_information_intervention/  # 信息干预
    exp5_network_structure/     # 网络结构影响
    exp6_generational_dynamics/ # 代际动态
    exp7_ai_competition/        # AI 竞争
    exp8_context_sensitivity/   # 情境敏感性
    exp9_filter_bubble/         # 信息茧房
    exp10_systemic_risk/        # 系统性风险
 visualization/          # 可视化模块
 frontend/               # Web 交互界面
 latex_report/           # LaTeX 学术论文
 results/                # 实验结果输出
`

---

##  实验模块说明

### 1. 基线实验 (aseline_exp1)
验证 Ising-D-I-B 模型的基础动力学行为，展示消费者态度演化和等级分布。

### 2. 消费者记忆机制 (exp2_consumer_memory)
研究记忆效应对消费者决策的影响，比较有记忆 vs 无记忆场景。

### 3. AI 进化机制 (exp3_ai_evolution)
模拟 AI 智能体的策略学习和进化过程。

### 4. 信息干预 (exp4_information_intervention)
分析不同信息干预策略 (保护消费者、推广 AI、平衡策略) 的效果。

### 5. 网络结构影响 (exp5_network_structure)
探索不同社交网络拓扑结构对传播动力学的影响。

### 6. 代际动态 (exp6_generational_dynamics)
研究多代消费者共存时的文化传递和价值观演化。

### 7. AI 竞争 (exp7_ai_competition)
模拟多个 AI 代理在市场中的竞争博弈。

### 8. 情境敏感性 (exp8_context_sensitivity)
分析不同情境因素对决策的调节作用。

### 9. 信息茧房 (exp9_filter_bubble)
研究算法推荐导致的信息窄化现象。

### 10. 系统性风险 (exp10_systemic_risk)
评估市场系统的稳定性和风险传播机制。

---

##  核心功能

###  智能体建模
- **AI 智能体**: 基于强化学习的策略优化
- **消费者智能体**: D-I-B框架 ( Desire-Intention-Behavior )
- **异质性**: 支持多种消费者类型和行为模式

###  社会网络
- **Ising 模型**: 物理启发的态度传播模型
- **网络拓扑**: 支持规则网络、随机网络、小世界网络等
- **群体动力学**: 涌现现象和相变分析

###  市场环境
- **信息传播**: 多渠道信息扩散机制
- **竞争格局**: 多品牌/产品竞争模拟
- **外部干预**: 政策、广告等外生冲击

###  数据分析
- **实时可视化**: 动力学过程动态展示
- **统计分析**: 自动计算关键指标
- **结果导出**: 支持 CSV、PNG、PDF 等格式

---

##  技术栈

- **核心框架**: Python 3.8+
- **科学计算**: NumPy, Pandas
- **网络建模**: NetworkX
- **可视化**: Matplotlib, Seaborn
- **前端界面**: HTML/CSS/JavaScript
- **论文排版**: LaTeX

---

##  典型输出

每个实验会自动生成以下结果:

1. **动力学图**: 展示系统随时间演化的关键变量
2. **分布图**: 消费者状态/等级的统计分布
3. **热力图**: 参数空间的系统性扫描
4. **对比图**: 不同实验条件的效果比较
5. **综合分析报告**: 多指标雷达图/柱状图

---

##  文档

- **各实验详细说明**: 参见 experiments/ 下各子目录的 README.txt
- **仿真平台文档**: 参见 [bm_simulation/README.md](abm_simulation/README.md)
- **学术论文**: 参见 latex_report/main.pdf (如有)

---

##  配置说明

### 环境变量 (可选)

`ash
# 设置随机种子 (复现性)
export RANDOM_SEED=42

# 设置并行计算核心数
export NUMBA_NUM_THREADS=4
`

### 参数调整

每个实验脚本都支持命令行参数:

`ash
# 示例：自定义仿真步数和智能体数量
python experiments/baseline_exp1/run_baseline.py --steps 100 --agents 500
`

---

##  贡献指南

欢迎通过以下方式贡献:

1. Fork 本仓库
2. 创建特性分支 (git checkout -b feature/AmazingFeature)
3. 提交更改 (git commit -m 'Add some AmazingFeature')
4. 推送到分支 (git push origin feature/AmazingFeature)
5. 开启 Pull Request

---

##  许可证

本项目仅供**学术研究**使用。

---

##  致谢

感谢所有为本项目做出贡献的研究人员和合作者。

---

##  联系方式

- **问题反馈**: 请通过 GitHub Issues 提交
- **合作洽谈**: 请通过邮件联系

---

##  相关资源

- [Ising 模型维基百科](https://en.wikipedia.org/wiki/Ising_model)
- [Agent-Based Modeling 综述](https://www.nature.com/articles/nphys2007)
- [D-I-B 框架论文](TODO: 添加引用)

---

<div align="center">

**如果这个项目对你有帮助，请考虑给一个  Star!**

</div>
