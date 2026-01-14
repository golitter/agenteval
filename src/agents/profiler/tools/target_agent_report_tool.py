from langchain_core.tools import tool
import os
from config import load_config
import time

@tool
def generate_target_agent_analysis_report_md(task: str, tools: str, additional_info: str) -> str:
    """
    生成目标智能体分析报告的Markdown格式内容。
    Args:
        task (str): 目标智能体的任务描述，内容精简，不超过500字。
        tools (str): 目标智能体使用的工具列表及其功能描述，内容要详尽。
        additional_info (str): 目标智能体使用的额外信息，内容要详尽。
    Returns:
        str: 生成的Markdown格式报告内容。
    
    形式如下：{# 目标智能体分析报告
## 1. 智能体的任务
{task}

## 2. 智能体使用的工具列表及其功能描述
{tools}

## 3. 智能体使用的额外信息
{additional_info}}
    """

    report_md = f"""# 目标智能体分析报告
## 1. 智能体的任务
{task}

## 2. 智能体使用的工具列表及其功能描述
{tools}

## 3. 智能体使用的额外信息
{additional_info}
"""
    _config = load_config()
    target_agent_md_file = _config.get('agent', 'target_agent_md_file')
    memory_dir = _config.get('agent', 'memory_dir')
    backup_memory_dir = _config.get('agent', 'backup_memory_dir')
    full_path = os.path.join(memory_dir, target_agent_md_file)
    backup_memory_dir = os.path.join(backup_memory_dir, "target_agent_reports")
    current_time_str = time.strftime("%Y%m%d%H%M%S")
    backup_path = os.path.join(backup_memory_dir, f"{current_time_str}.md")

    os.makedirs(memory_dir, exist_ok=True)
    os.makedirs(backup_memory_dir, exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
    
    return report_md

if __name__ == "__main__":
    # 测试生成报告工具
    task = "该智能体旨在协助用户完成各种任务，包括信息检索、数据分析和自动化操作。"
    tools = "- 信息检索工具：用于从互联网获取相关信息。\n- 数据分析工具：用于处理和分析数据集。\n- 自动化操作工具：用于执行预定义的任务和工作流程。"
    additional_info = "该智能体还集成了自然语言处理功能，能够理解和生成多种语言的文本内容。"
    
    report = generate_target_agent_analysis_report_md.invoke({
        "task": task,
        "tools": tools,
        "additional_info": additional_info
    })
    print(report)
