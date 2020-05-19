from instapy import InstaPy

# login credentials
insta_username = 'escapodelamuerte'
insta_password = '21822138'

session = InstaPy(username=insta_username, password=insta_password, headless_browser=True)
session.login()
session.set_relationship_bounds(enabled=True,
                                max_followers=5000,
                                min_followers=45,
                                min_following=77)

# session.set_dont_like(["naked", "nsfw", "Junior", "JuniorTúPapa", "outfit",
#                        "amor", "ropa","tiendaonline", "veneca", "love"])
# session.set_do_follow(True, percentage=50)
#
# session.like_by_tags(["carnavaldebarranquilla2020"], amount=3)

session.follow_user_followers(['andreavaldirisos'], amount=25, randomize=False, sleep_delay=60)
