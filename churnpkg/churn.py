"""
churnpkg.churn
────────────────────────────────────────────────────────
核心函数：输入 dataset（DataFrame） + customer_id → 返回该客户的 churn 概率（churn_prob）。

这个文件属于你的 package（churnpkg），用于 Step 4：
- 供 dashboard / 其他脚本直接 import 使用
- 供单元测试 tests/test_churn.py 调用

注意：
- df 必须包含两列：
  1) CustomerId   : 客户唯一ID
  2) churn_prob   : Step 3 训练 Logit 后预测出的流失概率
"""


def churn_prob_for_customer(df, customer_id):
    """根据 CustomerId 查询该客户的流失概率（churn_prob）。

    Parameters
    ----------
    df : pandas.DataFrame
        必须包含 "CustomerId" 和 "churn_prob" 两列。
        - "CustomerId"：客户编号
        - "churn_prob"：流失概率（0~1），由 scripts/build_model.py 生成
    customer_id : int
        要查询的客户 ID。

    Returns
    -------
    float
        该客户的流失概率（0~1）。

    Raises
    ------
    ValueError
        如果 customer_id 不在 df 中（题目要求必须抛出这个错误信息）。
    """

    # ① 先检查 customer_id 是否存在
    # 题目要求：如果不存在，必须抛出 ValueError，且消息要严格一致
    # （注意：这里不要随便改报错文本，否则可能扣分）
    if customer_id not in df["CustomerId"].values:
        raise ValueError("CustomerId not found in dataset.")

    # ② 定位该客户对应的 churn_prob
    # df.loc[条件, "列名"] 会返回一个 Series（可能有多行）
    row = df.loc[df["CustomerId"] == customer_id, "churn_prob"]

    # ③ 返回该客户的概率
    # 如果同一个 CustomerId 在 df 中出现多行，这里默认取第一条（iloc[0]）
    return float(row.iloc[0])
