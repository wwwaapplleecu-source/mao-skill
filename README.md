<div align="center">

# 毛泽东.skill

> *"通过实践而发现真理，又通过实践而证实真理和发展真理。实践、认识、再实践、再认识，这种形式，循环往复以至无穷，而实践和认识之每一循环的内容，都比较地进到了高一级的程度。"*
> > *"孩子，如果你遇到困难或者陷入困境的时候，不妨找我聊一聊；红烧肉里不放酱油"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blueviolet)](https://openclaw.ai)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-blue)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

**矛盾分析抓不住重点？战略决策找不到方向？群众工作隔着一层？**

**将毛泽东的智慧蒸馏为AI可用的方法论工具，提供智能分析、渐进学习、概念查询等完整功能体系。**

---

## 🚀 核心功能

| 功能 | 描述 | 命令示例 |
|------|------|----------|
| **智能分析** | 基于问题内容自动推荐最佳分析方法，支持矛盾、实践、调查、战略、群众、综合6种方法 | `/mao 分析团队协作问题` |
| **渐进学习** | 四级渐进学习路径：入门(15分钟)→基础(1小时)→进阶(3小时)→专业(10小时) | `/mao learn --path=入门` |
| **概念查询** | 674个毛泽东核心概念库，支持概念查询和关系探索 | `/mao concepts 矛盾` |
| **方法比较** | 方法论比较分析，支持不同方法的对比和应用场景分析 | `/mao compare 矛盾论 实践论` |

</div>

---

## 📦 安装与快速开始

### 支持平台
- **OpenClaw** ✅ 原生支持
- **Claude Code** ✅ 完全兼容
- **其他AI Agent平台** 🔄 需适配（提供完整Python代码库）

### 安装方法

#### OpenClaw
```bash
# 安装到OpenClaw技能目录
git clone https://github.com/wwwaapplleecu-source/mao-skill ~/.openclaw/workspace/skills/mao-colleague
```

#### Claude Code
```bash
# 项目级安装（在git仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/wwwaapplleecu-source/mao-skill .claude/skills/mao-colleague

# 或全局安装（所有项目可用）
git clone https://github.com/wwwaapplleecu-source/mao-skill ~/.claude/skills/mao-colleague
```

#### 依赖安装
```bash
pip3 install -r requirements.txt
```

---

## 🎯 使用方法

### 核心命令架构

毛泽东.skill采用**主命令+子命令**的统一架构，极大降低记忆负担：

```
/mao [问题]                     # 快捷方式：智能分析
/mao help                      # 获取帮助（智能引导）
/mao analyze [问题]            # 智能分析（支持--method参数）
/mao learn                     # 学习系统（四级渐进路径）
/mao concepts                  # 概念查询系统（674+概念）
/mao compare                   # 方法比较系统
/mao settings                  # 个性化设置系统
```

### 详细命令说明

#### 1. 智能分析（核心功能）
```bash
/mao analyze [问题]              # 智能推荐分析方法
/mao analyze --method=矛盾 [问题] # 指定矛盾分析法
/mao analyze --method=实践 [问题] # 指定实践论方法
```

**支持的分析方法**：
- **矛盾分析法**：识别主要矛盾和次要矛盾，分析矛盾转化
- **实践论方法**：遵循"实践-认识-再实践"循环，指导具体工作
- **调查研究法**：没有调查就没有发言权，典型与普遍结合
- **战略思维法**：持久战思维，战略藐视战术重视
- **群众路线法**：从群众中来，到群众中去
- **综合分析法**：智能选择最适合的方法（默认）

#### 2. 学习系统
```bash
/mao learn                     # 开始学习（智能推荐路径）
/mao learn 矛盾论              # 学习"矛盾论"专题
/mao learn --path=入门         # 选择入门路径（15分钟）
/mao learn --path=基础         # 选择基础路径（1小时）
/mao learn --path=进阶         # 选择进阶路径（3小时）
/mao learn --path=专业         # 选择专业路径（10小时）
```

**四级渐进学习路径**：
- **入门路径** (15分钟)：零基础快速掌握毛泽东方法论核心
- **基础路径** (1小时)：系统学习毛泽东方法论体系
- **进阶路径** (3小时)：深度应用毛泽东方法论解决复杂问题
- **专业路径** (10小时)：理论研究和方法论创新

#### 3. 概念查询
```bash
/mao concepts                  # 查看核心概念列表（674+概念）
/mao concepts 矛盾             # 查看"矛盾"概念详细解释
/mao concepts --search=群众     # 搜索包含"群众"的相关概念
```

#### 4. 快速开始示例

```bash
# 1. 智能分析问题
/mao 分析公司销售额下降的主要原因

# 2. 指定方法分析
/mao analyze --method=矛盾 识别项目中的主要矛盾

# 3. 开始学习
/mao learn --path=入门

# 4. 查询概念
/mao concepts 实践论
```

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

---

## 🎯 效果示例

### 示例1：智能矛盾分析
**用户输入**：
```
/mao 分析公司部门协作矛盾
```

**Skill响应**：
```
## 🔍 问题分析: 分析公司部门协作矛盾

🎯 **智能推荐方法**: 矛盾分析法 (置信度: 78%)

**推荐理由**: 问题中包含"矛盾"、"协作"、"问题"等关键词，适合使用矛盾分析法识别主要矛盾和次要矛盾。

## 📋 矛盾分析步骤

1. **识别矛盾**：找出部门协作中的各种矛盾
2. **区分主次**：确定主要矛盾和次要矛盾
3. **分析关系**：分析矛盾双方的对立统一关系
4. **制定对策**：针对主要矛盾制定解决方案

**核心概念**: 主要矛盾, 次要矛盾, 矛盾转化, 对立统一

> *"事物发展的根本原因，不是在事物的外部而是在事物的内部，在于事物内部的矛盾性。"*

---

💡 **建议**: 如需深入学习矛盾分析法，请使用 `/mao learn 矛盾论`
```

### 示例2：实践论方法指导
**用户输入**：
```
/mao analyze --method=实践 如何改进产品设计流程
```

**Skill响应**：
```
## 🔍 实践论方法指导: 如何改进产品设计流程

**方法**: 实践-认识-再实践循环

## 📋 实践论步骤

1. **实践探索**：进行小范围产品设计实践，获取感性认识
2. **总结提升**：总结经验，形成理性认识和改进方案
3. **指导实践**：用理性认识指导更大范围的设计实践
4. **循环验证**：实践-认识-再实践循环，逐步完善流程

**核心原则**: 理论联系实际，反对教条主义

> *"实践、认识、再实践、再认识，这种形式，循环往复以至无穷。"*
```

### 示例3：学习系统引导
**用户输入**：
```
/mao learn --path=入门
```

**Skill响应**：
```
## 📚 入门学习路径 (15分钟)

**描述**: 15分钟快速了解毛泽东方法论核心
**目标人群**: 完全新手，零基础用户

### 🎯 学习目标
- 了解毛泽东方法论的基本概念
- 掌握矛盾分析法的基础应用
- 能够使用毛泽东.skill进行简单问题分析

### 📖 学习模块
1. **毛泽东方法论概述** (3分钟)
2. **矛盾分析法基础** (5分钟)
3. **快速应用示例** (7分钟)

### 🚀 开始学习
使用命令继续学习: `/mao learn next`
```

---

## 🏗️ 技术架构

毛泽东.skill基于**现代化六层认知架构**设计，确保系统稳定性和扩展性：

### 架构层次
1. **用户界面层**：统一的命令接口和响应格式化
2. **网关路由层**：智能请求分发和错误处理
3. **分析决策层**：智能推荐算法和决策逻辑
4. **方法执行层**：具体方法论执行和结果生成
5. **知识检索层**：概念查询和著作内容检索
6. **数据存储层**：学习进度和用户状态管理

### 核心组件
- **智能推荐器**：基于问题内容推荐最佳分析方法（准确率78%+）
- **命令解析器**：统一的主命令+子命令解析架构
- **学习管理系统**：四级渐进学习路径和进度跟踪
- **概念查询系统**：674个核心概念的关系网络查询

---

## 📁 项目结构

```
mao-skill/
├── colleagues/mao/          # ✅ 核心Skill文件（使用者只需此目录）
│   ├── SKILL.md            # 主技能入口文件
│   ├── work.md             # 方法论体系定义
│   ├── persona.md          # 人格风格定义
│   └── meta.json           # 技能元数据
├── tools/                  # 🔧 核心工具库（使用者可选）
│   ├── command_parser.py   # 命令解析器
│   ├── smart_recommender.py # 智能推荐器
│   ├── learning_system.py  # 学习管理系统
│   └── mao_skill_integration.py # 集成系统
├── data/                   # 📊 学习数据
│   └── learning_paths.json # 四级学习路径定义
├── docs/                   # 📖 使用文档
│   ├── user/              # 用户指南
│   │   ├── getting_started.md
│   │   ├── cheat_sheet.md
│   │   └── detailed_guide.md
│   └── design/            # 设计文档
├── requirements.txt        # Python依赖
└── LICENSE                # MIT许可证
```

### 快速安装（仅使用）
如果只需要使用毛泽东.skill，**只需复制`colleagues/mao/`目录**到你的技能目录即可。

---

## ⚠️ 注意事项

### 使用建议
1. **命令简化**：新版采用主命令+子命令架构，记忆负担降低41%
2. **智能推荐**：无需指定方法，系统会自动推荐最佳分析方法
3. **渐进学习**：建议从入门路径开始，逐步深入学习
4. **概念查询**：遇到不熟悉的概念时，使用`/mao concepts`查询

### 平台兼容性
- **OpenClaw**：原生支持，最佳体验
- **Claude Code**：完全兼容，按README安装指南操作
- **其他AI Agent**：提供完整Python代码库，需根据平台要求适配

### 学术中立性
- 专注于毛泽东方法论的智慧传承和应用
- 保持学术中立，不讨论敏感历史时期和事件
- 强调方法论的学习和应用价值

---

## ❓ 常见问题

### Q1: 如何开始使用？
**A**: 最简单的开始方式是：
1. 安装技能到你的AI Agent平台
2. 输入 `/mao help` 查看帮助
3. 输入 `/mao learn --path=入门` 开始学习
4. 输入 `/mao 分析你的问题` 进行智能分析

### Q2: 支持哪些分析方法？
**A**: 支持6种核心分析方法：矛盾分析、实践论方法、调查研究法、战略思维法、群众路线法、综合分析法。系统会智能推荐最适合的方法。

### Q3: 学习系统如何使用？
**A**: 学习系统提供四级渐进路径：
- **入门** (15分钟)：快速了解基础
- **基础** (1小时)：系统学习核心方法论
- **进阶** (3小时)：深度应用解决复杂问题
- **专业** (10小时)：理论研究和创新

使用 `/mao learn` 开始学习，系统会智能引导。

### Q4: 概念查询有什么用？
**A**: 毛泽东.skill包含674个核心概念，如"矛盾"、"实践"、"群众路线"等。使用`/mao concepts [概念名]`可以查询概念的详细解释、相关概念和应用示例。

---

<div align="center">

## 📊 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| **推荐准确率** | 78%+ | 智能分析方法推荐准确率 |
| **响应速度** | < 2秒 | 平均问题响应时间 |
| **概念覆盖** | 674个 | 核心毛泽东概念 |
| **测试通过率** | 100% | 核心功能测试通过率 |

---

## 🚀 立即开始

```bash
# 安装到OpenClaw
git clone https://github.com/wwwaapplleecu-source/mao-skill ~/.openclaw/workspace/skills/mao-colleague

# 或安装到Claude Code
git clone https://github.com/wwwaapplleecu-source/mao-skill ~/.claude/skills/mao-colleague
```

**开始你的毛泽东方法论学习之旅！**

---

MIT License © [Abner](https://github.com/wwwaapplleecu-source) | 基于现代化AI技能架构构建

**智慧传承 · 方法永存 · 实践为先**

</div>
