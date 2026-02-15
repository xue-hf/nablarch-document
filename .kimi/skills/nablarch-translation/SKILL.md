# Nablarch 文档翻译 Skill

本 Skill 用于辅助 Nablarch 框架文档的中文翻译工作。

## 功能

1. **术语对照** - 提供日文-中文术语对照表，支持动态扩展
2. **翻译指南** - 翻译规范和最佳实践
3. **进度跟踪** - 协助维护翻译进度文档
4. **质量保证** - 确保翻译质量（无日文假名、术语一致）

## 快速开始

### 翻译单个文件

告诉我要翻译的文件：

```
请翻译 ja/application_framework/application_framework/web/architecture.rst
```

AI 会：
1. 参考现有术语表进行翻译
2. 保持 RST 格式不变
3. 确保翻译后的文件无日文假名

### 批量翻译

```
请批量翻译 application_framework/application_framework/handlers/web/ 下的所有未翻译文件
```

### 更新术语表

发现新术语时，AI 会自动更新术语表：

```
请将 "スレッドコンテキスト" 添加到术语表，翻译为 "线程上下文"
```

### 更新翻译进度

```
请更新翻译进度文档
```

AI 会：
1. 扫描所有文件
2. 统计翻译进度
3. 更新 TRANSLATION_STATUS.md

## 文件结构

```
.kimi/skills/nablarch-translation/
├── SKILL.md                    # 本文件
├── guides/
│   └── TRANSLATION_GUIDE.md    # 翻译指南
├── terms/
│   └── TERMINOLOGY.md          # 术语对照表（AI维护）
└── scripts/
    └── check_translation.py    # 检查脚本（可选）
```

## AI 工作流程

### 翻译文件时

1. **读取原文**：从 `ja/` 目录读取日文原文
2. **参考术语**：查询 `TERMINOLOGY.md` 获取术语对照
3. **翻译内容**：
   - 保持 RST 格式不变
   - 标题和正文使用术语表中的翻译
   - 代码注释翻译，代码本身不变
4. **质量检查**：确保无日文假名残留
5. **保存文件**：保存到 `zh_CN/` 对应位置
6. **更新术语**：如有新术语，更新术语表

### 更新进度时

1. 扫描 `ja/` 和 `zh_CN/` 目录
2. 对比文件判断是否已翻译
3. 统计数量并计算进度
4. 生成新的 `TRANSLATION_STATUS.md`

### 维护术语表时

1. 从已翻译文件中提取术语对照
2. 去重并分类
3. 更新 `TERMINOLOGY.md`（Markdown 表格格式）

## 术语表使用

### 核心术语

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| ハンドラ | handler/处理器 | Handler | 标题用 handler，正文可用"处理器" |
| アクションクラス | Action类 | Action Class | 类名保留英文 |
| フォームクラス | Form类 | Form Class | 也可说"表单类" |
| エンティティクラス | Entity类 | Entity Class | 也可说"实体类" |
| バリデーション | 验证 | Validation | 也可说"校验" |
| バッチ | Batch | Batch | 保留英文 |

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

```bash
# 检查翻译状态（可选）
python .kimi/skills/nablarch-translation/scripts/check_translation.py
```

AI 可以直接完成所有任务，脚本仅作为辅助工具。
