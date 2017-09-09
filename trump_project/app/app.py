from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from data_reader import get_recent20

app = Flask(__name__)
Bootstrap(app)
DATA_PATH = "../data/cleaned_data/trumps_twitter_data_with_scores.json"
# DATA_PATH = "/var/www/projects/trump_project/data/cleaned_data/trumps_twitter_data_with_scores.json"


@app.route("/")
def home():
    return render_template("main.html", tweets=get_recent20(DATA_PATH))


def main():
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
