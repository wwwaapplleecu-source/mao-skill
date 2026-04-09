#!/usr/bin/env python3
"""
六层认知架构协议定义

定义层间通信的标准数据格式、错误代码和接口规范
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum

class LayerType(Enum):
    """层类型枚举"""
    UI = "ui_layer"           # 用户界面层
    GATEWAY = "gateway_layer" # 入口网关层
    ANALYTICS = "analytics_layer"  # 分析决策层
    METHOD = "method_layer"   # 方法执行层
    KNOWLEDGE = "knowledge_layer"  # 知识检索层
    STORAGE = "storage_layer" # 数据存储层

class RequestType(Enum):
    """请求类型枚举"""
    ANALYZE = "analyze"       # 分析请求
    LEARN = "learn"           # 学习请求
    CONCEPTS = "concepts"     # 概念请求
    COMPARE = "compare"       # 比较请求
    HELP = "help"             # 帮助请求
    SETTINGS = "settings"     # 设置请求

class ErrorCode(Enum):
    """错误代码枚举"""
    # 通用错误 (00-99)
    UNKNOWN_ERROR = "GENERAL_001"
    INVALID_REQUEST = "GENERAL_002"
    TIMEOUT_ERROR = "GENERAL_003"
    RESOURCE_LIMIT = "GENERAL_004"
    
    # 网关层错误 (100-199)
    GATEWAY_VALIDATION = "GATEWAY_001"
    GATEWAY_RATE_LIMIT = "GATEWAY_002"
    GATEWAY_AUTH_ERROR = "GATEWAY_003"
    
    # 分析层错误 (200-299)
    ANALYTICS_RECOMMENDATION = "ANALYTICS_001"
    ANALYTICS_CLASSIFICATION = "ANALYTICS_002"
    ANALYTICS_NO_METHOD = "ANALYTICS_003"
    
    # 方法层错误 (300-399)
    METHOD_EXECUTION = "METHOD_001"
    METHOD_NOT_FOUND = "METHOD_002"
    METHOD_INVALID_PARAMS = "METHOD_003"
    
    # 知识层错误 (400-499)
    KNOWLEDGE_NOT_FOUND = "KNOWLEDGE_001"
    KNOWLEDGE_QUERY_ERROR = "KNOWLEDGE_002"
    KNOWLEDGE_FORMAT_ERROR = "KNOWLEDGE_003"
    
    # 存储层错误 (500-599)
    STORAGE_READ_ERROR = "STORAGE_001"
    STORAGE_WRITE_ERROR = "STORAGE_002"
    STORAGE_FORMAT_ERROR = "STORAGE_003"

class Protocol:
    """协议工具类"""
    
    @staticmethod
    def create_request(
        raw_input: str,
        source_layer: LayerType,
        target_layer: LayerType,
        request_type: Optional[RequestType] = None,
        user_id: str = "default_user",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        创建标准请求
        
        Args:
            raw_input: 原始输入内容
            source_layer: 源层
            target_layer: 目标层
            request_type: 请求类型
            user_id: 用户ID
            metadata: 额外元数据
            
        Returns:
            标准请求字典
        """
        # 生成请求ID
        import time
        import hashlib
        timestamp = int(time.time() * 1000)
        random_part = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        request_id = f"req_{timestamp}_{random_part}"
        
        # 构建请求
        request = {
            'request_id': request_id,
            'raw_input': raw_input,
            'source_layer': source_layer.value,
            'target_layer': target_layer.value,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        # 添加请求类型
        if request_type:
            request['request_type'] = request_type.value
        
        # 添加元数据
        if metadata:
            if 'metadata' not in request:
                request['metadata'] = {}
            request['metadata'].update(metadata)
        
        return request
    
    @staticmethod
    def create_response(
        request: Dict[str, Any],
        response_data: Any,
        success: bool = True,
        processing_time: Optional[float] = None,
        layer_trace: Optional[List[str]] = None,
        errors: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        创建标准响应
        
        Args:
            request: 原始请求
            response_data: 响应数据
            success: 是否成功
            processing_time: 处理时间
            layer_trace: 处理层跟踪
            errors: 错误列表
            
        Returns:
            标准响应字典
        """
        response = {
            'request_id': request.get('request_id', 'unknown'),
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        # 添加响应数据
        if success:
            response['data'] = response_data
        else:
            response['error_data'] = response_data
        
        # 添加处理信息
        if processing_time is not None:
            response['processing_time'] = processing_time
        
        if layer_trace:
            response['layer_trace'] = layer_trace
        
        # 添加错误信息
        if errors:
            response['errors'] = errors
        elif not success and not errors:
            # 如果失败但没有提供错误，创建默认错误
            response['errors'] = [{
                'error_code': ErrorCode.UNKNOWN_ERROR.value,
                'error_message': '处理失败，但未提供具体错误信息'
            }]
        
        # 添加请求元数据引用
        response['request_metadata'] = {
            'user_id': request.get('user_id'),
            'original_timestamp': request.get('timestamp'),
            'source_layer': request.get('source_layer')
        }
        
        return response
    
    @staticmethod
    def create_error(
        error_code: ErrorCode,
        error_message: str,
        error_details: Optional[Dict[str, Any]] = None,
        suggested_fix: Optional[str] = None,
        retry_possible: bool = True,
        fallback_action: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        创建标准错误
        
        Args:
            error_code: 错误代码
            error_message: 错误消息
            error_details: 错误详情
            suggested_fix: 建议修复方法
            retry_possible: 是否可重试
            fallback_action: 备用操作
            
        Returns:
            标准错误字典
        """
        error = {
            'error_code': error_code.value,
            'error_message': error_message,
            'timestamp': datetime.now().isoformat(),
            'retry_possible': retry_possible
        }
        
        if error_details:
            error['error_details'] = error_details
        
        if suggested_fix:
            error['suggested_fix'] = suggested_fix
        
        if fallback_action:
            error['fallback_action'] = fallback_action
        
        return error
    
    @staticmethod
    def validate_request(request: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        验证请求格式
        
        Args:
            request: 要验证的请求
            
        Returns:
            错误列表，空列表表示验证通过
        """
        errors = []
        
        # 检查必要字段
        required_fields = ['request_id', 'raw_input', 'source_layer', 'target_layer', 'user_id']
        for field in required_fields:
            if field not in request:
                errors.append(Protocol.create_error(
                    ErrorCode.INVALID_REQUEST,
                    f"缺少必要字段: {field}"
                ))
        
        # 检查字段类型
        if 'raw_input' in request and not isinstance(request['raw_input'], str):
            errors.append(Protocol.create_error(
                ErrorCode.INVALID_REQUEST,
                "raw_input 必须是字符串"
            ))
        
        if 'user_id' in request and not isinstance(request['user_id'], str):
            errors.append(Protocol.create_error(
                ErrorCode.INVALID_REQUEST,
                "user_id 必须是字符串"
            ))
        
        # 检查层类型
        if 'source_layer' in request:
            valid_layers = [layer.value for layer in LayerType]
            if request['source_layer'] not in valid_layers:
                errors.append(Protocol.create_error(
                    ErrorCode.INVALID_REQUEST,
                    f"无效的源层: {request['source_layer']}，有效值: {valid_layers}"
                ))
        
        if 'target_layer' in request:
            valid_layers = [layer.value for layer in LayerType]
            if request['target_layer'] not in valid_layers:
                errors.append(Protocol.create_error(
                    ErrorCode.INVALID_REQUEST,
                    f"无效的目标层: {request['target_layer']}，有效值: {valid_layers}"
                ))
        
        return errors
    
    @staticmethod
    def validate_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        验证响应格式
        
        Args:
            response: 要验证的响应
            
        Returns:
            错误列表，空列表表示验证通过
        """
        errors = []
        
        # 检查必要字段
        required_fields = ['request_id', 'success', 'timestamp']
        for field in required_fields:
            if field not in response:
                errors.append(Protocol.create_error(
                    ErrorCode.INVALID_REQUEST,
                    f"响应缺少必要字段: {field}"
                ))
        
        # 检查success字段类型
        if 'success' in response and not isinstance(response['success'], bool):
            errors.append(Protocol.create_error(
                ErrorCode.INVALID_REQUEST,
                "success 必须是布尔值"
            ))
        
        # 检查错误信息格式
        if 'errors' in response:
            if not isinstance(response['errors'], list):
                errors.append(Protocol.create_error(
                    ErrorCode.INVALID_REQUEST,
                    "errors 必须是列表"
                ))
            else:
                for error in response['errors']:
                    if not isinstance(error, dict):
                        errors.append(Protocol.create_error(
                            ErrorCode.INVALID_REQUEST,
                            "错误项必须是字典"
                        ))
                    elif 'error_code' not in error or 'error_message' not in error:
                        errors.append(Protocol.create_error(
                            ErrorCode.INVALID_REQUEST,
                            "错误项必须包含 error_code 和 error_message"
                        ))
        
        return errors

# ============================================================================
# 数据格式定义
# ============================================================================

class RequestFormats:
    """请求数据格式定义"""
    
    @staticmethod
    def analyze_request(question: str, method: Optional[str] = None, style: str = "work") -> Dict[str, Any]:
        """分析请求格式"""
        return {
            'question': question,
            'method': method,
            'style': style,
            'options': {
                'include_concepts': True,
                'include_examples': True,
                'max_length': 1000
            }
        }
    
    @staticmethod
    def learn_request(path: str = "auto", topic: Optional[str] = None) -> Dict[str, Any]:
        """学习请求格式"""
        return {
            'path': path,
            'topic': topic,
            'options': {
                'include_practice': True,
                'track_progress': True
            }
        }
    
    @staticmethod
    def concepts_request(concept: Optional[str] = None, search: Optional[str] = None) -> Dict[str, Any]:
        """概念请求格式"""
        return {
            'concept': concept,
            'search': search,
            'options': {
                'include_related': True,
                'include_examples': True
            }
        }
    
    @staticmethod
    def compare_request(topic1: str, topic2: str) -> Dict[str, Any]:
        """比较请求格式"""
        return {
            'topic1': topic1,
            'topic2': topic2,
            'options': {
                'include_differences': True,
                'include_similarities': True
            }
        }

class ResponseFormats:
    """响应数据格式定义"""
    
    @staticmethod
    def analyze_response(
        analysis_result: str,
        method_used: str,
        confidence: float,
        concepts_used: List[str],
        processing_time: float
    ) -> Dict[str, Any]:
        """分析响应格式"""
        return {
            'analysis_result': analysis_result,
            'method_used': method_used,
            'confidence': confidence,
            'concepts_used': concepts_used,
            'suggested_actions': [
                f'使用 /mao analyze --method={method_used} 进行类似分析',
                '使用 /mao learn 学习更多方法论',
                '使用 /mao concepts 查看相关概念'
            ],
            'processing_info': {
                'time': processing_time,
                'cache_hit': False
            }
        }
    
    @staticmethod
    def learn_response(
        learning_content: str,
        path: str,
        progress: Dict[str, Any],
        next_steps: List[str],
        processing_time: float
    ) -> Dict[str, Any]:
        """学习响应格式"""
        return {
            'learning_content': learning_content,
            'path': path,
            'progress': progress,
            'next_steps': next_steps,
            'suggested_actions': [
                '使用 /mao learn next 继续学习',
                '使用 /mao learn progress 查看进度',
                '使用 /mao learn recommendations 获取推荐'
            ],
            'processing_info': {
                'time': processing_time,
                'module_completed': False
            }
        }
    
    @staticmethod
    def concepts_response(
        concept_info: Dict[str, Any],
        related_concepts: List[str],
        examples: List[str],
        processing_time: float
    ) -> Dict[str, Any]:
        """概念响应格式"""
        return {
            'concept_info': concept_info,
            'related_concepts': related_concepts,
            'examples': examples,
            'suggested_actions': [
                '使用 /mao analyze 应用这个概念',
                '查看其他相关概念',
                '使用 /mao learn 系统学习'
            ],
            'processing_info': {
                'time': processing_time,
                'concepts_found': len(related_concepts) + 1
            }
        }

# ============================================================================
# 性能监控数据格式
# ============================================================================

class PerformanceMetrics:
    """性能监控数据格式"""
    
    @staticmethod
    def request_metrics(
        request_id: str,
        start_time: datetime,
        end_time: datetime,
        layer_times: Dict[str, float],
        cache_hits: Dict[str, bool],
        memory_usage: Optional[int] = None
    ) -> Dict[str, Any]:
        """请求性能指标"""
        total_time = (end_time - start_time).total_seconds()
        
        return {
            'request_id': request_id,
            'timing': {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'total_time': total_time,
                'layer_times': layer_times
            },
            'cache': cache_hits,
            'resource_usage': {
                'memory_mb': memory_usage,
                'cpu_percent': None  # 可在实际实现中获取
            },
            'efficiency': {
                'cache_hit_rate': sum(cache_hits.values()) / len(cache_hits) if cache_hits else 0,
                'time_per_layer': {layer: time/total_time if total_time > 0 else 0 
                                 for layer, time in layer_times.items()}
            }
        }
    
    @staticmethod
    def system_metrics(
        current_time: datetime,
        requests_last_hour: int,
        average_response_time: float,
        error_rate: float,
        cache_hit_rate: float,
        active_users: int
    ) -> Dict[str, Any]:
        """系统性能指标"""
        return {
            'timestamp': current_time.isoformat(),
            'throughput': {
                'requests_last_hour': requests_last_hour,
                'requests_per_minute': requests_last_hour / 60 if requests_last_hour > 0 else 0
            },
            'performance': {
                'average_response_time': average_response_time,
                'p95_response_time': average_response_time * 1.5,  # 估算
                'p99_response_time': average_response_time * 2.0   # 估算
            },
            'reliability': {
                'error_rate': error_rate,
                'success_rate': 1 - error_rate,
                'uptime_percentage': 99.9  # 示例值
            },
            'efficiency': {
                'cache_hit_rate': cache_hit_rate,
                'active_users': active_users
            }
        }

# ============================================================================
# 测试和示例
# ============================================================================

def test_protocols():
    """测试协议"""
    print("🔍 测试六层架构协议\n")
    print("=" * 70)
    
    # 测试创建请求
    print("\n1. 创建分析请求:")
    request = Protocol.create_request(
        raw_input="/mao analyze --method=矛盾 分析问题",
        source_layer=LayerType.UI,
        target_layer=LayerType.GATEWAY,
        request_type=RequestType.ANALYZE,
        user_id="test_user_001",
        metadata={"session_id": "sess_001", "platform": "webchat"}
    )
    print(f"  请求ID: {request['request_id']}")
    print(f"  源层: {request['source_layer']}")
    print(f"  目标层: {request['target_layer']}")
    print(f"  用户ID: {request['user_id']}")
    
    # 测试请求验证
    print("\n2. 验证请求:")
    validation_errors = Protocol.validate_request(request)
    if validation_errors:
        print(f"  ❌ 验证失败: {len(validation_errors)} 个错误")
        for error in validation_errors:
            print(f"    - {error['error_message']}")
    else:
        print("  ✅ 验证通过")
    
    # 测试创建错误
    print("\n3. 创建标准错误:")
    error = Protocol.create_error(
        error_code=ErrorCode.ANALYTICS_RECOMMENDATION,
        error_message="无法推荐分析方法",
        error_details={"question": "测试问题", "extracted_keywords": []},
        suggested_fix="请尝试指定分析方法",
        retry_possible=True,
        fallback_action="使用综合分析法"
    )
    print(f"  错误代码: {error['error_code']}")
    print(f"  错误消息: {error['error_message']}")
    print(f"  可重试: {error['retry_possible']}")
    
    # 测试创建响应
    print("\n4. 创建分析响应:")
    response_data = ResponseFormats.analyze_response(
        analysis_result="## 分析结果...",
        method_used="矛盾分析",
        confidence=0.85,
        concepts_used=["主要矛盾", "次要矛盾"],
        processing_time=1.23
    )
    
    response = Protocol.create_response(
        request=request,
        response_data=response_data,
        success=True,
        processing_time=1.23,
        layer_trace=["ui", "gateway", "analytics", "method"],
        errors=[]
    )
    
    print(f"  请求ID: {response['request_id']}")
    print(f"  成功: {response['success']}")
    print(f"  处理时间: {response.get('processing_time', 0)} 秒")
    print(f"  层跟踪: {response.get('layer_trace', [])}")
    
    # 测试响应验证
    print("\n5. 验证响应:")
    response_errors = Protocol.validate_response(response)
    if response_errors:
        print(f"  ❌ 验证失败: {len(response_errors)} 个错误")
        for error in response_errors:
            print(f"    - {error['error_message']}")
    else:
        print("  ✅ 验证通过")
    
    # 测试数据格式
    print("\n6. 测试数据格式:")
    analyze_request = RequestFormats.analyze_request(
        question="分析公司部门协作问题",
        method="矛盾",
        style="work"
    )
    print(f"  分析请求格式: {analyze_request['question'][:30]}...")
    
    # 测试性能指标
    print("\n7. 测试性能指标:")
    from datetime import datetime, timedelta
    metrics = PerformanceMetrics.request_metrics(
        request_id="req_001",
        start_time=datetime.now() - timedelta(seconds=1.5),
        end_time=datetime.now(),
        layer_times={"gateway": 0.1, "analytics": 0.3, "method": 0.8, "knowledge": 0.3},
        cache_hits={"gateway": False, "analytics": True, "method": False},
        memory_usage=128
    )
    print(f"  总时间: {metrics['timing']['total_time']:.3f} 秒")
    print(f"  缓存命中率: {metrics['efficiency']['cache_hit_rate']:.1%}")
    
    print("\n" + "=" * 70)
    print("✅ 协议测试完成")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="六层架构协议工具")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--create-request", help="创建请求示例")
    parser.add_argument("--create-error", help="创建错误示例")
    
    args = parser.parse_args()
    
    if args.test:
        test_protocols()
    elif args.create_request:
        # 示例：创建分析请求
        request = Protocol.create_request(
            raw_input=args.create_request,
            source_layer=LayerType.UI,
            target_layer=LayerType.GATEWAY,
            request_type=RequestType.ANALYZE,
            user_id="example_user"
        )
        print("📨 创建的请求:")
        print(json.dumps(request, indent=2, ensure_ascii=False))
    elif args.create_error:
        # 示例：创建错误
        error = Protocol.create_error(
            error_code=ErrorCode.ANALYTICS_RECOMMENDATION,
            error_message=args.create_error,
            suggested_fix="请检查输入或指定分析方法"
        )
        print("❌ 创建的错误:")
        print(json.dumps(error, indent=2, ensure_ascii=False))
    else:
        print("请提供参数或使用 --test 运行测试")
        print("示例: python protocols.py --create-request '/mao 分析问题'")

if __name__ == "__main__":
    import json
    main()