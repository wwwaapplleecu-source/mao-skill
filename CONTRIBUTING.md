# 为毛泽东.skill贡献指南

欢迎为毛泽东.skill项目贡献内容！本项目旨在构建一个完整的毛泽东方法论AI Skill，需要更多毛泽东著作资料和代码改进。

## 📚 如何贡献毛泽东著作

### 1. 著作分类标准

毛泽东著作按以下分类存放：

| 分类 | 目录 | 内容示例 | 文件格式 |
|------|------|----------|----------|
| **方法论类** | `knowledge/methodology/` | 《实践论》《矛盾论》 | `.md` |
| **军事类** | `knowledge/military/` | 《论持久战》 | `.md` |
| **选集类** | `knowledge/selected_works/` | 《毛泽东选集》 | `.md` |
| **重要讲话** | `knowledge/speeches/` | 在延安文艺座谈会上的讲话 | `.md` |
| **书信** | `knowledge/letters/` | 致徐特立同志的信 | `.md` |
| **批注笔记** | `knowledge/annotations/` | 哲学批注摘录 | `.md` |
| **哲学思考** | `knowledge/philosophy/` | 关于自由与必然的思考 | `.md` |
| **工作方法** | `knowledge/work_methods/` | 关于领导方法的若干问题 | `.md` |

### 2. 文件格式要求

#### 编码
- 必须使用 **UTF-8 编码**
- 文件名使用 **正确的中文名称**
- 内容使用标准简体中文

#### 内容结构
```markdown
# 文章标题

**作者**（可选）
（写作时间，可选）

## 章节标题

正文内容...

## 另一个章节

更多内容...
```

#### 质量要求
- 内容完整，无缺失段落
- 文字准确，无错别字
- 格式清晰，分段合理
- 来源可靠，版本权威

### 3. 获取著作的渠道

#### 推荐渠道
1. **官方出版物**：人民出版社《毛泽东选集》《毛泽东文集》
2. **权威数据库**：马克思主义文库、学习强国平台
3. **学术资源**：各大学图书馆数字资源
4. **公开档案**：党史文献资料

#### 注意事项
- 优先使用官方权威版本
- 注意著作的完整性
- 尊重知识产权
- 保持学术严谨性

### 4. 贡献流程

1. **查找著作**：找到需要添加的毛泽东著作
2. **格式转换**：转换为UTF-8编码的Markdown文件
3. **正确分类**：放入对应的知识库目录
4. **文件命名**：使用正确的中文文件名
5. **提交PR**：通过GitHub提交Pull Request

### 5. 批量处理工具

项目提供了文本处理工具，可以自动处理添加的著作：

```bash
# 处理单个文件
python tools/text_processor.py --file knowledge/speeches/为人民服务.md --output processed/为人民服务.json

# 处理整个目录
python tools/text_processor.py --input-dir knowledge --output-dir processed
```

## 💻 如何贡献代码

### 1. 代码结构

```
mao-colleague/
├── tools/               # 工具脚本
│   ├── text_processor.py    # 文本处理器
│   └── repair_filenames.py  # 文件名修复
├── tests/               # 测试文件
│   ├── validate_skill.py    # 验证脚本
│   └── test_suite.json      # 测试用例
├── prompts/             # Prompt模板
│   ├── mao_work_analyzer.md    # 工作技能分析
│   ├── mao_persona_analyzer.md # 人格分析
│   └── mao_*_builder.md        # 生成模板
├── colleagues/mao/      # Skill文件
│   ├── SKILL.md         # Skill说明
│   ├── work.md          # 工作技能
│   └── persona.md       # 人格风格
└── knowledge/           # 知识库
```

### 2. 开发环境

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
python tests/validate_skill.py --all

# 运行文本处理器
python tools/text_processor.py --input-dir knowledge --output-dir processed
```

### 3. 代码贡献方向

#### 文本分析增强
- 添加新的分析维度
- 改进现有算法
- 优化处理性能

#### 测试框架扩展
- 添加新的测试用例
- 改进验证方法
- 增加性能测试

#### 工具脚本改进
- 添加新的处理功能
- 改进用户界面
- 增加错误处理

#### 文档完善
- 补充使用说明
- 添加开发文档
- 完善API文档

### 4. 提交规范

#### Commit信息格式
```
类型(范围): 描述

详细说明（可选）

相关issue: #123
```

#### 类型说明
- `feat`: 新功能
- `fix`: 修复问题
- `docs`: 文档更新
- `test`: 测试相关
- `refactor`: 代码重构
- `style`: 代码格式
- `chore`: 构建/依赖

#### 示例
```
feat(text_processor): 添加毛泽东比喻识别功能

- 新增extract_mao_analogies函数
- 识别星星之火、纸老虎等经典比喻
- 添加相关测试用例

相关issue: #45
```

## 🔬 如何贡献测试用例

### 1. 测试框架

测试用例保存在 `tests/test_suite.json` 中，按类别组织：

```json
{
  "category": "方法论测试",
  "tests": [
    {
      "name": "矛盾论方法测试",
      "description": "测试矛盾分析方法的准确性",
      "input": "分析当前项目的主要矛盾",
      "expected_keywords": ["主要矛盾", "次要矛盾", "分析", "抓住"]
    }
  ]
}
```

### 2. 测试类型

#### 方法论测试
- 验证毛泽东方法论的准确性
- 测试具体方法的正确应用
- 检查概念使用的准确性

#### 表达风格测试
- 验证毛泽东表达风格的还原度
- 测试特定修辞手法的使用
- 检查语言风格的连贯性

#### 边界测试
- 验证历史局限性的认知
- 测试价值观底线的坚守
- 检查敏感问题的处理

### 3. 添加测试用例

1. 在 `tests/test_suite.json` 中添加新的测试对象
2. 在 `tests/validate_skill.py` 中实现测试逻辑
3. 运行测试验证正确性
4. 提交Pull Request

## 📈 项目路线图

### 第一阶段：基础扩展（已完成）
- ✅ 知识库架构建立
- ✅ 概念词典扩展（70+ → 150+）
- ✅ 文本处理器增强
- ✅ 验证机制建立
- ✅ 实用命令扩展

### 第二阶段：深度优化（进行中）
- 数据填充：添加更多毛泽东著作
- 质量验证：完善测试和验证
- 性能优化：改进处理效率
- 用户体验：优化命令和交互

### 第三阶段：架构升级（计划中）
- 六层认知架构实现
- 智能层间路由系统
- 高级分析功能
- 多模态输出支持

## 🏆 贡献者荣誉

### 核心贡献者
- [Abner](https://github.com/wwwaapplleecu-source) - 项目创建者和维护者

### 著作贡献者
- 欢迎添加您的姓名和贡献内容

### 代码贡献者
- 欢迎添加您的姓名和贡献内容

## 📞 联系方式

- **GitHub Issues**: 报告问题、提出建议
- **Pull Requests**: 提交代码和内容贡献
- **讨论区**: 项目相关讨论

## 📜 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

**感谢您的贡献！让我们共同完善毛泽东.skill，让伟人智慧更好地服务现代实践。**