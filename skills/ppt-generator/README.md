# PPT大纲生成器 (PPT Outline Generator)

将文本内容、大纲或主题描述转换为结构化的 Markdown 格式 PPT 大纲。

## 功能特点

- **7种演示类型**：自动识别商业提案、产品发布、季度复盘、培训、技术分享、项目启动、团队汇报
- **逐页结构**：每页包含标题、要点内容、演讲者备注和布局建议
- **智能页数**：根据类型和内容长度推荐页数，支持自定义
- **中英双语**：根据输入语言自动匹配输出语言
- **多轮交互**：支持增删页面、调整内容深度、修改风格、重新排序

## 使用方式

### 触发方式

- 说"做PPT"、"生成PPT大纲"、"帮我做演示文稿"
- 粘贴文本内容要求转为 PPT 结构
- 说"make a presentation"、"generate slides"

### 示例

**输入**（主题描述）：
```
帮我做一个PPT，下个月要发布新的智能客服产品，
主要卖点：基于大模型、准确率95%、定价只有竞品的60%。
```

**输出**：12页结构化 Markdown PPT 大纲，包含逐页内容、演讲者备注和布局建议。

## 目录结构

```
ppt-generator/
├── SKILL.md              # 技能主文件（指令与流程）
├── manifest.json         # 技能元数据
├── README.md             # 说明文档
├── examples/             # 输入输出示例
│   ├── example-1-product-launch.md
│   ├── example-2-quarterly-review.md
│   └── example-3-technical.md
├── references/           # 参考文档
│   ├── slide-design-guide.md  # 布局设计指南
│   ├── output-templates.md    # 7种PPT类型模板
│   └── writing-guide.md       # 写作风格指南
└── scripts/              # 辅助脚本
    └── format.py         # 类型检测与格式化
```

## 依赖

- Python 3.10+（运行 format.py）

## 作者

丁雨薇
