"""
churnpkg
────────
客户流失预测（churn prediction）相关的工具包。

把常用函数在这里“导出”，这样用户可以：
    from churnpkg import churn_prob_for_customer
"""

# 从子模块 churn.py 导入核心函数，并暴露为包的公开 API
from .churn import churn_prob_for_customer

# 可选：声明对外公开的接口（更规范，防止乱导出）
__all__ = ["churn_prob_for_customer"]
