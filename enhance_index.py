#!/usr/bin/env python3
"""
Phase C Task 3: Enhance existing _index.md with learning path sections.

All layers already have _index.md. This script adds a "## 学习路径建议"
section to each, with recommended node reading order and prerequisite awareness.
"""

import os

BASE = "/mnt/d/00_Hermes/AI_Knowledge_Graph"

LEARNING_PATHS = {
    "Layer-0-数学基础": """
## 学习路径建议

1. **基础先修**：凸优化 → 梯度下降（理解优化基础）
2. **信息论基础**：熵与KL散度 → 交叉熵（为分类损失函数打基础）
3. **概率方法**：贝叶斯推断 → MCMC（理解后验采样）
4. **进阶**：SVD → KV Cache（理解低秩分解在Transformer中的应用）
""",
    "Layer-1-数据工程": """
## 学习路径建议

1. **数据管道**：ETL → 数据清洗/特征工程
2. **数据降维**：PCA → t-SNE（可与Layer-2A配合学习）
3. **数据高效利用**：主动学习 → 联邦学习
""",
    "Layer-2A-经典ML": """
## 学习路径建议

1. **监督学习入门**：逻辑回归 → 决策树 → 随机森林 → XGBoost
2. **核方法**：SVM → 高斯过程（理解核技巧）
3. **无监督学习**：KMeans → t-SNE（聚类→可视化）
4. **模型优化**：贝叶斯优化 → 高斯过程（超参数调优利器）
5. **前置依赖**：建议先完成Layer-0的凸优化和梯度下降
""",
    "Layer-2B-深度学习": """
## 学习路径建议

### 2B-1（非Transformer）
1. **基础组件**：激活函数 → MLP → 梯度反向传播
2. **训练技巧**：BatchNorm → Dropout → Adam
3. **CNN系列**：CNN → ResNet（理解残差连接在深层网络中的作用）
4. **序列模型**：RNN → LSTM
5. **生成模型**：GAN（理解对抗训练范式）

### 2B-2（Transformer/Scaling）
1. **核心架构**：Self-Attention → 位置编码 → Transformer
2. **预训练模型**：BERT → GPT（理解两种预训练范式）
3. **对齐技术**：RLHF → DPO（理解偏好优化演进）
4. **推理增强**：CoT → RAG（扩展模型能力边界）
5. **效率优化**：KV Cache → MoE（理解推理加速与稀疏激活）
""",
    "Layer-2C-强化学习": """
## 学习路径建议

1. **基础理论**：MDP → Bellman方程（理解RL的数学框架）
2. **经典算法**：Q-Learning → DQN（从表格到深度RL）
3. **策略优化**：PPO → SAC（on-policy vs off-policy）
4. **多智能体**：PPO → MAPPO（从单智能体扩展到多智能体）
5. **前置依赖**：建议了解Layer-2B-1中的MLP和CNN
""",
    "Layer-3-化工与过程控制": """
## 学习路径建议

### 3A→3B：从经典到先进控制
PID控制 → 串级控制 → 内模控制IMC → MPC → 鲁棒MPC/经济MPC

### 3C：建模与辨识（为APC提供模型）
系统辨识 → 机理建模 → 混合建模 → 软测量

### 3D：优化层
实时优化RTO → 动态优化 → 调度优化 → 数据驱动RTO

### 3E：安全层
HAZOP分析 → SIL → 报警管理 → 数据驱动FDD→PCA故障检测

### AI融合学习路径
1. **数据驱动建模**：系统辨识 → 混合建模（结合MLP/LSTM）
2. **智能控制**：PID → 自适应控制 → RL调参（结合Layer-2C）
3. **智能运维**：软测量 → 数据驱动FDD（结合Layer-2B-1 CNN/LSTM）
""",
    "Layer-4-Agent生态": """
## 学习路径建议

1. **基础能力**：Function Calling → MCP协议（理解工具使用标准）
2. **框架入门**：LangChain → LangGraph（从线性链到图编排）
3. **多Agent协作**：LangGraph → CrewAI
4. **评估基准**：SWE-bench（理解Agent能力度量）
5. **前置依赖**：建议先完成Layer-2B-2的Transformer、CoT和RAG
""",
    "Layer-5-MLOps": """
## 学习路径建议

1. **实验管理**：MLflow → Optuna（实验追踪+超参优化）
2. **模型注册与分发**：MLflow → HuggingFace Hub
3. **工作流编排**：Kubeflow（生产级ML管道）
4. **前置依赖**：理解基本的ML训练流程（Layer-2A/2B）
""",
    "横切A-数据驱动方法论": """
## 学习路径建议

1. **因果推断**：DAG因果图（理解因果关系 vs 相关关系的基础框架）
2. **时间序列**：Kalman滤波（状态估计的经典方法）
3. **交叉应用**：本层方法可应用于任意其他层的实验设计和不确定性量化
""",
    "横切B-AI系统属性": """
## 学习路径建议

1. **可解释性入门**：SHAP（模型解释的标准工具）
2. **AI安全**：建议在理解LLM基础（Layer-2B-2）后学习
3. **隐私计算**：联邦学习（与Layer-1联邦学习节点联动）
4. **交叉应用**：本层属性应贯穿所有层的模型开发全生命周期
""",
}


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    count = 0
    for layer, learning_path in LEARNING_PATHS.items():
        path = os.path.join(BASE, layer, "_index.md")
        content = read_file(path)
        if content is None:
            print(f"NOT FOUND: {path}")
            continue

        # Check if learning path already exists
        if "学习路径" in content:
            print(f"SKIP (exists): {path}")
            continue

        # Add learning path before the last line
        # Find the end of the content (before any trailing newlines)
        content = content.rstrip()
        content += learning_path.rstrip() + "\n"
        write_file(path, content)
        print(f"ENHANCED: {path}")
        count += 1

    print(f"\nDone. Enhanced {count} _index.md files.")


if __name__ == "__main__":
    main()
