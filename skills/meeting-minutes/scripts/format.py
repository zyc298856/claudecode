#!/usr/bin/env python3
"""
会议纪要格式化工具脚本

提供 SRT/VTT 字幕解析、纯文本预处理和 Markdown 输出功能。
用于辅助 meeting-minutes skill 处理不同格式的会议输入。
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class SubtitleEntry:
    """字幕条目"""
    index: int
    start_time: str
    end_time: str
    text: str


@dataclass
class MeetingInfo:
    """会议基本信息"""
    title: str = "待确认"
    date: str = "待确认"
    attendees: list = field(default_factory=list)
    recorder: str = "待确认"
    topics: list = field(default_factory=list)
    action_items: list = field(default_factory=list)
    lang: str = "zh"  # "zh" 或 "en"


def parse_time_srt(time_str: str) -> str:
    """将 SRT 时间格式转为可读格式。

    Args:
        time_str: SRT 时间戳，如 "00:12:34,567"

    Returns:
        可读时间字符串，如 "00:12:34"
    """
    match = re.match(r"(\d{2}):(\d{2}):(\d{2})", time_str.strip())
    if match:
        return f"{match.group(1)}:{match.group(2)}:{match.group(3)}"
    return time_str


def parse_time_vtt(time_str: str) -> str:
    """将 VTT 时间格式转为可读格式。

    Args:
        time_str: VTT 时间戳，如 "00:12:34.567" 或 "12:34.567"

    Returns:
        可读时间字符串，如 "00:12:34"
    """
    match = re.match(r"(\d{1,2}):(\d{2}):(\d{2})", time_str.strip())
    if match:
        return f"{match.group(1).zfill(2)}:{match.group(2)}:{match.group(3)}"
    # MM:SS.mmm 格式，补全为 HH:MM:SS
    match = re.match(r"(\d{1,2}):(\d{2})", time_str.strip())
    if match:
        return f"00:{match.group(1).zfill(2)}:{match.group(2)}"
    return time_str


def parse_srt(content: str) -> list:
    """解析 SRT 字幕文件内容。

    Args:
        content: SRT 文件的文本内容

    Returns:
        SubtitleEntry 对象列表
    """
    entries = []
    blocks = re.split(r"\n\s*\n", content.strip())

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue

        # 解析序号
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue

        # 解析时间戳行
        time_match = re.match(
            r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})",
            lines[1].strip()
        )
        if not time_match:
            continue

        start_time = parse_time_srt(time_match.group(1))
        end_time = parse_time_srt(time_match.group(2))
        text = " ".join(line.strip() for line in lines[2:])

        entries.append(SubtitleEntry(
            index=index,
            start_time=start_time,
            end_time=end_time,
            text=text
        ))

    return entries


def parse_vtt(content: str) -> list:
    """解析 VTT 字幕文件内容。

    Args:
        content: VTT 文件的文本内容

    Returns:
        SubtitleEntry 对象列表
    """
    entries = []
    # 移除 WEBVTT 头部
    content = re.sub(r"^WEBVTT.*\n", "", content.strip())
    blocks = re.split(r"\n\s*\n", content.strip())

    idx = 1
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue

        # 查找时间戳行
        time_line_idx = 0
        for i, line in enumerate(lines):
            if "-->" in line:
                time_line_idx = i
                break

        time_match = re.match(
            r"(\d{1,2}:\d{2}(?::\d{2})?[\.,]\d{3})\s*-->\s*(\d{1,2}:\d{2}(?::\d{2})?[\.,]\d{3})",
            lines[time_line_idx].strip()
        )
        if not time_match:
            continue

        start_time = parse_time_vtt(time_match.group(1))
        end_time = parse_time_vtt(time_match.group(2))
        text = " ".join(
            line.strip()
            for line in lines[time_line_idx + 1:]
            if line.strip()
        )

        entries.append(SubtitleEntry(
            index=idx,
            start_time=start_time,
            end_time=end_time,
            text=text
        ))
        idx += 1

    return entries


def subtitles_to_text(entries: list) -> str:
    """将字幕条目列表转换为带时间标记的纯文本。

    Args:
        entries: SubtitleEntry 对象列表

    Returns:
        带时间标记的文本字符串
    """
    lines = []
    for entry in entries:
        lines.append(f"[{entry.start_time}] {entry.text}")
    return "\n".join(lines)


def subtitles_to_plain_text(entries: list) -> str:
    """将字幕条目列表转换为纯文本（不含时间戳）。

    Args:
        entries: SubtitleEntry 对象列表

    Returns:
        纯文本字符串
    """
    return " ".join(entry.text for entry in entries)


def preprocess_text(content: str) -> str:
    """预处理纯文本会议记录。

    清理多余空行、统一标点、移除无关标记。

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
    return content.strip()


def detect_format(content: str) -> str:
    """自动检测输入文本的格式。

    Args:
        content: 输入文本内容

    Returns:
        格式标识: "srt", "vtt", "plain"
    """
    stripped = content.strip()
    if stripped.startswith("WEBVTT"):
        return "vtt"
    if re.search(r"\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}", stripped):
        return "srt"
    return "plain"


def parse_input(content: str) -> str:
    """自动检测并解析输入内容，返回纯文本。

    Args:
        content: 输入文本（SRT/VTT/纯文本）

    Returns:
        解析后的纯文本
    """
    fmt = detect_format(content)

    if fmt == "srt":
        entries = parse_srt(content)
        return subtitles_to_text(entries)
    elif fmt == "vtt":
        entries = parse_vtt(content)
        return subtitles_to_text(entries)
    else:
        return preprocess_text(content)


def generate_markdown(meeting: MeetingInfo) -> str:
    """生成 Markdown 格式的会议纪要。

    Args:
        meeting: MeetingInfo 对象

    Returns:
        Markdown 格式的会议纪要
    """
    lang = meeting.lang
    en = lang == "en"

    attendees_str = (
        ", ".join(meeting.attendees) if en
        else "、".join(meeting.attendees)
    ) if meeting.attendees else ("TBD" if en else "待确认")

    tbd = "TBD" if en else "待确认"
    unassigned = "Unassigned" if en else "待分配"

    labels = {
        "title": "Meeting Minutes" if en else "会议纪要",
        "date": "**Date**" if en else "**日期**",
        "attendees": "**Attendees**" if en else "**参会人**",
        "recorder": "**Recorder**" if en else "**记录人**",
        "topic": "Topic" if en else "议题",
        "unnamed": "Untitled Topic" if en else "未命名议题",
        "discussion": "Discussion Points" if en else "讨论要点",
        "decisions": "Decisions" if en else "决议",
        "actions": "Action Items" if en else "待办事项",
        "task": "Task" if en else "任务",
        "owner": "Owner" if en else "责任人",
        "deadline": "Deadline" if en else "截止日期",
        "footer": "> These minutes were AI-assisted. Attendees should review for accuracy." if en
                  else "> 本纪要由 AI 辅助整理，如有遗漏或误述请参会人员及时修正。",
    }

    parts = [
        f"# {labels['title']}：{meeting.title}",
        "",
        f"{labels['date']}：{meeting.date}",
        f"{labels['attendees']}：{attendees_str}",
        f"{labels['recorder']}：{meeting.recorder}",
        "",
        "---",
    ]

    cn_nums = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    for i, topic in enumerate(meeting.topics):
        if en:
            num = str(i + 1)
        else:
            num = cn_nums[i] if i < len(cn_nums) else str(i + 1)
        parts.append(f"## {labels['topic']}{num}：{topic.get('title', labels['unnamed'])}")
        parts.append("")

        if topic.get("discussion"):
            parts.append(f"### {labels['discussion']}")
            parts.append("")
            for point in topic["discussion"]:
                parts.append(f"- {point}")
            parts.append("")

        if topic.get("decisions"):
            parts.append(f"### {labels['decisions']}")
            parts.append("")
            for j, decision in enumerate(topic["decisions"], 1):
                parts.append(f"{j}. {decision}")
            parts.append("")

        parts.append("---")
        parts.append("")

    if meeting.action_items:
        parts.append(f"## {labels['actions']}")
        parts.append("")
        parts.append(f"| # | {labels['task']} | {labels['owner']} | {labels['deadline']} |")
        parts.append("|---|------|--------|----------|")
        for k, item in enumerate(meeting.action_items, 1):
            task = item.get("task", tbd)
            owner = item.get("owner", unassigned)
            deadline = item.get("deadline", tbd)
            parts.append(f"| {k} | {task} | {owner} | {deadline} |")
        parts.append("")
        parts.append("---")
        parts.append("")

    parts.append(labels["footer"])

    return "\n".join(parts)


ALLOWED_EXTENSIONS = {".txt", ".srt", ".vtt", ".md"}


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
    """将内容保存为 Markdown 文件。

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
        print("用法: python format.py <input_file> [--output <output_file>]")
        print("  input_file: 会议记录文件（支持 .txt, .srt, .vtt）")
        print("  --output:   指定输出 Markdown 文件路径（可选）")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    input_path = Path(input_file).resolve()
    if input_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        print(f"错误: 不支持的文件格式 {input_path.suffix}，仅支持 {', '.join(ALLOWED_EXTENSIONS)}")
        sys.exit(1)
    content = input_path.read_text(encoding="utf-8")
    parsed = parse_input(content)

    discussion_points = [
        line.strip() for line in parsed.split("\n") if line.strip()
    ]
    meeting = MeetingInfo(
        title=input_path.stem,
        date="待确认",
        topics=[{"title": "会议内容", "discussion": discussion_points}],
    )
    result = generate_markdown(meeting)

    if output_file:
        saved_path = save_markdown(result, output_file)
        print(f"已保存到: {saved_path}")
    else:
        print(result)
