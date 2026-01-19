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
        
    def _dump_json_file(self, data: Any, file_path: str):
        resolved_path = self._resolve_path(file_path)
        with open(resolved_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

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
    
    def save_described_data(self, described_data: List[Dict[str, Any]]):
        """保存重写后的测试描述数据"""
        describer_output_file = self.config.get('eval', 'describer_output_file')
        output_dir = os.path.dirname(describer_output_file)
        if output_dir:
            resolved_output_dir = self._resolve_path(output_dir)
            os.makedirs(resolved_output_dir, exist_ok=True)

        resolved_path = self._resolve_path(describer_output_file)
        self._dump_json_file(described_data, resolved_path)

    def load_described_data(self) -> List[Dict[str, Any]]:
        """加载重写后的测试描述数据"""
        describer_output_file = self.config.get('eval', 'describer_output_file')
        return self._load_json_file(describer_output_file)
    
    def save_evaluated_results(self, evaluated_results: List[Dict[str, Any]]):
        """保存评估结果数据"""
        evaluator_output_file = self.config.get('eval', 'evaluator_output_file')
        output_dir = os.path.dirname(evaluator_output_file)
        if output_dir:
            resolved_output_dir = self._resolve_path(output_dir)
            os.makedirs(resolved_output_dir, exist_ok=True)

        resolved_path = self._resolve_path(evaluator_output_file)
        self._dump_json_file(evaluated_results, resolved_path)
    
    def load_evaluated_results(self) -> List[Dict[str, Any]]:
        """加载评估结果数据"""
        evaluator_output_file = self.config.get('eval', 'evaluator_output_file')
        return self._load_json_file(evaluator_output_file)

    def save_analysis_report(self, csv_report: str):
        """保存分析报告为 CSV 文件"""
        analysis_report_file = self.config.get('eval', 'analysis_report_file')
        output_dir = os.path.dirname(analysis_report_file)
        if output_dir:
            resolved_output_dir = self._resolve_path(output_dir)
            os.makedirs(resolved_output_dir, exist_ok=True)

        resolved_path = self._resolve_path(analysis_report_file)
        with open(resolved_path, 'w', encoding='utf-8') as f:
            f.write(csv_report)
    
if __name__ == "__main__":
    data_loader = DataLoader()
    all_data = data_loader.load_all()
    print(all_data)

    test_data = data_loader.load_test_data()
    print(test_data)