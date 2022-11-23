"""This is the example of a module. Please write the documentation along with your code."""
import typer
import requests
import os
from aganitha_base_utils import logconfig
from bs4 import BeautifulSoup
import csv

logconfig.setup_logging()


app = typer.Typer()


@app.command()
def download(input_file: str, out_directory: str) -> None:
    """Downloads the url content"""
    valid_url_checker(input_file)
    with open('valid_urls.txt', 'r') as file:
        files_num: int = 0
        for url in file:
            r: requests.models.Response = requests.get(url, allow_redirects=True)
            content_type: str = r.headers.get('content-type')
            if content_type.split(';')[0] != "text/html":
                continue
            if not os.path.exists("./" + out_directory):
                os.mkdir("./" + out_directory)
            with open(out_directory + '/' + str(files_num) + ".txt", 'wb') as des:
                des.write(r.content)
            files_num += 1
    title_parser(input_file, out_directory)


def title_parser(input_file: str, out_directory: str):
    """Extracts the Title"""
    url_num: int = 0
    all_urls: list[str] = []
    with open(input_file) as file:
        for url in file:
            all_urls.append(url)
    for file in os.listdir("./" + out_directory):
        with open(os.path.join(".",out_directory,str(file)), 'r') as open_file:
            index = open_file.read()
            soup = BeautifulSoup(index, 'html.parser')
            with open('titles.csv', 'a') as csv_file:
                writer = csv.writer(csv_file)
                if soup.h1:
                    writer.writerow([soup.h1.get_text(), all_urls[url_num]])
                elif soup.head:
                    writer.writerow([soup.head.title.get_text(), all_urls[url_num]])
        url_num += 1


def valid_url_checker(input_file: str) -> None:
    """Checks the valid urls and returns only those that are valid"""
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
