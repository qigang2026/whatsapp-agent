#!/usr/bin/env python3
"""
批次 3 · v4 清理残留 submenu-item 实例（最终版）
策略：找到 父菜单 </a> 之后到下一个 menu-item 起始之前的整段内容，删掉
   - 父菜单: <a href="WhatsApp-Agent-PC.html" class="menu-item active">...</a>
   - 残留区段起始: 第一个 submenu-item 或 <!-- 跟进线索 注释
   - 残留区段结束: 下一个 <div class="menu-item"> 之前
"""
import re
from pathlib import Path

FILES = [
    "WhatsApp Agent/AI 跟进概要-PC.html",
    "WhatsApp Agent/统一客服收件箱-PC.html",
    "WhatsApp Agent/收件箱-AI跟进中-PC.html",
    "WhatsApp Agent/收件箱-待销售接管-PC.html",
    "WhatsApp Agent/收件箱-销售跟进中-PC.html",
    "WhatsApp Agent/线索详情-PC.html",
]

ROOT = Path("/Users/qigangye/Mstar")


def cleanup_file(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")

    # 父菜单结束位置
    parent_end = re.search(
        r'<a href="WhatsApp-Agent-PC\.html" class="menu-item active">[\s\S]*?</a>',
        src,
    )
    if not parent_end:
        return False
    cursor = parent_end.end()

    # 下一个 menu-item 起始位置（线索详情可能是 <!-- 用户管理 --> 注释开头）
    # 兼容：<!-- 用户管理 --> 或 <div class="menu-item">
    next_menu = re.search(
        r'<\!--\s*(?:用户管理|内容库|System Monitor|线索库)',
        src[cursor:],
    )
    if not next_menu:
        # 兜底: 找下一个 div class="menu-item"（含不展开的菜单）
        next_menu = re.search(r'<div class="menu-item[^"]*">', src[cursor:])
    if not next_menu:
        print(f"  ✗ 找不到下一个菜单: {path.name}")
        return False

    # 删除 cursor 到 cursor + next_menu.start() 之间所有内容
    start_pos = cursor
    end_pos = cursor + next_menu.start()
    new_src = src[:start_pos] + src[end_pos:]

    path.write_text(new_src, encoding="utf-8")
    deleted = end_pos - start_pos
    print(f"  ✓ 清理 {deleted} 字符: {path.name}")
    return True


def main():
    print("=== 批次 3 · v4 清理残留 submenu-item（最终版） ===\n")
    ok = 0
    for rel in FILES:
        p = ROOT / rel
        if not p.exists():
            print(f"  ✗ 文件不存在: {rel}")
            continue
        if cleanup_file(p):
            ok += 1
    print(f"\n完成: {ok}/{len(FILES)}")


if __name__ == "__main__":
    main()