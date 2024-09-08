# dify2openai



### 安装说明

1. 确保已安装 Python 3.7+。

2. 创建并激活虚拟环境（可选但推荐）：
```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
```

3. 安装所需依赖：
```bash
pip install -r requirements.txt
```

4. 创建一个 `.env` 文件，并添加您的 Dify API 密钥：
```
DIFY_API_KEY=your_dify_api_key_here
```

### 使用说明

1. 确保 `main.py` 和 `difyapi.py` 文件在同一目录下。

2. 运行 FastAPI 服务器：
```bash
python main.py
```

3. 服务器将在 `http://0.0.0.0:8000` 上运行。

4. 要使用聊天功能，向 `/chat/completions` 端点发送 POST 请求，格式如下：
```json
{
  "messages": [
    {"role": "user", "content": "你好，请介绍一下自己。"}
  ]
}
```

5. 如果需要保持对话上下文，可以在请求头中添加 `X-Task-Id`。

6. 服务器将以 Server-Sent Events (SSE) 格式返回流式响应。

注意：确保您有有效的 Dify API 密钥，并且了解 Dify API 的使用条款和限制。


