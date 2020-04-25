# sudo apt-get install chromium-chromedriver
# install the following packages before running this script #
# pip install gitpython schedule pandas beautifulsoup4 selenium

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
from git import Repo

# make sure .git folder is properly configured
PATH_OF_GIT_REPO = '/home/abhiroop43/abhiroop43.github.io/.git'
COMMIT_MESSAGE = 'commit from python script'


class CoronaScraper:

    def git_push(self):
        try:
            start = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            print('Updating the repo started at: ' + start)
            repo = Repo(PATH_OF_GIT_REPO)
            repo.git.add(update=True)
            repo.index.commit(COMMIT_MESSAGE)
            origin = repo.remote(name='origin')
            origin.push()
            start = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            print('Updating the repo completed at: ' + start)
        except Exception as e:
            print('Some error occured while pushing the code: ' + e)

    def scrapeForCorona(self):

        # Obtain current time
        start = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        print('Starting scrape at: ' + start)
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(
                "/usr/bin/chromedriver", options=chrome_options)

            country_list = []
            total_cases_list = []
            new_cases_list = []
            total_deaths_list = []
            new_deaths_list = []
            total_recovered_list = []
            active_cases_list = []
            serious_critical_list = []
            cases_1M_pop_list = []
            deaths_1M_pop_list = []
            total_tests_list = []
            tests_1M_pop_list = []

            driver.get('https://www.worldometers.info/coronavirus/')
            content = driver.page_source
            soup = BeautifulSoup(content, features="html.parser")
            dataRows = soup.find('table', attrs={'id': 'main_table_countries_today'}).find(
                "tbody").find_all("tr")

            for row in dataRows:
                # parse row to get the cells #
                cells = row.find_all("td")

                # get values #
                country = cells[0].get_text().strip()
                if (country == ''):
                    continue
                total_cases = cells[1].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')
                new_cases = cells[2].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')
                total_deaths = cells[3].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')
                new_deaths = cells[4].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')
                total_recovered = cells[5].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')
                active_cases = cells[6].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')
                serious_critical = cells[7].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')
                cases_1M_pop = cells[8].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')
                deaths_1M_pop = cells[9].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')
                total_tests = cells[10].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')
                tests_1M_pop = cells[11].get_text().strip().replace(
                    '+', '').replace('-', '').replace(',', '')

                # append values to list #
                country_list.append(country)
                total_cases_list.append(total_cases)
                new_cases_list.append(new_cases)
                total_deaths_list.append(total_deaths)
                new_deaths_list.append(new_deaths)
                total_recovered_list.append(total_recovered)
                active_cases_list.append(active_cases)
                serious_critical_list.append(serious_critical)
                cases_1M_pop_list.append(cases_1M_pop)
                deaths_1M_pop_list.append(deaths_1M_pop)
                total_tests_list.append(total_tests)
                tests_1M_pop_list.append(tests_1M_pop)

            # df = pd.DataFrame(
            #     {'Country, Other': country_list, 'Total Cases': total_cases_list, 'New Cases': new_cases_list,
            #      'Total Deaths': total_deaths_list, 'New Deaths': new_deaths_list, 'Total Recovered': total_recovered_list,
            #      'Active Cases': active_cases_list, 'Serious, Critical': serious_critical_list, 'Total Cases/1M pop': cases_1M_pop_list,
            #      'Deaths/1M pop': deaths_1M_pop_list, 'Total Tests': total_tests_list, 'Tests/1M pop': tests_1M_pop_list})

            # make dataframe more json friendly
            df = pd.DataFrame(
                {'country': country_list, 'totalCases': total_cases_list, 'newCases': new_cases_list,
                 'totalDeaths': total_deaths_list, 'newDeaths': new_deaths_list, 'totalRecovered': total_recovered_list,
                 'activeCases': active_cases_list, 'seriousCritical': serious_critical_list, 'totalCasesPerMillion': cases_1M_pop_list,
                 'deathsPerMillion': deaths_1M_pop_list, 'totalTests': total_tests_list, 'testsPerMillion': tests_1M_pop_list})

            df.to_json('/home/abhiroop43/abhiroop43.github.io/scrape/corona_today.json',
                       orient='records', indent=4)
            # df.to_csv('corona_today.csv', index=False, encoding='utf-8')
            start = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            print('Completed scrape at: ' + start)
            self.git_push()
        except Exception as e:
            print('Failed to scrape data: ' + e)
            # raise


while True:
    scrape_me = CoronaScraper()
    scrape_me.scrapeForCorona()
    time.sleep(3600)  # refresh every hour
