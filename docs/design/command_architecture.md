# 毛泽东.skill 命令架构重构设计

## 🎯 设计目标

### 1. 核心目标
- **降低记忆负担**：减少用户需要记忆的命令数量
- **提高使用便捷性**：简化命令结构，提高使用效率
- **增强可扩展性**：支持新功能的轻松添加
- **保持向后兼容**：老命令继续支持一段时间

### 2. 具体指标
- **记忆命令数**：从12个减少到≤8个
- **入门时间**：新用户入门时间≤15分钟
- **使用效率**：常用任务操作步骤减少30%

---

## 🔧 架构设计原则

### 1. 主命令+子命令模式
- **统一入口**：所有功能通过`/mao`主命令访问
- **逻辑分组**：相关功能组织在同一子命令下
- **自然语言**：子命令使用自然语言词汇

### 2. 智能引导优先
- **默认智能**：主命令自动选择最佳分析方法
- **可选指定**：支持用户手动指定分析方法
- **解释说明**：推荐方法时说明推荐理由

### 3. 渐进式复杂
- **简单开始**：新手使用最简单命令即可开始
- **逐步深入**：随着使用深入发现更多功能
- **高级可选**：高级功能不影响基础使用

### 4. 一致性原则
- **命名一致**：相似功能使用相似命名
- **参数一致**：相似参数使用相似格式
- **响应一致**：相似操作得到相似响应格式

---

## 📋 新命令架构设计

### 核心命令结构

```
/mao [问题]                     # 快捷方式：智能分析
/mao help                      # 获取帮助（智能引导）
/mao analyze [问题]            # 智能分析（主功能）
/mao learn                     # 学习系统
/mao concepts                  # 概念系统
/mao compare                   # 比较系统
/mao settings                  # 设置系统
```

### 详细命令说明

#### 1. 快捷命令
```
/mao [问题]
```
**功能**: 智能分析快捷方式
**说明**: 等同于`/mao analyze [问题]`
**示例**: 
- `/mao 分析项目主要矛盾`
- `/mao 如何开展调查研究`
- `/mao 制定团队发展计划`

#### 2. 帮助系统
```
/mao help
/mao help [主题]
```
**功能**: 获取帮助和引导
**子命令**:
- `help` - 获取基本帮助和引导
- `help analyze` - 分析方法帮助
- `help learn` - 学习系统帮助
- `help concepts` - 概念系统帮助
- `help compare` - 比较系统帮助

**示例**:
- `/mao help` - 获取总体帮助
- `/mao help analyze` - 获取分析方法帮助

#### 3. 分析系统（核心）
```
/mao analyze [问题]
/mao analyze --method=[方法] [问题]
```
**功能**: 毛泽东方法论分析
**参数**:
- `[问题]` - 需要分析的问题
- `--method` - 指定分析方法（可选）

**支持的方法**:
- `矛盾` - 矛盾分析法
- `实践` - 实践论方法
- `调查` - 调查研究法
- `战略` - 战略思维法
- `群众` - 群众路线法
- `综合` - 综合分析法（默认）

**示例**:
- `/mao analyze 分析市场竞争格局` - 智能选择方法
- `/mao analyze --method=矛盾 识别团队内部问题` - 指定矛盾分析
- `/mao analyze --method=实践 改进工作流程` - 指定实践方法

#### 4. 学习系统
```
/mao learn
/mao learn [主题]
/mao learn --path=[路径]
```
**功能**: 毛泽东方法论学习
**子命令**:
- `learn` - 开始学习（智能推荐路径）
- `learn 矛盾论` - 学习矛盾论
- `learn 实践论` - 学习实践论
- `learn --path=入门` - 指定学习路径

**支持的学习路径**:
- `入门` - 新手入门路径
- `基础` - 基础知识路径
- `进阶` - 进阶应用路径
- `专业` - 专业研究路径

#### 5. 概念系统
```
/mao concepts
/mao concepts [概念]
/mao concepts --search=[关键词]
```
**功能**: 毛泽东概念查询和学习
**子命令**:
- `concepts` - 查看核心概念列表
- `concepts 矛盾` - 查看"矛盾"概念解释
- `concepts --search=群众` - 搜索相关概念

#### 6. 比较系统
```
/mao compare
/mao compare [主题1] [主题2]
/mao compare --aspect=[方面]
```
**功能**: 方法论比较和分析
**子命令**:
- `compare` - 比较系统介绍
- `compare 矛盾论 实践论` - 比较两个方法论
- `compare --aspect=应用场景` - 按方面比较

#### 7. 设置系统
```
/mao settings
/mao settings [选项]
```
**功能**: 个性化设置
**子命令**:
- `settings` - 查看当前设置
- `settings 详细程度=高` - 设置响应详细程度
- `settings 风格=现代` - 设置响应风格

---

## 🔄 向后兼容方案

### 1. 老命令支持
老命令在过渡期内继续支持，但会建议使用新命令。

#### 老命令到新命令的映射：
- `/mao [问题]` → 保持不变
- `/mao-work [问题]` → `/mao analyze --style=work [问题]`
- `/mao-persona [问题]` → `/mao analyze --style=persona [问题]`
- `/mao-analyze 矛盾 [问题]` → `/mao analyze --method=矛盾 [问题]`
- `/mao-concepts` → `/mao concepts`
- `/mao-examples` → `/mao learn --topic=examples`
- `/mao-help` → `/mao help`
- `/mao-version` → 保留或整合到`/mao help version`

### 2. 过渡期策略
**第一阶段（1-2周）**：
- 新老命令同时支持
- 使用老命令时给出迁移建议
- 文档更新为新命令

**第二阶段（3-4周）**：
- 老命令标记为"即将废弃"
- 强烈建议使用新命令
- 提供迁移工具

**第三阶段（5周后）**：
- 老命令可配置是否支持
- 默认关闭老命令支持
- 提供完整迁移指南

---

## 🛠️ 技术实现方案

### 1. 命令解析器设计

#### 核心解析逻辑：
```python
class MaoCommandParser:
    def parse(self, command_text):
        # 1. 去除斜杠，分割命令
        parts = command_text.lstrip('/').split()
        
        # 2. 识别主命令
        if not parts or parts[0] != 'mao':
            return {'error': '无效命令'}
        
        # 3. 解析子命令
        if len(parts) == 1:
            return {'command': 'help'}  # 默认帮助
        
        subcommand = parts[1]
        
        # 4. 根据子命令类型解析
        if subcommand == 'analyze':
            return self._parse_analyze(parts[2:])
        elif subcommand == 'learn':
            return self._parse_learn(parts[2:])
        # ... 其他子命令
```

#### 智能分析命令解析：
```python
def _parse_analyze(self, args):
    result = {
        'command': 'analyze',
        'method': 'auto',  # 默认智能选择
        'question': None
    }
    
    # 解析参数
    i = 0
    while i < len(args):
        if args[i].startswith('--'):
            # 解析选项参数
            if args[i] == '--method':
                if i+1 < len(args):
                    result['method'] = args[i+1]
                    i += 2
            elif args[i] == '--style':
                if i+1 < len(args):
                    result['style'] = args[i+1]
                    i += 2
        else:
            # 问题文本
            result['question'] = ' '.join(args[i:])
            break
    
    return result
```

### 2. 智能方法推荐算法

#### 推荐逻辑：
```python
class MethodRecommender:
    def recommend_method(self, question):
        # 1. 关键词提取
        keywords = self.extract_keywords(question)
        
        # 2. 概念匹配
        matched_concepts = self.match_concepts(keywords)
        
        # 3. 方法评分
        method_scores = self.score_methods(matched_concepts)
        
        # 4. 推荐最佳方法
        best_method = max(method_scores.items(), key=lambda x: x[1])
        
        return {
            'method': best_method[0],
            'confidence': best_method[1],
            'alternative_methods': self.get_alternatives(method_scores)
        }
```

#### 关键词到方法映射表：
```python
METHOD_KEYWORDS = {
    '矛盾': ['矛盾', '冲突', '问题', '对立', '主要', '次要'],
    '实践': ['如何做', '实施', '方法', '步骤', '操作', '执行'],
    '调查': ['调查', '研究', '了解', '数据', '信息', '收集'],
    '战略': ['战略', '规划', '长远', '目标', '方向', '计划'],
    '群众': ['团队', '管理', '群众', '员工', '人员', '组织']
}
```

### 3. 响应生成器设计

#### 响应模板结构：
```python
class ResponseGenerator:
    def generate(self, command_result, question):
        # 1. 确认问题理解
        understanding = self.confirm_understanding(question)
        
        # 2. 方法说明（如果是指定或推荐的方法）
        method_explanation = self.explain_method(command_result['method'])
        
        # 3. 核心分析
        analysis = self.perform_analysis(question, command_result['method'])
        
        # 4. 实践指导
        guidance = self.provide_guidance(analysis)
        
        # 5. 关键概念
        key_concepts = self.extract_key_concepts(analysis)
        
        # 6. 相关推荐
        recommendations = self.get_recommendations(analysis)
        
        # 7. 总结升华
        summary = self.summarize(analysis)
        
        return {
            'understanding': understanding,
            'method': method_explanation,
            'analysis': analysis,
            'guidance': guidance,
            'concepts': key_concepts,
            'recommendations': recommendations,
            'summary': summary
        }
```

---

## 📊 迁移计划

### 第一阶段：设计与准备（第1周）
1. **架构设计**：完成命令架构设计文档
2. **技术方案**：确定技术实现方案
3. **测试计划**：制定迁移测试计划
4. **文档准备**：更新用户文档

### 第二阶段：开发实现（第2周）
1. **命令解析器**：实现新命令解析器
2. **智能推荐**：实现智能方法推荐算法
3. **响应生成器**：更新响应生成器支持新架构
4. **兼容层**：实现老命令兼容层

### 第三阶段：测试验证（第3周）
1. **单元测试**：测试每个命令功能
2. **集成测试**：测试命令组合使用
3. **兼容测试**：测试老命令兼容性
4. **用户测试**：邀请用户测试新命令

### 第四阶段：部署上线（第4周）
1. **灰度发布**：先向部分用户发布
2. **收集反馈**：收集用户反馈和建议
3. **问题修复**：修复发现的问题
4. **全面推广**：向所有用户推广新命令

---

## 🎯 预期效果

### 1. 用户体验提升
- **记忆负担降低**：命令数从12个减少到7个
- **使用效率提高**：常用任务操作步骤减少30%
- **学习曲线降低**：新用户入门时间从30分钟减少到15分钟

### 2. 功能效果提升
- **智能引导使用率**：预计达到60%以上
- **分析方法准确率**：通过智能推荐提高20%
- **用户满意度**：预计提升25%

### 3. 技术质量提升
- **代码可维护性**：命令逻辑更加清晰和模块化
- **扩展性**：新功能添加更加容易
- **测试覆盖率**：命令解析器测试覆盖率≥90%

---

## 📝 风险与应对

### 1. 技术风险
**风险**：智能推荐算法准确率不达标
**应对**：
- 建立多级推荐机制，提供备选方案
- 基于用户反馈持续优化算法
- 允许用户手动选择方法

### 2. 用户接受度风险
**风险**：用户不习惯新命令
**应对**：
- 保持老命令兼容性
- 提供详细的迁移指南
- 通过交互式引导帮助用户适应

### 3. 开发进度风险
**风险**：开发进度滞后
**应对**：
- 优先实现核心功能（分析系统）
- 采用迭代开发，先发布最小可行版本
- 建立严格的进度跟踪机制

### 4. 兼容性风险
**风险**：老命令兼容性出现问题
**应对**：
- 建立完整的兼容性测试
- 提供老命令到新命令的自动转换
- 在过渡期提供双重支持

---

## 🔗 相关文档

1. [用户体验问题诊断报告](./user_experience_diagnosis.md)
2. [第三阶段优化计划](../PHASE3_PLAN.md)
3. [智能推荐算法设计](./smart_recommendation_algorithm.md)（待创建）
4. [响应模板优化设计](./response_template_optimization.md)（待创建）

---

**设计完成时间**: 2026年4月9日 16:00  
**设计负责人**: AI架构设计团队  
**下一步行动**: 开始命令解析器开发和智能推荐算法实现