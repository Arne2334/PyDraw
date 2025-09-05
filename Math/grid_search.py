from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# 示例数据集
X, y = make_classification(n_samples=100, n_features=4, random_state=42)

# 定义模型
model = RandomForestClassifier(random_state=42)

# 定义参数网格
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 5, 10]
}

# 创建 GridSearchCV 对象
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=5,  # 5折交叉验证
    scoring='accuracy',  # 评估指标
    n_jobs=-1  # 使用所有可用的CPU核心
)

# 运行网格搜索
grid_search.fit(X, y)

# 输出最佳参数和分数
print("最佳参数组合:", grid_search.best_params_)
print("最佳分数:", grid_search.best_score_)