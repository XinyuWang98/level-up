
# ---------------------------------------------------------
# 进阶任务: Bootstrap 置信区间 (The "Scientific" Way) 🧪
# ---------------------------------------------------------
# 为什么不用普通公式？
# 1. 我们的 Revenue 数据严重偏态 (大量0和几个超大值)，不符合正态分布。
# 2. 普通的 T-test 置信区间公式 (mean ± 1.96*SE) 假设样本均值呈正态分布，
#    但在小样本或极度偏态时，这个假设可能失效。
# 3. Bootstrap 是"暴力模拟"：从现有数据里"有放回地" (replace=True) 抽样 10000 次，
#    算出 10000 个均值差，直接看这 10000 个结果的分布情况 (比如取第 2.5% 和 97.5% 分位数)。

def bootstrap_ci(series_control, series_test, n_bootstrap=10000, alpha=0.05):
    """
    计算两个独立样本均值差的 Bootstrap 置信区间
    """
    # 转成 numpy array 加速运算
    pool_c = series_control.values
    pool_t = series_test.values
    
    # 1. 算实际差异 (Point Estimate)
    real_diff = pool_t.mean() - pool_c.mean()
    
    # 2. 暴力抽样 (Resampling)
    diffs = []
    # 这里用循环模拟 (实际生产中可以用矩阵运算加速，但循环更直观)
    # 每次从 Control 组里随机抽 n 个，从 Test 组里随机抽 m 个 (允许重复抽到同一个人)
    for _ in range(n_bootstrap):
        sample_c = np.random.choice(pool_c, size=len(pool_c), replace=True)
        sample_t = np.random.choice(pool_t, size=len(pool_t), replace=True)
        diffs.append(sample_t.mean() - sample_c.mean())
        
    # 3. 找百分位 (Percentile)
    # alpha=0.05 时，找 2.5% 和 97.5% 的位置
    ci_lower = np.percentile(diffs, (alpha/2)*100)
    ci_upper = np.percentile(diffs, (1-alpha/2)*100)
    
    return real_diff, ci_lower, ci_upper

# 这里的运算量有点大，可能会跑几秒钟
# 我们针对 ARPU (总体人均值) 算一下置信区间
diff, lower, upper = bootstrap_ci(group_5['revenue'], group_10['revenue'])

print(f"真实提升 (Mean Lift): {diff:.4f}")
print(f"95% 置信区间 (CI): [{lower:.4f}, {upper:.4f}]")

if lower > 0:
    print("结论: 区间不包含 0，且完全在正数区间 -> 显著提升！🚀")
else:
    print("结论: 区间包含了 0 -> 可能没效果。")
