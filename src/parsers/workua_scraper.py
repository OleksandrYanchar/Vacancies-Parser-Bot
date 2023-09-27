import requests
from bs4 import BeautifulSoup
import csv
from src.configs.settings import key_words, ban_words


class WorkUaParser:
    """
    Class with logic for parsing Work.ua website to retrieve job vacancies.
    """

    all_vacancies = []  # List to store all unique vacancies

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    def __init__(self, links_list, path_to_csv) -> None:
        """
        Initialize the WorkUaParser class.

        :param links_list: List of URLs to parse for job vacancies.
        :param csv_filename: Path to the CSV file where parsed data will be saved.
        """

        self.links_list = links_list
        self.path_to_csv = path_to_csv

    def get_vacancies_from_page(self, page_url: str):
        """
        Retrieve job vacancies from a specific page URL.

        :param page_url: URL of the page to retrieve job vacancies from.
        :return: List of job vacancies as dictionaries.
        """

        response = requests.get(page_url, headers=self.headers)
        vacancies_list = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            vacancies = soup.find_all(
                "div", class_="card card-hover card-visited wordwrap job-link"
            )

            for vacancy in vacancies:
                vacancy_title = vacancy.find("h2").text.strip()
                vacancy_link = vacancy.find("a", href=True)["href"]

                if not any(
                    keyword.lower() in vacancy_title.lower() for keyword in ban_words
                ):
                    if any(
                        keyword.lower() in vacancy_title.lower()
                        for keyword in key_words
                    ):
                        vacancies_list.append(
                            {
                                "vacancy_title": vacancy_title,
                                "vacancy_link": f"https://www.work.ua{vacancy_link}",
                            }
                        )

        return vacancies_list

    def get_all_vacancies(self) -> None:
        """
        Retrieve all job vacancies from the provided list of URLs.
        """
        for link in self.links_list:
            page_number = 1

            print(f"Parsing: {link}")

            while True:
                print(f"Parsing page number {page_number}")

                page_url = f"{link}?page={page_number}"
                vacancies_on_page = self.get_vacancies_from_page(page_url=page_url)

                if not vacancies_on_page:
                    break

                self.all_vacancies.extend(vacancies_on_page)
                page_number += 1

    def remove_duplicates(self) -> None:
        """
        Remove duplicate job vacancies from the list.
        """

        self.all_vacancies = [
            dict(t) for t in {tuple(d.items()) for d in self.all_vacancies}
        ]

    def save_to_csv(self) -> None:
        """
        Save the parsed job vacancies to a CSV file.
        """

        try:
            with open(self.path_to_csv, "a", newline="", encoding="utf-8") as file:
                fieldnames = ["vacancy_title", "vacancy_link"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                for vacancy in self.all_vacancies:
                    writer.writerow(vacancy)

        except Exception as e:
            print(e)
