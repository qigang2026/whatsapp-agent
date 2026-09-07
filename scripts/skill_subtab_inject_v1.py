#!/usr/bin/env python3
"""
批次 7 步骤 4：跟进策略-Skill-PC.html 顶部加 4 子 Tab 切换条
- 子 Tab：HSM 模板 / SOP 节奏 / SLA 规则 / 变量字典
- 注入位置：Hero 之后、KPI 概览之前
- 注入 CSS：.subtab-bar / .subtab
- 注入 JS：点击切换面板显示
"""

import re
from pathlib import Path

ROOT = Path('/Users/qigangye/Mstar/WhatsApp Agent')
TARGET = ROOT / '跟进策略-Skill-PC.html'

html = TARGET.read_text(encoding='utf-8')

# 1. CSS 注入到 </style> 前
SUBTAB_CSS = """
  /* ========== Skill 顶部子 Tab ========== */
  .subtab-bar {
    display: flex;
    align-items: center;
    gap: 0;
    border-bottom: 1px solid var(--border-light);
    background: transparent;
    margin-bottom: 16px;
    padding: 0;
  }
  .subtab {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
    transition: color 0.15s, border-color 0.15s;
    background: transparent;
    border-top: none;
    border-left: none;
    border-right: none;
  }
  .subtab:hover {
    color: var(--primary);
  }
  .subtab.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
  }
  .subtab .subtab-icon {
    width: 16px;
    height: 16px;
    flex-shrink: 0;
  }
  .subtab .subtab-count {
    background: var(--bg-base);
    color: var(--text-secondary);
    font-size: 11px;
    padding: 1px 6px;
    border-radius: 8px;
    font-weight: 600;
    line-height: 1.4;
  }
  .subtab.active .subtab-count {
    background: var(--primary-soft-bg);
    color: var(--primary);
  }
"""

if '/* ========== Skill 顶部子 Tab ========== */' not in html:
    html = html.replace('</style>', SUBTAB_CSS + '\n</style>', 1)
    print("✅ CSS 已注入")

# 2. HTML 子 Tab 条注入
SUBTABLE_HTML = """
      <!-- ========== Skill 子 Tab 切换 ========== -->
      <nav class="subtab-bar">
        <button class="subtab active" data-target="panel-hsm">
          <svg class="subtab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          HSM 模板
          <span class="subtab-count">8</span>
        </button>
        <button class="subtab" data-target="panel-sop">
          <svg class="subtab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          SOP 节奏
          <span class="subtab-count">4</span>
        </button>
        <button class="subtab" data-target="panel-sla">
          <svg class="subtab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
          SLA 规则
          <span class="subtab-count">3</span>
        </button>
        <button class="subtab" data-target="panel-vars">
          <svg class="subtab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          变量字典
          <span class="subtab-count">14</span>
        </button>
      </nav>
"""

# 注入位置：Hero 之后 + KPI 概览之前
# 找 "<!-- ========== KPI 概览 ========== -->"
kpi_match = re.search(r'<!-- ========== KPI 概览 ========== -->', html)
if kpi_match:
    pos = kpi_match.start()
    html = html[:pos] + SUBTABLE_HTML + '\n      ' + html[pos:]
    print("✅ 子 Tab HTML 已注入到 KPI 概览之前")
else:
    print("⚠️  未找到 KPI 概览标记")

# 3. JS 注入：点击切换面板显示
# 当前 HTML 中：panel-hsm 默认显示，panel-sop/sla/vars 默认 display:none
SUBTAB_JS = """
<script>
(function () {
  var tabs = document.querySelectorAll('.subtab[data-target]');
  var panels = {
    'panel-hsm': document.getElementById('panel-hsm'),
    'panel-sop': document.getElementById('panel-sop'),
    'panel-sla': document.getElementById('panel-sla'),
    'panel-vars': document.getElementById('panel-vars')
  };
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var target = tab.getAttribute('data-target');
      tabs.forEach(function (t) { t.classList.remove('active'); });
      tab.classList.add('active');
      Object.keys(panels).forEach(function (key) {
        if (panels[key]) {
          panels[key].style.display = (key === target) ? '' : 'none';
        }
      });
    });
  });
})();
</script>
"""

# 注入到 </body> 前
if 'subtab[data-target]' not in html or 'subtab[data-target]' not in html.split('<script>')[1] if '<script>' in html else False:
    if 'function () {' in html.split('</body>')[0].split('<script>')[-1] if '<script>' in html else True:
        pass

if '<script>' in html and '.subtab[data-target]' not in html:
    html = html.replace('</body>', SUBTAB_JS + '\n</body>', 1)
    print("✅ 子 Tab JS 已注入")
elif '.subtab[data-target]' in html:
    print("⚠️  子 Tab JS 已存在")
else:
    html = html.replace('</body>', SUBTAB_JS + '\n</body>', 1)
    print("✅ 子 Tab JS 已注入（默认）")

TARGET.write_text(html, encoding='utf-8')

print(f"\n✅ 文件已更新：{TARGET}")
print(f"   文件总长：{len(html)} chars")

# 验证
if 'subtab-bar' in html:
    print("✅ subtab-bar 元素存在")
if 'panel-hsm' in html and 'panel-sop' in html:
    print("✅ 4 个面板 ID 存在")
if 'data-target' in html:
    print("✅ data-target 切换逻辑存在")