import unittest
import pandas as pd

class TestSalesAnalysisWithCSV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data = pd.read_csv('Sampath_Supermarket_sales.csv')

        # Preprocess the data
        cls.test_data['Date'] = pd.to_datetime(cls.test_data['Date'], format='%m/%d/%Y', errors='coerce')
        cls.test_data['Month'] = cls.test_data['Date'].dt.to_period('M')
        cls.test_data['Week'] = cls.test_data['Date'].dt.isocalendar().week 

        # Create an instance of SalesAnalysis with the processed data
        cls.sales_analysis = SalesAnalysis(cls.test_data)

    def test_price_payment_analysis(self):
        # Call the method to test
        result = self.sales_analysis.price_payment_analysis()

        # Check if the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check if the result contains expected columns
        self.assertIn('Payment', result.columns)
        self.assertIn('Product line', result.columns)
        self.assertIn('Unit price', result.columns)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
