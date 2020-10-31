import unittest
from selenium import webdriver
import page


class PythonOrgSearch(unittest.TestCase):
    
    def setUp(self):
        # Run every time when the test case function is run
        PATH = "/home/nxhuy/Downloads/chromedriver_linux64/chromedriver"
        self.driver = webdriver.Chrome(PATH)
        self.driver.get("http://www.python.org")

    def test_example(self):
        # Name function convention: always start with 'test' (lowercase)
        # This method will be automatically run when you run Unitest
        print("test")
        assert True

    def test_search_python(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.is_title_matches()
        mainPage.search_text_element = "pycon"
        mainPage.click_go_button()
        search_result_page = page.SearchResultPage(self.driver)
        assert search_result_page.is_results_found()

    def tearDown(self):
        # Run after the test case is finished
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()