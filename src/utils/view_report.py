import os
from typing import Optional
def view_document(file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
    """
    查看文档内容：
    - 如果只提供文件路径，返回总行数
    - 如果提供起始行和结束行，返回该范围内的内容
    """
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return f"错误：文件 不存在"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return f"读取文件时出错：{str(e)}"
    
    total_lines = len(lines)
    
    # 场景1：只查看总行数
    if start_line is None and end_line is None:
        importance_lines_content = ["## 1. 智能体的任务",
                                    "## 2. 智能体使用的工具列表及其功能描述",
                                    "## 3. 智能体使用的额外信息"
                                    ]
        importance_content = ""
        for i, line in enumerate(lines, start=1):
            line = line.strip()
            if line in importance_lines_content:
                importance_content += f" {i} 行| {line}\n"
        return f"文档 总共有 {total_lines} 行，其中：\n{importance_content}"
    
    # 场景2：查看指定行范围
    # 默认 start_line 从1开始，转换为0-based索引
    start_idx = (start_line - 1) if start_line is not None else 0
    if start_idx < 0:
        start_idx = 0
    
    # 默认 end_line 到文件末尾
    if end_line is None:
        end_idx = total_lines
    else:
        end_idx = end_line  # 切片是右开区间，所以不用减1
    
    # 边界检查
    if start_idx >= total_lines:
        return f"错误：起始行 {start_line} 超出文档总行数 {total_lines}"
    
    if end_idx > total_lines:
        end_idx = total_lines
    
    # 提取指定行
    selected_lines = lines[start_idx:end_idx]
    
    # 构建结果
    result = f"文档 第 {start_line or 1} 行到第 {end_line or total_lines} 行的内容：\n\n"
    
    # 添加行号前缀
    for i, line in enumerate(selected_lines, start=start_idx + 1):
        result += f"{i:5d} | {line}"
    
    result += f"\n\n（共显示 {len(selected_lines)} 行，文档总行数：{total_lines}）"
    
    return result

if __name__ == "__main__":
    # 测试代码
    from config import load_config
    config = load_config()
    memory = config.get("agent", "memory_dir")
    target_agent_md_file = config.get("agent", "target_agent_md_file")
    file = os.path.join(memory, target_agent_md_file)
    test_file = file  # 替换为实际测试文件路径    
    # 场景1：查看总行数
    print(view_document(test_file))
    
    # 场景2：查看指定行范围
    print(view_document(test_file, start_line=5, end_line=15))