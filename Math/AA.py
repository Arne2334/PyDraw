import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 导弹位置
missiles = {
    'M1': (20000, 0, 2000),
    'M2': (19000, 600, 2100),
    'M3': (18000, -600, 1900)
}

# 无人机位置
drones = {
    'FY1': (17800, 0, 1800),
    'FY2': (12000, 1400, 1400),
    'FY3': (6000, -3000, 700),
    'FY4': (11000, 2000, 1800),
    'FY5': (13000, -2000, 1300)
}

# 目标位置
targets = {
    '假目标': (0, 0, 0),
    '真目标': (0, 200, 0)
}

# 创建主图
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# 在主图中添加子图（画中画）
ax_inset = inset_axes(ax, width="20%", height="20%", loc='lower right', bbox_to_anchor=(0.1, 0.1, 0.8, 0.8), bbox_transform=ax.transAxes, axes_class=Axes3D)
ax_inset.set_title("放大视图", fontsize=8)
ax_inset.set_xlim(-50, 50)
ax_inset.set_ylim(-50, 50)
ax_inset.set_zlim(-10, 20)

# 绘制导弹位置
for name, pos in missiles.items():
    ax.scatter(pos[0], pos[1], pos[2], c='red', marker='^', s=100, label=f'导弹{name}' if name == 'M1' else "")
    ax.text(pos[0], pos[1], pos[2], f'{name}', color='red')

# # 绘制无人机位置
# for name, pos in drones.items():
#     ax.scatter(pos[0], pos[1], pos[2], c='blue', marker='o', s=100, label=f'无人机{name}' if name == 'FY1' else "")
#     ax.text(pos[0], pos[1], pos[2], f'{name}', color='blue')

# 定义绘制圆柱体的函数
def plot_cylinder(ax, center, radius, height, resolution=100, color='gray', alpha=0.5):
    theta = np.linspace(0, 2 * np.pi, resolution)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    z_bottom = np.full_like(x, center[2])
    z_top = np.full_like(x, center[2] + height)

    for i in range(len(theta) - 1):
        verts = [
            [(x[i], y[i], z_bottom[i]), (x[i + 1], y[i + 1], z_bottom[i + 1]), (x[i + 1], y[i + 1], z_top[i + 1]), (x[i], y[i], z_top[i])]
        ]
        ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=alpha))

    ax.plot_surface(
        np.array([x, x]),
        np.array([y, y]),
        np.array([z_bottom, z_top]),
        color=color,
        alpha=alpha
    )

# 定义绘制烟雾团的函数
def plot_smoke_cloud(ax, center, radius, resolution=50, color='gray', alpha=0.3):
    """
    在3D图中绘制烟雾团
    :param ax: 3D轴对象
    :param center: 烟雾中心坐标 (x, y, z)
    :param radius: 烟雾半径
    :param resolution: 烟雾的分辨率（越高越平滑）
    :param color: 烟雾颜色
    :param alpha: 透明度
    """
    # 生成球体的参数
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # 绘制烟雾团
    ax.plot_surface(x, y, z, color=color, alpha=alpha)

# 在假目标位置上方绘制烟雾团（高度设为500米）
# plot_smoke_cloud(ax, center=(0, 0, 500), radius=100, color='gray', alpha=0.3)
# plot_smoke_cloud(ax, center=(0, 200, 500), radius=100, color='gray', alpha=0.3)

# 在主图中绘制圆柱体（原始大小）
plot_cylinder(ax, center=(0, 0, 0), radius=7, height=10, color='purple', alpha=0.3)
plot_cylinder(ax, center=(0, 200, 0), radius=7, height=10, color='purple', alpha=0.3)

# 在子图中绘制放大的圆柱体
plot_cylinder(ax_inset, center=(0, 0, 0), radius=20, height=20, color='purple', alpha=0.5)
plot_cylinder(ax_inset, center=(0, 200, 0), radius=20, height=20, color='purple', alpha=0.5)

# 设置坐标轴标签
ax.set_xlabel('X坐标 (m)')
ax.set_ylabel('Y坐标 (m)')
ax.set_zlabel('Z坐标 (m)')

# 设置标题
ax.set_title('导弹和无人机位置分布3D图（画中画）')

# 调整视角
ax.view_init(elev=20, azim=45)
ax_inset.view_init(elev=20, azim=45)

# 显示图形
plt.tight_layout()
plt.show()
