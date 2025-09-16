# 意大利笑话 MCP 服务器 🇮🇹

一个模型上下文协议 (MCP) 服务器，通过意大利笑话 API 提供意大利笑话访问。该服务器允许 AI 助手获取和分享各种类型的意大利笑话。

## 功能特性

- 🎭 **多种笑话类型**: 访问不同子类型的笑话，包括单行笑话、观察笑话、刻板印象笑话、文字游戏笑话和长笑话
- 🔄 **随机选择**: 获取随机笑话或指定特定子类型
- 🌐 **API 集成**: 无缝集成意大利笑话 API
- 📝 **丰富格式**: 返回带有适当格式和元数据的笑话
- ⚡ **快速响应**: 优化以实现快速笑话检索

## 可用工具

### `get_italian_joke`
检索一个随机的意大利笑话或特定子类型的笑话。

**参数:**
- `subtype` (可选): 要获取的笑话类型
  - 可用选项: `All`, `One-liner`, `Observational`, `Stereotype`, `Wordplay`, `Long`

### `list_joke_subtypes`
列出所有可用的意大利笑话子类型。

## 安装

1. 克隆或下载此仓库
2. 安装依赖:
   ```bash
   npm install
   ```
3. 构建项目:
   ```bash
   npm run build
   ```

## 使用

### 开发模式
在开发模式下运行服务器:
```bash
npm run dev
```

### 生产模式
构建并运行服务器:
```bash
npm run build
npm start
```

### 与 LLM 助手集成

将此服务器添加到您的 LLM 助手配置中:

```json
{
  "mcpServers": {
    "italian-jokes": {
      "command": "node",
      "args": ["path/to/italian-jokes-mcp-server/dist/index.js"]
    }
  }
}
```
### 数据来源归属

此 MCP 服务器使用由 Daniel Bliss 创建的意大利笑话 API。笑话和 API 结构来源于:

- **API 网站**: [https://italian-jokes.vercel.app/](https://italian-jokes.vercel.app/)
- **源代码仓库**: [https://github.com/d-bliss/italian-jokes-api](https://github.com/d-bliss/italian-jokes-api)

所有笑话和 API 响应均由意大利笑话 API 服务提供。此 MCP 服务器充当桥梁，使这些笑话可以通过模型上下文协议访问。

## 使用示例

一旦与 MCP 兼容的客户端集成:

1. **获取随机笑话**:
   - 使用不带参数的 `get_italian_joke` 工具

2. **获取特定类型的笑话**:
   - 使用带有 `subtype: "One-liner"` 参数的 `get_italian_joke` 工具

3. **列出可用子类型**:
   - 使用 `list_joke_subtypes` 工具

## 错误处理

服务器包含全面的错误处理，包括:
- 网络超时
- API 不可用
- 无效的子类型
- 格式错误的响应

## 贡献

欢迎通过以下方式贡献:
- 添加新功能
- 改进错误处理
- 增强文档
- 报告错误

## 许可证

MIT 许可证 - 欢迎在您自己的项目中使用!

## 致谢

此 MCP 服务器建立在以下优秀工作的基础上:

- **Daniel Bliss** - [意大利笑话 API](https://github.com/d-bliss/italian-jokes-api) 的创建者
- **意大利笑话 API** - 为此 MCP 服务器提供支持的底层笑话服务
- **模型上下文协议** - 实现 AI 助手集成的协议标准

### 第三方服务

- **意大利笑话 API**: [https://italian-jokes.vercel.app/](https://italian-jokes.vercel.app/)
  - 提供所有笑话内容和 API 功能
  - 由 Daniel Bliss 创建和维护
  - 采用 MIT 许可证

此 MCP 服务器充当模型上下文协议和意大利笑话 API 之间的桥梁，使 AI 助手能够以标准化方式访问意大利笑话。

---

*Viva la risata! (笑声长存!)* 🎉