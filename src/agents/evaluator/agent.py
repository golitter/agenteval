import asyncio
from typing import Any, Dict, Optional

from loguru import logger
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, BaseMessage

from config import Configuration, load_prompt_templates
from src.agents.evaluator.tools.module import evaluator_tools_list
from src.utils.memory import FileMemory
from src.utils.callback import SyncCallbackHandler

EvaluatorAgent_SYSTEM_PROMPT = load_prompt_templates()["evaluator"]["system_prompt"]

class EvaluatorAgent:
    """Evaluator Agent ，无状态调用 Agent 并管理对话历史。"""

    def __init__(self, config: Configuration = Configuration()) -> None:
        self.config = config

    async def ainvoke(self, input_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None, agent_api_extras: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        异步调用 Evaluator Agent 进行评估任务。
        Args:
            input_data: 包含输入数据的字典，必须包含 "input" 键。
            config: 可选的配置字典，用于覆盖默认配置。
            agent_api_extras: 可选的额外参数字典，传递给 待测试的Agent API。
        Returns:
            包含评估结果的字典。
        """
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
            tools=evaluator_tools_list,
            system_prompt=EvaluatorAgent_SYSTEM_PROMPT,
        )

        user_message = HumanMessage(input_data.get("input", ""))

        # agent_api_extras 参数处理
        if not agent_api_extras:
            agent_api_extras = {}
        
        agent_response = await agent.ainvoke({
            "messages": initial_messages + [user_message] # type: ignore
        },
        config={"callbacks": [SyncCallbackHandler()], "configurable": {"agent_api_extras": agent_api_extras} }
        )

        messages_to_save = [
            BaseMessage(content=msg.content, type=msg.type)
            for msg in agent_response["messages"]
        ]
        FileMemory(agent_type="evaluator").save(messages_to_save, backup=True)

        return {"messages": agent_response["messages"]}

async def main():
    config = Configuration()
    evaluator_agent = EvaluatorAgent(config)

    input_data = {
        "input": "调用 agent_chat_inference 工具，向智能体发送查询：介绍一下你自己。",
    }
    # 简单调用
    # response = await evaluator_agent.ainvoke(input_data)
    # 传递复杂的 agent_api_extras 参数
    import json
    # import os
    # from config import load_config
    # config_ini = load_config()
    # extras_evaluator_config = config_ini.get("agent_api_extras", "evaluator")
    # with open(extras_evaluator_config, "r", encoding="utf-8") as f:
    #     extras_evaluator_config = json.load(f)
    # print("extras_evaluator_config:", extras_evaluator_config)
    a = {"session_id": "test-session-001", "a": 123, "b": [1,2,3], "c": {"key": "value"}}
    a_json = json.dumps(a)
    a = json.loads(a_json)
    response = await evaluator_agent.ainvoke(input_data, agent_api_extras=a)
    # for msg in response["messages"]:
    #     print(f"{msg.type}: {msg.content}")
    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
