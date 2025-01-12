import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from google.colab import files
import io

# ----------------------------- Data Loader Factory ----------------------------- #
class DataLoader:
    def load_data(self):
        raise NotImplementedError("Subclasses must implement 'load_data' method.")

class CSVDataLoader(DataLoader):
    def load_data(self):
        uploaded = files.upload()  # This will prompt you to upload the file
        for filename in uploaded.keys():
            if filename.endswith('.csv'):
                data = pd.read_csv(io.StringIO(uploaded[filename].decode('utf-8')))
                return data
        raise ValueError("Unsupported file type. Please upload a CSV file.")

class DataLoaderFactory:
    @staticmethod
    def get_data_loader(file_type):
        if file_type == "csv":
            return CSVDataLoader()
        # Future extensions: Add other data loaders here (e.g., JSON, Excel)
        raise ValueError(f"Unsupported file type: {file_type}")

# ----------------------------- Data Preprocessing Class ----------------------------- #
class DataPreprocessor:
    def preprocess(self, data):
        data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y', errors='coerce')
        if data['Date'].isnull().any():
            raise ValueError("Invalid date format detected. Ensure dates follow 'mm/dd/yyyy'.")
        data['Month'] = data['Date'].dt.to_period('M')
        data['Week'] = data['Date'].dt.isocalendar().week  # Extract week number
        return data

# ----------------------------- Sales Analysis Class ----------------------------- #
class SalesAnalysis:
    def __init__(self, data):
        self.data = data

    def monthly_sales(self):
        monthly_sales = self.data.groupby(['Branch', 'Month'])['Total'].sum().reset_index()
        monthly_sales['Month'] = monthly_sales['Month'].dt.to_timestamp()
        return monthly_sales

    def weekly_sales(self):
        weekly_sales = self.data.groupby('Week')['Total'].sum().reset_index()
        return weekly_sales

    def price_payment_analysis(self):
        price_payment_analysis = self.data.groupby(['Product line', 'Payment'])['Unit price'].mean().reset_index()
        return price_payment_analysis

    def product_preference_customer_type(self):
        product_preference_customer_type = self.data.groupby(['Product line', 'Customer type'])['Total'].sum().reset_index()
        return product_preference_customer_type

    def forecast_sales(self, monthly_sales):
        global_combined = pd.DataFrame()
        global_forecast = pd.DataFrame()

        for branch in monthly_sales['Branch'].unique():
            branch_sales = monthly_sales[monthly_sales['Branch'] == branch]
            branch_sales = branch_sales.reset_index(drop=True)
            branch_sales['Time'] = np.arange(len(branch_sales))
            X = branch_sales[['Time']]
            y = branch_sales['Total']

            # Fit Linear Regression Model
            model = LinearRegression()
            model.fit(X, y)

            # Predict future sales (combine existing and forecasted)
            future_time = np.arange(len(branch_sales), len(branch_sales) + 3).reshape(-1, 1)
            forecast = model.predict(future_time)

            # Fix forecast months: generate forecast months without any gap
            last_month = branch_sales['Month'].max()
            forecast_months = [last_month + pd.DateOffset(months=i) for i in range(1, 4)]  # Next 3 months

            # Combine actual and forecasted sales
            combined_months = branch_sales['Month'].tolist() + forecast_months
            combined_totals = branch_sales['Total'].tolist() + forecast.tolist()

            # Append combined data for all branches
            branch_combined = pd.DataFrame({
                'Month': combined_months,
                'Total': combined_totals,
                'Branch': branch
            })
            global_combined = pd.concat([global_combined, branch_combined], ignore_index=True)

            forecast_combined = pd.DataFrame({
                'Month': forecast_months,
                'Total': forecast.tolist(),
                'Branch': branch
            })
            global_forecast = pd.concat([global_forecast, forecast_combined], ignore_index=True)

        return global_combined, global_forecast

# ----------------------------- Plotting Class ----------------------------- #
class SalesPlotter:
    def plot_monthly_sales(self, global_combined, global_forecast):
        plt.figure(figsize=(12, 8))
        for branch in global_combined['Branch'].unique():
            branch_data = global_combined[global_combined['Branch'] == branch]
            branch_forecast = global_forecast[global_forecast['Branch'] == branch]
            plt.plot(branch_data['Month'], branch_data['Total'], marker='o', linestyle='-', label=f'Branch {branch}')
            plt.plot(branch_forecast['Month'], branch_forecast['Total'], marker='o', linestyle='--', label=f'Branch {branch} Forecast')

        plt.title('Monthly Sales Analysis with 3-Month Forecast for All Branches')
        plt.xlabel('Month')
        plt.ylabel('Total Sales')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.show()

    def plot_price_payment(self, price_payment_pivot):
        plt.figure(figsize=(12, 6))
        for payment in price_payment_pivot.columns:
            plt.plot(price_payment_pivot.index, price_payment_pivot[payment], marker='o', label=f'{payment} Payment')

        plt.title('Average Unit Price by Product Line and Payment Method')
        plt.xlabel('Product Line')
        plt.ylabel('Average Unit Price')
        plt.xticks(rotation=45)
        plt.legend(title='Payment Method')
        plt.grid(True)
        plt.show()

    def plot_product_preference(self, product_preference_customer_type):
        plt.figure(figsize=(12, 6))
        sns.barplot(data=product_preference_customer_type, x='Product line', y='Total', hue='Customer type')
        plt.title('Product Preference Based on Customer Type')
        plt.xlabel('Product Line')
        plt.ylabel('Total Sales')
        plt.xticks(rotation=45)
        plt.legend(title='Customer Type')
        plt.show()

    def plot_weekly_sales(self, weekly_sales):
        plt.figure(figsize=(12, 6))
        plt.plot(weekly_sales['Week'], weekly_sales['Total'], marker='o', linestyle='-', color='b')
        plt.title('Weekly Sales Analysis of Supermarket Network')
        plt.xlabel('Week Number')
        plt.ylabel('Total Sales')
        plt.grid(True)
        plt.show()

    def plot_histogram(self, data):
        plt.figure(figsize=(12, 6))
        sns.histplot(data['Total'], kde=True, color='purple')
        plt.title('Distribution of Total Sales Amount of Purchases')
        plt.xlabel('Total Sales Amount')
        plt.ylabel('Frequency')
        plt.show()

# ----------------------------- Singleton Sales Analysis System ----------------------------- #
class SalesAnalysisSystem:
    _instance = None

    def __new__(cls):
        """Ensure that only one instance of the SalesAnalysisSystem exists."""
        if not cls._instance:
            cls._instance = super(SalesAnalysisSystem, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.data_loader = DataLoaderFactory.get_data_loader('csv')  # Use Factory
            self.data_preprocessor = DataPreprocessor()
            self.sales_analysis = None
            self.sales_plotter = SalesPlotter()

    def run(self):
        # Load and preprocess data
        data = self.data_loader.load_data()
        processed_data = self.data_preprocessor.preprocess(data)

        # Perform sales analysis
        self.sales_analysis = SalesAnalysis(processed_data)
        monthly_sales = self.sales_analysis.monthly_sales()
        weekly_sales = self.sales_analysis.weekly_sales()
        price_payment_analysis = self.sales_analysis.price_payment_analysis()
        product_preference_customer_type = self.sales_analysis.product_preference_customer_type()

        # Forecast sales and combine results
        global_combined, global_forecast = self.sales_analysis.forecast_sales(monthly_sales)

        # Plot results
        self.sales_plotter.plot_monthly_sales(global_combined, global_forecast)
        price_payment_pivot = price_payment_analysis.pivot(index='Product line', columns='Payment', values='Unit price')
        self.sales_plotter.plot_price_payment(price_payment_pivot)
        self.sales_plotter.plot_product_preference(product_preference_customer_type)
        self.sales_plotter.plot_weekly_sales(weekly_sales)
        self.sales_plotter.plot_histogram(data)

# ----------------------------- Run the System ----------------------------- #
if __name__ == "__main__":
    system = SalesAnalysisSystem()  # Ensures only one instance is created
    system.run()
