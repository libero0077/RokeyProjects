import gradio as gr
import pandas as pd
import sqlite3


# 데이터베이스에서 원하는 데이터를 쿼리하여 DataFrame 생성
def fetch_data():
    conn = sqlite3.connect("result.db")
    query = """
    SELECT datetime,
           COUNT(*) AS Total,
           SUM(is_defective) AS Defect,
           COUNT(*) - SUM(is_defective) AS Good
    FROM product
    GROUP BY datetime
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # datetime 형식을 원하는 형식으로 변환
    df["datetime"] = pd.to_datetime(df["datetime"]).dt.strftime("%m/%d %H")

    return df


# 데이터베이스에서 불량 항목만 쿼리하여 DataFrame 생성
def fetch_defect_data():
    conn = sqlite3.connect("result.db")
    query = """
    SELECT datetime, uuid, defect_reason
    FROM product
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


with gr.Blocks() as demo:
    df = fetch_data()
    gr.Markdown("# Product Data Report")
    gr.Markdown(
        "This report displays the total, defective, and good quantities by datetime."
    )
    gr.Markdown("### TOTAL Count")
    gr.BarPlot(
        fetch_data, x="datetime", y="Total", y_aggregate="sum", live=True
    )
    gr.Markdown("### Good Count")
    gr.BarPlot(fetch_data, x="datetime", y="Good", y_aggregate="sum")
    gr.Markdown("### Defect Count")
    gr.BarPlot(fetch_data, x="datetime", y="Defect", y_aggregate="sum")

    gr.Markdown("# Defective Products Report")
    gr.Markdown("This table displays only defective products by datetime.")

    # 불량 데이터만 출력
    gr.DataFrame(fetch_defect_data)

demo.launch()