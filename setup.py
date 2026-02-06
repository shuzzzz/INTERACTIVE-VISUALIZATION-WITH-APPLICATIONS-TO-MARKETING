"""
setup.py
────────
用于把 churnpkg 打包成可安装的 Python package。

安装方式（在项目根目录 churn_project/ 下）：
    pip install -e .
"""

from setuptools import setup, find_packages

setup(
    # 包名（pip install 用的名字）
    name="churnpkg",

    # 版本号（发布/迭代用）
    version="0.1.0",

    # 简短描述
    description="客户流失概率查询包（Day 5 Exercise）",

    # 自动找到所有包含 __init__.py 的包目录（这里会找到 churnpkg）
    packages=find_packages(),

    # 运行依赖：装包时会自动安装这些库
    # 注意：如果你的包只是“查询 churn_prob”，严格来说只需要 pandas；
    # statsmodels 是 build_model.py 训练模型时需要的依赖。
    install_requires=[
        "pandas",
        "statsmodels",
    ],

    # Python 版本要求（按你课程环境写）
    python_requires=">=3.9",
)
