from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from typing import Any, Dict, Optional

from loguru import logger
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, BaseMessage
from config import Configuration
from src.utils.memory import FileMemory
from src.utils.callback import SyncCallbackHandler
import json
import os
MCDAgent_SYSTEM_PROMPT = "你是麦当劳的智能助手，专注于帮助用户完成各种任务。你拥有访问多种工具的能力，可以根据用户的需求选择合适的工具来提供帮助。请确保在回答用户问题时，充分利用可用的工具，以提供准确和有用的信息。"

def load_mcp_config():
    relative_path = "./examples/mcd_mcp_agent_test/mcp_config.json"
    with open(relative_path, "r", encoding="utf-8") as f:
        servers_cfg = json.load(f)
    servers = servers_cfg.get("mcpServers", {})
    # print(servers)
    # export MCP_TOKEN={your_token_here}
    if os.getenv("MCP_TOKEN") is None:
        raise ValueError("Please set MCP_TOKEN environment variable")

    authorization_bearer = servers['mcd-mcp']['headers']['Authorization']
    authorization_bearer = authorization_bearer.replace("{YOUR_MCP_TOKEN}", os.getenv("MCP_TOKEN"))
    servers['mcd-mcp']['headers']['Authorization'] = authorization_bearer
    # print(servers['mcd-mcp']['headers']['Authorization'])
    return servers

servers = load_mcp_config()
mcp_client = MultiServerMCPClient(servers)

class MCDAgent:
    """Profiler Agent ，无状态调用 Agent 并管理对话历史。"""

    def __init__(self, config: Configuration = Configuration()) -> None:
        self.config = config

    async def ainvoke(self, input_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        异步调用 麦当劳 Agent 进行分析智能体。
        Args:
            input_data: 包含输入数据的字典，必须包含 "input" 键。
            config: 可选的配置字典，用于覆盖默认配置。
        Returns:
            包含分析信息的字典。
        """
        config = config or {}

        initial_messages = []

        mcd_tools = await mcp_client.get_tools()

        llm = ChatDeepSeek(
            model=self.config.model, # type: ignore
            api_key=self.config.api_key, # type: ignore
            base_url=self.config.base_url,
            callbacks=[SyncCallbackHandler()],
        )
        agent = create_agent(
            model=llm,
            tools=mcd_tools,
            system_prompt=MCDAgent_SYSTEM_PROMPT,
        )

        user_message = HumanMessage(input_data.get("input", ""))

        agent_response = await agent.ainvoke({
            "messages": initial_messages + [user_message] # type: ignore
        },
        config={"callbacks": [SyncCallbackHandler()]}
        )

        messages_to_save = [
            BaseMessage(content=msg.content, type=msg.type)
            for msg in agent_response["messages"]
        ]
        FileMemory(agent_type="mcd").save(messages_to_save, backup=True)

        return {"messages": agent_response["messages"]}

async def main():
    config = Configuration()
    mcd_agent = MCDAgent(config)

    input_data = {
        "input": "你可以干什么"
    }
    response = await mcd_agent.ainvoke(input_data)
    # for msg in response["messages"]:
    #     print(f"{msg.type}: {msg.content}")
    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
