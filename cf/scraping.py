from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def make_contest_url(contest_id):
    return f"https://codeforces.com/contest/{contest_id}"


def make_problem_url(contest_id, problem_id):
    return f"https://codeforces.com/contest/{contest_id}/problem/{problem_id}"


class Scraper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def get_test_cases(self, problem_url):
        self.driver_get_url(problem_url)
        sleep(0.1)
        html = self.driver.page_source

        soup = BeautifulSoup(html, "html.parser")
        sample_div = soup.find("div", class_="sample-test")
        if not sample_div:
            raise NameError("Something went wrong with html...")

        inputs = sample_div.find_all("div", class_="input")
        outputs = sample_div.find_all("div", class_="output")

        input_test, output_test = "", ""
        for i in range(len(inputs)):
            input_test += inputs[i].pre.get_text(separator="\n").strip() + "\n"
            output_test += outputs[i].pre.get_text(separator="\n").strip() + "\n"

        return input_test.strip(), output_test.strip()

    def get_problem_list(self, contest_url):
        self.driver_get_url(contest_url)
        html = self.driver.page_source
        sleep(0.1)

        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", class_="problems")
        problems = []
        for row in table.find_all("tr")[1:]:  # Skip the header row
            columns = row.find_all("td")
            if len(columns) > 1:  # Ensure the row contains data
                problem_id = columns[0].find("a").text.strip()
                problems.append(problem_id)

        return problems

    def driver_get_url(self, url):
        self.driver.get(url)
        sleep(1)

    def driver_quit(self):
        if self.driver:
            self.driver.quit()
