import unittest
from data_manager import DataManager
from models import Question, Category


class TestQuizApp(unittest.TestCase):
    def setUp(self):
        self.dm = DataManager('test_data.json')

    def test_save_load(self):
        q = Question("Test?", ["a", "b", "c", "d"], 1, "test")
        cat = Category("TestCat", [q])
        self.dm.add_category(cat)
        self.dm.load_data()
        self.assertEqual(len(self.dm.categories), 1)
        self.assertEqual(self.dm.categories[0].name, "TestCat")
        self.assertEqual(len(self.dm.categories[0].questions), 1)
        self.assertEqual(self.dm.categories[0].questions[0].text, "Test?")

    def test_result_save(self):
        self.dm.add_result("testuser", 8, 10)
        self.assertEqual(len(self.dm.results), 1)
        r = self.dm.results[0]
        self.assertEqual(r['user'], "testuser")
        self.assertEqual(r['score'], 8)
        self.assertEqual(r['total'], 10)
        self.assertGreaterEqual(r['percent'], 79.9)
        self.assertLessEqual(r['percent'], 80.1)


if __name__ == '__main__':
    unittest.main()