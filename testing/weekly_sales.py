import unittest
import pandas as pd

class TestSalesAnalysisWithCSV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data = pd.read_csv('Sampath_Supermarket_sales.csv')

        # Preprocess the data
        cls.test_data['Date'] = pd.to_datetime(cls.test_data['Date'], format='%m/%d/%Y', errors='coerce')

        # Generate Month and Week columns
        cls.test_data['Month'] = cls.test_data['Date'].dt.to_period('M')
        cls.test_data['Week'] = cls.test_data['Date'].dt.isocalendar().week  # Extract week number

        # Create an instance of SalesAnalysis with the processed data
        cls.sales_analysis = SalesAnalysis(cls.test_data)

    def test_weekly_sales(self):
        # Call the method to test
        result = self.sales_analysis.weekly_sales()

        # Check if the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check if the necessary columns exist in the result
        self.assertIn('Week', result.columns)
        self.assertIn('Total', result.columns)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
