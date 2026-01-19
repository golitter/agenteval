"""
eval.orchestrator 编排器，协调各阶段的执行流程
"""
import asyncio
import tqdm

from src.agents import (
    EvaluatorAgent,
    ProfilerAgent,
    DescriberAgent,
)

class Orchestrator:
    def __init__(self, data_loader):
        self.data_loader = data_loader

    async def profile(self, query: str = "请分析这个智能体的设计目的和使用的工具。"):
        profiler = ProfilerAgent()
        return await profiler.ainvoke({"input": query})

    async def describes(self):
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
        test_description = self.data_loader.load_described_data()
        evaluated_results = []
        for item in tqdm.tqdm(test_description, desc="Evaluating"):
            evaluator = EvaluatorAgent()
            response = await evaluator.ainvoke({"input": str(item)})
            evaluated_result = response["messages"][-1].content
            evaluated_results.append(evaluated_result)
        self.data_loader.save_evaluated_results(evaluated_results)
        return evaluated_results

async def main():
    from src.eval.utils.data_loader import DataLoader

    data_loader = DataLoader()
    orchestrator = Orchestrator(data_loader)

    # profile_response = await orchestrator.profile()
    # print(profile_response)
    # described_data = await orchestrator.describes()
    # print(described_data)
    evaluated_results = await orchestrator.evaluates()
    print(evaluated_results)
if __name__ == "__main__":
    asyncio.run(main())