import ast
from typing import Any, Dict, List, Optional

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.outputs import LLMResult


def clean_log_of_ids(log_string: str) -> str:
    """
    从日志字符串中提取字典，移除指定的ID字段，然后将处理后的字典
    替换回原始字符串中。
    """
    try:
        start_index = log_string.find('{')
        end_index = log_string.rfind('}') + 1

        if start_index == -1 or end_index == 0:
            return log_string

        dict_str = log_string[start_index:end_index]
        dict_obj = ast.literal_eval(dict_str)
        dict_obj.pop("session_id", None)
        dict_obj.pop("run_id", None)

        cleaned_dict_str = str(dict_obj)
        return log_string.replace(dict_str, cleaned_dict_str)

    except (ValueError, SyntaxError):
        return log_string


class SyncCallbackHandler(BaseCallbackHandler):
    """同步回调处理器"""

    def __init__(self):
        self.logs: List[str] = []
        self.final_output: Optional[str] = None

    def _log(self, text: str) -> None:
        self.logs.append(text)
        print(text)

    # ===== Chain =====

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        run_id: str,
        parent_run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        # 只在根 Runnable 打印一次
        if parent_run_id is None:
            user_input = inputs.get("input")
            if isinstance(user_input, str):
                self._log(f"\n🚀 **开始处理**: {user_input}")

    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        run_id: str,
        parent_run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        # 只在根 Runnable 打印一次
        if parent_run_id is None:
            self._log("\n🏁 **处理完成**")

    # ===== LLM =====

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        run_id: str,
        parent_run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self._log("\n🤖 **LLM开始生成响应...**")

    def on_llm_new_token(
        self,
        token: str,
        run_id: str,
        parent_run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        pass

    def on_llm_end(
        self,
        response: LLMResult,
        run_id: str,
        parent_run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        for generation_list in response.generations:
            need_content = ""
            for generation in generation_list:
                # 优先从 generation.text 提取（标准 Generation 对象属性）
                if hasattr(generation, 'text') and generation.text:
                    # print(generation.text)
                    need_content = generation.text
                # 兼容性写法：检查 message 属性
                elif hasattr(generation, 'message'):  # type: ignore
                    message = generation.message  # type: ignore
                    if hasattr(message, 'content') and message.content:  # type: ignore
                        need_content = str(message.content)  # type: ignore
        self._log("\n✅ **LLM生成完成**" + need_content)

    # ===== Agent =====

    def on_agent_action(
        self,
        action: AgentAction,
        run_id: str,
        parent_run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        raw_string = action.log
        final_log_string = clean_log_of_ids(raw_string)
        self._log(f"\n🤔 **思考中**: {final_log_string}")

    def on_agent_finish(
        self,
        finish: AgentFinish,
        run_id: str,
        parent_run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        output = finish.return_values.get("output", "")
        self._log(f"\n🎉 **最终结果**: {output}")
        self.final_output = output

    # ===== Tool =====

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        run_id: str,
        parent_run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        tool_name = serialized.get("name", "未知工具")
        final_input_str = clean_log_of_ids(input_str)
        self._log(
            f"\n🛠️ **开始调用工具**: `{tool_name}`\n📥 输入参数: `{final_input_str}`"
        )

    def on_tool_end(
        self,
        output: str,
        run_id: str,
        parent_run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        output_str = output.content if hasattr(output, 'content') else str(output)
        self._log("\n✅ **工具执行完成**" + " 输出结果: " + output_str)

    # ===== Utils =====

    def get_logs(self) -> str:
        return "".join(self.logs)