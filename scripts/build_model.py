"""
build_model.py（Day 5 - Step 1~3）
========================================================
目标：读取两份客户数据 → 合并 → 训练 Logit（逻辑回归）模型 → 给每个客户预测 churn_prob（流失概率）
最后把带 churn_prob 的结果保存为 CSV（供 Step 4 的函数/单元测试/仪表盘使用）

使用方式（在项目根目录 churn_project 下）：
1) 先确保数据放在：churn_project/Data/
   - Data/data_customer.csv
   - Data/data_personal.csv
2) 运行：
   python scripts/build_model.py

输出：
- churn_project/data_with_churn_prob.csv
"""

from pathlib import Path
import pandas as pd
import statsmodels.api as sm


# ════════════════════════════════════════════════════════════════
# 路径设置：用项目根目录做基准（比 "../../.." 稳很多）
# scripts/build_model.py 的上一级就是项目根 churn_project/
# ════════════════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # churn_project/
DATA_DIR = Path("/Users/zhiwu/Documents/R-Python - a non-technical overview of big data techniques/Data")
OUT_PATH = PROJECT_ROOT / "data_with_churn_prob.csv"


def main():
    # ════════════════════════════════════════════════════════════════
    # Step 1) 读数据
    # ════════════════════════════════════════════════════════════════
    cust_path = DATA_DIR / "data_customer.csv"
    pers_path = DATA_DIR / "data_personal.csv"

    if not cust_path.exists():
        raise FileNotFoundError(f"找不到文件：{cust_path}")
    if not pers_path.exists():
        raise FileNotFoundError(f"找不到文件：{pers_path}")

    cust = pd.read_csv(cust_path)
    pers = pd.read_csv(pers_path)

    print("cust shape:", cust.shape)
    print("pers shape:", pers.shape)

    # ════════════════════════════════════════════════════════════════
    # Step 2) 合并 + 类型处理 + 基本检查
    # 目标：
    #   1) 用 CustomerId 合并两张表
    #   2) 把 Exited / Gender 设为 category（题目要求）
    #   3) 输出 dtypes / describe 做 sanity check
    # ════════════════════════════════════════════════════════════════
    df = cust.merge(pers, on="CustomerId", how="inner")

    # 题目要求：Exited / Gender 设成分类变量
    df["Exited"] = df["Exited"].astype("category")
    df["Gender"] = df["Gender"].astype("category")

    print("\ndtypes:\n", df.dtypes)
    print("\ndescribe:\n", df.describe(include="all"))

    # 防呆检查：Exited 里应该是 0/1（如果不是，你需要改 y 的构造方式）
    print("\nExited unique values:", df["Exited"].unique())

    # ════════════════════════════════════════════════════════════════
    # Step 3) 训练 Logit（逻辑回归）并预测 churn_prob
    # 题目指定：
    #   y = Exited
    #   X = CreditScore, Gender, Age, Tenure, Balance, NumOfProducts,
    #       HasCrCard, IsActiveMember, EstimatedSalary
    #
    # 关键点：
    #   - statsmodels.Logit 要求 y 是数值（0/1），X 也必须全是数值
    #   - Gender 是类别 → 必须做 dummy（0/1）编码
    #   - statsmodels 默认不自动加截距项 → 需要 add_constant
    # ════════════════════════════════════════════════════════════════

    # 3.1 构造 y（更稳的写法：明确把 Exited==1 当成“流失=1”）
    # 如果 Exited 是字符串（比如 "Yes"/"No"），这句会变成全 0，需要你根据实际值改。
    y = (df["Exited"] == 1).astype(int)

    # 3.1 构造 X（选题目指定的 9 个特征）
    X = df[
        [
            "CreditScore",
            "Gender",
            "Age",
            "Tenure",
            "Balance",
            "NumOfProducts",
            "HasCrCard",
            "IsActiveMember",
            "EstimatedSalary",
        ]
    ]

    # 3.1 把 Gender 从类别变量变成 dummy 变量（例如 Gender_Male）
    # drop_first=True：丢掉一个基准类别，避免完全共线（dummy trap）
    # dtype=int：让 dummy 是 0/1 的整型（更干净）
    X = pd.get_dummies(X, columns=["Gender"], drop_first=True, dtype=int)

    # 3.1 加截距项 const（statsmodels 不会自动加）
    X = sm.add_constant(X)

    # 3.2 拟合 Logit 模型（disp=False 不输出拟合过程）
    model = sm.Logit(y, X).fit(disp=False)

    # summary 会显示：系数、显著性、pseudo R^2 等
    print("\n=========== Logit model summary ===========\n")
    print(model.summary())

    # 3.3 预测每行（每个客户记录）的流失概率
    df["churn_prob"] = model.predict(X)

    # 3.4 找 churn_prob 最大/最小的客户
    highest = df.loc[df["churn_prob"].idxmax()]
    lowest = df.loc[df["churn_prob"].idxmin()]
    print("\n最高流失概率客户:", highest["CustomerId"], "→", round(float(highest["churn_prob"]), 4))
    print("最低流失概率客户:", lowest["CustomerId"], "→", round(float(lowest["churn_prob"]), 4))

    # 3.5 按性别计算平均 churn_prob
    avg_by_gender = df.groupby("Gender", as_index=False)["churn_prob"].mean()
    print("\n按性别平均 churn_prob:\n", avg_by_gender)

    # ════════════════════════════════════════════════════════════════
    # 保存结果：给 Step 4（函数/单元测试）和 Step 5（dashboard）使用
    # ════════════════════════════════════════════════════════════════
    df.to_csv(OUT_PATH, index=False)
    print(f"\n✅ 已保存至 {OUT_PATH}")


if __name__ == "__main__":
    main()
