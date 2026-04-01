#!/usr/bin/env python3
"""
PPT 大纲格式化工具脚本

提供演示类型识别、输入类型检测、文本预处理和 Markdown 输出功能。
用于辅助 ppt-generator skill 将文本内容转换为结构化 PPT 大纲。
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass, field


# 演示类型关键词映射
TYPE_KEYWORDS = {
    "business-proposal": [
        "提案", "方案汇报", "竞标", "投标", "商务", "合作方案",
        "proposal", "pitch", "bid", "business case",
    ],
    "product-launch": [
        "发布", "上线", "新品", "产品发布", "发布会", "推出",
        "launch", "release", "rollout", "go-live",
    ],
    "quarterly-review": [
        "季度", "复盘", "Q1", "Q2", "Q3", "Q4", "年度总结", "年中回顾",
        "review", "retrospective", "quarterly", "annual",
    ],
    "training-material": [
        "培训", "教程", "课程", "教学", "讲座", "入职培训",
        "training", "tutorial", "course", "workshop", "onboarding",
    ],
    "technical-presentation": [
        "技术", "架构", "方案设计", "技术分享", "微服务", "系统设计",
        "technical", "architecture", "engineering", "system design",
    ],
    "project-kickoff": [
        "启动", "立项", "开项", "项目启动", "kickoff",
    ],
    "team-meeting": [
        "述职", "汇报", "团队汇报", "周会", "月度汇报", "工作汇报",
        "standup", "report", "team meeting",
    ],
}

# 演示类型默认页数
DEFAULT_SLIDE_COUNTS = {
    "business-proposal": 14,
    "product-launch": 12,
    "quarterly-review": 15,
    "training-material": 20,
    "technical-presentation": 14,
    "project-kickoff": 10,
    "team-meeting": 10,
}

# 演示类型中英文名称
TYPE_NAMES = {
    "business-proposal": {"zh": "商业提案", "en": "Business Proposal"},
    "product-launch": {"zh": "产品发布", "en": "Product Launch"},
    "quarterly-review": {"zh": "季度复盘", "en": "Quarterly Review"},
    "training-material": {"zh": "培训材料", "en": "Training Material"},
    "technical-presentation": {"zh": "技术演示", "en": "Technical Presentation"},
    "project-kickoff": {"zh": "项目启动", "en": "Project Kickoff"},
    "team-meeting": {"zh": "团队汇报", "en": "Team Meeting"},
}


@dataclass
class SlideContent:
    """单页幻灯片内容"""
    number: int
    title: str
    bullets: list = field(default_factory=list)
    layout_hint: str = ""
    speaker_notes: str = ""
    section: str = ""


@dataclass
class PresentationInfo:
    """演示文稿数据结构"""
    pres_type: str = "business-proposal"
    title: str = "待确认"
    subtitle: str = ""
    author: str = ""
    date: str = ""
    slides: list = field(default_factory=list)
    target_count: int = 0
    lang: str = "zh"  # "zh" 或 "en"


def detect_presentation_type(content: str, explicit_type: str = "") -> str:
    """自动判断演示类型。

    Args:
        content: 用户输入的文本内容
        explicit_type: 用户明确指定的类型，优先级最高

    Returns:
        7 种演示类型之一
    """
    valid_types = list(TYPE_KEYWORDS.keys())

    if explicit_type in valid_types:
        return explicit_type

    text = content.lower()
    scores = {}
    for ptype, keywords in TYPE_KEYWORDS.items():
        scores[ptype] = sum(1 for kw in keywords if kw.lower() in text)

    max_score = max(scores.values()) if scores else 0
    if max_score == 0:
        return "business-proposal"

    # 返回得分最高的类型
    return max(scores, key=scores.get)


def detect_input_type(content: str) -> str:
    """判断输入类型。

    Args:
        content: 用户输入的文本

    Returns:
        "topic"（主题描述）、"outline"（大纲）或 "document"（长文档）
    """
    stripped = content.strip()

    # 短文本，无结构标记 → 主题描述
    if len(stripped) < 100 and not re.search(r"^[\-\*\d]", stripped, re.MULTILINE):
        return "topic"

    # 包含列表标记 → 大纲
    if re.search(r"^[\-\*]\s", stripped, re.MULTILINE) or re.search(r"^\d+[.、)]\s", stripped, re.MULTILINE):
        return "outline"

    # 长文本，段落式 → 长文档
    if len(stripped) > 500:
        return "document"

    return "topic"


def detect_language(content: str) -> str:
    """检测文本语言。

    Args:
        content: 输入文本

    Returns:
        "zh" 或 "en"
    """
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", content))
    english_chars = len(re.findall(r"[a-zA-Z]", content))
    return "zh" if chinese_chars > english_chars else "en"


def estimate_slide_count(pres_type: str, content_length: int, target: int = 0) -> int:
    """推荐幻灯片页数。

    Args:
        pres_type: 演示类型
        content_length: 输入文本长度（字符数）
        target: 用户指定的目标页数（0 表示未指定）

    Returns:
        推荐页数
    """
    if target > 0:
        return target

    base = DEFAULT_SLIDE_COUNTS.get(pres_type, 12)

    # 根据内容长度微调
    if content_length > 2000:
        base = int(base * 1.3)
    elif content_length < 200:
        base = int(base * 0.8)

    return base


def preprocess_text(content: str) -> str:
    """预处理输入文本。

    清理多余空行、统一标点、移除无关标记。

    Args:
        content: 原始文本

    Returns:
        清理后的文本
    """
    content = re.sub(r"\n{3,}", "\n\n", content)
    lines = [line.strip() for line in content.split("\n")]
    content = "\n".join(lines)
    content = re.sub(r"[ \t]+", " ", content)
    return content.strip()


def generate_slide_markdown(slide: SlideContent, lang: str = "zh") -> str:
    """生成单页幻灯片的 Markdown 块。

    Args:
        slide: SlideContent 对象
        lang: "zh" 或 "en"

    Returns:
        Markdown 格式的幻灯片块
    """
    en = lang == "en"
    labels = {
        "content": "Content" if en else "内容",
        "layout": "Layout" if en else "布局建议",
        "notes": "Speaker Notes" if en else "演讲者备注",
    }

    parts = [f"<!-- slide: {slide.number} -->"]
    parts.append(f"## {slide.title}")
    parts.append("")

    if slide.bullets:
        parts.append(f"### {labels['content']}")
        parts.append("")
        for bullet in slide.bullets:
            parts.append(f"- {bullet}")
        parts.append("")

    if slide.layout_hint:
        parts.append(f"### {labels['layout']}")
        parts.append("")
        parts.append(f"> {slide.layout_hint}")
        parts.append("")

    if slide.speaker_notes:
        parts.append(f"### {labels['notes']}")
        parts.append("")
        parts.append(f"> {slide.speaker_notes}")
        parts.append("")

    parts.append("---")
    parts.append("")

    return "\n".join(parts)


def generate_presentation_markdown(presentation: PresentationInfo) -> str:
    """生成完整的演示文稿 Markdown 输出。

    Args:
        presentation: PresentationInfo 对象

    Returns:
        Markdown 格式的完整 PPT 大纲
    """
    en = presentation.lang == "en"
    tbd = "TBD" if en else "待确认"
    type_name = TYPE_NAMES.get(presentation.pres_type, {"zh": presentation.pres_type, "en": presentation.pres_type})

    labels = {
        "title": "Presentation Outline" if en else "演示文稿大纲",
        "type": "Type" if en else "演示类型",
        "slides": "Total Slides" if en else "总页数",
        "author": "Author" if en else "演讲者",
        "date": "Date" if en else "日期",
        "footer": "> Generated by AI. Please review and adjust before presenting." if en
                  else "> 本大纲由 AI 辅助生成，请在使用前审核并调整内容。",
    }

    # 元信息头
    parts = [
        f"# {presentation.title or tbd}",
        "",
    ]

    if presentation.subtitle:
        parts.append(f"> {presentation.subtitle}")
        parts.append("")

    parts.append(f"**{labels['type']}**：{type_name[en and 'en' or 'zh']}")
    if presentation.author:
        parts.append(f"**{labels['author']}**：{presentation.author}")
    if presentation.date:
        parts.append(f"**{labels['date']}**：{presentation.date}")
    if presentation.target_count:
        parts.append(f"**{labels['slides']}**：{presentation.target_count}")

    parts.append("")
    parts.append("---")
    parts.append("")

    # 幻灯片内容
    for slide in presentation.slides:
        parts.append(generate_slide_markdown(slide, presentation.lang))

    # 页脚
    parts.append(labels["footer"])

    return "\n".join(parts)


def reindex_slides(slides: list) -> list:
    """重新编号幻灯片列表。

    在添加或删除幻灯片后调用，确保编号连续。

    Args:
        slides: SlideContent 对象列表

    Returns:
        重新编号后的列表
    """
    for i, slide in enumerate(slides, 1):
        slide.number = i
    return slides


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
        print("用法: python format.py <input_text> [--type <type>] [--slides <count>] [--output <file>]")
        print("  input_text: 文本内容或文件路径")
        print("  --type:     演示类型（可选，自动识别）")
        print("  --slides:   目标页数（可选，自动推荐）")
        print("  --output:   指定输出 Markdown 文件路径（可选）")
        sys.exit(1)

    input_text = sys.argv[1]
    pres_type = ""
    slide_target = 0
    output_file = None

    if "--type" in sys.argv:
        idx = sys.argv.index("--type")
        if idx + 1 < len(sys.argv):
            pres_type = sys.argv[idx + 1]

    if "--slides" in sys.argv:
        idx = sys.argv.index("--slides")
        if idx + 1 < len(sys.argv):
            try:
                slide_target = int(sys.argv[idx + 1])
            except ValueError:
                pass

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

    processed = preprocess_text(content)
    detected_type = detect_presentation_type(content, pres_type)
    lang = detect_language(content)
    target = estimate_slide_count(detected_type, len(content), slide_target)

    # 从内容中提取标题（取第一行非空行）
    lines = [l.strip() for l in processed.split("\n") if l.strip()]
    title = lines[0] if lines else "待确认"

    # 解析内容为幻灯片
    bullets = [line.lstrip("- *0123456789.、)") for line in lines[1:] if line.strip()]

    slides = []
    for i, bullet in enumerate(bullets[:target - 2], 2):  # 保留首页和末页
        slides.append(SlideContent(
            number=i,
            title=bullet[:30] if len(bullet) > 30 else bullet,
            bullets=[bullet],
            section="",
        ))

    # 添加首页
    slides.insert(0, SlideContent(number=1, title=title, section=""))

    presentation = PresentationInfo(
        pres_type=detected_type,
        title=title,
        slides=reindex_slides(slides),
        target_count=target,
        lang=lang,
    )

    result = generate_presentation_markdown(presentation)

    if output_file:
        saved_path = save_markdown(result, output_file)
        print(f"已保存到: {saved_path}")
    else:
        print(result)
