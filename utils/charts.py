import matplotlib.pyplot as plt
import plotly.express as px

def plot_monthly_expense(df):
  monthly_expense = df.groupby('month')['debit'].sum()
  plt.figure(figsize=(10, 6))
  monthly_expense.plot(kind='bar', color='skyblue', edgecolor='black')
  plt.title("Monthly Expenses", fontsize=16)
  plt.xlabel("Month", fontsize=14)
  plt.ylabel("Total Expenses", fontsize=14)
  plt.xticks(rotation=45)
  plt.grid(axis='y', linestyle='--', alpha=0.7)
  plt.tight_layout()
  plt.show()

def plot_monthwise_catwise(df):
  # Expenses by month and category
  expense_summary = df.groupby(['month', 'description'])['debit'].sum().unstack(fill_value=0)
  
  # Plotting the month-wise category stacked bar chart
  ax = expense_summary.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='tab20', width=0.8)

  # Customizing the chart
  plt.title("Month-Wise Category-Wise Expenses - Stacked Bar Chart", fontsize=16)
  plt.xlabel("Month", fontsize=14)
  plt.ylabel("Total Expenses", fontsize=14)
  plt.xticks(rotation=45)
  plt.legend(title="Expense Categories", bbox_to_anchor=(1.05, 1), loc='upper left')
  plt.tight_layout()
  
  # Show the chart
  plt.show()


def plot_monthly_expense_line(df):
  # Calculate total expenses per month
  monthly_expense = df.groupby('month')['debit'].sum()

  # Plotting the monthly expenses line chart
  plt.figure(figsize=(14, 8))
  plt.plot(monthly_expense.index.astype(str), monthly_expense.values, marker='o', color='b', linestyle='-', linewidth=2)

  # Customizing the chart
  plt.title("Monthly Expenses Line Chart", fontsize=16)
  plt.xlabel("Month", fontsize=14)
  plt.ylabel("Total Expenses", fontsize=14)
  plt.xticks(rotation=45)
  plt.grid(True, linestyle='--', alpha=0.5)
  plt.tight_layout()
  
  # Show the chart
  plt.show()

def plot_monthwise_catwise_line(df):
  # Group by month and description (category) and sum the expenses
  monthly_category_expenses = df.groupby(['month', 'description'])['debit'].sum().unstack(fill_value=0)

  # Plotting the month-wise category-wise line chart
  plt.figure(figsize=(14, 8))
  monthly_category_expenses.plot(kind='line', marker='o', figsize=(14, 8), lw=2)

  # Customizing the chart
  plt.title("Month-Wise Category-Wise Expenses - Line Chart", fontsize=16)
  plt.xlabel("Month", fontsize=14)
  plt.ylabel("Total Expenses", fontsize=14)
  plt.xticks(rotation=45)
  plt.grid(True, linestyle='--', alpha=0.5)
  plt.legend(title="Expense Categories", bbox_to_anchor=(1.05, 1), loc='upper left')
  plt.tight_layout()
  
  # Show the chart
  plt.show()