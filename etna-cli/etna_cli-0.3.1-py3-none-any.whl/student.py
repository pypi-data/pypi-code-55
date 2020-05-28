import click
from etna_cli import config


def roundify(average: str = None) -> float:
    if average is None:
        return None
    else:
        return round(float(average), 2)


@click.group(name="student")
def main():
    """Student stuff."""


@main.command()
@click.argument("student", type=click.STRING, required=False)
def info(student: str = None):
    """Get student's info."""
    wrapper = config.setup_api()
    user_data = wrapper.get_user_info(student)

    if "not found" in user_data:
        print("user not found")
        return

    for i in user_data.keys():
        # older users have roles instead of groups
        if i in ("roles", "groups"):
            print("groups : ", end="")
            [print(group, end=" ") for group in user_data[i]]
            print(end="\n")
        else:
            print("{}  : {}".format(i, user_data[i]))


@main.command()
@click.argument("student", type=click.STRING, required=False)
@click.option("-p", "--promo", help="specify student's promotion")
@click.option("-a", "--activity", help="marks for a specific activity")
def grades(student: str = None, promo: int = None, activity: str = None):
    """Get student's grades."""
    wrapper = config.setup_api()
    if promo is None:
        promo = wrapper.get_user_promotion(student)[0]['id']
    grades_data = wrapper.get_grades(login=student, promotion_id=promo)

    for i, _ in enumerate(grades_data):
        print("==============================")
        print("activity: {}".format(grades_data[i]['activity_name']))
        print("type    : {}".format(grades_data[i]['activity_type']))
        print("UV name : {}".format(grades_data[i]['uv_name']))
        print("mark    : {}".format(grades_data[i]['student_mark']))
        print("average : {}".format(roundify(grades_data[i]['average'])))
        print("max     : {}".format(grades_data[i]['maximal']))
        print("min     : {}".format(grades_data[i]['minimal']))


@main.command()
@click.argument("student", type=click.STRING, required=False)
def promo(student: str = None):
    """Get student's promotions."""
    wrapper = config.setup_api()
    promo_data = wrapper.get_user_promotion(student)

    for i, _ in enumerate(promo_data):
        print("==============================")
        print("id    : {}".format(promo_data[i]['id']))
        print("promo : {}".format(promo_data[i]['promo']))
        print("name  : {}".format(promo_data[i]['wall_name']))
        print("start : {}".format(promo_data[i]['learning_start']))
        print("end   : {}".format(promo_data[i]['learning_end']))
        if promo_data[i]['spe'] != '':
            print("spe   : {}".format(promo_data[i]['spe']))
