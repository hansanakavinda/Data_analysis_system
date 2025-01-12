import unittest
import pandas as pd

# Assuming the SalesAnalysis class is already imported from your code.

class TestSalesAnalysisWithCSV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data = pd.read_csv('Sampath_Supermarket_sales.csv')
        cls.test_data['Date'] = pd.to_datetime(cls.test_data['Date'], format='%m/%d/%Y', errors='coerce')
        cls.test_data['Month'] = cls.test_data['Date'].dt.to_period('M')

        # Create an instance of SalesAnalysis with the uploaded data
        cls.sales_analysis = SalesAnalysis(cls.test_data)

    def test_monthly_sales(self):
        # Call the method to test
        result = self.sales_analysis.monthly_sales()

        # Check if the result has expected columns
        expected_columns = ['Branch', 'Month', 'Total']
        self.assertTrue(all(col in result.columns for col in expected_columns), "Result columns do not match expected columns.")

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
