"""
app.py (Step 5 - Python Shiny Dashboard)
---------------------------------------
要求实现：
1) sidebar layout
2) 主面板：显示 churn_prob 最高的 top10 客户，并展示 Gender, Age, Tenure
3) 侧边栏：输入 CustomerId，显示该客户 churn_prob
"""

from pathlib import Path

import pandas as pd
from shiny import App, ui, render, reactive

# 复用你 Step 4 的包函数（你已经写好了）
from churnpkg import churn_prob_for_customer


# ─────────────────────────────────────────────────────────────
# 读取 Step 3 生成的数据：data_with_churn_prob.csv
# 注意：这个文件应放在项目根目录 churn_project/ 下
# ─────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data_with_churn_prob.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"找不到 {DATA_PATH}。\n"
        "请先在项目根目录运行：python scripts/build_model.py\n"
        "生成 data_with_churn_prob.csv"
    )

df = pd.read_csv(DATA_PATH)

# 防呆：确保需要的列存在（否则 dashboard 会炸）
required_cols = {"CustomerId", "Gender", "Age", "Tenure", "churn_prob"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"数据缺少必要列：{missing}")

# 预先算好 top10（避免每次刷新都重新排序，提高效率）
top10 = (
    df.sort_values("churn_prob", ascending=False)
      .head(10)[["CustomerId", "Gender", "Age", "Tenure", "churn_prob"]]
      .reset_index(drop=True)
)

# ─────────────────────────────────────────────────────────────
# UI（左侧输入 + 右侧输出）
# ─────────────────────────────────────────────────────────────
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h4("Customer Churn Lookup"),
        ui.input_selectize(
            "customer_id",
            "CustomerId",
            choices=[str(x) for x in df["CustomerId"].dropna().unique()],
            selected=str(df["CustomerId"].dropna().iloc[0]),
        ),
        ui.p("Enter a CustomerId to see the predicted churn probability."),
    ),
    ui.h3("Churn Dashboard (Python Shiny)"),
    ui.card(
        ui.card_header("Churn Probability for Selected Customer"),
        ui.output_text("customer_prob_text"),
    ),
    ui.card(
        ui.card_header("Top 10 Customers by Churn Probability (Gender / Age / Tenure)"),
        ui.output_data_frame("top10_table"),
    ),
)


# ─────────────────────────────────────────────────────────────
# Server（如何根据输入更新输出）
# ─────────────────────────────────────────────────────────────
def server(input, output, session):

    @reactive.calc
    def selected_customer_id() -> int:
        """
        把下拉框选中的值转成 int。
        因为用了 selectize，用户只能选已有的 ID，不会出现 not found。
        """
        return int(input.customer_id())

    @render.text
    def customer_prob_text():
        """
        读取输入的 customer_id，调用你 Step4 写的函数，返回 churn_prob。
        如果 customer 不存在，显示错误信息而不是让 app 崩掉。
        """
        cid = selected_customer_id()
        try:
            prob = churn_prob_for_customer(df, cid)
            return f"Churn probability for CustomerId {cid} = {prob:.4f}"
        except ValueError as e:
            # 题目要求的 ValueError 文本你 Step4 已经写对了，这里直接显示
            return f"❌ Error: {e}"

    @render.data_frame
    def top10_table():
        """
        显示 churn_prob 最高的 top10 客户。
        题目要求主面板展示 Gender, Age, Tenure；
        用 render.DataGrid 让列对齐、样式更整齐。
        """
        # 题目要求只显示 Gender, Age, Tenure 三列
        return render.DataGrid(top10[["Gender", "Age", "Tenure"]])


app = App(app_ui, server)
