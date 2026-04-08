<div align="center">

# 毛泽东.skill

> *"通过实践而发现真理，又通过实践而证实真理和发展真理。实践、认识、再实践、再认识，这种形式，循环往复以至无穷，而实践和认识之每一循环的内容，都比较地进到了高一级的程度。"*
> > *"孩子，如果你遇到困难或者陷入困境的时候，不妨找我聊一聊；红烧肉里不放酱油"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blueviolet)](https://openclaw.ai)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

战略决策总是找不到方向？<br>
矛盾分析总是抓不住重点？<br>
调查研究总是流于表面？<br>
群众工作总是隔着一层？<br>
战略规划总是缺乏章法？<br>

**将毛泽东的智慧蒸馏为AI可用的方法论工具，让伟人思想指导现代实践！**

<br>

提供毛泽东著作原文（实践论、矛盾论、论持久战、毛选全卷）<br>
生成一个**真正能运用毛式思维的AI Skill**<br>
用他的矛盾分析法分析问题，用他的实践论指导工作，用他的群众路线服务人民

[著作来源](#核心著作来源) · [安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [详细技术文档](docs/TECHNICAL.md)

[**English**](README_EN.md) · [**中文**](README.md) · [**Español**](README_ES.md) · [**日本語**](README_JA.md) · [**Русский**](README_RU.md)

</div>

---

> 🆕 **2026.04.08 第一阶段扩展完成** — 毛泽东.skill v1.1.0 扩展版发布！
>
> **第一阶段扩展成果**：
> - ✅ **知识库结构扩展**：新增speeches、letters、annotations等目录
> - ✅ **概念词典增强**：从70+扩展到150+毛泽东核心概念
> - ✅ **文本分析升级**：新增论证结构分析、比喻识别、修辞模式识别
> - ✅ **验证机制建立**：创建测试套件，包含7个验证用例
> - ✅ **实用命令增加**：新增`/mao-analyze`系列专门分析命令
>
> 基于colleague-skill框架构建，完整实现毛式方法论体系，可直接用于战略分析、矛盾解决、调查研究等场景。
>
> 👉 **[立即体验](#使用)**
>
> 已集成：实践论分析 · 矛盾论分析 · 持久战思维 · 调查研究法 · 群众路线法
>
> 🚀 项目已开源，欢迎Star和贡献！

---

Created by [Abner](https://github.com/wwwaapplleecu-source) | Powered by OpenClaw · Colleague-Skill Framework

> **April 8th Update：** 项目已在GitHub开源，包含完整的源代码、示例文件和详细的文档说明！

## 核心著作来源

> 毛泽东.skill基于原始毛泽东著作构建，确保方法论的纯正性和准确性。

| 著作类别 | 核心著作 | 方法论贡献 | 人格风格 | 应用场景 |
|----------|:--------:|:----------:|:--------:|----------|
| **哲学方法论** | 《实践论》 | 实践-认识循环 | 实事求是 | 认识论指导 |
| **哲学方法论** | 《矛盾论》 | 矛盾分析法 | 辩证思维 | 问题分析 |
| **军事战略** | 《论持久战》 | 持久战理论 | 战略定力 | 长期规划 |
| **综合选集** | 《毛泽东选集》1-4卷 | 综合方法论 | 完整人格 | 全面指导 |
| **工作方法** | 《反对本本主义》 | 调查研究法 | 务实作风 | 调研指导 |
| **群众工作** | 《关心群众生活》 | 群众路线法 | 人民立场 | 群众工作 |

### 推荐的著作获取渠道

以下为公开可得的毛泽东著作资源，本项目不包含著作原文，仅提供处理工具和Skill生成框架：

| 渠道 | 格式 | 说明 |
|------|------|------|
| 人民出版社 | 纸质/电子 | 官方权威版本 |
| 马克思主义文库 | 在线/电子 | 免费数字资源 |
| 学习强国平台 | 在线 | 官方学习平台 |
| 各大学图书馆 | 多种格式 | 学术研究资源 |

> 建议使用官方或权威版本，确保内容的准确性和完整性。

---

## 安装

### OpenClaw

```bash
# 安装到OpenClaw技能目录
git clone https://github.com/wwwaapplleecu-source/mao-skill ~/.openclaw/workspace/skills/mao-colleague
```

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/wwwaapplleecu-source/mao-skill .claude/skills/mao-colleague

# 或安装到全局（所有项目都能用）
git clone https://github.com/wwwaapplleecu-source/mao-skill ~/.claude/skills/mao-colleague
```

### 依赖安装

```bash
pip3 install -r requirements.txt
```

> 文本处理需要jieba分词和pypinyin库，详见 [requirements.txt](requirements.txt)

---

## 使用

在支持的环境中输入：

```
/mao
```

或使用特定命令调用不同功能：

| 命令 | 说明 |
|------|------|
| `/mao` | 调用完整Skill（Persona + Work） |
| `/mao-work` | 仅工作能力（方法论体系） |
| `/mao-persona` | 仅人物性格（表达风格） |

### 管理命令

| 命令 | 说明 |
|------|------|
| `/list-mao-versions` | 列出Skill版本信息 |
| `/mao-help` | 显示帮助信息 |

### 快速开始

如果你只是想使用毛泽东.skill，不需要创建过程：

1. 复制 `colleagues/mao/` 目录下的所有文件到你的技能目录
2. 在支持的环境中调用：
   ```bash
   /mao 分析当前项目的主要矛盾
   /mao-work 制定用户调研方案
   /mao-persona 用毛式风格写动员讲话
   ```

---

## 效果示例

> 输入：`/mao 分析公司销售额下降的问题`

**场景一：矛盾分析**

```
用户 ❯ 分析公司销售额下降的问题

毛泽东.skill ❯ 首先要找出主要矛盾。销售额下降是现象，不是本质。
我们要分析内部矛盾：是产品质量问题？是市场策略问题？还是销售团队问题？
也要分析外部矛盾：市场竞争加剧？消费者需求变化？政策环境影响？
抓住主要矛盾，问题就迎刃而解。
```

**场景二：战略制定**

```
用户 ❯ 制定新市场进入战略

毛泽东.skill ❯ 市场进入如用兵，要讲究战略战术。第一阶段（防御）：深入调研，了解市场，建立据点。
第二阶段（相持）：试点推广，积累经验，站稳脚跟。第三阶段（反攻）：全面铺开，扩大战果。
要集中优势资源，先打歼灭战，再打运动战。
```

**场景三：工作方法**

```
用户 ❯ /mao-work 如何开展用户需求调研

毛泽东.skill ❯ 调查研究是基本功。第一，亲自到一线，与用户面对面交流。
第二，典型调查与普遍调查结合，既深入又全面。第三，材料要丰富，观点要准确。
第四，分析要客观，结论要可靠。没有调查，就没有发言权；没有正确的调查，同样没有发言权。
```

---

## 功能特性

### 生成的 Skill 结构

每个毛泽东.skill由两部分组成，共同驱动输出：

| 部分 | 内容 |
|------|------|
| **Part A — Work Skill** | 负责方法论体系：实践论、矛盾论、调查研究法、群众路线法 |
| **Part B — Persona** | 6层人格结构：核心性格 → 世界观 → 表达风格 → 决策模式 → 人际行为 → 知识结构 |

运行逻辑：`接到任务 → Persona 判断风格 → Work Skill 执行分析 → 用毛式语气输出`

### 核心方法论

**实践论方法**：实践 → 认识 → 再实践 → 再认识
**矛盾论方法**：对立统一规律，主要矛盾分析，矛盾转化
**调查研究法**：没有调查就没有发言权，典型与普遍结合
**群众路线法**：从群众中来，到群众中去
**持久战思维**：防御 → 相持 → 反攻，集中优势兵力

### 表达风格特征

**高频词汇**：实事求是、群众路线、矛盾、斗争、团结、革命、实践、认识
**句式特点**：长短结合、善用设问、排比句式、对比鲜明
**修辞手法**：比喻生动、典故信手、对比强烈、引用经典

### 进化机制

- **追加著作** → 自动分析增量 → merge进对应部分，丰富知识库
- **对话纠正** → 说「这里应该更强调实践」→ 写入Correction层，立即生效
- **版本管理** → 每次更新自动存档，支持方法论演进追踪

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准，基于colleague-skill框架构建：

```
mao-colleague/
├── SKILL.md                 # skill 入口（官方 frontmatter）
├── prompts/                 # Prompt 模板
│   ├── mao_work_analyzer.md    # 毛式方法论分析
│   ├── mao_persona_analyzer.md # 毛式人格分析
│   ├── mao_work_builder.md     # work.md 生成模板
│   └── mao_persona_builder.md  # persona.md 六层结构模板
├── tools/                   # Python 工具
│   └── text_processor.py    # 文本处理器（含毛泽东概念词典）
├── knowledge/               # 原始著作（示例）
│   ├── methodology/         # 方法论著作
│   ├── military/            # 军事著作
│   └── selected_works/      # 选集著作
├── processed/               # 处理后的结构化数据
├── colleagues/              # 生成的毛泽东 Skill
│   └── mao/
│       ├── SKILL.md        # 主入口文件
│       ├── work.md         # 方法论体系
│       ├── persona.md      # 人格风格
│       └── meta.json       # 元数据
├── LICENSE
└── requirements.txt
```

---

## 注意事项

- **著作质量决定Skill质量**：完整著作 > 节选片段 > 他人解读
- 建议优先使用：原著原文 > 权威版本 > 学术研究
- 保持学术中立，专注于方法论和思维方式的提取
- 不讨论敏感历史时期和事件，专注于智慧传承

### 学术研究价值

> **毛泽东.skill：基于知识蒸馏的历史人物AI技能生成框架**
>
> 本项目展示了如何将历史人物的著作和思想蒸馏为可操作的AI技能，为历史研究、领导力培养、战略思维训练提供了新的技术路径。
>
> 👉 **[查看技术报告](docs/TECHNICAL_REPORT.md)**
>
> 涵盖：知识蒸馏方法、双层架构设计、文本处理技术、技能评估标准

---

## Star History

<a href="https://www.star-history.com/#wwwaapplleecu-source/mao-skill&Date">
 <picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=wwwaapplleecu-source/mao-skill&type=date&theme=dark" />
 <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=wwwaapplleecu-source/mao-skill&type=date" />
 <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=wwwaapplleecu-source/mao-skill&type=date" />
 </picture>
</a>

---

<div align="center">

MIT License © [Abner](https://github.com/wwwaapplleecu-source) | 基于 [colleague-skill](https://github.com/titanwings/colleague-skill) 框架构建

**智慧传承，方法永存**

</div>
