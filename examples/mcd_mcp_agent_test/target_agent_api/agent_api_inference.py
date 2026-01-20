import asyncio
from examples.mcd_mcp_agent_test.agent import MCDAgent
mcd_agent = MCDAgent()

def agent_api_health_check() -> dict:

    return {"status":200, "message":"智能体正常"}

def agent_api_inference(query: str) -> str:
    input_data = {
        "input": query
    }
    response = asyncio.run(mcd_agent.ainvoke(input_data))
    return response["messages"][-1].content

if __name__ == "__main__":
    # 测试健康检查接口
    health_status = agent_api_health_check()
    print(f"Health Check: {health_status}")

    # 测试推理接口
    test_query = "你可以干什么"
    inference_response = agent_api_inference(test_query)
    print(f"Inference Response: {inference_response}")