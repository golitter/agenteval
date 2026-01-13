from langchain_core.tools import tool
from src.mock.agent_api_inference import agent_api_inference, agent_api_health_check
@tool()
def agent_chat_inference(query: str) -> str:
    """
    向待测试的智能体发送查询并返回响应。
    Args:
        query (str): 发送给智能体的查询内容。
    Returns:
        str: 智能体的响应内容。
    """
    return agent_api_inference(query=query, session_id="test_session")

@tool()
def agent_chat_status() -> dict:
    """
    获取待测试智能体的当前状态信息。
    Returns:
        str: 智能体的状态描述。
    """
    status = agent_api_health_check()

    return status

if __name__ == "__main__":
    answer = agent_chat_inference.invoke({"query": "介绍一下你自己。"})
    print(f"智能体响应: {answer}")

    status = agent_chat_status.invoke({})
    print(f"智能体状态: {status}")