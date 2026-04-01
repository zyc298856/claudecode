#!/usr/bin/env python3
"""
工作报告格式化工具脚本

提供报告类型识别、文本预处理和 Markdown 输出功能。
用于辅助 work-report skill 将散乱的工作记录整理为结构化报告。
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timedelta


# 周报关键词
WEEKLY_KEYWORDS = [
    "周报", "本周", "这周", "上周", "一周", "weekly",
    "周一", "周二", "周三", "周四", "周五", "周六", "周日",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
    "Saturday", "Sunday", "week",
]

# 日报关键词
DAILY_KEYWORDS = [
    "日报", "今天", "今日", "昨天", "daily", "今日工作",
    "今天工作", "日常", "当日", "本日",
]


@dataclass
class ReportInfo:
    """报告数据结构"""
    report_type: str = "daily"  # "daily" 或 "weekly"
    author: str = ""
    department: str = ""
    date: str = ""
    items: list = field(default_factory=list)           # 工作事项列表
    groups: list = field(default_factory=list)           # 分组（周报按项目/模块分组）
    achievements: list = field(default_factory=list)     # 关键成果
    problems: list = field(default_factory=list)         # 问题与风险
    plans: list = field(default_factory=list)            # 下一步计划


def detect_report_type(content: str, explicit_type: str = "") -> str:
    """自动判断报告类型（日报或周报）。

    Args:
        content: 用户输入的文本内容
        explicit_type: 用户明确指定的类型（"daily" 或 "weekly"），优先级最高

    Returns:
        "daily" 或 "weekly"
    """
    if explicit_type in ("daily", "weekly"):
        return explicit_type

    text = content.lower()

    weekly_score = sum(1 for kw in WEEKLY_KEYWORDS if kw.lower() in text)
    daily_score = sum(1 for kw in DAILY_KEYWORDS if kw.lower() in text)

    if weekly_score > daily_score:
        return "weekly"
    elif daily_score > weekly_score:
        return "daily"
    else:
        return "weekly"  # 无法判断时默认周报


def preprocess_text(content: str) -> str:
    """预处理散乱的工作记录文本。

    清理多余空行、统一标点、合并重复项、移除无关标记。

    Args:
        content: 原始文本

    Returns:
        清理后的文本
    """
    # 移除多余空行（保留段落分隔）
    content = re.sub(r"\n{3,}", "\n\n", content)
    # 移除行首尾空白
    lines = [line.strip() for line in content.split("\n")]
    content = "\n".join(lines)
    # 统一全角/半角空格
    content = re.sub(r"[ \t]+", " ", content)
    # 移除常见的列表标记（如微信消息前缀）
    content = re.sub(r"^[\-\*]\s*", "- ", content, flags=re.MULTILINE)
    return content.strip()


def _get_date_label(report_type: str) -> str:
    """获取日期标签字符串。

    Args:
        report_type: "daily" 或 "weekly"

    Returns:
        格式化的日期字符串
    """
    today = datetime.now()
    if report_type == "daily":
        return f"{today.year}年{today.month}月{today.day}日"
    else:
        # 周报默认显示本周范围（周一到周日）
        weekday = today.weekday()
        monday = today - timedelta(days=weekday)
        sunday = today + timedelta(days=6 - weekday)
        return f"{monday.month}月{monday.day}日 - {sunday.month}月{sunday.day}日"


def generate_daily_markdown(report: ReportInfo) -> str:
    """生成日报格式的 Markdown 报告。

    Args:
        report: ReportInfo 对象，包含日报数据

    Returns:
        Markdown 格式的日报
    """
    date_label = report.date or _get_date_label("daily")

    parts = [
        f"# 工作日报：{date_label}",
        "",
    ]

    if report.author:
        parts.append(f"**姓名**：{report.author}")
    if report.department:
        parts.append(f"**部门**：{report.department}")

    if report.author or report.department:
        parts.append("")

    parts.append("---")
    parts.append("")

    # 今日完成
    parts.append("## 今日完成")
    parts.append("")
    if report.items:
        for item in report.items:
            if isinstance(item, str):
                parts.append(f"- {item}")
            else:
                module = item.get("module", "")
                desc = item.get("description", "待确认")
                if module:
                    parts.append(f"- {desc}（{module}）")
                else:
                    parts.append(f"- {desc}")
    else:
        parts.append("- 待整理")
    parts.append("")

    # 遇到问题（仅在有内容时包含）
    if report.problems:
        parts.append("## 遇到问题")
        parts.append("")
        for problem in report.problems:
            if isinstance(problem, str):
                desc = problem
            else:
                desc = problem.get("description", "")
            if desc:
                parts.append(f"- {desc}")
        parts.append("")

    # 明日计划
    parts.append("## 明日计划")
    parts.append("")
    if report.plans:
        for plan in report.plans:
            if isinstance(plan, str):
                parts.append(f"- {plan}")
            else:
                desc = plan.get("description", str(plan))
                module = plan.get("module", "")
                if module:
                    parts.append(f"- {desc}（{module}）")
                else:
                    parts.append(f"- {desc}")
    else:
        parts.append("- 待规划")
    parts.append("")

    parts.append("---")
    parts.append("")
    parts.append("> 本报告由 AI 辅助整理。")

    return "\n".join(parts)


def generate_weekly_markdown(report: ReportInfo) -> str:
    """生成周报格式的 Markdown 报告。

    Args:
        report: ReportInfo 对象，包含周报数据

    Returns:
        Markdown 格式的周报
    """
    date_label = report.date or _get_date_label("weekly")

    parts = [
        f"# 工作周报：{date_label}",
        "",
    ]

    if report.author:
        parts.append(f"**姓名**：{report.author}")
    if report.department:
        parts.append(f"**部门**：{report.department}")

    if report.author or report.department:
        parts.append("")

    parts.append("---")
    parts.append("")

    # 本周总结（按项目/模块分组）
    parts.append("## 本周总结")
    parts.append("")
    if report.groups:
        for group in report.groups:
            group_name = group.get("name", "未分类")
            group_items = group.get("items", [])
            parts.append(f"### {group_name}")
            parts.append("")
            for item in group_items:
                desc = item if isinstance(item, str) else item.get("description", "待确认")
                parts.append(f"- {desc}")
            parts.append("")
    elif report.items:
        # 未分组时，按事项列表输出
        for item in report.items:
            desc = item if isinstance(item, str) else item.get("description", "待确认")
            parts.append(f"- {desc}")
        parts.append("")

    # 关键成果
    if report.achievements:
        parts.append("## 关键成果")
        parts.append("")
        for achievement in report.achievements:
            parts.append(f"- {achievement}")
        parts.append("")

    # 问题与风险
    if report.problems:
        parts.append("## 问题与风险")
        parts.append("")
        parts.append("| # | 问题描述 | 影响范围 | 当前状态 |")
        parts.append("|---|---------|---------|---------|")
        for i, problem in enumerate(report.problems, 1):
            if isinstance(problem, dict):
                desc = problem.get("description", "待确认")
                impact = problem.get("impact", "待评估")
                status = problem.get("status", "进行中")
            else:
                desc = str(problem)
                impact = "待评估"
                status = "进行中"
            parts.append(f"| {i} | {desc} | {impact} | {status} |")
        parts.append("")

    # 下周计划
    parts.append("## 下周计划")
    parts.append("")
    if report.plans:
        for plan in report.plans:
            if isinstance(plan, dict):
                desc = plan.get("description", str(plan))
                module = plan.get("module", "")
                if module:
                    parts.append(f"- {desc}（{module}）")
                else:
                    parts.append(f"- {desc}")
            else:
                parts.append(f"- {plan}")
    else:
        parts.append("- 待规划")
    parts.append("")

    parts.append("---")
    parts.append("")
    parts.append("> 本报告由 AI 辅助整理。")

    return "\n".join(parts)


ALLOWED_EXTENSIONS = {".txt", ".md"}


def _validate_path(file_path: str, allowed_dir: str = ".") -> Path:
    """验证文件路径安全性，防止路径遍历。

    Args:
        file_path: 待验证的文件路径
        allowed_dir: 允许的根目录

    Returns:
        解析后的安全路径

    Raises:
        ValueError: 路径不合法时抛出
    """
    resolved = Path(file_path).resolve()
    allowed = Path(allowed_dir).resolve()
    try:
        resolved.relative_to(allowed)
    except ValueError:
        raise ValueError(f"文件路径必须在 {allowed_dir} 目录下")
    return resolved


def save_markdown(content: str, output_path: str) -> str:
    """将报告内容保存为 Markdown 文件。

    Args:
        content: Markdown 内容
        output_path: 输出文件路径

    Returns:
        保存的文件绝对路径
    """
    path = _validate_path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


# 命令行入口
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python format.py <input_text> [--type daily|weekly] [--output <output_file>]")
        print("  input_text: 工作内容文本或文件路径")
        print("  --type:     报告类型 daily 或 weekly（可选，自动识别）")
        print("  --output:   指定输出 Markdown 文件路径（可选）")
        sys.exit(1)

    input_text = sys.argv[1]
    report_type = ""
    output_file = None

    if "--type" in sys.argv:
        idx = sys.argv.index("--type")
        if idx + 1 < len(sys.argv):
            report_type = sys.argv[idx + 1]

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    # 检查输入是否为文件路径
    input_path = Path(input_text)
    if input_path.exists() and input_path.suffix.lower() in ALLOWED_EXTENSIONS:
        content = input_path.read_text(encoding="utf-8")
    else:
        content = input_text

    detected_type = detect_report_type(content, report_type)
    processed = preprocess_text(content)

    report = ReportInfo(
        report_type=detected_type,
        items=[{"description": line.lstrip("- ")} for line in processed.split("\n") if line.strip()],
    )

    if detected_type == "daily":
        result = generate_daily_markdown(report)
    else:
        result = generate_weekly_markdown(report)

    if output_file:
        saved_path = save_markdown(result, output_file)
        print(f"已保存到: {saved_path}")
    else:
        print(result)
