from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class TestResult(str, Enum):
    """测试是否通过的结果枚举"""
    PASSED = "通过"
    FAILED = "失败"
    PARTIAL = "部分通过"
    UNKNOWN = "未知"


class AnalystAgentResponse(BaseModel):
    """Analyst Agent 的最终固定 JSON 输出格式"""
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 必填字段
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    test_result: TestResult = Field(
        ...,
        description="测试是否通过：通过/失败/部分通过/未知"
    )
    
    score: float = Field(
        ...,
        description="得分（根据具体任务，例如 0-10 分）",
        ge=0,
        le=10
    )
    
    reason: str = Field(
        ...,
        description="得出结论的原因/依据说明"
    )
    
    improvement_areas: List[str] = Field(
        ...,
        description="智能体待改进的部分（支持多条）"
    )
    
    confidence: float = Field(
        ...,
        description="整体评估的置信度 0~1",
        ge=0,
        le=1
    )
    
    strengths: Optional[List[str]] = Field(
        ...,
        description="智能体的优点/做得好的部分"
    )
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 可选字段 - 自行添加的实用字段
    #
    # evaluation_time : 时间戳 datetime.datetime.now().isoformat()
    #
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    