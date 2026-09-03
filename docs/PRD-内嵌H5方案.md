# WhatsApp AI Agent 内嵌H5方案

在 24 小时服务窗口内（场景A），AI Agent 具备发送 H5 链接的完整能力。对于响应机制，行业内主要有两种主流实现方式：

### 发送方式与呈现效果

AI Agent 无法直接在聊天框内“内嵌渲染”一个完整的 HTML5 网页，但可以通过以下方式优雅地呈现给用户：

- **方式一：文字/卡片 \+ 链接预览（最基础）**

- **Agent 直接发送包含 URL 的文本。WhatsApp 会自动提取 H5 的 Open Graph 元数据（标题、封面图、描述），生成一个可点击的商品预览卡片。**

- **方式二：带 URL 的交互式按钮（CTA Button / 推荐）**

- Agent 发送一条带有 **“查看详情”** 或 **“立即申请”** 按钮的交互式消息（Call\-to\-Action）。

- 样式更精美、点击率显著高于纯文字链接。

### 用户点击后的 2 种响应与交互机制

#### 模式 A：跳转外部 H5 页面（第三方完全接管）

用户点击按钮/链接后，手机会调用默认浏览器（如 Safari 或 Chrome）打开Autocava H5 页面。

- **数据如何流转回 WhatsApp AI Agent？**

1. **带参数的动态 URL**：AI Agent 发送链接时，在 URL 尾部带上用户的 WhatsApp ID（如 `[``https://your-site.com/form?phone=52155xxxx&lead_id=123](https://your-site.com/form?phone=52155xxxx&lead_id=123)`）。

1. **第三方提交处理**：用户在 H5 完成表单提交或商品浏览。

1. **Webhook 异步回调（关键）**：Autocava H5 的后端服务器拿到数据后，通过 Webhook 调回你的 AI Agent/WhatsApp 系统。

1. **AI 接续对话**：AI Agent 在 WhatsApp 内部收到通知，主动向用户追加一条消息：“*智利先生，系统已收到您提交的 INE 审核材料，我们将在 15 分钟内为您出具额度！*”

#### 模式 B：使用 WhatsApp Flows 原生表单（体验最好，无需跳转）

Meta 官方提供了名为 **WhatsApp Flows** 的功能，可以将复杂的“表单/商品选择卡片”直接渲染在 WhatsApp 聊天框内部。

- **用户体验**：点击“填写表单”按钮后，页面像弹窗一样在 WhatsApp 内部展开（原生体验，无需打开浏览器） 

- **Autocava响应**：

- 当用户在内嵌 Flow 表单中点“提交”时，数据会直接作为 JSON 格式的 Webhook 传给Autocava API 服务

- Autocava系统处理完（比如完成了简单的车贷初审计算），再将结果返回给 Agent，Agent立即在聊天框内回复用户。

### 业务落地建议

**意图收集**：AI Agent与客户沟通，确定其想购买的车型（如 *Nissan Versa*）。

**发送 H5 / 卡片**：

- AI 发送一个 H5 试算页面链接：“*您可以点击这里选择首付比例，查看专属的月供方案。*”

**第三方页面收集敏感信息**：

- 在 H5 页面上引导客户上传 INE（身份证件）照片或提交月收入，避免客户在 WhatsApp 聊天记录中直接暴露过于敏感的隐私。

**数据回传与 AI 接管**：

- 第三方 H5 验证完毕后，通过 API 唤醒 AI Agent，AI Agent 在 WhatsApp 里接着向客户推“约访预约卡片”或“销售代表接单通知”。

