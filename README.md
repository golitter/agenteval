# AgentEval

tool-use agent 评估框架 - 评估工具使用智能体性能的多智能体系统

## 简介

AgentEval 是一个专门用于评估 **tool-use agent**（工具使用智能体）性能的框架。不同于普通对话智能体，tool-use agent 需要正确选择工具、准确传递参数、按序执行操作、处理工具返回结果。本框架通过多智能体协作的方式，对目标智能体的工具使用能力进行全面评估。

**核心价值**：评估工具选择准确性、参数传递正确性、执行顺序合理性、结果处理完整性。

## 快速开始

```python
import asyncio
from src.eval.coordinator import Coordinator
from src.eval.utils.data_loader import DataLoader

async def main():
    data_loader = DataLoader()
    coordinator = Coordinator(data_loader)

    # 1. 分析目标 tool-use agent 的工具列表和调用模式
    profile = await coordinator.profile()
    print(profile)

    # 2. 描述工具调用测试用例
    await coordinator.describes()

    # 3. 执行工具调用评估
    await coordinator.evaluates()

    # 4. 生成工具使用分析报告
    csv_report = await coordinator.analyze()
    print(csv_report)

asyncio.run(main())
```

## TODO

### 已知问题

- [ ] **测试过程数据 checkpoint**：评估过程中缺少中间结果保存机制，异常中断后无法恢复
- [ ] **Agent memory 超限**：长对话可能导致 memory 超出上下文限制，需要分段或压缩机制
- [ ] **Profiler 分析局限**：单次分析 + 循环限制可能无法完整生成 agent 文档，复杂 agent 需要多次交互
- [ ] **Evaluator 过程验证缺失**：缺少对 evaluator 执行过程的有效性检查，无法确定评估是否奏效
- [ ] **Describer 异常处理**：通过提示词固定自然语言测试语句，可能存在生成异常或不符合预期的情况

## 核心功能

### 四个专用智能体

| 智能体 | 职责 |
|--------|------|
| **ProfilerAgent** | 分析 tool-use agent 的工具列表、工具功能、参数模式、调用频率 |
| **EvaluatorAgent** | 模拟用户发起工具调用，评估工具选择正确性、参数准确性、结果处理 |
| **DescriberAgent** | 将工具调用测试用例转换为自然语言描述 |
| **AnalystAgent** | 分析工具调用成功率、错误类型、参数错误分布 |

### 评估编排器（Coordinator）

```python
test.json → Describer → described_test_samples.json
    → Evaluator → evaluation_results.json
    → Analyst → analysis_report.csv
```

## 安装

### 环境要求

- Python >= 3.10

### 安装依赖

```bash
pip install -e .
```

### 依赖项

```
langchain>=1.2.3
langchain-deepseek>=1.0.1
langchain-mcp-adapters>=0.2.1
loguru>=0.7.3
pandas>=2.3.3
python-dotenv>=1.2.1
```

## 配置说明

### 1. 环境变量（.env）

```ini
DS_API_KEY=your_deepseek_api_key
DS_BASE_URL=https://api.deepseek.com
DS_MODEL=deepseek-chat
```

### 2. 配置文件（config.ini）

```ini
[prompts]
prompt_template = ./src/prompts.yaml

[agent]
memory_dir = ./data/file_memory
backup_memory_dir = ./data/file_memory/backup
target_agent_md_file = target_agent_doc.md

[agent_api_extras]
profiler = ./data/datasets/extras_profiler.json
evaluator = ./data/datasets/extras_evaluator.json

[eval]
describer_output_file = ./data/datasets/described_test_samples.json
evaluator_output_file = ./data/eval_results/evaluation_results.json
analysis_report_file = ./data/eval_results/analysis_report.csv

[test]
test_description_file = ./data/datasets/description.json
test_data_file = ./data/datasets/test.json
```

### 3. API 额外参数（extras_*.json）

用于配置目标 tool-use agent 的 API 接口参数，更详细内容见`src/extensions/`的README.md内容。

**extras_profiler.json**（示例）：
```json
[
    {
        "base_url": "http://localhost:8000",
        "session_id": "profiler_session"
    }
]
```

**extras_evaluator.json**（示例，每个测试用例对应一个配置）：
```json
[
    {"base_url": "http://localhost:8000", "session_id": "test_1"},
    {"base_url": "http://localhost:8000", "session_id": "test_2"}
]
```

## 使用方法

### 完整评估流程

```python
from src.eval.coordinator import Coordinator
from src.eval.utils.data_loader import DataLoader
import asyncio

async def full_evaluation():
    data_loader = DataLoader()
    coordinator = Coordinator(data_loader)

    # 阶段1: 分析工具列表和调用模式
    profile = await coordinator.profile("请分析这个智能体支持哪些工具及其调用方式。")

    # 阶段2: 描述工具调用测试用例
    described = await coordinator.describes()

    # 阶段3: 执行工具调用评估
    results = await coordinator.evaluates()

    # 阶段4: 分析工具调用结果
    report = await coordinator.analyze()

asyncio.run(full_evaluation())
```

### Examples

#### 1. lab_agent_test

基础 tool-use agent 测试框架，使用 `query` + `session_id` 参数。

将`target_agent_api`内的文件按照相同文件名分别填充到`src/uitls/agent_inference.py`和`src/mock/agent_api_inference.py`。

#### 2. mcd_mcp_agent_test

麦当劳 MCP tool-use agent 测试，使用 Model Context Protocol

将`target_agent_api`内的文件按照相同文件名分别填充到`src/uitls/agent_inference.py`和`src/mock/agent_api_inference.py`。


## 开发指南

### 项目结构

```
agenteval/
├── README.md
├── pyproject.toml              # 项目依赖
├── config.ini                  # 配置文件
├── config.py                   # 配置加载器
├── main.py                     # 入口文件
├── src/
│   ├── agents/                 # 智能体实现
│   │   ├── describer/          # 描述智能体
│   │   ├── evaluator/          # 评估智能体
│   │   ├── profiler/           # 分析智能体
│   │   └── analyst/            # 分析智能体
│   ├── eval/                   # 评估编排
│   │   ├── coordinator.py      # 协调器
│   │   └── utils/
│   │       ├── data_loader.py  # 数据加载
│   │       └── analysis.py     # 结果分析
│   ├── tools/                  # LangChain 工具
│   ├── utils/                  # 工具模块
│   │   ├── callback.py
│   │   ├── logger.py
│   │   └── memory.py
│   └── prompts.yaml            # 提示词模板
├── data/
│   ├── datasets/               # 测试数据
│   │   ├── test.json
│   │   ├── description.json
│   │   ├── extras_profiler.json
│   │   └── extras_evaluator.json
│   ├── eval_results/           # 评估结果
│   └── file_memory/            # 对话历史
└── examples/                   # 测试示例
    ├── lab_agent_test/
    └── mcd_mcp_agent_test/
```

### 数据格式

> 可以自行扩展、修改

**test.json**（工具调用测试用例）：
```json
[
    {
        "query": "调用工具生成 Fe-C 二元相图",
        "result": "Fe-C 二元相图的描述",
        "intermediate_steps": [
            "使用默认值",
            "进行确认"
        ]
    }
]
```

**description.json**（测试类型描述）：
```json
{
    "query": "测试的输入",
    "result": "返回的描述性文本",
    "intermediate_steps": ["中间的过程描述"]
}
```

### 扩展开发

添加新的 tool-use agent 适配器：

1. 创建适配器类，实现 `ainvoke` 方法：
```python
class MyToolUseAgent:
    async def ainvoke(self, input_data: Dict[str, Any], config: Optional[Dict] = None):
        # 实现 tool-use agent API 调用逻辑
        return {"messages": [...]}
```

2. 在 `examples/` 下创建测试目录

3. 配置 `extras_*.json` 文件

4. 运行评估流程

### 工作流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                      tool-use agent 评估流程                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐                                               │
│  │  可选：Profiler  │ → target_agent_doc.md（工具列表、调用模式）   │
│  └─────────────────┘         或                                    │
│         ↑                     用户自行提供 agent 描述文档             │
│         │                                                         │
│         │ (可选)                                                   │
│         │                                                         │
│  test.json（工具调用测试用例）                                       │
│      │                                                              │
│      ▼                                                              │
│  ┌─────────────┐    described_test_samples.json                     │
│  │ Describer   │──────────────────────┐                            │
│  └─────────────┘                      │                            │
│                                       ▼                            │
│                            ┌─────────────┐                         │
│                            │  Evaluator  │                         │
│                            └─────────────┘                         │
│                                       │                            │
│                                       ▼                            │
│                          evaluation_results.json                   │
│                                       │                            │
│                                       ▼                            │
│                            ┌─────────────┐                         │
│                            │   Analyst   │                         │
│                            └─────────────┘                         │
│                                       │                            │
│                                       ▼                            │
│                          analysis_report.csv                       │
│                        （工具调用成功率、错误分布）                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 贡献指南

欢迎提交 Issue 和 Pull Request。
