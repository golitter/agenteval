import configparser
import json
import os
from typing import Any, Dict
from dotenv import load_dotenv
import yaml


def load_config():
    config = configparser.ConfigParser()
    config_file_path = './config.ini'
    if not os.path.exists(config_file_path):
        print(f"错误：配置文件 '{config_file_path}' 不存在！")
        exit()
    config.read(config_file_path, encoding='utf-8')
    return config


def load_prompt_templates() -> dict:
    config = load_config()
    prompt_template_path = config.get('prompts', 'prompt_template')
    if not os.path.exists(prompt_template_path):
        raise FileNotFoundError(f"配置文件未找到: {prompt_template_path}")

    with open(prompt_template_path, 'r', encoding='utf-8') as f:
        # 使用 safe_load 防止执行任意代码，更安全
        prompts = yaml.safe_load(f)
    
    return prompts

class Configuration:
    """读取 .env 与 servers_config.json"""

    def __init__(self) -> None:
        # 从环境变量中加载 API key, base_url 和 model
        load_dotenv()

        self.api_key = os.getenv('DS_API_KEY')
        self.base_url = os.getenv('DS_BASE_URL')
        self.model = os.getenv('DS_MODEL')
        if self.base_url is None or self.model is None or self.api_key is None:
            raise ValueError("❌ 未找到 LLM 配置，请在 .env 文件中配置")

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        """
        从 JSON 文件加载服务器配置
        
        Args:
            file_path: JSON 配置文件路径
        
        Returns:
            包含服务器配置的字典
        """
        with open(file_path, "r") as f:
            return json.load(f)