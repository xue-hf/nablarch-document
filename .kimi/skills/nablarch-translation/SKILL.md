---
name: nablarch-translation
description: 我的项目中用于 Nablarch 框架文档翻译的 Skill，提供术语对照、翻译指南和质量保证功能，确保翻译质量和一致性。同时包含了文件翻译状态查询工具说明
---

# Nablarch 文档翻译 Skill

本 Skill 用于辅助 Nablarch 框架文档的中文翻译工作。

## 功能

1. **术语对照** - 提供日文-中文术语对照表，支持动态扩展
2. **翻译指南** - 翻译规范和最佳实践
3. **质量保证** - 确保翻译质量（无日文假名、术语一致）
4. **行数检查** - 检查翻译文件与原文的行数偏差，发现翻译严重不足的文件

> **注意**：翻译进度统一在 `@TRANSLATION_STATUS.md` 中维护。

## TRANSLATION_STATUS.md 格式规范

该文件必须严格遵循以下结构（**不得增加或删除章节**）：

```markdown
# Nablarch 文档中文翻译状态

## 总体进度

| 指标     | 数量         |
| -------- | ------------ |
| 总文件数 | {数字}       |
| 已翻译   | {数字}       |
| 未翻译   | {数字}       |
| **进度** | **{百分比}** |

---

## 各模块翻译状态

| 模块     | 文件数 | 已翻译 | 未翻译 | 进度     |
| -------- | ------ | ------ | ------ | -------- |
| {模块名} | {数字} | {数字} | {数字} | {百分比} |

---

## 剩余未翻译文件

### {模块名}

- `{文件路径}`
```

**约束规则**：

1. 不得增加新的顶级章节（如"翻译历史"、"已完成模块"等）
2. 不得删除现有三个章节（总体进度、各模块翻译状态、剩余未翻译文件）
3. 各模块内的文件列表仅保留文件路径列表，不添加描述文字
4. 数字和百分比通过运行 `python check_translation.py` 确认结果后更新
5. 各模块按字母顺序排列

## 快速开始

### 翻译单个文件

告诉我要翻译的文件：

```
请翻译 ja/application_framework/application_framework/web/architecture.rst
```

AI 应该：

1. 参考现有术语表进行翻译
2. 保持 RST 格式不变
3. 确保翻译后的文件无日文假名（可以通过脚本）

### 批量翻译

```
请批量翻译 application_framework/application_framework/handlers/web/ 下的所有未翻译文件
```

### 更新术语表

发现新术语时，AI 会自动更新术语表：

```
请将 "スレッドコンテキスト" 添加到术语表，翻译为 "线程上下文"
```

### 查看翻译进度

翻译进度统一维护在 `@TRANSLATION_STATUS.md` 中。

如需确认进度，运行：

```bash
python check_translation.py
```

## 文件结构

```
.kimi/skills/nablarch-translation/
├── SKILL.md                    # 本文件
├── guides/
│   ├── TRANSLATION_GUIDE.md    # 翻译指南
│   └── LINE_COUNT_CHECK.md     # 行数偏差检查工具说明
├── terms/
│   └── TERMINOLOGY.md          # 术语对照表（AI维护）
└── scripts/
    └── check_translation.py    # 检查脚本（可选）

项目根目录/
├── check_translation.py        # 翻译状态检查脚本
└── check_line_count_diff.py    # 行数偏差检查脚本
```

## AI 工作流程

### 翻译文件时

1. **读取原文**：从 `ja/` 目录读取日文原文
2. **参考术语**：查询 `TERMINOLOGY.md` 获取术语对照
3. **翻译内容**：
   - 保持 RST 格式不变
   - 标题和正文使用术语表中的翻译
   - 代码注释翻译，代码本身不变

### 翻译文件后

1. **清理临时文件**：删除 `_translated.txt` 和 `_untranslated.txt` 临时文件
2. **质量检查**：确保无日文假名残留
3. **保存文件**：保存到 `zh_CN/` 对应位置
4. **更新术语**：如有新术语，更新术语表
5. **清理临时文件**：删除 `_translated.txt` 和 `_untranslated.txt` 临时文件

### 维护术语表时

1. 从已翻译文件中提取术语对照
2. 去重并分类
3. 更新 `TERMINOLOGY.md`（Markdown 表格格式）

## 术语表使用

### 核心术语

| 日文               | 中文           | 英文         | 备注                             |
| ------------------ | -------------- | ------------ | -------------------------------- |
| ハンドラ           | handler/处理器 | Handler      | 标题用 handler，正文可用"处理器" |
| アクションクラス   | Action类       | Action Class | 类名保留英文                     |
| フォームクラス     | Form类         | Form Class   | 也可说"表单类"                   |
| エンティティクラス | Entity类       | Entity Class | 也可说"实体类"                   |
| バリデーション     | 验证           | Validation   | 也可说"校验"                     |
| バッチ             | Batch          | Batch        | 保留英文                         |

更多术语请参考 `terms/TERMINOLOGY.md`

## 翻译原则

1. **准确性** - 技术术语准确，符合中文技术文档习惯
2. **一致性** - 同一术语全文统一翻译
3. **可读性** - 语句通顺，符合中文表达习惯
4. **保留英文** - 专有名词、Java类名保留英文
5. **无日文假名** - 翻译后的文件不应包含日文假名（平假名/片假名）

## 判断标准

### 文件已翻译

- 文件中**不包含日文假名**（ひらがな/カタカナ）
- 与原文不完全相同

### 术语提取

从已翻译文件中识别：

- 标题对照
- 正文中的术语（日文→中文）
- 括号注释（如：ハンドラ(handler)）

## 与脚本的关系

本 Skill 主要由 AI 驱动，但提供了可选的检查脚本：

### 1. 翻译状态检查脚本

```bash
# 检查所有文件的翻译状态
python check_translation.py

# 检查指定目录的翻译状态
python check_translation.py -d application_framework/handlers

# 检查单个文件的翻译状态
python check_translation.py -f application_framework/handlers/web/index.rst

# 只显示缺失的文件（与-d选项配合使用）
python check_translation.py -d development_tools --missing
```

| 选项              | 说明                               | 示例                                              |
| ----------------- | ---------------------------------- | ------------------------------------------------- |
| `-d, --directory` | 检查指定目录（相对于ja目录的路径） | `-d application_framework/handlers`               |
| `-f, --file`      | 检查单个文件（相对路径）           | `-f application_framework/handlers/web/index.rst` |
| `--missing`       | 只显示缺失的文件（与-d配合使用）   | `-d development_tools --missing`                  |

**判断标准**：

- ✅ **已翻译**：文件不含日文假名（平假名/片假名）
- 🟡 **含日文**：文件包含日文假名，需要翻译
- 🔴 **与原文相同**：文件内容与原文完全一致
- 🔴 **文件缺失**：中文译文文件不存在

### 2. 行数偏差检查脚本

用于检测翻译内容是否严重不足（行数差异过大）：

```bash
# 检查所有文件的行数偏差
python check_line_count_diff.py

# 检查指定目录
python check_line_count_diff.py application_framework/handlers

# 使用阈值 5（更严格）
python check_line_count_diff.py --threshold 5

# 显示详细信息
python check_line_count_diff.py --verbose
```

**输出格式**：
```
文件路径: +偏差值 (日文行数 -> 中文行数)
web/index.rst: +5 (120 -> 125)
web/architecture.rst: -15 (200 -> 185)  [严重不足]
```

**偏差值说明**：

| 偏差值 | 含义 | 建议 |
|--------|------|------|
| +N | 中文比日文多 N 行 | 可能添加了说明，正常 |
| 0 | 行数相同 | 理想状态 |
| -1 ~ -9 | 轻微不足 | 可接受 |
| -10 ~ -20 | 中度不足 | 建议检查 |
| < -20 | 严重不足 | 必须检查 |

> **注意**：脚本位于项目根目录下，使用前先切换到项目根目录。

AI 可以直接完成所有任务，脚本仅作为辅助工具。
