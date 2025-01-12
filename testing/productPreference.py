import unittest
import pandas as pd

class TestSalesAnalysisWithCSV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data = pd.read_csv('Sampath_Supermarket_sales.csv') 
        cls.test_data['Date'] = pd.to_datetime(cls.test_data['Date'], format='%m/%d/%Y', errors='coerce')

        # Create an instance of SalesAnalysis with the processed data
        cls.sales_analysis = SalesAnalysis(cls.test_data)

    def test_product_preference_customer_type(self):
        # Call the method to test
        result = self.sales_analysis.product_preference_customer_type()

        # Check if the result has the expected columns
        self.assertIn('Product line', result.columns)
        self.assertIn('Customer type', result.columns)
        self.assertIn('Total', result.columns)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
