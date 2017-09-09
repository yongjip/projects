from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from data_reader import get_recent20
from sqlalchemy import MetaData, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from db_url import url

Base = declarative_base()

table_name = 'trump_twitter_data'
url = url

engine = create_engine(url, client_encoding="utf8", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

meta = MetaData(bind=engine)
trump_twitter_data = Table(table_name, meta, autoload=True)
cols = trump_twitter_data.columns.keys()

q = trump_twitter_data.select().order_by('id DESC').limit(20)
result = session.execute(q)
outputs = result.fetchall()
data = pd.DataFrame(outputs, columns=cols)
tweets = list(data.T.to_dict().values())

app = Flask(__name__)
Bootstrap(app)
#DATA_PATH = "../data/cleaned_data/trumps_twitter_data_with_scores.json"
#DATA_PATH = "/var/www/projects/trump_project/data/cleaned_data/trumps_twitter_data_with_scores.json"


@app.route("/")
def hello():
    return render_template("main.html", tweets=tweets)


def main():
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
