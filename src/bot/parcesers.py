from src.parsers.jobs_scraper import JobsScraper
from src.parsers.jooble_scraper import JoobleScraper
from src.parsers.workua_scraper import WorkUaParser
from src.configs.settings import jobs_url, jooble_url, vacansies_txt, csv_filename, urls

def joobl_launcher():
    job_scraper = JoobleScraper(jooble_url, csv_filename)
    vacancies = job_scraper.get_vacancies_from_page()

    with open(vacansies_txt, 'a', encoding='utf-8') as file:
        for vacancy in vacancies:
            file.write(vacancy + '\n\n\n')

    for vacancy in vacancies:
        job_link, job_title = vacancy.split(" - ", 1)
        job_scraper.save_to_csv(job_title, job_link)

    print("Посилання та назви вакансій з Jooble були записані у файл 'vacancies.txt'")

def jobs_launcher():
    job_scraper = JobsScraper(jobs_url, csv_filename)
    vacancies = job_scraper.get_vacancies_from_page()

    with open(vacansies_txt, 'a', encoding='utf-8') as file:
        for vacancy in vacancies:
            file.write(vacancy + '\n\n\n')

    for vacancy in vacancies:
        job_link, job_title = vacancy.split(" - ", 1)
        job_scraper.save_to_csv(job_title, job_link)

    print("Посилання та назви вакансій з Joobs.duo були записані у файл 'vacancies.txt'")

def workua_launcher():
    """
    Main function to initiate the parsing process.
    """

    parser = WorkUaParser(links_list=urls, path_to_csv=csv_filename)
    parser.get_all_vacancies()
    parser.remove_duplicates()
    parser.save_to_csv()
    parser.save_to_txt()
    print("Посилання та назви вакансій з Workua були записані у файл 'vacancies.txt'")
