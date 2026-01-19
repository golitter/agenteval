"""数据加载模块"""

import json
import os
from typing import Any, Dict, List

import config


class DataLoader:
    """从 config.ini 加载数据集数据"""

    def __init__(self):
        self.config = config.load_config()

    def _resolve_path(self, path: str) -> str:
        if os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', path))

    def _load_json_file(self, file_path: str) -> Any:
        resolved_path = self._resolve_path(file_path)
        if not os.path.exists(resolved_path):
            raise FileNotFoundError(f"文件未找到: {resolved_path}")
        with open(resolved_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_test_data(self) -> List[Dict[str, Any]]:
        """加载测试数据"""
        test_data_file = self.config.get('test', 'test_data_file')
        return self._load_json_file(test_data_file)

    def load_test_description(self) -> Dict[str, Any]:
        """加载测试描述"""
        test_description_file = self.config.get('test', 'test_description_file')
        return self._load_json_file(test_description_file)

    def load_all(self) -> Dict[str, Any]:
        """加载所有测试数据"""
        return {
            'test_data': self.load_test_data(),
            'test_description': self.load_test_description(),
        }

if __name__ == "__main__":
    data_loader = DataLoader()
    all_data = data_loader.load_all()
    print(all_data)

    test_data = data_loader.load_test_data()
    print(test_data)