from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from pathlib import Path
from accountinfo import username, password


def get_articles():
    url = "https://www.reuters.com/business/macromatters/"
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")

    html_class = "StoryCollection__story___3EY8PG"
    articles = soup.find_all("div", {"class": html_class})

    article_data = []
    for article in articles:
        html_name_class = "Text__text___3eVx1j Text__dark-grey___AS2I_p Text__medium___1ocDap Text__heading_6___m3CqfX Heading__base___1dDlXY Heading__heading_6___1ON736 MediaStoryCard__heading___1K4tAO"
        try:
            name = article.find_all('span', {'class': html_name_class})[0].text
        except:
            name = "[Title not found]"
        date = article.find('time').text
        link = 'https://www.reuters.com/' + article.find('a')["href"]
        tpl = (name, date, link)
        article_data.append(tpl)

    return article_data


def send_email():
    daily_articles = get_articles()

    variables = {}
    for x in range(9):
        variables[f"name{x}"] = daily_articles[x][0]
        variables[f"date{x}"] = daily_articles[x][1]
        variables[f"url{x}"] = daily_articles[x][2]

    template = Template(Path("template.html").read_text())
    body = template.substitute(variables)

    message = MIMEMultipart()
    message['from'] = "Python Bot"
    message['to'] = "twhiteley@islstudent.ch"
    message['subject'] = "Daily news articles"
    message.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(message)

    return None


send_email()
