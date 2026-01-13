import os
import json
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List, Dict, Any

from config import load_config

_config = load_config()
DEFAULT_MEMORY_DIR = _config["agent"]["memory_dir"]
BACKUP_MEMORY_DIR = _config["agent"].get("backup_memory_dir")


class FileMemory:
    """
    基于本地 JSON 文件的对话记忆管理类。
    每个 session_id 对应一个独立的历史文件。
    负责所有与文件读写相关的操作。
    """

    def __init__(self, agent_type: str, base_dir: str = DEFAULT_MEMORY_DIR):
        self.agent_type = agent_type
        self.base_dir = base_dir
        self.file_path = os.path.join(base_dir, f"{agent_type}.json")

        # 自动创建目录
        os.makedirs(base_dir, exist_ok=True)

    def load(self) -> List[BaseMessage]:
        """
        从本地文件加载历史消息，并转换为 LangChain 的 BaseMessage 对象列表。
        
        Returns:
            List[BaseMessage]: 包含历史对话的消息列表。
        """
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data: List[Dict[str, Any]] = json.load(f)
        except Exception as e:
            print(f"[Warning] 无法读取 memory 文件 {self.file_path}: {e}")
            return []

        messages: List[BaseMessage] = []
        for item in data:
            if "human" in item:
                messages.append(HumanMessage(content=item["human"]))
            elif "ai" in item:
                messages.append(AIMessage(content=item["ai"]))
        return messages

    def save(self, messages: List[BaseMessage], backup: bool = False) -> None:
        """
        将 LangChain 的 BaseMessage 对象列表保存到本地文件。
        
        Args:
            messages: 包含完整对话历史的 BaseMessage 列表.
            backup: 是否创建备份文件。
        """
        history: List[Dict[str, str]] = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                # 确保内容是字符串格式
                content = str(msg.content) if not isinstance(msg.content, str) else msg.content
                history.append({"human": content})
            elif isinstance(msg, AIMessage):
                # 确保内容是字符串格式
                content = str(msg.content) if not isinstance(msg.content, str) else msg.content
                history.append({"ai": content})
            elif isinstance(msg, BaseMessage):
                # 处理其他类型的消息
                content = str(msg.content) if not isinstance(msg.content, str) else msg.content
                type = str(getattr(msg, "type", "base"))
               
                history.append({type: content})
        if backup:
            backup_dir = os.path.join(BACKUP_MEMORY_DIR, self.agent_type)
            backup_path = os.path.join(backup_dir, f"{self.agent_type}.json.bak")
            try:
                with open(backup_path, "w", encoding="utf-8") as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"[Error] 无法保存备份 memory 文件 {backup_path}: {e}")

        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Error] 无法保存 memory 文件 {self.file_path}: {e}")

    def summary(self, history_list: list) -> str:
        return ""
    
    # 截断历史记录，只保留最近的 N 次 OC 计算工具调用及其之后的对话
    def trim(self, history_list: list, max_oc_comp_count: int) -> list:
        return []

    def clear(self) -> None:
        """删除对应的历史文件"""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)