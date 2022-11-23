"""This is the example of a module. Please write the documentation along with your code."""
import typer
import requests
import os
import aganitha_base_utils as aco_log
from bs4 import BeautifulSoup
import csv

aco_log.logconfig.setup_logging()


app = typer.Typer()


@app.command()
def download(input_file: str, out_directory: str) -> None:
    """Downloads the url content and extracts the title for you"""
    valid_url_checker(input_file)
    with open('valid_urls.txt', 'r') as file:
        files: int = 0
        for url in file:
            r: requests.models.Response = requests.get(url, allow_redirects=True)
            content_type: str = r.headers.get('content-type')
            if content_type.split(';')[0] != "text/html":
                continue
            if os.path.exists("./" + out_directory):
                with open(out_directory + '/' + str(files) + ".txt", 'wb') as des:
                    des.write(r.content)
            else:
                os.mkdir("./" + out_directory)
                with open(out_directory + '/' + str(files) + ".txt", 'wb') as des:
                    des.write(r.content)
            with open(os.path.join(out_directory, str(files) + ".txt"), 'r') as open_file:
                index = open_file.read()
                soup = BeautifulSoup(index, 'html.parser')
                if soup.h1:
                    with open('titles.csv', 'a') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow([soup.h1.get_text(), url])
                elif soup.head:
                    with open('titles.csv', 'a') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow([soup.head.title.get_text(), url])
            files += 1


def valid_url_checker(input_file: str) -> None:
    if not os.path.exists(input_file):
        print("The input file {} does not exist in home directory.".format(input_file),
              "Please create an input text file and add urls in it ")
        exit()
    with open(input_file, 'r') as file:
        if os.path.exists('valid_urls.txt'):
            with open('valid_urls.txt', 'a') as url_file:
                url_file.write('\n')
        for url in file:
            r: requests.models.Response = requests.get(url, allow_redirects=True)
            if r.status_code < 400:
                with open('valid_urls.txt', 'a') as url_file:
                    url_file.write(url)
            else:
                print("This url {} is not downloadable".format(url))


if __name__ == "__main__":
    app()
