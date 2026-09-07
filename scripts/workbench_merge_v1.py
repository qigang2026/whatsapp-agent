#!/usr/bin/env python3
"""
批次 6 步骤 1：把 AI 跟进概要-PC.html 的内容整合到 WhatsApp-Agent-PC.html
- 保留工作台现有的侧栏 + topbar + 5 Tab 切换条
- 替换 <div class="scroll"> ... </div> 内部全部内容
  - 删除原 5 KPI + 4 模块卡片网格 + 信息行
  - 插入：Hero + 时间筛选 + 4 KPI + 生命周期 + 趋势/漏斗 + SLA/车型 + 异常表 + 底部信息
"""

import re
from pathlib import Path

ROOT = Path('/Users/qigangye/Mstar/WhatsApp Agent')
TARGET = ROOT / 'WhatsApp-Agent-PC.html'

html = TARGET.read_text(encoding='utf-8')

# 标记位：从 <div class="scroll"> 开始；到 <div class="info-row"> 的 </div></div></div></div> 结束
# 更稳妥：从 <div class="scroll"> 起到 "</div>\n  </div>\n</div>\n\n<script>" 之前的所有内容（结尾的 </div></div></div> 是 info-row + scroll + main + layout 的关闭）
# 实际结构：scroll > [hero, kpi-strip, workspace-grid, info-row] > /scroll > /main > /layout > script
# 我们要替换：scroll 的内部（保留 scroll 标签本身）

# 用 regex 匹配 <div class="scroll"> 开始的所有内容，到 </div> 关闭 scroll 之前
# scroll 内最后是 </div> 关闭 info-row 后的 </div> 关闭 scroll

# 简单做法：用明确的起始标记 + 结束标记
# 起始：<!-- Hero -->  （在 WhatsApp-Agent-PC.html 中首次出现）
# 结束： </div>\n  </div>\n</div>\n\n<script>  （关闭 layout 标签前）
start_marker = '      <!-- Hero -->'
end_marker = '</div>\n  </div>\n</div>\n\n<script>'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)
if start_idx == -1 or end_idx == -1:
    print(f"未找到标记：start={start_idx}, end={end_idx}")
    raise SystemExit(1)

# 把这一整段（从 start_marker 到 end_marker）替换为新内容
new_content = """      <!-- ========== Hero ========== -->
      <div class="hero hero-compact">
        <h1>
          <span class="wa-mark">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
          </span>
          工作台 · 今日总览
        </h1>
        <p>WhatsApp 端 AI 主动跟进 + 销售接管的全流程入口。AI 推进 4 步主路径，转人工为特殊出口；销售用 CAVi 实时查资料回客户。</p>
      </div>

      <!-- ========== 时间筛选 ========== -->
      <div class="time-filter">
        <button>今天</button>
        <button class="active">最近 7 天</button>
        <button>最近 30 天</button>
        <button>本季度</button>
      </div>

      <!-- ========== KPI 卡片行 ========== -->
      <div class="kpi-row">
        <a class="kpi-card kpi-danger" href="统一客服收件箱-PC.html?tab=handoff">
          <div class="kpi-label">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F56C6C" stroke-width="2.5"><circle cx="12" cy="12" r="9"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>
            <span>待销售接管</span>
          </div>
          <div class="kpi-value text-danger">18</div>
          <div class="kpi-foot">
            <span class="delta-down">↑ 3 较昨日</span>
            <span>SLA 平均剩 4 分 12 秒</span>
          </div>
        </a>

        <a class="kpi-card kpi-primary" href="统一客服收件箱-PC.html?tab=ai">
          <div class="kpi-label">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#419EFE" stroke-width="2"><rect x="4" y="8" width="16" height="12" rx="2"/><circle cx="9" cy="14" r="1.5"/><circle cx="15" cy="14" r="1.5"/><path d="M12 4v4"/><circle cx="12" cy="3" r="1"/></svg>
            <span>AI 接管中</span>
          </div>
          <div class="kpi-value text-primary">47</div>
          <div class="kpi-foot">
            <span class="delta-up">+ 8 较昨日</span>
            <span>自动跟进，无需干预</span>
          </div>
        </a>

        <a class="kpi-card kpi-success" href="收件箱-销售跟进中-PC.html">
          <div class="kpi-label">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#67C23A" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
            <span>销售接管</span>
          </div>
          <div class="kpi-value text-success">32</div>
          <div class="kpi-foot">
            <span class="delta-up">+ 5 较昨日</span>
            <span>人工跟进中</span>
          </div>
        </a>

        <a class="kpi-card kpi-warning" href="统一客服收件箱-PC.html?tab=ai">
          <div class="kpi-label">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#E6A23C" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <span>已超时</span>
          </div>
          <div class="kpi-value text-warning">6</div>
          <div class="kpi-foot">
            <span class="delta-down">↑ 2 较昨日</span>
            <span>超过 1h 未响应</span>
          </div>
        </a>
      </div>

      <!-- ========== 线索生命周期分布 ========== -->
      <div class="card" style="margin-bottom: 16px;">
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 8px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M7 16l4-4 4 4 5-5"/></svg>
            <span style="font-weight: 600; font-size: 15px;">线索生命周期分布</span>
          </div>
        </div>
        <div class="card-body" style="padding-top: 8px;">
          <div class="life-dist" id="lifeDist">
            <div class="life-row"><span class="life-label">首次跟进</span><div class="life-bar-track"><div class="life-bar" style="width:72%;background:#419EFE;"></div></div><span class="life-val">18</span></div>
            <div class="life-row"><span class="life-label">用户孵化</span><div class="life-bar-track"><div class="life-bar" style="width:56%;background:#E6A23C;"></div></div><span class="life-val">14</span></div>
            <div class="life-row"><span class="life-label">预审收集</span><div class="life-bar-track"><div class="life-bar" style="width:48%;background:#7C4DFF;"></div></div><span class="life-val">12</span></div>
            <div class="life-row"><span class="life-label">待销售接管</span><div class="life-bar-track"><div class="life-bar" style="width:40%;background:#F56C6C;"></div></div><span class="life-val">10</span></div>
            <div class="life-row"><span class="life-label">销售跟进</span><div class="life-bar-track"><div class="life-bar" style="width:64%;background:#67C23A;"></div></div><span class="life-val">16</span></div>
            <div class="life-row"><span class="life-label">暂缓 / 再激活</span><div class="life-bar-track"><div class="life-bar" style="width:20%;background:#909399;"></div></div><span class="life-val">5</span></div>
            <div class="life-row"><span class="life-label">战败 / 失活</span><div class="life-bar-track"><div class="life-bar" style="width:28%;background:#C0C4CC;"></div></div><span class="life-val">7</span></div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top: 14px;">
            <span class="stage-chip">窗内自由文本 · 占比 61%</span>
            <span class="stage-chip">窗外 HSM · 占比 27%</span>
            <span class="stage-chip">转人工触发 · 10 次</span>
            <span class="stage-chip">系统拦截 / 不发 · 3 次</span>
          </div>
        </div>
      </div>

      <!-- ========== 第一行图表：趋势折线 + 漏斗 ========== -->
      <div class="charts-row">
        <div class="card">
          <div class="card-header">
            趋势分析 · 近 7 天
            <div class="actions">
              <span class="link-btn">导出数据</span>
              <span style="color: var(--text-placeholder);">·</span>
              <span>AI 接管 / 转人工 / 超时</span>
            </div>
          </div>
          <div class="card-body">
            <div id="chart-trend" class="chart"></div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">转化漏斗</div>
          <div class="card-body">
            <div id="chart-funnel" class="chart"></div>
          </div>
        </div>
      </div>

      <!-- ========== 第二行图表：SLA 环图 + 车型热度 ========== -->
      <div class="charts-row-2">
        <div class="card">
          <div class="card-header">SLA 达标率 · 转人工响应</div>
          <div class="card-body">
            <div id="chart-sla" class="chart-tall"></div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">车型热度 Top 5 · 近 7 天</div>
          <div class="card-body">
            <div id="chart-cars" class="chart-tall"></div>
          </div>
        </div>
      </div>

      <!-- ========== 异常会话表 ========== -->
      <div class="card" style="margin-bottom: 16px;">
        <div class="card-header">
          今日异常会话
          <div class="actions">
            <span style="color: var(--text-secondary);">超时 / 即将超时 / 待人未接 / 流程卡住</span>
            <span style="color: var(--text-placeholder);">·</span>
            <a class="link-btn" href="收件箱-待销售接管-PC.html" style="text-decoration:none;">查看全部 (3)</a>
          </div>
        </div>
        <div class="card-body flush">
          <table class="exception-table">
            <thead>
              <tr>
                <th>客户</th>
                <th>车型</th>
                <th>等待时长</th>
                <th>异常类型</th>
                <th>当前状态</th>
                <th>建议操作</th>
                <th style="text-align: right;">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr onclick="window.location.href='收件箱-待销售接管-PC.html#ana'" style="cursor: pointer;">
                <td>
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 28px; height: 28px; border-radius: 50%; background: var(--danger); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600;">AL</div>
                    Ana Lopez Castillo
                  </div>
                </td>
                <td>Tiguan</td>
                <td><span class="tag tag-danger">8 分钟</span></td>
                <td><span class="tag tag-danger">转人工 SLA 即将超时</span></td>
                <td><span class="tag tag-danger">待销售接管</span></td>
                <td>立即接管 · SLA 工时内 30 分钟将尽</td>
                <td style="text-align: right;"><span class="link-btn">接管 →</span></td>
              </tr>
              <tr onclick="window.location.href='收件箱-待销售接管-PC.html#fernanda'" style="cursor: pointer;">
                <td>
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 28px; height: 28px; border-radius: 50%; background: var(--danger); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600;">FS</div>
                    Fernanda Soto Gil
                  </div>
                </td>
                <td>XPENG G6</td>
                <td><span class="tag tag-danger">26 分钟</span></td>
                <td><span class="tag tag-danger">该人接却无人接 · 预审 8/8</span></td>
                <td><span class="tag tag-danger">待销售接管</span></td>
                <td>客户催促回电 · 立即认领推进</td>
                <td style="text-align: right;"><span class="link-btn">接管 →</span></td>
              </tr>
              <tr onclick="window.location.href='收件箱-待销售接管-PC.html#laura'" style="cursor: pointer;">
                <td>
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 28px; height: 28px; border-radius: 50%; background: var(--warning); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600;">LM</div>
                    Laura Martinez Solis
                  </div>
                </td>
                <td>JAC E10X</td>
                <td><span class="tag tag-warning">1 小时 12 分</span></td>
                <td><span class="tag tag-warning">转人工 SLA 已超时</span></td>
                <td><span class="tag tag-warning">已超时</span></td>
                <td>超时未认领 · 认领安抚或升级主管</td>
                <td style="text-align: right;"><span class="link-btn">处理 →</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ========== 底部说明：产品规则 + 决策依赖 ========== -->
      <div class="info-row">
        <div class="panel">
          <div class="panel-title">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            工作台主路径 · 一句话
            <span class="tag">产品规则</span>
          </div>
          <ul>
            <li><strong>AI 4 步主路径</strong>：① 首次跟进 → ② 收集需求 → ③ 意向识别 → ④ 预审收集；按 SOP 节奏推进。</li>
            <li><strong>转人工是特殊出口</strong>：不按"第 N 步"走；预审通过 / 客户明确要求 / AI 兜不住时触发，进「待销售接管」队列。</li>
            <li><strong>销售接管 SLA</strong>：工作时间内 30 分钟响应；非工作时间顺延到次日工作时间内 30 分钟。</li>
            <li><strong>收入入口仅一个</strong>：ycloud 收发 + Webhook + HSM；任务引擎 / 状态机 / 收件箱 / Handoff 全部 CAVi 自建。</li>
          </ul>
        </div>
        <div class="panel">
          <div class="panel-title">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            待 PM 拍板
          </div>
          <ul>
            <li>跟进策略 Skill 是否允许销售编辑？</li>
            <li>推荐话术是否标注「AI 已审 / 未审」？</li>
            <li>新会话 CAVi 是否需要客户授权？</li>
            <li>四件套移动端是否折叠？</li>
          </ul>
        </div>
      </div>
"""

new_html = html[:start_idx] + new_content + html[end_idx:]

TARGET.write_text(new_html, encoding='utf-8')

print(f"✅ 已替换：起始位置 {start_idx}, 结束位置 {end_idx}, 文件总长 {len(new_html)}")
print(f"原文件长度 {len(html)}, 新文件长度 {len(new_html)}")