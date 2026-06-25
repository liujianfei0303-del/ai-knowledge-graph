#!/usr/bin/env python3
"""
Phase C Task 2: Add wikilinks between knowledge graph nodes.

Analyzes content of each node and inserts [[Layer-X/Node]] wikilinks
where concepts from other nodes are mentioned. Each node gets 1-4 links.
"""

import os
import re
import json

BASE = "/mnt/d/00_Hermes/AI_Knowledge_Graph"

# Comprehensive keyword → (layer_prefix, filename) mapping
# Built from analyzing all 91 node filenames and their concepts
CONCEPT_MAP = {
    # === Layer-0-数学基础 ===
    "SVD": ("Layer-0-数学基础", "SVD.md"),
    "奇异值分解": ("Layer-0-数学基础", "SVD.md"),
    "奇异值": ("Layer-0-数学基础", "SVD.md"),
    "MCMC": ("Layer-0-数学基础", "MCMC.md"),
    "马尔可夫链蒙特卡洛": ("Layer-0-数学基础", "MCMC.md"),
    "交叉熵": ("Layer-0-数学基础", "交叉熵.md"),
    "凸优化": ("Layer-0-数学基础", "凸优化.md"),
    "梯度下降": ("Layer-0-数学基础", "梯度下降.md"),
    "随机梯度下降": ("Layer-0-数学基础", "梯度下降.md"),
    "SGD": ("Layer-0-数学基础", "梯度下降.md"),
    "KL散度": ("Layer-0-数学基础", "熵与KL散度.md"),
    "KL divergence": ("Layer-0-数学基础", "熵与KL散度.md"),
    "相对熵": ("Layer-0-数学基础", "熵与KL散度.md"),
    "信息熵": ("Layer-0-数学基础", "熵与KL散度.md"),
    "贝叶斯推断": ("Layer-0-数学基础", "贝叶斯推断.md"),
    "贝叶斯方法": ("Layer-0-数学基础", "贝叶斯推断.md"),
    "贝叶斯定理": ("Layer-0-数学基础", "贝叶斯推断.md"),
    "KV Cache": ("Layer-0-数学基础", "KV Cache.md"),
    "KV缓存": ("Layer-0-数学基础", "KV Cache.md"),

    # === Layer-1-数据工程 ===
    "ETL": ("Layer-1-数据工程", "ETL.md"),
    "ETL管道": ("Layer-1-数据工程", "ETL.md"),
    "PCA": ("Layer-1-数据工程", "PCA.md"),
    "主成分分析": ("Layer-1-数据工程", "PCA.md"),
    "主动学习": ("Layer-1-数据工程", "主动学习.md"),
    "联邦学习": ("Layer-1-数据工程", "联邦学习.md"),

    # === Layer-2A-经典ML ===
    "Boosting": ("Layer-2A-经典ML", "Boosting.md"),
    "提升方法": ("Layer-2A-经典ML", "Boosting.md"),
    "CNN": ("Layer-2A-经典ML", "CNN.md"),
    "卷积神经网络": ("Layer-2A-经典ML", "CNN.md"),
    "KMeans": ("Layer-2A-经典ML", "KMeans.md"),
    "K-Means": ("Layer-2A-经典ML", "KMeans.md"),
    "K-means": ("Layer-2A-经典ML", "KMeans.md"),
    "LogisticRegression": ("Layer-2A-经典ML", "LogisticRegression.md"),
    "逻辑回归": ("Layer-2A-经典ML", "LogisticRegression.md"),
    "SVM": ("Layer-2A-经典ML", "SVM.md"),
    "支持向量机": ("Layer-2A-经典ML", "SVM.md"),
    "XGBoost": ("Layer-2A-经典ML", "XGBoost.md"),
    "t-SNE": ("Layer-2A-经典ML", "t-SNE.md"),
    "决策树": ("Layer-2A-经典ML", "决策树.md"),
    "贝叶斯优化": ("Layer-2A-经典ML", "贝叶斯优化.md"),
    "随机森林": ("Layer-2A-经典ML", "随机森林.md"),
    "Random Forest": ("Layer-2A-经典ML", "随机森林.md"),
    "高斯过程": ("Layer-2A-经典ML", "高斯过程.md"),
    "GP": ("Layer-2A-经典ML", "高斯过程.md"),

    # === Layer-2B-深度学习/2B-1 ===
    "MLP": ("Layer-2B-深度学习/2B-1", "MLP.md"),
    "多层感知机": ("Layer-2B-深度学习/2B-1", "MLP.md"),
    "RNN": ("Layer-2B-深度学习/2B-1", "RNN.md"),
    "循环神经网络": ("Layer-2B-深度学习/2B-1", "RNN.md"),
    "LSTM": ("Layer-2B-深度学习/2B-1", "LSTM.md"),
    "长短期记忆": ("Layer-2B-深度学习/2B-1", "LSTM.md"),
    "ResNet": ("Layer-2B-深度学习/2B-1", "ResNet.md"),
    "残差网络": ("Layer-2B-深度学习/2B-1", "ResNet.md"),
    "残差连接": ("Layer-2B-深度学习/2B-1", "残差连接.md"),
    "BatchNorm": ("Layer-2B-深度学习/2B-1", "BatchNorm.md"),
    "批归一化": ("Layer-2B-深度学习/2B-1", "BatchNorm.md"),
    "Dropout": ("Layer-2B-深度学习/2B-1", "Dropout.md"),
    "GAN": ("Layer-2B-深度学习/2B-1", "GAN.md"),
    "生成对抗网络": ("Layer-2B-深度学习/2B-1", "GAN.md"),
    "Adam": ("Layer-2B-深度学习/2B-1", "Adam.md"),
    "Adam优化器": ("Layer-2B-深度学习/2B-1", "Adam.md"),
    "GELU": ("Layer-2B-深度学习/2B-1", "GELU.md"),
    "激活函数": ("Layer-2B-深度学习/2B-1", "激活函数.md"),
    "ReLU": ("Layer-2B-深度学习/2B-1", "激活函数.md"),

    # === Layer-2B-深度学习/2B-2 ===
    "Transformer": ("Layer-2B-深度学习/2B-2", "Transformer.md"),
    "Self-Attention": ("Layer-2B-深度学习/2B-2", "Self-Attention.md"),
    "自注意力": ("Layer-2B-深度学习/2B-2", "Self-Attention.md"),
    "BERT": ("Layer-2B-深度学习/2B-2", "BERT.md"),
    "GPT": ("Layer-2B-深度学习/2B-2", "GPT.md"),
    "RLHF": ("Layer-2B-深度学习/2B-2", "RLHF.md"),
    "人类反馈强化学习": ("Layer-2B-深度学习/2B-2", "RLHF.md"),
    "DPO": ("Layer-2B-深度学习/2B-2", "DPO.md"),
    "直接偏好优化": ("Layer-2B-深度学习/2B-2", "DPO.md"),
    "Chain-of-Thought": ("Layer-2B-深度学习/2B-2", "CoT.md"),
    "思维链": ("Layer-2B-深度学习/2B-2", "CoT.md"),
    "CoT": ("Layer-2B-深度学习/2B-2", "CoT.md"),
    "MoE": ("Layer-2B-深度学习/2B-2", "MoE.md"),
    "混合专家": ("Layer-2B-深度学习/2B-2", "MoE.md"),
    "RAG": ("Layer-2B-深度学习/2B-2", "RAG.md"),
    "检索增强生成": ("Layer-2B-深度学习/2B-2", "RAG.md"),
    "位置编码": ("Layer-2B-深度学习/2B-2", "位置编码.md"),

    # === Layer-2C-强化学习 ===
    "MDP": ("Layer-2C-强化学习", "MDP.md"),
    "马尔可夫决策过程": ("Layer-2C-强化学习", "MDP.md"),
    "Bellman方程": ("Layer-2C-强化学习", "Bellman方程.md"),
    "贝尔曼方程": ("Layer-2C-强化学习", "Bellman方程.md"),
    "Q-Learning": ("Layer-2C-强化学习", "Q-Learning.md"),
    "Q学习": ("Layer-2C-强化学习", "Q-Learning.md"),
    "DQN": ("Layer-2C-强化学习", "DQN.md"),
    "深度Q网络": ("Layer-2C-强化学习", "DQN.md"),
    "PPO": ("Layer-2C-强化学习", "PPO.md"),
    "近端策略优化": ("Layer-2C-强化学习", "PPO.md"),
    "MAPPO": ("Layer-2C-强化学习", "MAPPO.md"),
    "SAC": ("Layer-2C-强化学习", "SAC.md"),
    "软演员-评论家": ("Layer-2C-强化学习", "SAC.md"),

    # === Layer-3-化工与过程控制 ===
    "PID控制": ("Layer-3-化工与过程控制", "PID控制.md"),
    "PID": ("Layer-3-化工与过程控制", "PID控制.md"),
    "MPC": ("Layer-3-化工与过程控制", "MPC.md"),
    "模型预测控制": ("Layer-3-化工与过程控制", "MPC.md"),
    "DMC": ("Layer-3-化工与过程控制", "DMC.md"),
    "动态矩阵控制": ("Layer-3-化工与过程控制", "DMC.md"),
    "传递函数": ("Layer-3-化工与过程控制", "传递函数.md"),
    "串级控制": ("Layer-3-化工与过程控制", "串级控制.md"),
    "前馈控制": ("Layer-3-化工与过程控制", "前馈控制.md"),
    "分程控制": ("Layer-3-化工与过程控制", "分程控制.md"),
    "比值控制": ("Layer-3-化工与过程控制", "比值控制.md"),
    "Smith预估器": ("Layer-3-化工与过程控制", "Smith预估器.md"),
    "内模控制": ("Layer-3-化工与过程控制", "内模控制IMC.md"),
    "IMC": ("Layer-3-化工与过程控制", "内模控制IMC.md"),
    "自适应控制": ("Layer-3-化工与过程控制", "自适应控制.md"),
    "鲁棒MPC": ("Layer-3-化工与过程控制", "鲁棒MPC.md"),
    "经济MPC": ("Layer-3-化工与过程控制", "经济MPC.md"),
    "EMPC": ("Layer-3-化工与过程控制", "经济MPC.md"),
    "系统辨识": ("Layer-3-化工与过程控制", "系统辨识.md"),
    "机理建模": ("Layer-3-化工与过程控制", "机理建模.md"),
    "混合建模": ("Layer-3-化工与过程控制", "混合建模.md"),
    "软测量": ("Layer-3-化工与过程控制", "软测量.md"),
    "PRBS": ("Layer-3-化工与过程控制", "PRBS测试.md"),
    "动态优化": ("Layer-3-化工与过程控制", "动态优化.md"),
    "实时优化": ("Layer-3-化工与过程控制", "实时优化RTO.md"),
    "RTO": ("Layer-3-化工与过程控制", "实时优化RTO.md"),
    "数据驱动RTO": ("Layer-3-化工与过程控制", "数据驱动RTO.md"),
    "调度优化": ("Layer-3-化工与过程控制", "调度优化.md"),
    "数据驱动FDD": ("Layer-3-化工与过程控制", "数据驱动FDD.md"),
    "故障诊断": ("Layer-3-化工与过程控制", "数据驱动FDD.md"),
    "PCA故障检测": ("Layer-3-化工与过程控制", "PCA故障检测.md"),
    "报警管理": ("Layer-3-化工与过程控制", "报警管理.md"),
    "HAZOP": ("Layer-3-化工与过程控制", "HAZOP分析.md"),
    "SIL": ("Layer-3-化工与过程控制", "SIL.md"),
    "安全完整性等级": ("Layer-3-化工与过程控制", "SIL.md"),

    # === Layer-4-Agent生态 ===
    "LangChain": ("Layer-4-Agent生态", "LangChain.md"),
    "LangGraph": ("Layer-4-Agent生态", "LangGraph.md"),
    "CrewAI": ("Layer-4-Agent生态", "CrewAI.md"),
    "MCP协议": ("Layer-4-Agent生态", "MCP协议.md"),
    "MCP": ("Layer-4-Agent生态", "MCP协议.md"),
    "模型上下文协议": ("Layer-4-Agent生态", "MCP协议.md"),
    "Function Calling": ("Layer-4-Agent生态", "Function Calling.md"),
    "函数调用": ("Layer-4-Agent生态", "Function Calling.md"),
    "SWE-bench": ("Layer-4-Agent生态", "SWE-bench.md"),

    # === Layer-5-MLOps ===
    "MLflow": ("Layer-5-MLOps", "MLflow.md"),
    "Kubeflow": ("Layer-5-MLOps", "Kubeflow.md"),
    "HuggingFace Hub": ("Layer-5-MLOps", "HuggingFace Hub.md"),
    "Hugging Face": ("Layer-5-MLOps", "HuggingFace Hub.md"),
    "Optuna": ("Layer-5-MLOps", "Optuna.md"),

    # === 横切A-数据驱动方法论 ===
    "DAG因果图": ("横切A-数据驱动方法论", "DAG因果图.md"),
    "因果图": ("横切A-数据驱动方法论", "DAG因果图.md"),
    "DAG": ("横切A-数据驱动方法论", "DAG因果图.md"),
    "Kalman滤波": ("横切A-数据驱动方法论", "Kalman滤波.md"),
    "卡尔曼滤波": ("横切A-数据驱动方法论", "Kalman滤波.md"),

    # === 横切B-AI系统属性 ===
    "SHAP": ("横切B-AI系统属性", "SHAP.md"),
    "Shapley": ("横切B-AI系统属性", "SHAP.md"),
}


def get_node_self(rel_path):
    """Get (layer, filename) for the current node."""
    parts = rel_path.split("/")
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return parts[0] + "/" + parts[1], parts[2]


def wikilink_pattern(layer, filename):
    """Create a wikilink string [[Layer/File]] dropping .md."""
    name = filename.replace(".md", "")
    return f"[[{layer}/{name}]]"


def has_wikilink(text, layer, filename):
    """Check if text already has a wikilink for this target."""
    name = filename.replace(".md", "")
    return f"[[{layer}/{name}" in text


def count_existing_wikilinks(text):
    """Count how many wikilinks already exist in the text."""
    return len(re.findall(r'\[\[([^\]]+)\]\]', text))


def add_wikilinks_to_node(filepath, rel_path):
    """Add wikilinks to a single node file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split frontmatter from body
    parts = content.split("---", 2)
    if len(parts) < 3:
        return 0

    frontmatter = parts[1]
    body = parts[2]

    # Don't touch frontmatter — only body text
    self_layer, self_file = get_node_self(rel_path)
    self_name = self_file.replace(".md", "")
    self_wikilink = f"[[{self_layer}/{self_name}]]"

    # Count existing wikilinks
    existing_count = count_existing_wikilinks(body)

    # Sort keywords by length (longest first) to avoid partial matches
    # E.g., "K-Means" should match before "K"
    sorted_keywords = sorted(CONCEPT_MAP.keys(), key=len, reverse=True)

    links_added = 0
    max_links = 4  # Cap at 4 new links per node
    max_total = 8  # Maximum total wikilinks including existing ones

    for keyword in sorted_keywords:
        if links_added >= max_links:
            break
        if existing_count + links_added >= max_total:
            break

        target_layer, target_file = CONCEPT_MAP[keyword]
        target_name = target_file.replace(".md", "")

        # Skip self-links
        if target_layer == self_layer and target_name == self_name:
            continue

        # Skip if wikilink already exists
        if has_wikilink(body, target_layer, target_file):
            continue

        # Skip if keyword is too short (might cause false positives)
        if len(keyword) <= 2 and keyword.isascii():
            continue

        # Check if keyword appears in body (not inside existing wikilinks or code blocks)
        # First, remove wikilinks from the search text to avoid nested matches
        search_body = re.sub(r'\[\[([^\]]+)\]\]', '', body)

        # Also skip code blocks
        clean_body = re.sub(r'```.*?```', '', search_body, flags=re.DOTALL)

        if keyword in clean_body:
            wikilink = wikilink_pattern(target_layer, target_file)
            # Replace first occurrence of keyword with wikilink
            # Use a word-boundary-aware replacement for ASCII keywords
            if keyword.isascii():
                pattern = re.compile(r'(?<!\w)' + re.escape(keyword) + r'(?!\w)')
                new_body, count = pattern.subn(f"[[{target_layer}/{target_name}|{keyword}]]", body, count=1)
                if count > 0:
                    body = new_body
                    links_added += 1
            else:
                # For CJK keywords, just do simple replacement
                new_body = body.replace(keyword, f"[[{target_layer}/{target_name}|{keyword}]]", 1)
                if new_body != body:
                    body = new_body
                    links_added += 1

    if links_added > 0:
        new_content = "---" + frontmatter + "---" + body
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  +{links_added} links: {rel_path}")

    return links_added


def main():
    # Collect all node .md files (excluding _index.md and non-node files)
    node_files = []
    exclude_dirs = {".git", ".github", ".obsidian", "AI_Knowledge_Graph"}
    exclude_files = {"_index.md", "index.md", "2026-06-22.md",
                     "CC_Review_Prompt.md", "参考文献汇总.md",
                     "技术体系骨架设计.md", "robots.txt", ".gitignore",
                     "merge_refs.py", "add_wikilinks.py",
                     "refs_content_map.json", "content_map.json"}

    for root, dirs, files in os.walk(BASE):
        # Skip hidden dirs and non-node dirs
        rel_root = os.path.relpath(root, BASE)
        if rel_root == ".":
            continue
        parts = rel_root.split(os.sep)
        if parts[0] in exclude_dirs or parts[0].startswith("."):
            continue

        for f in files:
            if f in exclude_files or not f.endswith(".md"):
                continue
            rel_path = os.path.relpath(os.path.join(root, f), BASE)
            node_files.append((os.path.join(root, f), rel_path))

    total = len(node_files)
    linked = 0
    total_links = 0

    print(f"Processing {total} node files for wikilinks...\n")

    for filepath, rel_path in sorted(node_files):
        links = add_wikilinks_to_node(filepath, rel_path)
        if links > 0:
            linked += 1
            total_links += links

    print(f"\nDone. Added {total_links} wikilinks across {linked}/{total} nodes.")


if __name__ == "__main__":
    main()
