
class MockChatClient:
    def __init__(self):
        # 初始化状态计数器
        self.call_count = 0
        # 预定义的返回结果列表
        self.responses = [
            "这是第 1 次回复：Hello!",
            "这是第 2 次回复：World!",
            "这是第 3 次回复：Why?",
            "这是第 4 次回复：Because..."
        ]

    def chat(self, message: str) -> str:
        """
        模拟 chat 接口调用
        """
        
        # 获取当前应该返回的索引
        index = self.call_count % len(self.responses)
        response = self.responses[index]
        
        # 状态更新：计数器 +1
        self.call_count += 1
        
        return response

# --- 测试代码 ---

if __name__ == "__main__":
    # 实例化客户端
    client = MockChatClient()
    # 模拟多次调用
    print("--- 开始调用 ---")
    answer = client.chat("你好")
    print(answer)
    answer = client.chat("在吗")
    print(answer)
    answer = client.chat("干嘛呢")
    print(answer)
    answer = client.chat("再见")
    print(answer)
    answer = client.chat("又来了")
    print(answer)
    print("--- 调用结束 ---")
