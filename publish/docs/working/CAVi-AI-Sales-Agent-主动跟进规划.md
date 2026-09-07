# CAVi AI Sales Agent · 线索主动跟进规划

> **目标**：基于 **ycloud WA API（基础设施）+ CAVi 自建 Bot + 自建销售工作台 UI** 实现主动跟进。
> **核心边界**：ycloud 提供 WA 收发底层，**CAVi 自己做 Bot、AI Agent、Inbox UI、Assignment、Analytics**。
> **当前阶段**：规划（不做后端实现）—— 给 PM / 业务方 / 开发看的产品方案
> **触发点**：刚在「跟进线索 · 线索详情」面板加了「CAVi跟进」按钮（线索详情-PC.html）
> **参考文档**：
> - [ycloud n8n 集成示例：AI 自动回复](https://helpdocs.ycloud.com/help-center/zh/developer/n8n_integration/shi-li-1ai-zi-dong-hui-fu)
> - [ycloud AI 知识库](https://helpdocs.ycloud.com/help-center/zh/chatbot/ai-knowledge-base)
> - [ycloud Chatbot 是什么](https://helpdocs.ycloud.com/help-center/zh/chatbot/shen-me-shi-chatbot)
> - [CAVI 端到端业务全景 v1.0](../knowledge/CAVI-端到端业务全景.md)
> - [WhatsApp AI Agent 用户跟进规则](../销售agent/docs/decisions/用户跟进规则.md)

---

## 一、能力分工（最重要的边界）

### 1.1 ycloud 提供 vs CAVi 自建

| 能力 | ycloud 能否提供 | 是否需要自己做 |
|------|----------------|---------------|
| 收到 WhatsApp 消息 | ✅ Webhook | CAVi 接收 |
| 发送 WhatsApp 消息 | ✅ API | CAVi UI + 调 API |
| 消息状态（已送达 / 已读）| ✅ Webhook | CAVi 存储 |
| 图片/视频/文件 | ✅ | CAVi UI 展示 |
| 联系人 | ✅ Contact API | 可同步到 CAVi |
| Contact Tags | ✅ | 可同步 / 自己维护 |
| WhatsApp Template（HSM）| ✅ | CAVi UI 管理 |
| WhatsApp Flow | ✅ | CAVi UI 管理 |
| 24h 会话规则 | ✅ ycloud/Meta 底层 | CAVi 展示给销售看 |
| **Bot（聊天机器人逻辑）** | ✅ ycloud 有 | **我们自己用 CAVi 做** |
| **AI Agent（智能决策）** | ✅ ycloud 有 | **我们自己用 CAVi 做** |
| **Inbox UI（会话界面）** | ✅ ycloud 有 | **我们自己建** |
| **Human Agent（销售工作台）** | ✅ ycloud Inbox 有 | **我们自己建** |
| **Conversation Assignment（会话分配）** | ✅ ycloud Inbox 有 | **建议自己做** |
| **Team Inbox（团队收件箱）** | ✅ ycloud Inbox 有 | **建议自己做** |
| **Agent Handoff（人机交接）** | ✅ ycloud Inbox 有 | **建议自己做** |
| **Analytics（跟进数据）** | ✅ ycloud 有 | **建议自己做 CAVi Analytics** |

### 1.2 关键结论

| 层 | 提供方 | 关键产品 |
|----|-------|---------|
| **L4 · WA 底层协议** | ycloud | WA Business API / Webhook / Template / Flow |
| **L3 · Bot 逻辑 + AI** | **CAVi 自建** | 4 数据源 + cavi-guide-gen + 业务规则引擎 |
| **L2 · 销售工作台 UI** | **CAVi 自建** | Inbox / Team Inbox / Assignment / Handoff |
| **L1 · 业务数据** | **CAVi 自建** | CRM / Analytics / 跟进记录 |

**核心原则**：
- 🚫 **不依赖 ycloud 的 Inbox** —— 销售工作台完全 CAVi 自建
- 🚫 **不依赖 ycloud 的 Bot 能力** —— AI 决策用 cavi-guide-gen + 自建业务规则
- ✅ **只复用 ycloud 的 WA 底层**（Webhook 收发 + HSM + Flow 元数据）
- ✅ **CAVi 自己做销售工作台的所有 UI**

---

## 二、整体架构（4 层 + 边界清晰）

```
┌────────────────────────────────────────────────────────────────┐
│ Layer 4 · CAVi 销售工作台 UI（完全自建 · 不依赖 ycloud Inbox）       │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│ │ Inbox    │ │ Team     │ │Assign-   │ │Analytics │             │
│ │ 单会话视图 │ │ Inbox   │ │ment 分配  │ │跟进数据   │             │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
├────────────────────────────────────────────────────────────────┤
│ Layer 3 · CAVi Bot + AI Agent（自建 · 业务逻辑）                   │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│ │触发器     │ │AI 对话    │ │标签化     │ │Handoff  │             │
│ │·CRM 状态  │ │·cavi-    │ │·intention │ │·人机交接 │             │
│ │·24h 沉默  │ │ guide-   │ │·use_case │ │·转销售   │             │
│ │·已读未回  │ │ gen      │ │·budget   │ │·升级主管 │             │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
├────────────────────────────────────────────────────────────────┤
│ Layer 2 · ycloud WA 底层 API（只复用这层）                         │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│ │Webhook   │ │Send API  │ │HSM       │ │Flow      │             │
│ │inbound   │ │text/img  │ │Template  │ │元数据     │             │
│ │message   │ │file/pdf  │ │管理       │ │          │             │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
├────────────────────────────────────────────────────────────────┤
│ Layer 1 · CAVi CRM + 数据源                                       │
│ · 线索系统 · 客户画像 · 4 数据源 · 跟进记录                        │
└────────────────────────────────────────────────────────────────┘
```

---

## 三、CAVi 自建的产品清单（核心结论）

### 3.1 必须自建的产品（按优先级）

| # | 产品 | 复杂度 | MVP 阶段 |
|---|------|--------|---------|
| 1 | **线索详情 + CAVi跟进按钮** | 低 | ✅ 已做（MVP-2 入口） |
| 2 | **CAVi跟进 Modal**（3 条 AI 建议）| 中 | MVP-2（本月）|
| 3 | **Inbox 单会话视图**（销售 1v1 聊天）| 高 | MVP-3（M2）|
| 4 | **Team Inbox**（团队会话池）| 高 | MVP-3（M2）|
| 5 | **Assignment 分配规则** | 中 | MVP-3（M3）|
| 6 | **Agent Handoff**（AI→人 / 人→AI）| 高 | MVP-3（M3）|
| 7 | **Analytics 看板** | 中 | MVP-3（M4）|

### 3.2 不自建的部分

- ❌ ycloud Inbox UI（直接用 WA 收消息 webhook，自己画界面）
- ❌ ycloud Bot 编排（自己用 cavi-guide-gen + n8n 编排业务规则）
- ❌ ycloud AI Agent（自己用 CAVi 的 LLM 能力 + 知识库）

---

## 四、MVP-3 场景 1：首联过滤 + 需求明确（业务目标同 v0.3）

> **来了一条新线索 → ycloud 发 HSM 模版 → CAVi Bot 接客户回复 → 对话目标分层 → 资料齐 → 转销售**

### 4.1 对话目标分层（业务目标）

| 阶段 | 对话目标 | AI 任务 | 标签 |
|------|---------|---------|------|
| **1. 过滤** | 区分意向高低 | 引导说出基本需求 | `intention_high/low` |
| **2. 明确需求** | 弄清用车场景 + 预算 | 追问用车人数 / 预算 | `use_case` `budget` |
| **3. 贷款资料** | 资料收集（满足条件才进）| 引导上传 INE / 流水 | `loan_ready` |
| **4. 转人工** | 资料齐 + 需求明确 → 销售 | Handoff 到 Team Inbox | `handoff_to_sales` |

### 4.2 CAVi Bot 与 ycloud 的对接路径

```
CRM 状态变更
   ↓ (webhook)
CAVi Bot 触发器（自建）
   ↓
判断 status == "new" → 调 ycloud Send API 发 HSM 模版
   ↓
ycloud 把模版发给客户 WhatsApp
   ↓
客户回复 → ycloud inbound webhook → CAVi 接收
   ↓
CAVi AI 对话引擎（cavi-guide-gen + 知识库）
   ↓
处理客户消息 → 调 ycloud Send API 回复
   ↓
CAVi 写入 tags + variables + 状态
   ↓
若触发 Handoff 条件 → CAVi Team Inbox 通知销售
```

**关键**：CAVi Bot **不调用 ycloud 的 Bot 编排**，而是用 cavi-guide-gen + n8n 自己编排业务规则，ycloud 只负责"收发 WA 消息"。

---

## 五、CAVi 自建工作台的产品设计

### 5.1 Inbox 单会话视图（MVP-3 M2）

**位置**：销售工作台新增顶级菜单「Inbox」

**布局**：

```
┌─────────────────────────────────────────────────────────────┐
│ 顶部：会话状态条（lead_id / 客户名 / 当前状态 / SLA 倒计时）     │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│  AI 对话摘要  │          WA 消息流（左客户 / 右销售或 AI）     │
│  （自动生成）  │                                              │
│              │  · 客户消息（含图片/文件预览）                  │
│  标签云       │  · AI 回复（蓝色徽章）                        │
│  intention   │  · 销售回复（绿色徽章）                        │
│  use_case    │  · 系统消息（灰色）                           │
│  budget      │                                              │
│  loan_ready  │                                              │
│              │                                              │
│  客户档案     ├──────────────────────────────────────────────┤
│  姓名/电话    │  输入框（支持文本 / 图片 / 文件 / 模版）        │
│  车型/来源   │  [选 HSM 模版 ▼]  [选 AI 接管 / 销售接管]      │
│              │  [发送]                                        │
└──────────────┴──────────────────────────────────────────────┘
```

**核心交互**：
- ✅ 销售可一键**接管 AI 对话**（点"销售接管"按钮 → Bot 暂停）
- ✅ 销售可一键**交还 AI**（点"AI 接管"按钮 → Bot 继续）
- ✅ 显示 24h 服务窗口状态（绿色 = 窗口内 / 红色 = 已超时）
- ✅ 显示 AI 自动生成的对话摘要 + 标签
- ✅ 支持发 HSM 模版（点"选 HSM 模版"下拉）

### 5.2 Team Inbox（MVP-3 M2）

**位置**：销售工作台「Inbox」下子菜单

**布局**：

```
┌──────────────────────────────────────────────────────────────┐
│ 筛选：状态 / 销售 / AI / 标签 / SLA 超时                       │
├──────────────────────────────────────────────────────────────┤
│ 会话列表：                                                    │
│ ┌──────────┬──────────┬─────────┬────────┬────────┬─────────┐ │
│ │ 客户      │ 状态     │ 负责人  │ SLA    │ 标签    │ 操作    │ │
│ ├──────────┼──────────┼─────────┼────────┼────────┼─────────┤ │
│ │ Jose     │ AI 跟进  │ Bot     │ 30min  │高意向  │ 接管   │ │
│ │ Maria    │ 销售跟   │ Lisa    │ 5min   │待资料  │ 查看   │ │
│ │ Pedro    │ 已转人工 │ Lisa    │ 已超时 │战败    │ 关闭   │ │
│ │ ...                                                       │ │
│ └──────────┴──────────┴─────────┴────────┴────────┴─────────┘ │
│ 分页：1 2 3 ...                                              │
└──────────────────────────────────────────────────────────────┘
```

### 5.3 Assignment 分配规则（MVP-3 M3）

| 规则 | 说明 |
|------|------|
| **新线索自动分配** | 按销售负载均衡分配（最闲的销售） |
| **AI 转人工** | 按地区 + 车系偏好分配 |
| **超时升级** | 销售 5min 未响应 → 升级到主管 |
| **手动改派** | 销售主管可手动改派 |

### 5.4 Handoff（人机交接 · MVP-3 M3）

| 触发条件 | CAVi 动作 |
|---------|CAVi 动作|
| 客户说"quiero hablar con alguien" | AI 自动暂停 + 通知销售 |
| AI 置信度 < 0.7 | 暂停 + 标记"AI 不确定" + 通知销售 |
| 资料齐 + 需求明确 | 暂停 + 推送客户档案到销售工作台 |
| 销售点"接管" | AI 暂停（销售完全接管） |
| 销售点"交还 AI" | AI 继续（销售回到后台） |

### 5.5 Analytics（MVP-3 M4）

| 指标 | 来源 |
|------|------|
| AI 首联率（≤30min）| CRM + Inbox |
| AI→人 转人工率 | Handoff 事件 |
| 平均处理时长 | ycloud 消息状态 webhook |
| 标签分布（intention / use_case）| CAVi tags |
| 销售响应 SLA | CRM 时间戳 |
| 客户满意度 | ycloud 收到的客户回评 |

---

## 六、入口 → 交付 → 闭环（产品方法论 · 修正）

| 场景 | 入口 | 交付 | 闭环 |
|------|------|------|------|
| **新线索首联** | CRM `lead.created` | ycloud HSM 模版 | 客户回 → CAVi Inbox / 不回 → HSM 激活 |
| **AI 对话中** | ycloud inbound webhook | CAVi AI 自由对话 | 需求明确 → Handoff / 需求低 → 归档 |
| **资料收集** | CAVi Bot 状态变更 | AI 引导上传 | 资料齐 → Handoff / 缺料 → 提醒 |
| **Handoff 转人工** | 触发条件命中 | CAVi Team Inbox 通知销售 | 销售 Inbox 接 → 1v1 跟进 → 成交 |
| **销售接管 AI** | 销售在 Inbox 点"接管" | AI 暂停，销售接手 | 销售关单 → 通知 CRM 更新 |
| **AI 接管回退** | 销售点"交还 AI" | AI 继续对话 | — |

---

## 七、落地路径（3 个 MVP · 修正）

### MVP-1 · 被动应答 ✅ 已部分实现

| 范围 | 状态 |
|------|------|
| **入口** | autocava.com.mx CAVi 浮窗 |
| **交付** | cavi-guide-gen 答客户问 |
| **闭环** | 答不出 → 转销售 |

### MVP-2 · CAVi 跟进建议（销售选用）⭐ 本月做

| 范围 | 说明 |
|------|------|
| **入口** | 销售工作台「线索详情」**CAVi跟进按钮** |
| **交付** | 3 条 AI 跟进建议（话术 / 时机 / 切入角度）|
| **闭环** | 销售选用 → 生成 WA 草稿 → 销售手动发 |
| **依赖** | cavi-guide-gen + 4 数据源 + WA 对话历史 |

**Modal 设计**：
- 600×500 居中弹窗
- 上半部：客户对话上下文（最近 10 条）
- 中部：3 张 AI 建议卡片
- 每张卡：采用 / 改写 / 忽略
- 下半部：发送方式选择

### MVP-3 · ycloud WA API + CAVi 自建工作台（季度做）⭐ 本规划重点

| 子阶段 | 时间 | 范围 | 自建 vs 复用 |
|--------|------|------|-------------|
| **3a** | M1 | 场景 1：首联过滤 + 需求明确（HSM 4 条 + CAVi Bot 1 个）| 复用 ycloud WA API |
| **3b** | M1 | **CAVi Inbox 单会话视图** | **CAVi 自建** |
| **3c** | M2 | 场景 2：24h 沉默激活 + HSM 1 条 | 复用 ycloud WA API |
| **3d** | M2 | **CAVi Team Inbox** | **CAVi 自建** |
| **3e** | M3 | 场景 3：已读未回破冰 + 资料收集 | 复用 ycloud WA API |
| **3f** | M3 | **CAVi Assignment + Handoff** | **CAVi 自建** |
| **3g** | M4 | **CAVi Analytics** | **CAVi 自建** |

---

## 八、PM 拍板 4 件事

### 1. MVP-3a 优先做哪个对话分支？

- **A**：只做"首联过滤 + 需求明确"（推荐，4 周）
- **B**：做完首联 + 资料收集（8 周）
- **C**：全流程一次做（12 周）

### 2. CAVi 自建工作台的 UI 优先级

- **A**：先 Inbox 单会话（MVP-3b），再做 Team Inbox（MVP-3d）（推荐）
- **B**：先 Team Inbox（MVP-3d），后 Inbox 单会话（MVP-3b）
- **C**：两个一起做（资源风险大）

### 3. AI 主动发的时间窗

- **A**：工作日 9:00-21:00 + 周末 10:00-18:00（推荐）
- **B**：全天 24h

### 4. AI 转人工触发条件（优先级组合）

- **A**：客户明确说（必须）+ AI 置信度 < 0.7（兜底）+ 资料齐且需求明确（推荐）
- **B**：仅客户明确说 + 资料齐（最保守）

---

## 九、与 v1.2 端到端业务的衔接

| v1.2 阶段 | 现有能力 | 本规划新增 |
|-----------|---------|-----------|
| 阶段 2 报告生成 | cavi-guide-gen | — |
| 阶段 3 报告呈现 | 段 08 cavi_ai | — |
| **阶段 5 销售跟进** | 销售手动 1v1 WA | **CAVi AI Sales Agent + 自建工作台** |
| 节点 ⑥ 短期留资 | WA 跳转 + 销售响应 | AI 30min 首联（自动）|
| 节点 ⑦ 试驾预约 | 选车型 + 经销商 + 时段 | AI 跟进沉默（自动）|
| 节点 ⑧ 跟进 | 销售工作台 + 状态机 | **CAVi Inbox + Team Inbox + Handoff + Analytics** |

---

## 十、关键边界（不要混淆）

| 项 | 用 ycloud 吗？ | 用 CAVi 自建吗？ |
|----|---------------|----------------|
| WA 收发 | ✅ | — |
| HSM 模版管理 | ✅ | UI 自建 |
| Contact 联系人 | ✅ | 同步到 CAVi |
| 24h 会话规则 | ✅ Meta 底层 | UI 展示自建 |
| Bot 对话逻辑 | — | **CAVi 自建（cavi-guide-gen + 业务规则）**|
| AI Agent 决策 | — | **CAVi 自建（LLM + 知识库）**|
| Inbox UI | — | **CAVi 自建** |
| Team Inbox | — | **CAVi 自建** |
| Assignment | — | **CAVi 自建** |
| Handoff | — | **CAVi 自建** |
| Analytics | — | **CAVi 自建** |

**一句话总结**：ycloud 只做 WA 收发管道；Bot、AI、Inbox、Assignment、Handoff、Analytics 全 CAVi 自己建。

---

## 十一、关联文件

| 文件 | 用途 |
|------|------|
| `线索详情-PC.html` | 当前页面（侧栏 + 详情面板 + CAVi跟进按钮） |
| `销售收到客户从WhatsApp询问车辆解读报告.html` | MVP-1 已有原型 |
| `报告生成工作台-PC.html` | 销售工作台已有原型 |
| `../knowledge/CAVI-端到端业务全景.md` | v1.2 全景（能力基础）|
| `../knowledge/whatsapp-agent-技术方案.md` | WA Business API 技术方案 |
| `../销售agent/docs/decisions/用户跟进规则.md` | Meta WA 规则（24h / HSM）|
| `../车辆解读报告/docs/产品功能流程-v1.2.md` | v1.2 PRD 原文 |

---

**版本**：v0.4（基于 ycloud vs CAVi 自建边界修正）
**最后更新**：2026-09-01
**作者**：CAVi 产品规划
