# personal-finance-tracker
Python application for tracking personal finances.

# Personal Finance Tracker

A simple yet powerful Python application for tracking personal finances, visualizing spending patterns, and monitoring financial health over time.

## Features

- **Track Transactions**: Add income and expenses with categories and descriptions
- **Visual Dashboard**: See your financial data through interactive charts and graphs
- **Balance Tracking**: Monitor your balance over time with visual indicators
- **Category Analysis**: Understand spending patterns by category
- **Monthly Summaries**: Compare income vs. expenses and track savings rate
- **Simple CLI Interface**: Easy-to-use command-line interface for managing your finances

## Requirements

- Python 3.6+
- pandas
- numpy
- matplotlib

## Installation

Install required packages:
```
pip install pandas numpy matplotlib
```

## How to Use

1. Run the application:
   ```
   python main.py
   ```

2. Use the menu options to navigate the application:
   - **View Dashboard (1)**: Display visual charts of your financial data
   - **Add Transaction (2)**: Add a new income or expense entry
   - **View Recent Transactions (3)**: See your most recent financial activities
   - **View Monthly Summary (4)**: Get a summary of your monthly income, expenses, and savings rate
   - **Exit (5)**: Close the application

### Adding Transactions

When adding a transaction:
- Enter the date (YYYY-MM-DD format) or leave blank for today's date
- Enter the amount (positive for income, negative for expenses)
- Select a category from the available options
- Add a description for the transaction

## How It Works

The Personal Finance Tracker uses pandas and matplotlib to manage and visualize your financial data:

1. **Data Storage**: All transactions are stored in a CSV file (`finance_data.csv`) in the same directory as the application. If the file doesn't exist when the application is first run, a sample dataset will be created automatically.

2. **Data Processing**: The application processes your transactions to calculate:
   - Balance over time
   - Monthly spending by category
   - Income vs. expenses
   - Current month's spending breakdown
   - Monthly savings rate

3. **Visualization**: The dashboard presents your financial data through five key charts:
   - Balance over time (line chart)
   - Monthly spending by category (stacked bar chart)
   - Income vs. expenses (grouped bar chart)
   - Current month spending by category (pie chart)
   - Monthly savings rate (line chart)

4. **Financial Analysis**: The application automatically calculates metrics like:
   - Total income and expenses
   - Savings amount and rate
   - Spending patterns by category
   - Financial trends over time
