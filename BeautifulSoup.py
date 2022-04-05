import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import unidecode


class Jobs:

    def getUrl(self):
        html_text = requests.get(
            'https://www.blikk.hu/').text
        soup = BeautifulSoup(html_text, 'lxml')
        return soup

    def singleArticle(self):
        soup = self.getUrl()
        job = soup.find('section', class_='blockWrapper colMain')
        job_title = job.article.text.replace(" ", "")
        print(job_title)

    def getTopics(self):
        list_topics = []
        soup = self.getUrl()
        post = soup.find("div", class_="mainWrapper asideContainer")
        topics = post.findAll("p", class_="mark")
        for topic in topics:
            t = topic.text.strip().replace('"', '')
            unaccented_string = unidecode.unidecode(t)
            list_topics.append(re.sub("[!'@#$”„;:?,]", "", unaccented_string))
            list_topics.append(topic.text.strip())
        return list_topics

    def getTitle(self):
        titles = []
        soup = self.getUrl()
        post = soup.find("div", class_="mainWrapper asideContainer")
        sections = post.findAll("h2", class_="")
        for section in sections:
            title = section.text.strip().replace('"', '')
            unaccented_string = unidecode.unidecode(title)
            titles.append(re.sub("[!'@#$”„;:?,]", "", unaccented_string))
        return titles

    def getUrls(self):
        urls_list = []
        soup = self.getUrl()
        post = soup.find("div", class_="mainWrapper asideContainer")
        article = post.find("section", class_="blockWrapper colMain")
        urls = article.findAll("a", attrs={'href': re.compile("^https://")})
        for url in urls:
            link = url.text.strip().replace('"', '')
            unaccented_string = unidecode.unidecode(link)
            urls_list.append(re.sub("[!'@#$”„;:?,]", "", unaccented_string))
            urls_list.append(url.get('href'))
        return urls_list

    def saveTitleResults(self):
        titles = self.getTitle()
        with open("titles.csv", "w") as output:
            output.write("Title\n")
            for title in titles:
                output.write(title + "\n")

    def saveUrls(self):
        urls = self.getUrls()
        with open("urls.csv", "w") as output:
            for url in urls:
                output.write(url + "\n")


class IMDB:

    def getUrl(self):
        html_text = requests.get(
            'https://www.imdb.com/chart/top/', headers={"Accept-Language": "en-US, en;q=0.5"}).text
        soup = BeautifulSoup(html_text, 'lxml')
        return soup

    def getTopMovies(self):
        titles_list = []
        years_list = []
        ratings_list = []
        soup = self.getUrl()
        section = soup.find("tbody", class_="lister-list")
        titles = section.findAll("td", class_="titleColumn")
        years = section.findAll("span", class_="secondaryInfo")
        ratings = section.findAll("td", class_="ratingColumn imdbRating")
        for rating in ratings:
            ratings_list.append(rating.text.strip())
        for year in years:
            result = re.sub('[!@#$()]', '', year.text)
            years_list.append(result)
        for title in titles:
            r = title.text.strip().replace("\n", "").split(".")
            titles_list.append(r[1].replace('  ', ''))
        return titles_list, years_list, ratings_list

    def saveResults(self):
        titles_list, years_list, ratings_list = self.getTopMovies()
        test_df = pd.DataFrame({
            'title': titles_list,
            'year': years_list,
            'rating': ratings_list,
        })
        test_df.to_csv('TopMovies.csv', sep='\t')


