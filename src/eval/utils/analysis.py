from src.agents import AnalystAgent
import pandas as pd
import io

CSV_HEADER = [
    "query", "test_result", "score", "reason", "improvement_areas", "confidence", "strengths", "evaluation_time"
]
CSV_DESCRIPTION = [
    "测试语句", "测试结果", "评分", "评分理由", "改进建议", "置信度", "优点", "评测时间"
]

async def batch_analyze(samples):
    analyst = AnalystAgent()
    analyzed_results = []
    for item in samples:
        response = await analyst.ainvoke({"input": str(item)})
        answer = response["messages"]
        analyzed_results.append(answer)
    return analyzed_results

def merge_origin_inputs_with_results(origin_inputs, results):
    merged = []
    for origin, result in zip(origin_inputs, results):
        query = origin.get("query", "")
        result["query"] = query
        merged.append(result)
    
    return merged

def get_csv_report(results_list):
    if not results_list:
        return ""
    
    # 转换为 DataFrame
    df = pd.DataFrame(results_list)
    
    # 处理列表类型字段
    list_columns = ['improvement_areas', 'strengths']
    for col in list_columns:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: '; '.join(str(item) for item in x) 
                if isinstance(x, list) and x 
                else x if pd.notna(x) 
                else ''
            )
    
    # 处理空值
    df = df.fillna('')
    
    # 使用 CSV_HEADER（英文列名）指定列顺序
    df = df.reindex(columns=CSV_HEADER, fill_value='')
    
    # 生成 CSV 字符串（使用中文表头）
    output = io.StringIO()
    df.to_csv(output, index=False, header=CSV_DESCRIPTION, encoding='utf-8')
    
    return output.getvalue()