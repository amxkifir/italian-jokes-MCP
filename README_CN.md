# 意大利笑话 MCP 🇮🇹

一个模型上下文协议（MCP）服务器，为您的AI对话带来意大利式幽默！基于FastMCP框架构建，完全兼容SSE、Studio和Streamable HTTP协议。

## 功能特性

- 🎭 **多种笑话类别**：单行笑话、观察类笑话、刻板印象笑话、文字游戏笑话和长篇笑话
- 🚀 **FastMCP框架**：基于最新的FastMCP 2.0构建，性能优异
- 📡 **多协议支持**：支持stdio、HTTP、SSE和WebSocket连接
- 📦 **MCPB兼容**：打包为MCP Bundle，便于安装
- 🔄 **流式支持**：通过SSE和WebSocket实时推送笑话
- 🎯 **Studio集成**：完全兼容MCP Studio和Claude桌面应用

## 安装

### 作为MCPB Bundle（推荐）

1. 下载`.mcpb`文件
2. 使用Claude for macOS/Windows或任何MCPB兼容应用打开
3. 按照安装提示操作

### 手动安装

```bash
# 克隆或下载项目
cd italian-jokes-mcp

# 安装Python依赖
pip install -r requirements.txt

# 运行MCP服务器
python server.py

# 或运行HTTP服务器
python http_server.py
```

## 使用方法

### MCP工具

服务器提供多个工具来获取意大利笑话：

#### `get_italian_joke`
获取随机的意大利笑话，可选择类别筛选。

```python
# 获取任意笑话
get_italian_joke()

# 获取特定类型笑话
get_italian_joke(subtype="One-liner")
```

#### `get_multiple_jokes`
一次性获取多个笑话（1-10个）。

```python
get_multiple_jokes(count=5, subtype="Wordplay")
```

#### `list_joke_categories`
列出所有可用的笑话类别。

#### `health_check`
检查服务器和API连接状态。

### HTTP端点

运行HTTP服务器时（`python http_server.py`）：

- `GET /api/joke` - 获取单个笑话
- `GET /api/jokes` - 获取多个笑话
- `GET /api/categories` - 列出类别
- `GET /api/stream/jokes` - SSE笑话流
- `GET /api/stream/chunked` - 分块传输编码
- `WebSocket /ws/jokes` - 实时笑话推送

### 可用笑话类别

- **All**：所有类别的随机笑话
- **One-liner**：简短有力的单行笑话
- **Observational**：文化观察类幽默
- **Stereotype**：有趣的刻板印象笑话
- **Wordplay**：双关语和文字游戏笑话
- **Long**：长篇叙事笑话

## API响应格式

```json
{
  "success": true,
  "joke": {
    "id": 1,
    "text": "为什么意大利厨师拒绝做披萨？他需要一些空间！",
    "type": "Italian",
    "subtype": "Wordplay"
  }
}
```

## 配置

服务器可以通过环境变量或manifest配置：

- `API_TIMEOUT`：API请求超时时间（默认：10秒）
- `DEFAULT_JOKE_COUNT`：默认笑话数量（默认：3个）
- `HTTP_PORT`：HTTP服务器端口（默认：8000）
- `ENABLE_LOGGING`：启用详细日志记录（默认：true）

## 开发

### 项目结构

```
italian-jokes-mcp/
├── server.py              # 主MCP服务器
├── http_server.py         # HTTP/SSE/WebSocket服务器
├── manifest.json          # MCPB清单文件
├── requirements.txt       # Python依赖
├── package.json          # 项目元数据
├── README.md             # 英文说明文件
├── README_CN.md          # 中文说明文件
└── LICENSE               # MIT许可证
```

### 运行测试

```bash
python -m pytest tests/
```

### 代码质量

```bash
# 格式化代码
black *.py

# 代码检查
flake8 *.py
```

## 兼容性

- **MCP协议**：>=1.0.0
- **Python**：>=3.8
- **FastMCP**：>=2.0.0
- **平台**：Windows、macOS、Linux
- **Claude**：>=3.0.0

## 贡献

1. Fork 仓库
2. 创建功能分支
3. 进行修改
4. 添加测试（如适用）
5. 提交拉取请求

## 许可证

MIT许可证 - 详见LICENSE文件。

## 致谢

- [Italian Jokes API](https://italian-jokes.vercel.app/) 提供笑话内容
- [FastMCP](https://github.com/jlowin/fastmcp) 提供优秀的MCP框架
- [Anthropic](https://github.com/anthropics/mcpb) 提供MCPB规范

---

*Viva la risata!（笑口常开！）* 🇮🇹