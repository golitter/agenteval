# 待测试agent接口扩展
简单的agent接口，只需要：
- `agent_chat_inference`：只有`query`参数
- `agent_chat_status`：无需参数
可能中大型复杂agent的接口有多个参数，因此这个目录是**扩展接口参数**的说明和引导。

## 用到的模块
- **`src/agents/profiler/agent.py`**：分析待测智能体的功能
- **`src/agents/evaluator/agent.py`**：使用待测智能体进行评估
- **`src/eval/orchestrator.py`**：协调器，对`profiler` -> `describer` -> `evaluator` -> `analyst` 的编排。

## **具体实现方式**
langchain的工具添加`config: RunnableConfig`参数：
```python
def agent_chat_inference(query: str, config: RunnableConfig) -> str:
    ...
    agent_api_extras = config.get("configurable", {}).get("agent_api_extras", {})
    session_id = agent_api_extras.get("session_id", "test_default_session")
```
`profiler`和`evaluator`智能体的ainvoke方法中：
```python
response = await profiler_agent.ainvoke(input_data, agent_api_extras=extras)
```
其中`extras`参数为：
```json
{
    "session_id": "test-session-xx-id"
}
```
或者
```python
a = {"session_id": "test-session-001", "a": 123, "b": [1,2,3], "c": {"key": "value"}}
```