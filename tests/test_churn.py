"""
test_churn.py — 单元测试
────────────────────────
测试 churnpkg.churn_prob_for_customer 函数。
"""

import os
import sys
import unittest
import pandas as pd

# 让 import churnpkg 能找到
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from churnpkg import churn_prob_for_customer

# ── 加载带 churn_prob 的数据（由 build_model.py 生成） ──
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data_with_churn_prob.csv")
df = pd.read_csv(DATA_PATH)

# 找出最高 / 最低概率客户 ID
highest_id = int(df.loc[df["churn_prob"].idxmax(), "CustomerId"])
lowest_id  = int(df.loc[df["churn_prob"].idxmin(), "CustomerId"])


class TestChurnProbForCustomer(unittest.TestCase):
    """churn_prob_for_customer 的测试用例。"""

    def test_highest_greater_than_lowest(self):
        """最高概率客户的 churn_prob 必须 > 最低概率客户。"""
        self.assertGreater(
            churn_prob_for_customer(df, highest_id),
            churn_prob_for_customer(df, lowest_id),
        )

    def test_return_type_is_float(self):
        """函数返回值应该是 float。"""
        result = churn_prob_for_customer(df, highest_id)
        self.assertIsInstance(result, float)

    def test_prob_between_0_and_1(self):
        """概率值必须在 [0, 1] 范围内。"""
        prob = churn_prob_for_customer(df, highest_id)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)

    def test_invalid_customer_raises(self):
        """不存在的 CustomerId 应抛出 ValueError。"""
        with self.assertRaises(ValueError):
            churn_prob_for_customer(df, 99999999)


if __name__ == "__main__":
    unittest.main()
