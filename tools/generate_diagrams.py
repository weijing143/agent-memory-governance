#!/usr/bin/env python3
"""Generate repository directory tree and structure map PNGs.

Uses only matplotlib (no graphviz binary required).
"""
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager

# Try to find a CJK-capable font so Chinese labels render correctly.
# Searches common system fonts; falls back to matplotlib default if none found.
def _find_cjk_font():
    candidates = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/hpsimplifiedhans-regular.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    # Last resort: ask matplotlib's font manager for any font that claims CJK coverage.
    for font in font_manager.fontManager.ttflist:
        if "CJK" in font.name or "Hei" in font.name or "Song" in font.name:
            return font.fname
    return None


cjk_font_path = _find_cjk_font()
if cjk_font_path:
    font_manager.fontManager.addfont(cjk_font_path)
    plt.rcParams["font.family"] = font_manager.FontProperties(fname=cjk_font_path).get_name()
plt.rcParams["axes.unicode_minus"] = False

# Output next to this script: <repo>/assets/diagrams
OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "diagrams"


def draw_tree():
    fig, ax = plt.subplots(figsize=(17, 8))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 8)
    ax.axis("off")

    def node(x, y, text, color="#E2E8F0", width=2.6, height=0.55, text_color="#1E293B"):
        box = FancyBboxPatch(
            (x - width / 2, y - height / 2), width, height,
            boxstyle="round,pad=0.03,rounding_size=0.12",
            facecolor=color, edgecolor="#64748B", linewidth=1.2
        )
        ax.add_patch(box)
        ax.text(x, y, text, ha="center", va="center", fontsize=9,
                color=text_color, wrap=True)
        return box

    def edge(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], color="#94A3B8", linewidth=1.2, zorder=0)

    # Root
    node(8, 7.2, "agent-memory-governance\n(main · v1.2.5 · MIT)", "#1E293B", width=3.4, text_color="white")

    # Level 1: top-level files
    node(2.0, 5.8, "SKILL.md\n治理指南本体", "#DCFCE7", width=2.2)
    node(5.0, 5.8, "README.md\n项目简介", "#F1F5F9", width=1.9)
    node(8.0, 5.8, "CHANGELOG.md\n版本记录", "#F1F5F9", width=1.9)
    node(10.5, 5.8, "LICENSE\nMIT", "#F1F5F9", width=1.5)
    node(13.5, 5.8, "assets/\n图表资源", "#DBEAFE", width=1.5)

    edge(8, 6.9, 2.0, 6.05)
    edge(8, 6.9, 5.0, 6.05)
    edge(8, 6.9, 8.0, 6.05)
    edge(8, 6.9, 10.5, 6.05)
    edge(8, 6.9, 13.5, 6.05)

    node(13.5, 4.8, "diagrams/\ntree.png / map.png", "#DBEAFE", width=2.0)
    edge(13.5, 5.55, 13.5, 5.08)

    # Level 2: directories
    dirs = [
        (2.8, "scripts/", "#F3E8FF"),
        (5.4, "tools/\n图表生成", "#E0E7FF"),
        (7.6, "tests/\n单元测试", "#FCE7F3"),
        (11.6, "references/", "#FEF3C7"),
    ]
    for x, label, color in dirs:
        node(x, 4.4, label, color, width=1.5)
        edge(8, 6.45, x, 4.68)

    # Level 3: children
    node(2.8, 3.2, "memory_health.py\n健康检查脚本\n(纯标准库)", "#F3E8FF", width=2.4)
    edge(2.8, 4.12, 2.8, 3.48)

    node(5.4, 3.2, "generate_\ndiagrams.py", "#E0E7FF", width=1.7)
    edge(5.4, 4.12, 5.4, 3.48)

    node(7.6, 3.2, "test_memory_\nhealth.py", "#FCE7F3", width=1.7)
    edge(7.6, 4.12, 7.6, 3.48)

    ref_items = [
        (9.2, "implementation-\nblueprint.md\n实施蓝图"),
        (10.8, "hermes-\nintegration.md\nHermes 落地"),
        (12.4, "hermes-practice-\nreport.md\n实践报告"),
        (14.0, "openclaw-\ninvocation.md\nOpenClaw"),
        (15.6, "semi-automated-\npattern.md\n半自动模式"),
    ]
    for x, label in ref_items:
        node(x, 3.0, label, "#FEF3C7", width=1.5)
        edge(11.6, 4.12, x, 3.28)

    plt.tight_layout()
    fig.savefig(OUT_DIR / "tree.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def draw_map():
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis("off")

    def box(x, y, w, h, text, facecolor="#F8FAFC", edgecolor="#64748B", text_size=9):
        rect = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.15",
            facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(x, y, text, ha="center", va="center", fontsize=text_size,
                color="#1E293B", wrap=True)
        return rect

    def arrow(x1, y1, x2, y2, color="#94A3B8"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.3,
                                    connectionstyle="arc3,rad=0.05"))

    # Central principle source
    box(6.5, 7.0, 3.2, 0.9, "SKILL.md v1.2.5\n治理原则权威源", "#DCFCE7", "#16A34A", 10)

    # Facade layer
    box(2.2, 5.6, 2.0, 0.7, "README.md\n项目门面", "#DBEAFE", "#3B82F6", 9)
    box(4.8, 5.6, 2.0, 0.7, "CHANGELOG.md\n变更记录", "#DBEAFE", "#3B82F6", 9)
    box(7.4, 5.6, 1.6, 0.7, "LICENSE\nMIT", "#DBEAFE", "#3B82F6", 9)

    arrow(5.0, 6.7, 3.0, 5.95)
    arrow(5.5, 6.7, 4.9, 5.95)
    arrow(6.5, 6.7, 7.4, 5.95)

    # Implementation
    box(10.8, 5.6, 2.4, 0.9, "scripts/memory_health.py\n健康检查参考实现\n(标准库 · exit 0)", "#F3E8FF", "#8B5CF6", 9)
    arrow(8.1, 6.7, 10.2, 5.95)

    # References / platform guides
    refs = [
        (2.2, 3.9, "implementation-\nblueprint.md\n实施蓝图"),
        (4.8, 3.9, "hermes-\nintegration.md\nHermes 落地"),
        (7.4, 3.9, "hermes-practice-\nreport.md\n8 条教训"),
        (10.0, 3.9, "openclaw-\ninvocation.md\nOpenClaw"),
        (12.0, 3.9, "semi-automated-\npattern.md\n半自动模式"),
    ]
    for x, y, text in refs:
        box(x, y, 2.0, 1.0, text, "#FEF3C7", "#F59E0B", 9)
        arrow(6.5, 6.55, x, y + 0.5, color="#CBD5E1")

    # Three-zone data model
    box(3.5, 2.0, 2.4, 0.9, "活跃记忆\nActive memory\n用户确认的长期上下文", "#E0F2FE", "#0EA5E9", 9)
    box(6.5, 2.0, 2.4, 0.9, "参考归档\nReference archive\n分类收藏与快照", "#E0F2FE", "#0EA5E9", 9)
    box(9.5, 2.0, 2.4, 0.9, "临时对话\nTransient conversation\n当前会话上下文", "#E0F2FE", "#0EA5E9", 9)

    arrow(6.5, 6.3, 3.5, 2.45, color="#94A3B8")
    arrow(6.5, 6.3, 6.5, 2.45, color="#94A3B8")
    arrow(6.5, 6.3, 9.5, 2.45, color="#94A3B8")

    # Key principles banner
    ax.text(6.5, 0.6,
            "核心原则：三区隔离 · 冲突展示 · 先归档后删除 · 明确确认 · 年龄不是证据",
            ha="center", va="center", fontsize=10, color="#334155",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#F1F5F9", edgecolor="#94A3B8"))

    plt.tight_layout()
    fig.savefig(OUT_DIR / "map.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    draw_tree()
    draw_map()
    print(f"Diagrams saved to {OUT_DIR}/tree.png and {OUT_DIR}/map.png")
