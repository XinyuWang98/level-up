import pandas as pd
import numpy as np
import pyfixest as pf
import matplotlib.pyplot as plt

def run_placebo_test(df):
    """
    运行两种安慰剂检验：
    1. 假时间 (Placebo Time): 假设干预提前发生 (Week 3)
    2. 假处理 (Placebo Treatment): 随机打乱处理组城市
    """
    
    print("-" * 30)
    print("🧪 Running Placebo Test 1: Fake Time (Week 3)")
    print("-" * 30)
    
    # 1. 假时间测试
    # 逻辑：只取干预前的数据 (Week < 6)，假装干预发生在 Week 3
    # 预期：所有交互项系数都不显著 (CI 包含 0)
    df_placebo_time = df[df['week'] < 6].copy()
    df_placebo_time['week_relative_fake'] = df_placebo_time['week'] - 3
    
    # 建模
    fit_placebo_time = pf.feols(
        "gmv ~ i(week_relative_fake, is_treated, ref=-1) | city + week",
        data=df_placebo_time,
        vcov={'CRV1': 'city'}
    )
    
    print(fit_placebo_time.summary())
    
    # 可视化
    pf.iplot(fit_placebo_time, figsize=(10, 4), title="Placebo Time (Should be non-significant)")
    plt.show()

    print("\n" + "-" * 30)
    print("🧪 Running Placebo Test 2: Fake Treatment (Random Shuffle)")
    print("-" * 30)

    # 2. 假处理测试
    # 逻辑：随机打乱实验组/对照组标签，重新回归
    # 预期：交互项系数接近 0，且不显著
    
    # 创建随机种子保持可复现
    np.random.seed(42)

    # 随机抽取一半城市作为"假实验组"
    all_cities = df['city'].unique()
    fake_treated_cities = np.random.choice(all_cities, size=len(all_cities)//2, replace=False)
    
    df_placebo_treat = df.copy()
    df_placebo_treat['is_treated_fake'] = df_placebo_treat['city'].isin(fake_treated_cities).astype(int)

    # 建模
    fit_placebo_treat = pf.feols(
        "gmv ~ i(week_relative, is_treated_fake, ref=0) | city + week",
        data=df_placebo_treat,
        vcov={'CRV1': 'city'}
    )
    
    print(fit_placebo_treat.summary())
    
    # 可视化
    pf.iplot(fit_placebo_treat, figsize=(10, 4), title="Placebo Treatment (Randomized Cities)")
    plt.show()

# 使用说明
print("✅ 代码已生成。请将 `run_placebo_test(df)` 复制到 notebook 中运行。")
