import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

#function to retrive articles details
def get_articles():

    url = 'https://www.theverge.com'
    response = requests.get(url)    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    # search for <h2>
    for article in soup.find_all('h2'):

        #find title and link
        title_tag = article.find('a')
        if title_tag:
            title = title_tag.text.strip()
            link = url + title_tag['href']


            #find datetime
            parent = article.find_parent('div')
            siblings = [elem for elem in parent if elem != article]

            for sibling in siblings:
                if sibling.find('time'):
                    time = sibling.find('time')['datetime']
                    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
                    #1st of January 2022 onward
                    if time >= datetime(2022, 1, 1):
                        date = time.date()
                    break

            if date:
                articles.append({
                    'title': title, 
                    'link': link, 
                    'date': date}
                    )


    #sort articles by date
    articles = sorted(articles, key=lambda x: x['date'], reverse=True)
    return articles



@app.route('/')
def home():
    articles = get_articles()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
