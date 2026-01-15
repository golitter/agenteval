# AgentEval

智能体评估框架 - 用于分析和评估 AI 智能体性能的多智能体系统。

## 简介

AgentEval 是一个专门用于评估 AI 智能体性能的框架。通过多智能体协作的方式，系统可以深入分析目标智能体的能力、任务和工具，并对其进行全面的性能评估。

## 核心功能

### 1. Profiler Agent（分析智能体）
通过逆向工程分析目标智能体，深入了解其任务、工具和额外信息，并生成结构化的分析报告。

**主要功能：**
- 分析智能体的任务类型
- 识别智能体使用的工具列表及其功能
- 收集智能体的额外信息
- 生成 Markdown 格式的分析报告

### 2. Evaluator Agent（评估智能体）
基于预设的测试用例，模拟人类评估者对目标智能体进行测试和评分。

**主要功能：**
- 根据测试用例与智能体交互
- 评估智能体在测试中的表现
- 生成评分（1-10分）和详细评估报告
- 支持查看智能体文档辅助评估

### 3. Describer Agent（描述智能体）
将测试输入转换为描述性文本，便于理解和后续测试。

**主要功能：**
- 无状态处理，快速转换输入
- 根据测试类型生成清晰的描述性文本
- 支持自定义测试类型模板

## 项目结构

```
agenteval/
├── README.md                   # 项目文档
├── main.py                     # 简单入口文件
├── config.py                   # 配置加载器
├── config.ini                  # 配置文件
├── .env                        # 环境变量（需自行创建）
├── pyproject.toml              # 项目依赖
├── src/
│   ├── agents/                 # 智能体实现
│   │   ├── describer/          # 描述智能体
│   │   ├── evaluator/          # 评估智能体
│   │   └── profiler/           # 分析智能体
│   ├── mock/                   # 模拟 API 实现
│   │   └── agent_api_inference.py
│   ├── tools/                  # LangChain 工具
│   │   ├── agent_inference.py
│   │   └── generate_report.py
│   ├── utils/                  # 工具模块
│   │   ├── callback.py         # 回调处理器
│   │   ├── logger.py           # 日志工具
│   │   ├── memory.py           # 智能体短期记忆管理
│   │   └── view_report.py      # 报告查看
│   └── prompts.yaml            # 提示词模板
└── data/                       # 数据存储
    ├── datasets/               # 测试数据
    │   ├── test.json           # 测试用例
    │   └── description.json    # 测试类型描述
    └── file_memory/            # 对话历史存储
```

## 安装

### 环境要求

- Python >= 3.10

### 安装依赖

```bash
pip install -e .
```

## 配置

### 1. 环境变量配置

创建 `.env` 文件并配置以下内容：

```ini
DS_API_KEY=your_deepseek_api_key
DS_BASE_URL=https://api.deepseek.com
DS_MODEL=deepseek-chat
```

### 2. 配置文件 (config.ini)

```ini
[prompts]
prompt_template = ./src/prompts.yaml

[agent]
memory_dir = ./data/file_memory
backup_memory_dir = ./data/file_memory/backup
target_agent_md_file = target_agent_doc.md

[test]
test_description_file = ./data/datasets/description.json
test_data_file = ./data/datasets/test.json
```

## 使用方法
项目未完成。。。
## 数据文件格式

### test.json（测试用例）

```json
[
    {
        "query": "调用工具生成 Fe-C 二元相图",
        "result": "Fe-C 二元相图的描述",
        "middleware": [
            "使用默认值",
            "进行确认"
        ]
    }
]
```

### description.json（测试类型描述）

```json
{
    "query": "测试的输入",
    "result": "返回的描述性文本",
    "middleware": [
        "中间的过程描述"
    ]
}
```

## 工作流程

1. **Profiler Agent 工作流**
   ```
   输入 → 智能体分析 → 收集任务/工具信息 → 生成报告
   ```

2. **Evaluator Agent 工作流**
   ```
   测试用例 → 智能体交互 → 性能评估 → 生成评分 + 报告
   ```

3. **Describer Agent 工作流**
   ```
   输入文本 → 转换为描述 → 输出处理后的文本
   ```