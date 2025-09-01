import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'STHeiti'
def objective_function(x):
    """目标函数：f(x) = x^2"""
    return x**2

def simulated_annealing(initial_x, initial_temp, cooling_rate, min_temp, max_iter):
    """
    模拟退火算法
    
    参数:
    initial_x: 初始解
    initial_temp: 初始温度
    cooling_rate: 冷却率
    min_temp: 最低温度
    max_iter: 最大迭代次数
    
    返回:
    最优解和过程记录
    """
    # 初始化
    current_x = initial_x
    current_energy = objective_function(current_x)
    best_x = current_x
    best_energy = current_energy
    
    # 记录过程
    history = []
    
    temp = initial_temp
    iteration = 0
    
    while temp > min_temp and iteration < max_iter:
        # 生成新解（在当前解附近随机扰动）
        new_x = current_x + random.uniform(-2, 2)
        new_energy = objective_function(new_x)
        
        # 计算能量差
        energy_delta = new_energy - current_energy
        
        # 如果新解更优，直接接受
        if energy_delta < 0:
            current_x = new_x
            current_energy = new_energy
            if new_energy < best_energy:
                best_x = new_x
                best_energy = new_energy
        else:
            # 以概率接受劣解
            probability = math.exp(-energy_delta / temp) #e指数函数
            if random.random() < probability:
                current_x = new_x
                current_energy = new_energy
        
        # 记录当前状态
        history.append((current_x, current_energy, temp))
        
        # 降温
        temp *= cooling_rate
        iteration += 1
    
    return best_x, best_energy, history

# 运行模拟退火算法
initial_x = 10  # 初始解（离最优解0较远）
initial_temp = 1000  # 初始温度
cooling_rate = 0.95  # 冷却率
min_temp = 0.1  # 最低温度
max_iter = 500  # 最大迭代次数

best_x, best_energy, history = simulated_annealing(
    initial_x, initial_temp, cooling_rate, min_temp, max_iter
)

# 输出结果
print(f"最优解: x = {best_x:.4f}, f(x) = {best_energy:.4f}")

# 可视化过程
plt.figure(figsize=(12, 8))

# 绘制函数曲线
x_vals = np.linspace(-11, 11, 100)
y_vals = x_vals**2
plt.plot(x_vals, y_vals, 'b-', label='f(x) = x²')

# 绘制搜索过程
x_history = [h[0] for h in history]
y_history = [h[1] for h in history]
plt.plot(x_history, y_history, 'ro-', markersize=2, alpha=0.5, label='搜索路径')

# 标记最优解
plt.plot(best_x, best_energy, 'go', markersize=10, label='找到的最优解')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('模拟退火算法寻找函数最小值')
plt.legend()
plt.grid(True)
plt.show()

# 绘制能量和温度变化
plt.figure(figsize=(12, 6))

# 能量变化
plt.subplot(1, 2, 1)
energy_history = [h[1] for h in history]
plt.plot(energy_history)
plt.xlabel('迭代次数')
plt.ylabel('能量值')
plt.title('能量变化过程')
plt.grid(True)

# 温度变化
plt.subplot(1, 2, 2)
temp_history = [h[2] for h in history]
plt.plot(temp_history, 'r-')
plt.xlabel('迭代次数')
plt.ylabel('温度')
plt.title('温度下降过程')
plt.grid(True)

plt.tight_layout()
plt.show()