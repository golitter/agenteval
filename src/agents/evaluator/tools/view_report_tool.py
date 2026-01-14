from langchain_core.tools import tool
from src.utils.view_report import view_document
from typing import Optional
from config import load_config
import os

@tool
def view_report_tool(start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
    """
    查看分析报告的指定行范围内容。
    Args:
        start_line (Optional[int]): 起始行号（从1开始），默认为None表示从头开始。
        end_line (Optional[int]): 结束行号，默认为None表示到结尾。
    Returns:
        str: 指定行范围的报告内容。
    """
    config = load_config()
    memory_dir = config.get('agent', 'memory_dir')
    target_agent_md_file = config.get('agent', 'target_agent_md_file')
    full_path = os.path.join(memory_dir, target_agent_md_file)
    report_content = view_document(full_path, start_line, end_line)
    return report_content