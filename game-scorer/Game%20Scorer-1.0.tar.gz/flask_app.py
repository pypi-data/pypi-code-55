from flask import Flask, render_template, redirect, request, url_for
from scripts.game_adt import GameList
import json


app = Flask(__name__)
with open("data/games.json") as f:
    game_json = json.load(f)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for("quiz"))
    return render_template("index.html")


@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        data = request.form

        # Get age, if not integer, redirect to wrong_age.
        age = data.get("age")
        if not age.isdigit():
            return redirect(url_for("wrong_age"))
        else:
            age = int(age)

        # Get lists of genres, themes, game_modes, and platforms.
        genres = data.getlist("genres")
        themes = data.getlist("themes")
        game_modes = data.getlist("game_modes")
        platforms = data.getlist("platforms")

        # Get years, if not both integers, redirect to wrong_year.
        year_range = [data.get("year1"), data.get("year2")]
        if not (year_range[0].isdigit() and year_range[1].isdigit()):
            return redirect(url_for("wrong_year"))
        else:
            year_range = list(map(int, year_range))
            year_range.sort()

        # Finally, use the information to score the games
        # from my data/games.json database
        game_list = GameList(game_json)
        top_games = game_list.score(genres, themes, game_modes, platforms, year_range, age)

        return render_template("top_games.html", top_games=top_games)
    return render_template("quiz.html")


@app.route("/wrong_age", methods=['GET', 'POST'])
def wrong_age():
    if request.method == 'POST':
        return redirect(url_for("quiz"))
    return render_template("wrong_age.html")


@app.route("/wrong_year", methods=['GET', 'POST'])
def wrong_year():
    if request.method == 'POST':
        return redirect(url_for("quiz"))
    return render_template("wrong_year.html")


if __name__ == '__main__':
    app.run()
