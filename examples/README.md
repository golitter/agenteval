# 测试例子
## 内部agent测试
`examples/lab_agent_test`

> 这个评估智能体的思路来源于此，tool-use agent测试一个例子，中间要人为的进行确认、修改等，而且随着提示词或者代码逻辑的修改都要对所有功能进行测试，但是往往只是极个别例子可能会出现问题。人工测试费力不讨好，因此写了一个特化（专用于此agent的agent），之后从项目抛离，形成单独的个人项目。

### 待测试agent的api接口
只有两个：
- 交互
- 健康状态检查

其中`交互`接口里面有几个参数，但是测试中最多只用到了两个参数：`query`-用户的查询语句；`session_id`-会话id。

整个测试工程中的会话id只用一个也可以，但是也想要测试单独的会话情况，所以也进行扩展实现：在进行`proflie`和`evaluate`时选择一个测试例子用一个会话id。

## 麦当劳mcp agent测试

**!!需要先安装`langchain_mcp_adapters`库。**

### 待测试agent的api接口
只有两个：
- 交互
- 健康状态检查

只有交互接口有一个`qurey`参数。

`describer`异常：
```shell
langgraph.errors.GraphRecursionError: Recursion limit of 25 reached without hitting a stop condition. You can increase the limit by setting the `recursion_limit` config key.
```
> 单轮对话存在限制
