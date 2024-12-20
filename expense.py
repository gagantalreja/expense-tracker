import pandas as pd
from datetime import datetime
from utils.pdf_to_df import pdf_to_dataframe
from argparse import ArgumentParser
from utils.charts import (
    plot_monthly_expense,
    plot_monthwise_catwise,
    plot_monthly_expense_line,
    plot_monthwise_catwise_line
)

def analyze_expenses(file_path, create_csv):

    df = pdf_to_dataframe(file_path, create_csv=create_csv)
    df.columns = df.columns.str.strip().str.lower()

    # Clean and convert 'debit' and 'credit' columns
    for col in ["debit"]:
        df[col] = df[col].astype(str).str.strip()  # Remove whitespace
        df[col] = df[col].replace(["-", "", "None"], "0")
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    current_year = datetime.now().year
    df["date"] = df["date"].apply(lambda x: f"{x} {current_year}")
    df["date"] = pd.to_datetime(df["date"], format="%d %b %Y")
    df["month"] = df["date"].dt.to_period("M")

    total_expenses = df["debit"].sum()
    print("Total Expenses:", total_expenses)

    summary = df.groupby("description")["debit"].sum().sort_values(ascending=False)
    print("\nTop Expense Categories:")
    print(summary.head(10))

    monthly_expense = df.groupby("month")["debit"].sum()
    print("\nMonthly Expenses:")
    print(monthly_expense)

    # plot_monthwise_catwise(df)
    # plot_monthly_expense(df)
    # plot_monthly_expense_line(df)
    plot_monthwise_catwise_line(df)

def get_args():
    parser = ArgumentParser()

    parser.add_argument("--pdf", help="Expense PDF", required=True)
    parser.add_argument("--create-csv", action="store_true", help="Save modified and categorised data as csv")

    return parser.parse_args()

if __name__ == "__main__":
    
    args = get_args()
    analyze_expenses(args.pdf, args.create_csv)
