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


def _detect_language(content: str) -> str:
    """检测文本语言。

    全文字符级统计：中文字符数 vs 英文字母数。
    字符级统计比行级统计更稳定，不受短行（如 API、CI）影响。

    Args:
        content: 输入文本

    Returns:
        "zh" 或 "en"
    """
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", content))
    english_chars = len(re.findall(r"[a-zA-Z]", content))
    return "zh" if chinese_chars > english_chars else "en"


# 周报关键词（week 使用 \b 词边界匹配，避免 weekend/weekday 误命中）
WEEKLY_KEYWORDS = [
    "周报", "本周", "这周", "上周", "一周", "weekly",
    "周一", "周二", "周三", "周四", "周五", "周六", "周日",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
    "Saturday", "Sunday",
]
WEEKLY_PATTERNS = [r"\bweek\b"]  # 需要词边界匹配的英文关键词

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
    lang: str = "zh"  # "zh" 或 "en"


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
    weekly_score += sum(1 for pat in WEEKLY_PATTERNS if re.search(pat, text))
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


# ---- 微信聊天记录解析 ----

_WECHAT_MSG_HEADER = re.compile(
    r"^((?:\[.*?\])?[\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z0-9_\-\.\(\)（）\s]{0,28}?)\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*$"
)
_WECHAT_DATE_HEADER = re.compile(r"^\d{4}年\d{1,2}月\d{1,2}日")
# 仅匹配微信已知系统消息，避免误杀 [搜索模块] 等正常工作内容
_WECHAT_MEDIA = re.compile(
    r"^\[(图片|语音|视频|文件|表情|链接|位置|名片|小程序|聊天记录|红包|转账|拍一拍)\]$"
)
_WECHAT_NOISE = re.compile(
    r"(撤回了一条消息$|加入了群聊$|修改群名为|^你添加了|^现在可以开始)"
)


def detect_wechat(content: str) -> bool:
    """检测输入是否为微信聊天记录格式。

    判定条件：
    1. 至少 2 行匹配 "发言人 HH:MM" 模式
    2. 消息头之后存在非空内容行（排除纯时间戳日志如 "API 10:30"）

    Args:
        content: 输入文本

    Returns:
        True 表示为微信聊天记录格式
    """
    lines = content.strip().split("\n")
    header_count = 0
    has_content_after_header = False
    for i, line in enumerate(lines[:50]):
        stripped = line.strip()
        if _WECHAT_MSG_HEADER.match(stripped):
            header_count += 1
            # 检查消息头后是否有内容行（非空、非消息头、非日期行）
            for j in range(i + 1, min(i + 3, len(lines))):
                next_line = lines[j].strip()
                if not next_line:
                    continue
                if (not _WECHAT_MSG_HEADER.match(next_line)
                        and not _WECHAT_DATE_HEADER.match(next_line)):
                    has_content_after_header = True
                break
    return header_count >= 2 and has_content_after_header


def parse_wechat(content: str) -> str:
    """解析微信聊天记录，提取有效工作内容。

    过滤系统消息（撤回、加群、红包等），合并同一发言人的连续消息，
    输出为 "发言人：消息内容" 格式的结构化文本。

    Args:
        content: 微信聊天记录原始文本

    Returns:
        结构化的对话文本
    """
    lines = content.strip().split("\n")
    messages = []
    current_speaker = ""
    current_parts = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # 跳过日期行，同时 flush 当前发言人消息（避免跨天合并）
        if _WECHAT_DATE_HEADER.match(stripped):
            if current_speaker and current_parts:
                messages.append(f"{current_speaker}：{' '.join(current_parts)}")
            current_speaker = ""
            current_parts = []
            continue
        # 检测消息头：发言人 时间
        match = _WECHAT_MSG_HEADER.match(stripped)
        if match:
            new_speaker = match.group(1)
            # 同一发言人连续消息：合并，不 flush
            if new_speaker == current_speaker:
                continue
            # 不同发言人：保存上一个发言人的消息
            if current_speaker and current_parts:
                messages.append(f"{current_speaker}：{' '.join(current_parts)}")
            current_speaker = new_speaker
            current_parts = []
            continue
        # 过滤系统噪音（媒体标记 + 系统通知）
        if _WECHAT_MEDIA.match(stripped) or _WECHAT_NOISE.search(stripped):
            continue
        # 累积消息内容
        if current_speaker:
            current_parts.append(stripped)

    # 保存最后一个发言人的消息
    if current_speaker and current_parts:
        messages.append(f"{current_speaker}：{' '.join(current_parts)}")

    return "\n".join(messages)


def _get_date_label(report_type: str, lang: str = "zh") -> str:
    """获取日期标签字符串。

    Args:
        report_type: "daily" 或 "weekly"
        lang: "zh" 或 "en"

    Returns:
        格式化的日期字符串
    """
    today = datetime.now()
    en = lang == "en"
    if report_type == "daily":
        if en:
            return today.strftime("%B %d, %Y")
        return f"{today.year}年{today.month}月{today.day}日"
    else:
        weekday = today.weekday()
        monday = today - timedelta(days=weekday)
        sunday = today + timedelta(days=6 - weekday)
        if en:
            return f"{monday.strftime('%b %d')} - {sunday.strftime('%b %d, %Y')}"
        return f"{monday.month}月{monday.day}日 - {sunday.month}月{sunday.day}日"


def generate_daily_markdown(report: ReportInfo) -> str:
    """生成日报格式的 Markdown 报告。

    Args:
        report: ReportInfo 对象，包含日报数据

    Returns:
        Markdown 格式的日报
    """
    lang = report.lang
    en = lang == "en"
    tbd = "TBD" if en else "待确认"

    date_label = report.date or _get_date_label("daily", lang)

    labels = {
        "title": "Daily Report" if en else "工作日报",
        "name": "**Name**" if en else "**姓名**",
        "dept": "**Department**" if en else "**部门**",
        "completed": "Completed Today" if en else "今日完成",
        "issues": "Issues" if en else "遇到问题",
        "plans": "Plans for Tomorrow" if en else "明日计划",
        "pending": "- To be organized" if en else "- 待整理",
        "no_plans": "- To be planned" if en else "- 待规划",
        "footer": "> This report was AI-assisted." if en else "> 本报告由 AI 辅助整理。",
    }

    parts = [
        f"# {labels['title']}：{date_label}",
        "",
    ]

    if report.author:
        parts.append(f"{labels['name']}：{report.author}")
    if report.department:
        parts.append(f"{labels['dept']}：{report.department}")

    if report.author or report.department:
        parts.append("")

    parts.append("---")
    parts.append("")

    # 今日完成
    parts.append(f"## {labels['completed']}")
    parts.append("")
    if report.items:
        for item in report.items:
            if isinstance(item, str):
                parts.append(f"- {item}")
            else:
                module = item.get("module", "")
                desc = item.get("description", tbd)
                if module:
                    parts.append(f"- {desc}（{module}）")
                else:
                    parts.append(f"- {desc}")
    else:
        parts.append(labels["pending"])
    parts.append("")

    # 遇到问题（仅在有内容时包含）
    if report.problems:
        parts.append(f"## {labels['issues']}")
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
    parts.append(f"## {labels['plans']}")
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
        parts.append(labels["no_plans"])
    parts.append("")

    parts.append("---")
    parts.append("")
    parts.append(labels["footer"])

    return "\n".join(parts)


def generate_weekly_markdown(report: ReportInfo) -> str:
    """生成周报格式的 Markdown 报告。

    Args:
        report: ReportInfo 对象，包含周报数据

    Returns:
        Markdown 格式的周报
    """
    lang = report.lang
    en = lang == "en"
    tbd = "TBD" if en else "待确认"

    date_label = report.date or _get_date_label("weekly", lang)

    labels = {
        "title": "Weekly Report" if en else "工作周报",
        "name": "**Name**" if en else "**姓名**",
        "dept": "**Department**" if en else "**部门**",
        "summary": "Weekly Summary" if en else "本周总结",
        "uncategorized": "Uncategorized" if en else "未分类",
        "achievements": "Key Achievements" if en else "关键成果",
        "risks": "Issues & Risks" if en else "问题与风险",
        "problem": "Problem" if en else "问题描述",
        "impact": "Impact" if en else "影响范围",
        "status": "Status" if en else "当前状态",
        "assess": "TBD" if en else "待评估",
        "in_progress": "In Progress" if en else "进行中",
        "next_plans": "Plans for Next Week" if en else "下周计划",
        "no_plans": "- To be planned" if en else "- 待规划",
        "footer": "> This report was AI-assisted." if en else "> 本报告由 AI 辅助整理。",
    }

    parts = [
        f"# {labels['title']}：{date_label}",
        "",
    ]

    if report.author:
        parts.append(f"{labels['name']}：{report.author}")
    if report.department:
        parts.append(f"{labels['dept']}：{report.department}")

    if report.author or report.department:
        parts.append("")

    parts.append("---")
    parts.append("")

    # 本周总结（按项目/模块分组）
    parts.append(f"## {labels['summary']}")
    parts.append("")
    if report.groups:
        for group in report.groups:
            group_name = group.get("name", labels["uncategorized"])
            group_items = group.get("items", [])
            parts.append(f"### {group_name}")
            parts.append("")
            for item in group_items:
                desc = item if isinstance(item, str) else item.get("description", tbd)
                parts.append(f"- {desc}")
            parts.append("")
    elif report.items:
        for item in report.items:
            desc = item if isinstance(item, str) else item.get("description", tbd)
            parts.append(f"- {desc}")
        parts.append("")

    # 关键成果
    if report.achievements:
        parts.append(f"## {labels['achievements']}")
        parts.append("")
        for achievement in report.achievements:
            parts.append(f"- {achievement}")
        parts.append("")

    # 问题与风险
    parts.append(f"## {labels['risks']}")
    parts.append("")
    if report.problems:
        parts.append(f"| # | {labels['problem']} | {labels['impact']} | {labels['status']} |")
        parts.append("|---|---------|---------|---------|")
        for i, problem in enumerate(report.problems, 1):
            if isinstance(problem, dict):
                desc = problem.get("description", tbd)
                impact = problem.get("impact", labels["assess"])
                status = problem.get("status", labels["in_progress"])
            else:
                desc = str(problem)
                impact = labels["assess"]
                status = labels["in_progress"]
            parts.append(f"| {i} | {desc} | {impact} | {status} |")
    else:
        parts.append("- " + ("None" if en else "无"))
    parts.append("")

    # 下周计划
    parts.append(f"## {labels['next_plans']}")
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
        parts.append(labels["no_plans"])
    parts.append("")

    parts.append("---")
    parts.append("")
    parts.append(labels["footer"])

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
    if input_path.exists():
        if input_path.suffix.lower() in ALLOWED_EXTENSIONS:
            content = input_path.read_text(encoding="utf-8")
        else:
            print(f"错误: 不支持的文件格式 '{input_path.suffix}'，仅支持 {', '.join(ALLOWED_EXTENSIONS)}", file=sys.stderr)
            sys.exit(1)
    else:
        content = input_text

    if not content.strip():
        print("错误: 输入内容为空，请提供工作记录文本或文件路径。", file=sys.stderr)
        sys.exit(1)

    detected_type = detect_report_type(content, report_type)
    # 自动检测并解析微信聊天记录格式
    if detect_wechat(content):
        content = parse_wechat(content)
    processed = preprocess_text(content)
    lang = _detect_language(content)

    report = ReportInfo(
        report_type=detected_type,
        lang=lang,
        items=[{"description": re.sub(r"^[\-\*]\s+", "", line)} for line in processed.split("\n") if line.strip()],
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
