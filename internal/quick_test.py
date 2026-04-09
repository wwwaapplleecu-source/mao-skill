#!/usr/bin/env python3
from tools.skill_simulator_optimized import MaoSkillSimulatorOptimized

simulator = MaoSkillSimulatorOptimized()

# 测试工作重点
response1 = simulator.generate_response('分析工作重点')
print('工作重点响应:', response1)
print('包含"既要":', '既要' in response1)
print('包含"又要":', '又要' in response1)  
print('包含"还要":', '还要' in response1)

print('\n' + '='*60 + '\n')

# 测试动员讲话
response2 = simulator.generate_response('写一段动员讲话')
print('动员讲话响应:', response2)
print('包含"同志们":', '同志们' in response2)
print('包含"革命":', '革命' in response2)
print('包含"斗争":', '斗争' in response2)
print('包含"胜利":', '胜利' in response2)