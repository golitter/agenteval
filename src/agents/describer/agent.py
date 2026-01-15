import asyncio
from typing import Any, Dict, Optional
import json
from loguru import logger
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage

from config import Configuration, load_prompt_templates
from src.utils.callback import SyncCallbackHandler
from config import load_config

DescriberAgent_SYSTEM_PROMPT = load_prompt_templates()["describer"]["system_prompt"]

def get_full_system_prompt() -> str:
    _config = load_config()
    test_description_file = _config.get("test","test_description_file")
    if test_description_file:
        try:
            with open(test_description_file, "r", encoding="utf-8") as f:
                description_content = f.read()
            full_prompt = DescriberAgent_SYSTEM_PROMPT.replace("{test_description}", description_content)
            return full_prompt
        except Exception as e:
            logger.error(f"Failed to load test description file: {e}")
    return DescriberAgent_SYSTEM_PROMPT.replace("{test_description}", "No description available.")

class DescriberAgent:
    """Describer Agent ，无状态调用 Agent 并管理对话历史。"""

    def __init__(self, config: Configuration) -> None:
        self.config = config

    async def ainvoke(self, input_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """无状态调用：加载历史 → 创建 Agent → 调用 → 保存历史"""
        config = config or {}

        initial_messages = []

        llm = ChatDeepSeek(
            model=self.config.model, # type: ignore
            api_key=self.config.api_key, # type: ignore
            base_url=self.config.base_url,
            callbacks=[SyncCallbackHandler()],
        )
        agent = create_agent(
            model=llm,
            tools=[],
            system_prompt=get_full_system_prompt(),
        )

        user_message = HumanMessage(input_data.get("input", ""))
        agent_response = await agent.ainvoke({
            "messages": initial_messages + [user_message] # type: ignore
        },
        config={"callbacks": [SyncCallbackHandler()]}
        )
        return {"messages": agent_response["messages"]}

async def main():
    config = Configuration()
    describer_agent = DescriberAgent(config)
    config = load_config()
    test_file = config.get("test","test_data_file")
    with open(test_file, "r", encoding="utf-8") as f:
        test_examples = json.load(f)
    
    # print(test_examples)
    example = test_examples[0]
    print(str(example))
    input_data = {
        "input": str(example)
    }
    response = await describer_agent.ainvoke(input_data)
    # for msg in response["messages"]:
    #     print(f"{msg.type}: {msg.content}")
    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())