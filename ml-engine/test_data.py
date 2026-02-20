import os
import json
import pandas as pd

from clean_data import clean_data
from train_model import train_model

from analytics.summary import compute_summary
from analytics.line import line_chart
from analytics.bar import bar_chart
from analytics.pie import pie_chart


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_FILE = os.path.join(BASE_DIR, "data", "raw", "train.csv")


def main():
    print("\n🚀 Starting Full ML Engine Pipeline...\n")

    # ---------------------------------------------------
    # 1️⃣ CLEAN DATA
    # ---------------------------------------------------
    print("🔹 Cleaning dataset...")

    cleaned_df, report = clean_data(RAW_FILE)

    os.makedirs(os.path.join(BASE_DIR, "data", "cleaned"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "reports"), exist_ok=True)

    cleaned_path = os.path.join(
        BASE_DIR,
        "data",
        "cleaned",
        f"cleaned_{os.path.basename(RAW_FILE)}"
    )

    report_path = os.path.join(BASE_DIR, "reports", "analysis.json")

    cleaned_df.to_csv(cleaned_path, index=False)

    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"✅ Cleaned file saved: {cleaned_path}")
    print(f"✅ Report saved: {report_path}")

    # ---------------------------------------------------
    # 2️⃣ TRAIN MODEL
    # ---------------------------------------------------
    print("\n🔹 Training model...")

    train_result = train_model(cleaned_path)

    print(f"✅ Model saved: {train_result['model_file']}")
    print(f"✅ Metrics saved: {train_result['metrics_file']}")

    # ---------------------------------------------------
    # 3️⃣ ANALYTICS
    # ---------------------------------------------------
    print("\n🔹 Generating analytics...")

    df = pd.read_csv(cleaned_path)

    summary = compute_summary(df)

    summary_path = os.path.join(BASE_DIR, "reports", "summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)

    charts = {
        "line": line_chart(df),
        "bar": bar_chart(df),
        "pie": pie_chart(df)
    }

    charts_path = os.path.join(BASE_DIR, "reports", "charts.json")
    with open(charts_path, "w") as f:
        json.dump(charts, f, indent=4)

    print(f"✅ Summary saved: {summary_path}")
    print(f"✅ Charts saved: {charts_path}")

    print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!\n")


if __name__ == "__main__":
    main()
