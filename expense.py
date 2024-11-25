import pandas as pd
import json
from datetime import datetime
from argparse import ArgumentParser
from utils.charts import (
    plot_monthly_expense,
    plot_monthwise_catwise,
    plot_monthly_expense_line,
    plot_monthwise_catwise_line
)

def category_mapping(txt):
    with open("categories.json", "r+") as category_data:
        categories = json.loads(category_data.read())
        for category, vendors in categories.items():
            for v in vendors:
                if v in txt:
                    return category
        return "misc"
    

def analyze_expenses(file_path):

    df = pd.read_excel(file_path, sheet_name="Passbook Payment History")
    df = df[["Date", "Transaction Details", "Amount"]]
    df.rename({"Transaction Details": "description", "Date": "date"}, axis=1, inplace=True)
    
    df['Amount'] = df['Amount'].replace(',', '', regex=True).astype(float)
    df['debit'] = df['Amount'].apply(lambda x: -x if x is not None and x < 0 else 0) 
    df['credit'] = df['Amount'].apply(lambda x: x if x is not None and x > 0 else 0)
    df['category'] = df['description'].apply(lambda x: category_mapping(x.lower()))

    df.drop(columns='Amount', inplace=True)
    df.columns = df.columns.str.strip().str.lower()

    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df["month"] = df["date"].dt.to_period("M")

    df.to_csv("output.csv", index=None)

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

    parser.add_argument("--file", help="Expense Excel", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    
    args = get_args()
    analyze_expenses(args.file)
