from src.tools.agent_inference import agent_chat_inference, agent_chat_status
from src.agents.profiler.tools.target_agent_report_tool import generate_target_agent_analysis_report_md
profiler_tools_list = [
    # 待测试智能体对话接口
    agent_chat_inference,
    # 待测试智能体状态查询接口
    agent_chat_status,
    # 生成目标智能体分析报告的Markdown格式内容
    generate_target_agent_analysis_report_md,
]