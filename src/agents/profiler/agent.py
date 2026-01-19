import asyncio
from typing import Any, Dict, Optional

from loguru import logger
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, BaseMessage

from config import Configuration, load_prompt_templates
from src.agents.profiler.tools.module import profiler_tools_list
from src.utils.memory import FileMemory
from src.utils.callback import SyncCallbackHandler

from langchain.agents.middleware import TodoListMiddleware

ProfilerAgent_SYSTEM_PROMPT = load_prompt_templates()["profiler"]["system_prompt"]

class ProfilerAgent:
    """Profiler Agent ，无状态调用 Agent 并管理对话历史。"""

    def __init__(self, config: Configuration = Configuration()) -> None:
        self.config = config

    async def ainvoke(self, input_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None, agent_api_extras: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        异步调用 Profiler Agent 进行分析智能体。
        Args:
            input_data: 包含输入数据的字典，必须包含 "input" 键。
            config: 可选的配置字典，用于覆盖默认配置。
            agent_api_extras: 可选的额外参数字典，传递给 待测试的Agent API。
        Returns:
            包含分析信息的字典。
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
            tools=profiler_tools_list,
            middleware=[TodoListMiddleware(            
                system_prompt=(
                "在开始处理复杂任务时，先用 write_todos 工具创建一个待办清单；"
                "执行过程中根据进展更新待办清单，包括补充新任务或删除无效任务。"
            )
            )],
            system_prompt=ProfilerAgent_SYSTEM_PROMPT,
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
        FileMemory(agent_type="profiler").save(messages_to_save, backup=True)

        return {"messages": agent_response["messages"]}

async def main():
    config = Configuration()
    profiler_agent = ProfilerAgent(config)

    input_data = {
        "input": "请分析这个智能体的设计目的和使用的工具。"
    }
    # response = await profiler_agent.ainvoke(input_data)
    import json
    from config import load_config
    config_ini = load_config()
    extras_path = config_ini.get('agent_api_extras', 'profiler')
    with open(extras_path, 'r', encoding='utf-8') as f:
        extras = json.load(f)
    response = await profiler_agent.ainvoke(input_data, agent_api_extras=extras)
    # for msg in response["messages"]:
    #     print(f"{msg.type}: {msg.content}")
    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
