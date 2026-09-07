#!/usr/bin/env python3
"""
批次 5 · v2 补齐线索详情 + 新会话 CAVi 的 Tab bar
"""
import re
from pathlib import Path

ROOT = Path("/Users/qigangye/Mstar")


def make_tabbar(active_key: str) -> str:
    tabs = [
        ("dash",     "WhatsApp-Agent-PC.html", "rect",       "工作台"),
        ("overview", "AI 跟进概要-PC.html",   "chart",      "AI 跟进概要",   "11"),
        ("inbox",    "统一客服收件箱-PC.html", "inbox",     "统一客服收件箱", "2", "danger"),
        ("skill",    "跟进策略-Skill-PC.html", "star",       "跟进策略 Skill"),
        ("cavi",     "知识库(cavi).html",   "chat",       "知识库（CAVi）"),
    ]
    icon_svg = {
        "rect":  '<svg class="t-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>',
        "chart": '<svg class="t-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M7 16l4-4 4 4 5-5"/></svg>',
        "inbox": '<svg class="t-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
        "star":  '<svg class="t-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
        "chat":  '<svg class="t-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    }
    out = ['\n    <!-- ========== 5 Tab 切换条（批次 5 · 统一全页面） ========== -->\n', '    <nav class="wa-tabbar">\n']
    for e in tabs:
        key, href, icon, label = e[0], e[1], e[2], e[3]
        badge = e[4] if len(e) > 4 else None
        badge_cls = e[5] if len(e) > 5 else None
        active_cls = ' active' if key == active_key else ''
        badge_html = ''
        if badge:
            extra = f' {badge_cls}' if badge_cls else ''
            badge_html = f'<span class="t-badge{extra}">{badge}</span>'
        out.append(f'      <a href="{href}" class="wa-tab{active_cls}">\n')
        out.append(f'        {icon_svg[icon]}\n')
        out.append(f'        <span>{label}</span>\n')
        if badge_html:
            out.append(f'        {badge_html}\n')
        out.append('      </a>\n')
    out.append('    </nav>\n')
    return ''.join(out)


PLAN = [
    ("WhatsApp Agent/线索详情-PC.html",
     r'  <section class="main">\n',
     "inbox"),
    ("WhatsApp Agent/知识库(cavi).html",
     r'  <div class="main-area">\n',
     "cavi"),
]


def main():
    print("=== 批次 5 v2 · 补齐 2 个页面 Tab bar ===\n")
    ok = 0
    for rel, anchor, active in PLAN:
        p = ROOT / rel
        src = p.read_text(encoding='utf-8')
        if 'class="wa-tabbar"' in src:
            print(f"  · 已有，跳过: {p.name}")
            continue
        m = re.search(anchor, src)
        if not m:
            print(f"  ✗ 锚点未匹配: {p.name}")
            continue
        new_src = src[:m.end()] + make_tabbar(active) + src[m.end():]
        p.write_text(new_src, encoding='utf-8')
        print(f"  ✓ 注入 tabbar ({active} active): {p.name}")
        ok += 1
    print(f"\n完成: {ok}/{len(PLAN)}")


if __name__ == "__main__":
    main()