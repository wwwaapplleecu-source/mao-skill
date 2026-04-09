# 六层认知架构设计文档

## 🏗️ 架构概览

### 设计目标
1. **清晰的分层**：各层职责明确，便于开发和维护
2. **智能的路由**：基于内容分析自动选择最佳处理方法
3. **统一的接口**：标准化的数据交换格式和错误处理
4. **可扩展的设计**：支持新功能和新层的轻松添加
5. **向后兼容**：保持现有所有功能的正常工作

### 架构层次
```
┌─────────────────────────────────────────────┐
│            用户界面层 (UI Layer)            │
│  • 接收用户输入，格式化请求                │
│  • 展示最终结果，处理用户交互              │
│  • 当前实现：命令解析器                    │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│         入口网关层 (Gateway Layer)          │
│  • 统一请求接收和分发                      │
│  • 权限控制和限流                          │
│  • 日志记录和监控                          │
│  • 今日实现：router.py                     │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│        分析决策层 (Analytics Layer)         │
│  • 智能推荐和分析方法选择                  │
│  • 问题类型识别和分类                      │
│  • 当前实现：智能推荐器                    │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│          方法执行层 (Method Layer)          │
│  • 具体分析方法的执行                      │
│  • 方法论的应用和组合                      │
│  • 当前实现：各分析方法模块                │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│         知识检索层 (Knowledge Layer)        │
│  • 概念和知识查询                          │
│  • 文献和案例检索                          │
│  • 当前实现：概念系统、学习系统            │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│          数据存储层 (Storage Layer)         │
│  • 结构化数据存储                          │
│  • 概念关系网络存储                        │
│  • 用户学习进度存储                        │
│  • 当前实现：各种JSON数据文件              │
└─────────────────────────────────────────────┘
```

---

## 📋 各层详细设计

### 1. 用户界面层 (UI Layer)

#### 职责
- 接收用户原始输入（命令、问题等）
- 格式化请求为标准格式
- 展示处理结果给用户
- 处理用户交互和反馈

#### 当前实现
- `tools/command_parser.py` - 命令解析器
- `tools/mao_skill_integration.py` - 集成系统

#### 接口规范
```python
# 输入格式
{
    "raw_input": "/mao analyze --method=矛盾 分析问题",
    "user_id": "default_user",
    "timestamp": "2026-04-09T17:15:00Z"
}

# 输出格式
{
    "success": True,
    "response": "## 🔍 问题分析: ...",
    "processing_time": 1.23,
    "layer_trace": ["ui", "gateway", "analytics", "method", "knowledge"]
}
```

### 2. 入口网关层 (Gateway Layer)

#### 职责
- 统一接收所有请求
- 请求验证和预处理
- 路由分发到适当的处理层
- 监控和日志记录
- 限流和错误处理

#### 核心实现
- `architecture/router.py` - 核心路由机制
- `architecture/middleware.py` - 中间件支持

#### 路由逻辑
```python
# 路由决策逻辑
def route_request(request):
    if request.get('command') == 'analyze':
        return 'analytics_layer'
    elif request.get('command') == 'learn':
        return 'knowledge_layer' 
    elif request.get('command') == 'concepts':
        return 'knowledge_layer'
    else:
        return 'analytics_layer'  # 默认路由
```

### 3. 分析决策层 (Analytics Layer)

#### 职责
- 分析用户问题的类型和需求
- 推荐最适合的分析方法
- 决策处理流程和参数
- 组合多个方法处理复杂问题

#### 当前实现
- `tools/smart_recommender.py` - 智能推荐器

#### 推荐算法
```python
# 推荐逻辑
def recommend_method(question):
    # 1. 关键词提取
    keywords = extract_keywords(question)
    
    # 2. 方法匹配
    method_scores = {}
    for method, method_keywords in METHOD_KEYWORDS.items():
        score = calculate_match_score(keywords, method_keywords)
        method_scores[method] = score
    
    # 3. 智能选择
    best_method = max(method_scores, key=method_scores.get)
    confidence = method_scores[best_method]
    
    return {
        'method': best_method,
        'confidence': confidence,
        'alternative_methods': get_alternatives(method_scores)
    }
```

### 4. 方法执行层 (Method Layer)

#### 职责
- 执行具体的分析方法
- 组合多个方法处理复杂问题
- 管理方法执行的状态和结果
- 处理方法间的依赖和协调

#### 方法分类
1. **矛盾分析法** - 对立统一规律的应用
2. **实践论方法** - 实践-认识循环指导
3. **调查研究法** - 没有调查就没有发言权
4. **战略思维法** - 持久战和战略规划
5. **群众路线法** - 从群众中来，到群众中去
6. **综合分析法** - 多角度综合判断

### 5. 知识检索层 (Knowledge Layer)

#### 职责
- 概念和知识的查询和检索
- 文献和案例的搜索和匹配
- 学习内容的组织和递送
- 用户学习进度的跟踪和管理

#### 当前实现
- 概念查询系统
- 渐进式学习系统
- 案例库和文献库

#### 知识组织
```python
# 知识结构
knowledge_structure = {
    'concepts': {
        '矛盾': {'definition': '...', 'related': ['主要矛盾', '次要矛盾']},
        '实践': {'definition': '...', 'related': ['实践论', '认识论']}
    },
    'works': {
        '矛盾论': {'content': '...', 'concepts': ['矛盾', '对立统一']},
        '实践论': {'content': '...', 'concepts': ['实践', '认识']}
    },
    'learning_paths': {
        '入门': {'modules': [...], 'duration': 15},
        '基础': {'modules': [...], 'duration': 60}
    }
}
```

### 6. 数据存储层 (Storage Layer)

#### 职责
- 结构化数据的持久化存储
- 概念关系网络的存储和查询
- 用户状态和学习进度的存储
- 系统配置和元数据的存储

#### 存储策略
1. **JSON文件存储** - 配置、概念数据、学习内容
2. **内存缓存** - 热点数据的快速访问
3. **文件缓存** - 中间结果的持久化缓存
4. **日志文件** - 系统运行日志和用户行为日志

---

## 🔄 数据流设计

### 正常处理流程
```
用户输入 → UI层解析 → 网关层路由 → 分析层决策 → 方法层执行 → 知识层检索 → 结果整合 → 用户展示
```

### 异常处理流程
```
错误发生 → 错误捕获 → 错误分类 → 错误处理 → 用户提示 → 日志记录 → 系统恢复
```

### 缓存流程
```
请求到达 → 检查缓存 → 缓存命中 → 直接返回 → 缓存未命中 → 正常处理 → 结果缓存
```

### 性能监控流程
```
请求开始 → 记录开始时间 → 处理过程 → 记录结束时间 → 计算耗时 → 更新统计 → 监控报警
```

---

## 🧩 接口定义

### 层间通信协议

#### 请求格式
```python
{
    "request_id": "req_20260409171500_001",
    "layer_source": "ui_layer",
    "layer_target": "gateway_layer",
    "payload": {
        "command": "analyze",
        "method": "矛盾",
        "question": "分析公司部门协作问题",
        "options": {"style": "work"}
    },
    "metadata": {
        "user_id": "default_user",
        "timestamp": "2026-04-09T17:15:00Z",
        "session_id": "sess_001"
    }
}
```

#### 响应格式
```python
{
    "request_id": "req_20260409171500_001",
    "success": True,
    "layer_source": "method_layer",
    "layer_target": "gateway_layer",
    "payload": {
        "method_used": "矛盾分析",
        "analysis_result": "## 🔍 问题分析...",
        "concepts_used": ["主要矛盾", "次要矛盾"],
        "processing_time": 1.23
    },
    "metadata": {
        "processing_steps": ["ui", "gateway", "analytics", "method"],
        "cache_hit": False,
        "error_message": None
    },
    "errors": []
}
```

#### 错误格式
```python
{
    "error_code": "ANALYTICS_001",
    "error_type": "method_recommendation_error",
    "error_message": "无法推荐分析方法",
    "error_details": {
        "question": "分析问题",
        "extracted_keywords": [],
        "recommendation_scores": {}
    },
    "suggested_fix": "请尝试指定分析方法，如：/mao analyze --method=矛盾 分析问题",
    "retry_possible": True,
    "fallback_method": "综合"
}
```

---

## 🔧 核心实现

### 路由器实现 (router.py)

```python
class SixLayerRouter:
    """六层架构路由器"""
    
    def __init__(self):
        # 初始化各层实例
        self.layers = {
            'gateway': GatewayLayer(),
            'analytics': AnalyticsLayer(),
            'method': MethodLayer(),
            'knowledge': KnowledgeLayer()
        }
        
        # 初始化中间件
        self.middlewares = [
            LoggingMiddleware(),
            CachingMiddleware(),
            ErrorHandlingMiddleware()
        ]
    
    def process_request(self, request):
        """处理请求的完整流程"""
        
        # 应用中间件（预处理）
        for middleware in self.middlewares:
            request = middleware.pre_process(request)
        
        try:
            # 1. 网关层处理
            gateway_result = self.layers['gateway'].process(request)
            
            # 2. 路由决策
            target_layer = self._route_to_layer(gateway_result)
            
            # 3. 目标层处理
            if target_layer == 'analytics':
                result = self.layers['analytics'].process(gateway_result)
            elif target_layer == 'method':
                result = self.layers['method'].process(gateway_result)
            elif target_layer == 'knowledge':
                result = self.layers['knowledge'].process(gateway_result)
            else:
                # 默认路由到分析层
                result = self.layers['analytics'].process(gateway_result)
            
            # 4. 结果格式化
            formatted_result = self._format_result(result, request)
            
            # 应用中间件（后处理）
            for middleware in self.middlewares:
                formatted_result = middleware.post_process(formatted_result)
            
            return formatted_result
            
        except Exception as e:
            # 错误处理
            error_result = self._handle_error(e, request)
            return error_result
```

### 性能监控实现

```python
class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.alerts = []
    
    @contextmanager
    def measure_time(self, operation_name):
        """测量操作时间"""
        start_time = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start_time
            self.metrics[f"{operation_name}_time"].append(elapsed)
            
            # 检查是否超时
            if elapsed > 5.0:  # 5秒超时
                self.alert(f"{operation_name} 超时: {elapsed:.2f}秒")
    
    def alert(self, message):
        """发送性能警报"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "severity": "warning"
        }
        self.alerts.append(alert)
        
        # 可以扩展到发送通知等
        print(f"[性能警报] {message}")
```

### 缓存实现

```python
class SmartCache:
    """智能缓存系统"""
    
    def __init__(self, max_size=1000, ttl_seconds=300):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.hit_count = 0
        self.miss_count = 0
    
    def get(self, key):
        """获取缓存值"""
        if key in self.cache:
            entry = self.cache[key]
            # 检查是否过期
            if time.time() - entry['timestamp'] < self.ttl:
                self.hit_count += 1
                return entry['value']
            else:
                # 过期删除
                del self.cache[key]
        
        self.miss_count += 1
        return None
    
    def set(self, key, value):
        """设置缓存值"""
        # 如果缓存满了，删除最老的项
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), 
                            key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
    
    def hit_rate(self):
        """计算缓存命中率"""
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0
```

---

## 🧪 测试策略

### 单元测试
- 每层独立测试
- 接口一致性测试
- 错误处理测试

### 集成测试
- 层间集成测试
- 端到端流程测试
- 性能集成测试

### 性能测试
- 响应时间测试
- 并发压力测试
- 内存使用测试

### 兼容性测试
- 向后兼容测试
- 数据迁移测试
- 升级路径测试

---

## 📈 监控指标

### 业务指标
- 请求处理成功率
- 平均响应时间
- 用户满意度评分

### 性能指标
- 各层处理时间
- 缓存命中率
- 内存使用率

### 系统指标
- 错误率
- 超时率
- 资源使用率

### 用户指标
- 功能使用频率
- 学习完成率
- 用户留存率

---

## 🔄 部署与运维

### 开发环境
- 完整的本地测试环境
- 自动化测试套件
- 开发文档和指南

### 生产环境
- 性能监控和报警
- 日志收集和分析
- 备份和恢复机制

### 升级策略
- 渐进式升级
- 回滚方案
- 数据迁移工具

---

## 📚 附录

### 术语表
- **六层认知架构**：本系统采用的分层架构设计
- **层间通信**：各层之间的数据交换机制
- **智能路由**：基于内容分析的路由决策
- **性能监控**：系统运行状态的监控和分析

### 设计原则
1. **单一职责原则**：每层只负责一个明确的功能
2. **接口隔离原则**：层间通过明确定义的接口通信
3. **依赖倒置原则**：高层不依赖低层具体实现
4. **开闭原则**：对扩展开放，对修改关闭

### 参考文档
- 《毛泽东.skill 项目概述》
- 《第三阶段用户体验优化计划》
- 《智能推荐器设计文档》
- 《学习系统设计文档》

---

**版本**: 1.0  
**创建时间**: 2026年4月9日  
**更新记录**:  
- v1.0: 初始版本，完整定义六层认知架构