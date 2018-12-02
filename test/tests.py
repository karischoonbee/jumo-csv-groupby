import unittest
from jumo_csv_groupby.src.jumo_csv import Frame
import numpy as np

class TestCSV(unittest.TestCase):

    def setUp(self):
        self.f = Frame().from_csv('data/Loans.csv')
        self.f = Frame().from_csv('data/Loans.csv')

    def test_aggregation(self):
        self.assertEqual(18451, self.f.aggregate_on('Amount').columns['sum'])
        self.assertEqual(2306.375, self.f.aggregate_on('Amount', agg=np.mean).columns['mean'])
        self.assertEqual(1864.5, self.f.aggregate_on('Amount', agg=np.median).columns['median'])

    def test_aggregation_column_not_exist(self):
        with self.assertRaises(ValueError) as context:
            self.f.aggregate_on('Tnhoma')
            self.assertTrue(self.assertTrue('No column named' in str(context.exception)))

    def test_groupby(self):
        ret = self.f.aggregate_on('Amount', group_by=['Network', 'Product'])
        ind = [i for i, (v, x) in enumerate(zip(ret.columns['Product'], ret.columns['Network'])) if
               v == 'Loan Product 1' and x == 'Network 2'][0]
        self.assertEqual(6793, ret.columns['Amount'][ind])

    def test_groupby_all_groups(self):
        ret = self.f.aggregate_on('Amount', group_by=['Network', 'Product'], all_groups=True)
        ind = [i for i, (v, x) in enumerate(zip(ret.columns['Product'], ret.columns['Network'])) if
               v == 'Loan Product 3' and x == 'Network 1'][0]
        self.assertEqual(0, ret.columns['Amount'][ind])

    def test_groupby_column_not_exist(self):
        with self.assertRaises(ValueError) as context:
            self.f.aggregate_on('Amount', group_by=['Random', 'Words'])
            self.assertTrue(self.assertTrue('No column named' in str(context.exception)))

    def test_aggregate_csv_missing_values(self):
        with self.assertRaises(ValueError) as context:
            self.f = Frame().from_csv('data/Loans_missing_values.csv')
            self.f.aggregate_on('Amount', group_by=['Network', 'Product'])
            self.assertTrue(self.assertTrue('Column not of numeric type' in str(context.exception)))

    def test_aggregate_csv_column_different_datatypes(self):
        with self.assertRaises(ValueError) as context:
            self.f = Frame().from_csv('data/Loans_mixed_dtypes.csv')
            self.f.aggregate_on('Amount', group_by=['Network', 'Product'])
            self.assertTrue(self.assertTrue('Column not of numeric type' in str(context.exception)))

if __name__ == '__main__':
    unittest.main()
