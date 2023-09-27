import requests
import re
import csv
from bs4 import BeautifulSoup


class JoobleScraper:
    """
    Class with logic for parsing ua.jooble.org website to retrieve job vacancies.
    """

    def __init__(self, jooble_url, csv_filename):
        self.page_url = jooble_url
        self.csv_filename = csv_filename
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        """ Initialize the WorkUaParser class.
        :param jooble_url: URL to parse for job vacancies.
        :param csv_filename: Path to the CSV file where parsed data will be saved.
        """

    def check_matches(self, job_title):
        match = re.search(
            rf"(?i)(\b(?:python|backend)\b.*\b(?:junior|trainee)\b|\b(?:junior|trainee)\b.*\b(?:python|backend)\b)",
            job_title,
        )
        return bool(match)

    """
    Checks vacancies titles for keywords: python, backend, junior, trainee
    :return boolean value of matches
    """

    def get_vacancies_from_page(self):
        response = requests.get(self.page_url, headers=self.headers)
        vacancies_list = []

        """
        Retrieve job vacancies from a specific page URL.

        :param page_url: URL of the page to retrieve job vacancies from.
        :return: List of job vacancies as dictionaries.
        """

        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                elements = soup.find_all(class_="jkit_Efecu")

                for element in elements:
                    job_link = element["href"]
                    job_title = element.get_text(strip=True)

                    if job_link and job_title and self.check_matches(job_title):
                        vacancies_list.append(f"{job_link} - {job_title}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        return vacancies_list

    def save_to_csv(self, job_title, job_link):
        try:
            with open(self.csv_filename, "a", newline="", encoding="utf-8") as file:
                fieldnames = ["vacancy_title", "vacancy_link"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow({"vacancy_title": job_title, "vacancy_link": job_link})
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        """
        Save the parsed job vacancies to a CSV file.
        """
