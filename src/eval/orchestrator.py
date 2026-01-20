"""
eval.orchestrator 编排器，协调各阶段的执行流程
"""
import asyncio
import tqdm
import json
import os
from src.eval.utils.analysis import batch_analyze, merge_origin_inputs_with_results, get_csv_report
from config import load_config
from src.agents import (
    EvaluatorAgent,
    ProfilerAgent,
    DescriberAgent,
)
class Orchestrator:
    def __init__(self, data_loader):
        self.data_loader = data_loader

    async def profile(self, query: str = "请分析这个智能体的设计目的和使用的工具。"):
        """
        对待测智能体进行分析。
        Args:
            query: 用于分析智能体的查询字符串。
        Returns:
            包含分析信息的markdown文本。
        """
        profiler = ProfilerAgent()
        config_ini = load_config()
        extras_profile_config = config_ini.get("agent_api_extras", "profiler")
        if not extras_profile_config or not os.path.exists(extras_profile_config):
            raise FileNotFoundError(f"agent api 接口额外参数未找到: {extras_profile_config}")
        
        with open(extras_profile_config, "r", encoding="utf-8") as f:
            extras_profile_config = json.load(f)
        return await profiler.ainvoke({"input": query}, agent_api_extras=extras_profile_config)

    async def describes(self):
        """
        对格式化的测试样本进行描述，转述为自然语言。
        Args:
        Returns:
            包含自然语言描述的测试列表。
        """
        test_description = self.data_loader.load_test_data()
        described_samples = []
        # print(test_description)
        for item in tqdm.tqdm(test_description, desc="Describing"):
            describer = DescriberAgent()
            response = await describer.ainvoke({"input": str(item)})
            described_test_sample = response["messages"][-1].content
            described_samples.append(described_test_sample)
        self.data_loader.save_described_data(described_samples)
        return described_samples
    
    async def evaluates(self):
        """
        对自然语言形式的测试样本进行与智能体交互的评估。
        Args:
        Returns:
            包含评估结果的列表。
        """
        test_description = self.data_loader.load_described_data()
        evaluated_results = []
        config_ini = load_config()
        extras_profile_config = config_ini.get("agent_api_extras", "evaluator")
        if not extras_profile_config or not os.path.exists(extras_profile_config):
            raise FileNotFoundError(f"agent api 接口额外参数未找到: {extras_profile_config}")
        
        with open(extras_profile_config, "r", encoding="utf-8") as f:
            extras_profile_config = json.load(f)

        if len(extras_profile_config) != len(test_description):
            raise ValueError("❌ evaluator agent_api_extras 配置数量与测试样本数量不匹配，请检查配置文件内容。")
    
        for item_tuple in tqdm.tqdm(zip(test_description, extras_profile_config), desc="Evaluating"):
            item, extras_config = item_tuple
            evaluator = EvaluatorAgent()
            response = await evaluator.ainvoke({"input": str(item)}, agent_api_extras=extras_config)
            evaluated_result = response["messages"][-1].content
            evaluated_results.append(evaluated_result)
        self.data_loader.save_evaluated_results(evaluated_results)
        return evaluated_results

    async def analyze(self):
        """
        分析评估结果并生成报告。
        Args:
        Returns:
            包含分析报告的CSV字符串。
        """
        evaluated_results = self.data_loader.load_evaluated_results()
        origin_inputs = self.data_loader.load_test_data()

        analyzed_results = await batch_analyze(evaluated_results)
        # print("Analyzed Results:", analyzed_results)
        merged_results = merge_origin_inputs_with_results(origin_inputs, analyzed_results)
        csv_report = get_csv_report(merged_results)
        # print("CSV Report:\n", csv_report)
        self.data_loader.save_analysis_report(csv_report)
        return csv_report
async def main():
    from src.eval.utils.data_loader import DataLoader

    data_loader = DataLoader()
    orchestrator = Orchestrator(data_loader)

    # profile_response = await orchestrator.profile()
    # print(profile_response)
    # described_data = await orchestrator.describes()
    # print(described_data)
    # evaluated_results = await orchestrator.evaluates()
    # print(evaluated_results)
    csv_report = await orchestrator.analyze()
    print(csv_report)
if __name__ == "__main__":
    asyncio.run(main())