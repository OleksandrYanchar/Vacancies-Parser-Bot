import csv
from src.configs.settings import csv_filename
import threading
from src.bot.parcesers import jobs_launcher, joobl_launcher, workua_launcher

#creates first lines in csv file with names vacancy_title and vacancy_link 
def crate_table():
    with open(csv_filename, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["vacancy_title", "vacancy_link"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

# creates thread of funcsions to execute them  at same time
async def thread():
    funcs = [crate_table, joobl_launcher, jobs_launcher, workua_launcher ]


    max_threads = 7

    thread_semaphore = threading.Semaphore(max_threads)

    threads = []
    for func in funcs:
        thread = threading.Thread(target=func)
        threads.append(thread)

    for thread in threads:
        thread_semaphore.acquire()
        thread.start()

    for thread in threads:
        thread.join()


    thread_semaphore.release()
    print("Всі потоки завершили роботу")

