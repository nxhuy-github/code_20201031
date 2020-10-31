import unittest

from my_sum import sum

class TestSum(unittest.TestCase):
    def test_list_int(self):
        data = [1,2,3]
        total = sum(data)
        self.assertEqual(total, 6)

if __name__ == '__main__':
    unittest.main()