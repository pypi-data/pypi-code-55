import click
import operator

from etna_cli import config


@click.group(name="rank")
def main():
    """Rank by promotion."""


@main.command(name="list")
@click.argument("student", type=click.STRING, required=False)
@click.option("-p", "--promo", help="specify promo ID")
def get_student_rank(student: str = None, promo: str = None):
    """Get student rank."""
    wrapper = config.setup_api()
    if promo is None and student is None:
        student_info = wrapper.get_user_info()
        login = student_info['login']
        promo = wrapper.get_user_promotion(login)[0]['id']
    elif student is not None and promo is None:
        promo = wrapper.get_user_promotion(student)[0]['id']
    elif student is None and promo is not None:
        student_info = wrapper.get_user_info()
        login = student_info['login']
    else:
        return

    promo_list = get_students_by_promo(wrapper, int(promo))
    if promo_list is None:
        return
    student_marks = calc_student_marks(wrapper, promo_list, int(promo))
    sorted_students = sorted(student_marks.items(),
                             key=operator.itemgetter(1),
                             reverse=True)

    for i in range(0, len(sorted_students)):
        print("%d : %s (%d)" % (i + 1, sorted_students[i][0],
                                sorted_students[i][1]))


# default promo is Bachelor 2021, id : 425
def get_students_by_promo(wrapper, promo: int) -> list:
    """Get list of student by promo."""
    student_list = []
    students = wrapper.get_students(promotion_id=promo)

    if "does not exist" in students:
        print("Promo ID does not exist")
        return None

    for student in students['students']:
        student_list.append(student['login'])

    return student_list


def sum_them_all(student_marks):
    """Sum all marks of a student."""
    total_mark = 0
    for i in range(0, len(student_marks)):
        total_mark += int(student_marks[i]["student_mark"])
    return total_mark


def calc_student_marks(wrapper, student_list: list, promo: int):
    """Calculate student marks."""
    student_points = {}
    for i, _ in enumerate(student_list):
        try:
            print("grabing marks for %s" % student_list[i])
            student_marks = wrapper.get_grades(login=student_list[i],
                                               promotion_id=promo)
            total = sum_them_all(student_marks)
            student_points[student_list[i]] = total
        except Exception:
            student_marks = None

    return student_points
