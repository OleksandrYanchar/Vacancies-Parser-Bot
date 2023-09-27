import requests
import re
import csv
from bs4 import BeautifulSoup

class JobsScraper:
    def __init__(self, jobs_url, csv_filename):
        """ Initialize the JobsScraper class.
         :param jobs_url: URL to parse for job vacancies.
         :param csv_filename: Path to the CSV file where parsed data will be saved.
         """
        self.page_url = jobs_url
        self.csv_filename = csv_filename
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    
    def check_matches(self, job_title):
        """ 
        checks the vacancies titles for keywords: python, backend 
        :return boolean value of match
        """
        match = re.search(rf'(?i)(\b(?:python|backend)\b)', job_title)
        return bool(match)
    
    def check_banwords(self, job_title):
        """
        checks the vacancies titles for banwords: middle, senior
        :return boolean value of match
        """
        banwords = re.search(rf'(?i)(\b(?:middle|senior)\b)', job_title)
        return bool(banwords)

    def get_vacancies_from_page(self):
        """ 
        Retrieve job vacancies from a specific page URL
          """
        response = requests.get(self.page_url, headers=self.headers)
        vacancies_list = []

        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                elements = soup.find_all('a', class_='vt')  # Updated selector

                for element in elements:
                    job_link = element['href']
                    job_title = element.get_text(strip=True)

                    # Add job to the list if it matches the criteria and does not contain banwords.
                    if job_link and job_title and self.check_matches(job_title) and not self.check_banwords(job_title):
                        vacancies_list.append(f"{job_link} - {job_title}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        return vacancies_list

    def save_to_csv(self, job_title, job_link):
        """  
        Save the parsed job vacancies to a CSV file
        """
        try:
            with open(self.csv_filename, "a", newline="", encoding="utf-8") as file:
                fieldnames = ["vacancy_title", "vacancy_link"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow({"vacancy_title": job_title, "vacancy_link": job_link})
        except Exception as e:
            print(f"An error occurred: {str(e)}")
