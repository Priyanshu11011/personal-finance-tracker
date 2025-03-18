import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import datetime as dt
import os

# ----------------------------------------------------------------------------------------------------------------------

class PersonalFinanceDashboard:
    def __init__(self):

        self.transactions = None
        self.categories = ['Food', 'Transportation', 'Housing', 'Entertainment', 
                           'Utilities', 'Shopping', 'Health', 'Education', 'Income', 'Other']
        self.data_file = 'finance_data.csv'
        self.load_data()

# ----------------------------------------------------------------------------------------------------------------------
    
    def load_data(self):

        """Load transaction data from CSV or create a new file if it doesn't exist"""
        if os.path.exists(self.data_file):
            self.transactions = pd.read_csv(self.data_file, parse_dates=['Date'])
        else:
            # Create a new dataframe 

            sample_dataset = {

                'Date': [dt.datetime.now() - dt.timedelta(days=i) for i in range(30, 0, -1)],
                'Amount': [np.random.randint(-100, 100) for _ in range(30)],
                'Category': np.random.choice(self.categories, 30),
                'Description': ['Sample Transaction ' + str(i) for i in range(1, 31)]

            }
            self.transactions = pd.DataFrame(sample_dataset)
            self.save_data()
        
        #positive values for income
        mask = self.transactions['Category'] == 'Income'
        self.transactions.loc[mask, 'Amount'] = self.transactions.loc[mask, 'Amount'].abs()
        
        #negative values for expenses
        mask = self.transactions['Category'] != 'Income'
        self.transactions.loc[mask, 'Amount'] = -self.transactions.loc[mask, 'Amount'].abs()


# ----------------------------------------------------------------------------------------------------------------------
    
    def save_data(self):

        """Save transaction data to CSV"""
        self.transactions.to_csv(self.data_file, index=False)

# ----------------------------------------------------------------------------------------------------------------------

    
    def add_transaction(self, date, amount, category, description):

        """Add a new transaction to the dataset"""
        # Convert string date to datetime if needed
        if isinstance(date, str):
            date = pd.to_datetime(date)
        
        # Make amount negative for expenses, positive for income
        if category != 'Income' and amount > 0:
            amount = -amount
        elif category == 'Income' and amount < 0:
            amount = abs(amount)
        
        new_transaction = pd.DataFrame({
            'Date': [date],
            'Amount': [amount],
            'Category': [category],
            'Description': [description]
        })
        
        self.transactions = pd.concat([self.transactions, new_transaction], ignore_index=True)
        self.transactions = self.transactions.sort_values('Date', ascending=False)
        self.save_data()


# ----------------------------------------------------------------------------------------------------------------------
    
    def get_balance_over_time_history(self):

        """Calculate cumulative balance over time"""
        
        daily_sums = self.transactions.groupby(self.transactions['Date'].dt.date)['Amount'].sum()
        
        
        date_range = pd.date_range(
            start=self.transactions['Date'].min().date(),
            end=self.transactions['Date'].max().date(),
            freq='D'
        )
        
        # Create a series with all dates and fill missing values with 0
        daily_sums = daily_sums.reindex(date_range.date, fill_value=0)
        
  
        cumulative_balance = daily_sums.cumsum()
        
        return cumulative_balance
    

# ----------------------------------------------------------------------------------------------------------------------
    
    def get_monthly_spending_by_category(self):

        """Calculate monthly spending by category"""
        # Create a copy with month-year information

        df = self.transactions.copy()
        df['Month'] = df['Date'].dt.to_period('M')
        
        # Filter expenses only
        expenses = df[df['Amount'] < 0].copy()
        expenses['Amount'] = abs(expenses['Amount'])  # Convert to positive for display
        
        # Group by month and category
        monthly_by_category = expenses.pivot_table(
            index='Month', 
            columns='Category', 
            values='Amount', 
            aggfunc='sum',
            fill_value=0
        )
        
        return monthly_by_category
    
# ----------------------------------------------------------------------------------------------------------------------
    
    def get_income_vs_expenses_chart(self):

        """Calculate monthly income vs expenses"""
        # Create a copy with month-year information

        df = self.transactions.copy()
        df['Month'] = df['Date'].dt.to_period('M')
        
        # Group expenses and income
        expenses = df[df['Amount'] < 0].copy()
        expenses['Amount'] = abs(expenses['Amount'])
        income = df[df['Amount'] > 0]
        
        # Sum by month
        monthly_expenses = expenses.groupby('Month')['Amount'].sum()
        monthly_income = income.groupby('Month')['Amount'].sum()
        
        # Combine into a single dataframe

        monthly_summary = pd.DataFrame({
            'Income': monthly_income,
            'Expenses': monthly_expenses
        }).fillna(0)
        
        monthly_summary['Savings'] = monthly_summary['Income'] - monthly_summary['Expenses']
        monthly_summary['Savings_Rate'] = (monthly_summary['Savings'] / monthly_summary['Income'] * 100).fillna(0)
        
        return monthly_summary
    
# ----------------------------------------------------------------------------------------------------------------------
    
    def get_current_month_spending(self):

        """Get current month's spending by category"""

        current_month = pd.Timestamp.now().to_period('M')
        
        # Create a copy with month-year information
        df = self.transactions.copy()
        df['Month'] = df['Date'].dt.to_period('M')
        
        # Filter expenses for current month
        current_expenses = df[(df['Month'] == current_month) & (df['Amount'] < 0)].copy()
        current_expenses['Amount'] = abs(current_expenses['Amount'])
        
        return current_expenses.groupby('Category')['Amount'].sum()
    
# ----------------------------------------------------------------------------------------------------------------------
    
    def visualize_dashboard(self):

        """Generate a comprehensive financial dashboard with multiple charts"""

        # Create figure with subplots

        fig = plt.figure(figsize=(15, 10))

        fig.suptitle('Personal Finance Dashboard', fontsize=16)
        
        # Grid Setup
        gs = fig.add_gridspec(3, 2)
        ax1 = fig.add_subplot(gs[0, :])  # Balance over time - top row
        ax2 = fig.add_subplot(gs[1, 0])  # Monthly spending by category
        ax3 = fig.add_subplot(gs[1, 1])  # Income vs Expenses
        ax4 = fig.add_subplot(gs[2, 0])  # Current month spending by category
        ax5 = fig.add_subplot(gs[2, 1])  # Monthly savings rate
        
        #Balance over time

        balance_data = self.get_balance_over_time_history()

        dates = [pd.Timestamp(date) for date in balance_data.index]

        ax1.plot(dates, balance_data.values, 'b-', linewidth=2)

        ax1.fill_between(dates, balance_data.values, where=(balance_data.values > 0), 
                         color='green', alpha=0.3)
        
        ax1.fill_between(dates, balance_data.values, where=(balance_data.values < 0), 
                         color='red', alpha=0.3)
        
        ax1.set_title('Balance Over Time')

        ax1.set_ylabel('Balance (₹)')

        ax1.grid(True, linestyle='--', alpha=0.7)

        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
        
        
        ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'₹{x:,.2f}'))
        
        #Monthly spending by category

        monthly_cat_data = self.get_monthly_spending_by_category()

        if not monthly_cat_data.empty:

            # Get the last 6 months or all if less

            num_months = min(6, len(monthly_cat_data))
            monthly_cat_data = monthly_cat_data.iloc[-num_months:]
            
            monthly_cat_data.plot(kind='bar', stacked=True, ax=ax2, colormap='tab10')

            ax2.set_title('Monthly Spending by Category')

            ax2.set_ylabel('Amount (₹)')

            ax2.set_xlabel('')

            ax2.legend(loc='upper left', bbox_to_anchor=(1, 1))
            
            # Format x-axis 

            labels = [str(idx).replace('M', '-') for idx in monthly_cat_data.index]
            ax2.set_xticklabels(labels, rotation=45)
            
            # Format y-axis 

            ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'₹{x:,.0f}'))

        else:
            ax2.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax2.set_title('Monthly Spending by Category')
        
        #Income vs Expenses

        monthly_summary = self.get_income_vs_expenses_chart()

        if not monthly_summary.empty:
            # Get the last 6 months or all if less

            num_months = min(6, len(monthly_summary))
            monthly_summary = monthly_summary.iloc[-num_months:]
            
            bar_width = 0.35
            index = np.arange(len(monthly_summary.index))
            
            ax3.bar(index - bar_width/2, monthly_summary['Income'], bar_width, label='Income', color='green')
            ax3.bar(index + bar_width/2, monthly_summary['Expenses'], bar_width, label='Expenses', color='red')
            
            ax3.set_title('Income vs Expenses')
            ax3.set_ylabel('Amount (₹)')
            ax3.set_xlabel('')
            ax3.set_xticks(index)
            
            # Format x-axis 
            labels = [str(idx).replace('M', '-') for idx in monthly_summary.index]
            ax3.set_xticklabels(labels, rotation=45)
            
            ax3.legend()
            ax3.grid(True, linestyle='--', alpha=0.3, axis='y')
            
            # Format y-axis 
            ax3.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'₹{x:,.0f}'))

        else:
            ax3.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax3.set_title('Income vs Expenses')
        
        #Current month spending by category

        current_spending = self.get_current_month_spending()

        if not current_spending.empty:

            # Remove any categories with zero spending
            current_spending = current_spending[current_spending > 0]
            
            ax4.pie(current_spending, labels=current_spending.index, autopct='%1.1f%%',
                    startangle=90, counterclock=False, shadow=True)
            
            ax4.axis('equal')  # Equal aspect ratio 

            ax4.set_title(f'Current Month Spending by Category\nTotal: ₹{current_spending.sum():.2f}')

        else:
            ax4.text(0.5, 0.5, 'No expenses this month', ha='center', va='center')
            ax4.set_title('Current Month Spending')
            ax4.axis('off')
        
        #Monthly savings rate

        if not monthly_summary.empty:
            ax5.plot(range(len(monthly_summary)), monthly_summary['Savings_Rate'], 'go-', linewidth=2)
            ax5.set_title('Monthly Savings Rate')
            ax5.set_ylabel('Savings Rate (%)')
            ax5.set_xlabel('')
            ax5.set_xticks(range(len(monthly_summary)))
            
            # Format x-axis 
            labels = [str(idx).replace('M', '-') for idx in monthly_summary.index]
            ax5.set_xticklabels(labels, rotation=45)
            
            ax5.grid(True, linestyle='--', alpha=0.7)
            
            # Add a horizontal line at 0%
            ax5.axhline(y=0, color='r', linestyle='-', alpha=0.3)
            
            # Add threshold lines
            ax5.axhline(y=10, color='orange', linestyle='--', alpha=0.5)
            ax5.axhline(y=20, color='green', linestyle='--', alpha=0.5)
            
            # Add text annotations for the threshold lines
            ax5.text(0, 10, '10% - Good', verticalalignment='bottom', color='orange')
            ax5.text(0, 20, '20% - Excellent', verticalalignment='bottom', color='green')

        else:
            ax5.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax5.set_title('Monthly Savings Rate')
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

# ----------------------------------------------------------------------------------------------------------------------
    
    def run_cli(self):

        """Run a simple command-line interface for the dashboard"""
        print("\n===== Personal Finance Dashboard =====")
        
        while True:
            print("\nOptions:")
            print("1. View Dashboard")
            print("2. Add Transaction")
            print("3. View Recent Transactions")
            print("4. View Monthly Summary")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1':
                self.visualize_dashboard()
            
            elif choice == '2':
                print("\n--- Add New Transaction ---")
                
                # Get date (default to today)

                date_str = input("Date (YYYY-MM-DD, leave blank for today): ")
                if date_str.strip() == '':
                    date = dt.datetime.now()

                else:
                    try:
                        date = pd.to_datetime(date_str)
                    except:
                        print("Invalid date format. Using today's date.")
                        date = dt.datetime.now()
                
                # Get amount

                while True:
                    amount_str = input("Amount (positive for income, negative for expense): ")
                    try:
                        amount = float(amount_str)
                        break
                    except:
                        print("Invalid amount. Please enter a number.")
                
                # Get category

                print("\nCategories:", ', '.join(self.categories))
                while True:
                    category = input("Category: ")
                    if category in self.categories:
                        break
                    print(f"Category must be one of: {', '.join(self.categories)}")
                
                # Get description
                description = input("Description: ")
                
                # Add the transaction
                self.add_transaction(date, amount, category, description)
                print("Transaction added successfully!")
            
            elif choice == '3':
                print("\n--- Recent Transactions ---")
                pd.set_option('display.max_rows', None)
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                
                num_transactions = min(10, len(self.transactions))
                recent = self.transactions.head(num_transactions)
                
            
                display_df = recent.copy()
                display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
                display_df['Amount'] = display_df['Amount'].apply(lambda x: f"₹{x:,.2f}")
                
                print(display_df.to_string(index=False))
            
            elif choice == '4':

                print("\n--- Monthly Summary ---")
                monthly_summary = self.get_income_vs_expenses_chart()
                
                if not monthly_summary.empty:
                    
                    display_df = monthly_summary.copy()
                    display_df.index = display_df.index.astype(str)
                    
                    for col in ['Income', 'Expenses', 'Savings']:
                        display_df[col] = display_df[col].apply(lambda x: f"₹{x:,.2f}")
                    
                    display_df['Savings_Rate'] = display_df['Savings_Rate'].apply(lambda x: f"{x:.1f}%")
                    display_df = display_df.rename(columns={'Savings_Rate': 'Savings Rate'})
                    
                    print(display_df.to_string())
                else:
                    print("No data available for monthly summary.")
            
            elif choice == '5':
                print("\nExiting Personal Finance Dashboard. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    dashboard = PersonalFinanceDashboard()
    dashboard.run_cli()