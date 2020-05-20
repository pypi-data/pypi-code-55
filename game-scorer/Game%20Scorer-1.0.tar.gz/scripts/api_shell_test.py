# THIS FILE IS USED FOR TESTING VARIOUS ASPECTS OF THE API SHELL


from scripts.api_shell import IGDBAPI


fields = ['age_ratings', 'aggregated_rating', 'cover',
          'first_release_date', 'game_modes', 'genres', 'involved_companies',
          'name', 'platforms', 'popularity', 'screenshots', 'slug', 'status', 'summary', 'themes']
cats = ["where aggregated_rating > 90 & category = 0", "sort popularity desc", "limit 500"]


if __name__ == '__main__':
    api = IGDBAPI("19c706e2c8762c30f30d98511d7a942b")

    rating = api.get_cover(['url'], ['where id=76781'])
    # games = api.get_age_ratings(['rating', 'synopsis'], ['where id=24721', 'limit 10'])
    # games = api.get_status()
    # print(games)
    api.dump_json(rating, "testing.json")
