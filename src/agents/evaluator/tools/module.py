from src.tools.agent_inference import agent_chat_inference, agent_chat_status
from src.agents.evaluator.tools.view_report_tool import view_report_tool
evaluator_tools_list = [
    # 待测试智能体对话接口
    agent_chat_inference,
    # 待测试智能体状态查询接口
    agent_chat_status,
    # 查看分析报告工具
    view_report_tool,
]