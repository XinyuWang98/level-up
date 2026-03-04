import numpy as np
import pandas as pd
import os

# 常量定义
N_SAMPLES = 10000
SEED = 42

# 路径
DATA_DIR = './01_专项专栏/04_因果推断/data'
FILE_PATH = os.path.join(DATA_DIR, 'membership_ltv_data.csv')

def generate_data():
    np.random.seed(SEED)
    
    # 1. 混淆变量 (Confounders)
    # 收入水平 (1-10)
    income_level = np.random.normal(5, 2, N_SAMPLES).clip(1, 10)
    # 购物频率 (周)
    shopping_freq = np.random.poisson(3, N_SAMPLES)
    # 年龄
    age = np.random.normal(35, 10, N_SAMPLES).astype(int).clip(18, 70)
    
    # 2. 也是混淆因子，但可能有噪音
    # 用户活跃度 = 0.5*收入 + 0.3*频率 + 噪音
    activity_score = 0.5 * income_level + 0.3 * shopping_freq + np.random.normal(0, 1, N_SAMPLES)
    
    # 3. 处理 (Treatment): 是否购买会员 (is_member)
    # 收入越高，活跃度越高，越容易买会员 (Selection Bias)
    # Logit 概率
    logit = -3 + 0.5 * income_level + 0.2 * shopping_freq + 0.01 * age
    prob_member = 1 / (1 + np.exp(-logit))
    is_member = np.random.binomial(1, prob_member)
    
    # 4. 结果 (Outcome): 生命周期价值 (LTV)
    # 真实因果效应 (ATE): 会员带来的真实提升是 200 元
    TRUE_TREATMENT_EFFECT = 200
    
    # LTV = 基线 + 收入影响 + 频率影响 + 会员影响 + 噪音
    # 注意：这里收入对LTV影响很大，如果不控制收入，直接看会员vs非会员，差异会非常大（虚高）
    ltv = (
        500 
        + 100 * income_level 
        + 50 * shopping_freq 
        + TRUE_TREATMENT_EFFECT * is_member 
        + np.random.normal(0, 50, N_SAMPLES)
    )
    
    # 构造 DataFrame
    df = pd.DataFrame({
        'user_id': np.arange(N_SAMPLES),
        'income_level': np.round(income_level, 2),
        'shopping_freq': shopping_freq,
        'age': age,
        'activity_score': np.round(activity_score, 2),
        'is_member': is_member,
        'ltv': np.round(ltv, 2)
    })
    
    return df

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    df = generate_data()
    df.to_csv(FILE_PATH, index=False)
    print(f"Dataset generated at {FILE_PATH}")
    print(df.head())
