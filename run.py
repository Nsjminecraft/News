from flask import Flask, render_template, request
from newsapi import NewsApiClient

app = Flask(__name__)

newsapi = NewsApiClient(api_key='70fdb9ba81ba40b6bda148e672898bd9')

def get_sources_and_domains():
    all_sources = newsapi.get_sources()['sources']
    sources = []
    domains = []
    for e in all_sources:
        id = e['id']
        domain = e['url'].replace("http://", "")
        domain = domain.replace("https://", "")
        domain = domain.replace("www.", "")
        slash = domain.find('/')
        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)
    sources = ", ".join(sources)
    domains = ", ".join(domains)
    return sources, domains

@app.route("/", methods=['GET', 'POST'])
def home():
        top_headlines = newsapi.get_top_headlines(country="gb", language="en")
        total_results = top_headlines['totalResults']
        if total_results > 100:
            total_results = 100
        all_headlines = newsapi.get_top_headlines(country="gb",
                                                     language="en", 
                                                     page_size=total_results)['articles']
        return render_template("home.html", all_headlines = all_headlines)
        return render_template("home.html")

if __name__ == "__main__":
        app.run(host='0.0.0.0',port=8080, debug=True)
