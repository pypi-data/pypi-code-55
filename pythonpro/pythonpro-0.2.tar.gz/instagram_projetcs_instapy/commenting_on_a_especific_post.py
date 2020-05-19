from instapy import InstaPy

# login credentials
insta_username = 'escapodelamuerte'
insta_password = '21822138'

session = InstaPy(username=insta_username, password=insta_password, headless_browser=False)
session.login()
# set up all the settings
session.set_relationship_bounds(enabled=True,
                                delimit_by_numbers=True)
session.set_do_comment(True, percentage=100)
session.set_comments(['►', '☼', '☺'])

# do the actual liking
session.interact_by_URL(urls=["B4WPIQhH4v0LNOmA7lTVinx1R2AUakxK6JRATM0"], randomize=False, interact=True)

# end the bot session
session.end()
