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
from src.agents.analyst.schema import AnalystAgentResponse
from datetime import datetime

AnalystAgent_SYSTEM_PROMPT = load_prompt_templates()["analyst"]["system_prompt"]
class AnalystAgent:
    """Analyst Agent ，无状态调用 Agent 并管理对话历史。"""

    def __init__(self, config: Configuration = Configuration()) -> None:
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
            system_prompt=AnalystAgent_SYSTEM_PROMPT,
            response_format=AnalystAgentResponse
        )

        user_message = HumanMessage(input_data.get("input", ""))
        agent_response = await agent.ainvoke({
            "messages": initial_messages + [user_message] # type: ignore
        },
        config={"callbacks": [SyncCallbackHandler()]}
        )
        structured = agent_response["structured_response"]
        structed_output = structured.model_dump_json()
        structed_json_output = json.loads(structed_output)
        # 加入时间戳
        structed_json_output['evaluation_time'] = datetime.now().isoformat()
        return {"messages": structed_json_output}

async def main():
    # config = Configuration()
    analyst_agent = AnalystAgent()
    config = load_config()
    test_file = config.get("eval","evaluator_output_file")
    with open(test_file, "r", encoding="utf-8") as f:
        test_examples = json.load(f)
    
    # print(test_examples)
    example = test_examples[0]
    input_data = {
        "input": str(example)
    }
    response = await analyst_agent.ainvoke(input_data)
    answer = response["messages"]
    print(type(answer))
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())