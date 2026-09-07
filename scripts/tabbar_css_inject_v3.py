#!/usr/bin/env python3
"""
批次 5 v3 · 补齐 7 个子页面缺失的 wa-tabbar CSS
"""
import re
from pathlib import Path

ROOT = Path("/Users/qigangye/Mstar")

CSS_TABBAR = """
  /* ========== WhatsApp Agent Tab 切换条（批次 5 · 全页面统一） ========== */
  .wa-tabbar {
    height: 46px;
    background: #fff;
    border-bottom: 1px solid var(--border-lighter);
    padding: 0 16px;
    display: flex;
    align-items: stretch;
    gap: 4px;
    flex-shrink: 0;
    overflow-x: auto;
  }
  .wa-tabbar::-webkit-scrollbar { height: 2px; }
  .wa-tab {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 0 14px;
    font-size: 13px;
    color: var(--text-secondary);
    text-decoration: none;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
    transition: color 0.15s, border-color 0.15s;
    white-space: nowrap;
  }
  .wa-tab:hover { color: var(--primary); }
  .wa-tab.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
    font-weight: 500;
  }
  .wa-tab .t-icon { width: 14px; height: 14px; flex-shrink: 0; }
  .wa-tab .t-badge {
    background: var(--primary-soft-bg);
    color: var(--primary);
    font-size: 11px;
    padding: 1px 5px;
    border-radius: 8px;
    font-weight: 600;
    line-height: 1.2;
  }
  .wa-tab .t-badge.danger {
    background: var(--danger-soft-bg);
    color: var(--danger);
  }
"""


FILES = [
    "WhatsApp Agent/统一客服收件箱-PC.html",
    "WhatsApp Agent/收件箱-AI跟进中-PC.html",
    "WhatsApp Agent/收件箱-待销售接管-PC.html",
    "WhatsApp Agent/收件箱-销售跟进中-PC.html",
    "WhatsApp Agent/AI 跟进概要-PC.html",
    "WhatsApp Agent/线索详情-PC.html",
    "WhatsApp Agent/知识库(cavi).html",
]


def main():
    print("=== 批次 5 v3 · 补齐 Tab bar CSS ===\n")
    ok = 0
    for rel in FILES:
        p = ROOT / rel
        src = p.read_text(encoding='utf-8')
        if '.wa-tabbar {' in src:
            print(f"  · 已有 CSS，跳过: {p.name}")
            continue
        # 找 </style> 之前插入
        idx = src.rfind('</style>')
        if idx == -1:
            print(f"  ✗ 无 </style>: {p.name}")
            continue
        new_src = src[:idx] + CSS_TABBAR + '\n' + src[idx:]
        p.write_text(new_src, encoding='utf-8')
        print(f"  ✓ 注入 CSS: {p.name}")
        ok += 1
    print(f"\n完成: {ok}/{len(FILES)}")


if __name__ == "__main__":
    main()