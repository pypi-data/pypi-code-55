#!/usr/bin/env python3
# coding=utf-8
import os

import random
import re
import string

from Cheetah.Template import Template

from ep2_core.common import *

import csv

KEY_UE_TA_POINTS = 'ta_points'
KEY_UE_ATTENDED = 'attended'
KEY_UE_REMARKS = 'remarks'
KEY_UE_FEEDBACK = 'feedback'
KEY_UE_GRADING = 'grading'
KEY_UE_BUILD_STATUS = 'build_status'
KEY_UE_PRE_EVAL_EX = 'pre_eval_ex_%02d'


class TeamIndex:

    def __init__(self, group):
        self.students = group.student_list()
        csv_file = group.team_csv()
        self.index = {}
        self.marked = []
        self.team_name = {}
        with open(csv_file, 'r') as infile:
            reader = csv.DictReader(infile, teams_csv_fieldnames(), KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file)
                exit(1)

            for row in reader:
                member_1 = row[KEY_TEAM_MEMBER_1]
                member_2 = row[KEY_TEAM_MEMBER_2]
                member_3 = row[KEY_TEAM_MEMBER_3]

                self.index[member_1] = [member_2]
                self.index[member_2] = [member_1]
                self.team_name[member_1] = row[KEY_TEAM_NAME]
                self.team_name[member_2] = row[KEY_TEAM_NAME]

                if member_3 is not None and len(member_3) > 0:
                    self.index[member_3] = [member_1, member_2]
                    self.index[member_1] += [member_3]
                    self.index[member_2] += [member_3]
                    self.team_name[member_3] = row[KEY_TEAM_NAME]

    def other_students(self, student):
        self.marked += [student]
        self.marked += self.index[student]
        return self.index[student]

    def skip(self, student):
        return student in self.marked


def attendance_csv_fieldnames(ep2: Ep2, ue: int) -> [str]:
    if ue == 7:
        return pre_eval_csv_fieldnames_ta()
    return pre_eval_csv_fieldnames(ep2, ue)


def pre_eval_csv_fieldnames(ep2: Ep2, ue: int) -> [str]:
    sub_exercises = [KEY_UE_PRE_EVAL_EX % d for d in range(1, ep2.tests_for_exercise(ue) + 1)]
    return [KEY_STUDENT_ID, KEY_UE_ATTENDED, KEY_UE_REMARKS, KEY_UE_FEEDBACK, KEY_UE_BUILD_STATUS, KEY_UE_GRADING] + sub_exercises


def pre_eval_csv_fieldnames_ta():
    return [KEY_STUDENT_ID, KEY_UE_ATTENDED, KEY_UE_TA_POINTS, KEY_UE_REMARKS, KEY_UE_FEEDBACK]


@click.group()
@click.option("--verbose/--silent", default=False, help='output extra information about the current steps')
@click.option("--sudo", required=False, default=None, help='Perform actions as a different user, ONLY usable by admins')
@click.pass_context
def cli(ctx, verbose, sudo):
    """Utility for ep2 tutors to perform pre evaluations of submitted exercises"""
    if verbose:
        click.echo("[DEBUG] Verbose output enabled!")

    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['SUDO'] = sudo


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=click.INT)
@click.pass_context
def checkout(ctx, group, ue: int):
    """Checks out all repositories of a group for a given exercise."""
    curr_ue_type = ue_type(ue)

    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    students_file = group.students_csv()  # list of all students for this group
    pre_eval_file = group.pre_eval_csv(ue)
    f_info = FileInformation('Checkout')

    uebung_path = ep2.uebung_dir()
    errors = []

    student_list = group.student_info()
    tag = ep2.get_ue_tag(ue)

    click.echo("Checking out " + tag)

    with click.progressbar(student_list.values(), label="Clone/Pull") as reader:  # read students and create entries in attendance file

        for row in reader:
            if KEY_INVALID in row:
                click.secho('Malformed file: %s' % students_file, fg='red')
                exit(1)

            if not check_row(row):
                click.secho('Malformed file: %s. Missing column(s)!' % students_file, fg='red')
                exit(1)

            student_id = row[KEY_STUDENT_ID]
            repo = ep2.ue_repo(student_id)

            # clone or pull repo
            clone_result = ep2.clone_or_update(os.path.join(uebung_path, student_id), repo, tag)
            if clone_result.is_err():
                errors += [student_id + ": " + clone_result.value]

        if not os.path.exists(pre_eval_file):

            f_info.open_write(pre_eval_file, True)
            with open(pre_eval_file, 'w') as outfile:
                if curr_ue_type == ExerciseType.Normal:
                    writer = csv.DictWriter(outfile, fieldnames=pre_eval_csv_fieldnames(ep2, ue), lineterminator='\n')
                elif curr_ue_type == ExerciseType.Team:
                    writer = csv.DictWriter(outfile, fieldnames=pre_eval_csv_fieldnames_ta(), lineterminator='\n')
                else:
                    click.secho('Unknown exercise type %s' % curr_ue_type, fg='red')
                    exit(1)

                writer.writeheader()

                for row in student_list.values():
                    # no validation required, as file is the same

                    student_id = row[KEY_STUDENT_ID]

                    if curr_ue_type == ExerciseType.Normal:
                        sub_exercises = {KEY_UE_PRE_EVAL_EX % d: '0/0' for d in range(1, ep2.tests_for_exercise(ue) + 1)}
                        writer.writerow({KEY_STUDENT_ID: student_id, KEY_UE_GRADING: '_', KEY_UE_REMARKS: '', KEY_UE_FEEDBACK: '', KEY_UE_ATTENDED: 0, KEY_UE_BUILD_STATUS: 'unknown', **sub_exercises})
                    elif curr_ue_type == ExerciseType.Team:
                        writer.writerow(
                            {KEY_STUDENT_ID: student_id, KEY_UE_TA_POINTS: '_', KEY_UE_REMARKS: '',
                             KEY_UE_FEEDBACK: '', KEY_UE_ATTENDED: 0})

    if errors:
        click.secho('with errors', fg='yellow')

        for error in errors:
            click.secho('\t' + error, fg='yellow')

    f_info.print_info()
    click.echo('To grade an exercise run ' + click.style('%s grade' % EVAL_COMMAND_NAME, bold=True) + '.')
    click.echo(
        'To see a list of remaining exercises to grade run ' + click.style('%s list ungraded' % EVAL_COMMAND_NAME,
                                                                           bold=True) + '.')
    click.echo(
        'To load a project into IntelliJ IDEA run ' + click.style('%s idea' % UTIL_COMMAND_NAME, bold=True) + '.')


def validate_grading(ctx, param, value):
    if validate_ex_type(ctx, param, value):
        return value
    if value is None:
        return value
    match = re.match('^[+\\-~0]*$', value)
    if match is not None:
        return value
    else:
        raise click.BadParameter('can only consist of [\'+\', \'~\', \'-\', \'0\']')


def validate_ex_type(ctx, param, value):
    ue = ctx.params['ue']
    curr_ue_type = ue_type(ue)
    if curr_ue_type == ExerciseType.Team:
        if value is None:
            return True
        raise click.BadParameter('team exercise does not support %s! use --points instead' % param.name)
    return False


def validate_ex_type_ta(ctx, param, value):
    if value is None:
        return None
    ue = ctx.params['ue']
    curr_ue_type = ue_type(ue)
    if curr_ue_type == ExerciseType.Normal:
        raise click.BadParameter('exercise does not support %s! use --grading instead' % param.name)
    return value


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', is_eager=True,
              type=click.INT)
@click.option("--student", required=True, prompt=True, help='student id of the student, that should be graded',
              callback=validate_student_id)
@click.option("--student-feedback", prompt=True, default='', help='feedback for the student, will be part of the '
                                                                  'created issue')
@click.option("--solution-remarks", prompt=True, default='', help='remarks for the lecturer (keep short)')
@click.option("--grading", callback=validate_grading, prompt=False, required=False,
              help='grade for the submission')
@click.option('--tasks', type=int, help='number of tasks for this exercise', default=-1)
@click.option('--points', type=click.IntRange(0, 33), help='points for team exercise', callback=validate_ex_type_ta)
@click.pass_context
def grade(ctx, group, ue: int, student, grading, student_feedback, solution_remarks, tasks, points):
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)
    f_info = FileInformation('Grade')

    pre_eval_csv_file = group.pre_eval_csv(ue)  # file for reading
    tmp_file = pre_eval_csv_file + '.tmp'  # file for writing

    print(student)

    curr_ue_type = ue_type(ue)
    if curr_ue_type == ExerciseType.Team:
        if points is None:
            points = click.prompt('Points', prompt_suffix=' [0-33]: ', type=click.IntRange(0, 33))
    elif curr_ue_type == ExerciseType.Normal:
        if grading is None:
            grading = click.prompt('Grading')
            while not re.match('^[+\\-~0]*$', grading):
                grading = click.prompt('Grading')
    else:
        click.secho('Unknown exercise type %s' % curr_ue_type, fg='red')
        exit(1)

    try:
        team_index = TeamIndex(group)
    except:
        team_index = None

    with open(pre_eval_csv_file, 'r') as infile:
        f_info.open_write(tmp_file, True)
        with open(tmp_file, 'w') as outfile:

            if curr_ue_type == ExerciseType.Normal:
                reader = csv.DictReader(infile, fieldnames=pre_eval_csv_fieldnames(ep2, ue), strict=True, restkey=KEY_INVALID)

                headers = next(reader, None)
                if not validate_headers(headers):
                    click.secho('Malformed file: %s. Invalid headers!' % pre_eval_csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                writer = csv.DictWriter(outfile, fieldnames=pre_eval_csv_fieldnames(ep2, ue), lineterminator='\n')
            else:
                reader = csv.DictReader(infile, fieldnames=pre_eval_csv_fieldnames_ta(), strict=True,
                                        restkey=KEY_INVALID)

                headers = next(reader, None)
                if not validate_headers(headers):
                    click.secho('Malformed file: %s. Invalid headers!' % pre_eval_csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                writer = csv.DictWriter(outfile, fieldnames=pre_eval_csv_fieldnames_ta(), lineterminator='\n')

            writer.writeheader()

            for row in reader:
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % pre_eval_csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % pre_eval_csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                if curr_ue_type == ExerciseType.Normal:
                    student_id = row[KEY_STUDENT_ID]
                    if student_id == student:
                        row[KEY_UE_GRADING] = grading

                        if solution_remarks is not None:
                            row[KEY_UE_REMARKS] = escape_csv_string(solution_remarks)

                        # append feedback and store in csv
                        if student_feedback is not None and student_feedback != '':
                            row[KEY_UE_FEEDBACK] = escape_csv_string(student_feedback)

                    writer.writerow(row)
                else:
                    if team_index is None:
                        click.secho('Team index could not be loaded, make sure teams exist (might need to be created)',
                                    fg='red')
                        exit(3)

                    student_id = row[KEY_STUDENT_ID]
                    if student_id == student and not team_index.skip(student_id):
                        row[KEY_UE_TA_POINTS] = points

                        if solution_remarks is not None:
                            row[KEY_UE_REMARKS] = escape_csv_string(solution_remarks)

                        # append feedback and store in csv
                        if student_feedback is not None and student_feedback != '':
                            row[KEY_UE_FEEDBACK] = escape_csv_string(student_feedback)

                        writer.writerow(row)

                        team_members = team_index.other_students(student_id)
                        if len(team_members) > 0:
                            click.secho('adding other members of team %s (%s)' % (
                                team_index.team_name[student_id], team_members))
                        for team_member in team_members:
                            row[KEY_STUDENT_ID] = team_member
                            writer.writerow(row)
                    elif not team_index.skip(row[KEY_STUDENT_ID]):
                        writer.writerow(row)

    f_info.open_write(pre_eval_csv_file, True)
    shutil.move(tmp_file, pre_eval_csv_file)  # replace old file with tmp file
    f_info.delete(tmp_file, True)

    f_info.print_info()
    click.echo('Submit your results using ' + click.style('%s submit' % EVAL_COMMAND_NAME, bold=True) + '.')
    click.echo(
        'For a list of ungraded exercises run ' + click.style('%s list ungraded' % EVAL_COMMAND_NAME, bold=True) + '.')


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=click.INT)
@click.pass_context
def submit(ctx, group: str, ue: int):
    """Outputs all issues, that would be created, to verify them, before submission.

    To prevent accidental issue creation before validation, a challenge has to be entered, that is printed
    at the top of the output."""
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)
    f_info = FileInformation('Submit')

    challenge = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
    click.secho('Challenge %s' % challenge, bold=True)
    click.echo('\n' + ('=' * 30) + '\n')

    exercise_csv_file = group.pre_eval_csv(ue)
    exercise_csv_file_tmp = exercise_csv_file + '.tmp'

    issues = []  # type: [(str, str)]
    curr_ue_type = ue_type(ue)

    if curr_ue_type == ExerciseType.Normal:
        fnames = pre_eval_csv_fieldnames(ep2, ue)
    elif curr_ue_type == ExerciseType.Team:
        fnames = pre_eval_csv_fieldnames_ta()
    else:
        click.secho('Unknown exercise type %s' % curr_ue_type, fg='red')
        exit(1)
        return

    students = group.student_info()

    template = Template(file=ep2.template_path('pre_eval.tmpl'))
    template.tutor_gender = ep2.tutor_gender()

    with open(exercise_csv_file, 'r') as infile:
        reader = csv.DictReader(infile, fnames, KEY_INVALID, strict=True)

        headers = next(reader, None)
        if not validate_headers(headers):
            click.secho('Malformed file: %s. Invalid headers!' % exercise_csv_file, fg='red')
            f_info.print_info()
            exit(1)

        f_info.open_write(exercise_csv_file_tmp, True)
        with open(exercise_csv_file_tmp, 'w') as outfile:
            writer = csv.DictWriter(outfile, fnames, lineterminator='\n')

            writer.writeheader()

            for row in reader:
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % exercise_csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % exercise_csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                stud_data = students[row[KEY_STUDENT_ID]]

                if curr_ue_type == ExerciseType.Normal:
                    grading = row[KEY_UE_GRADING]   # for d in range(1, ep2.tests_for_exercise(ue) + 1)]
                    if any(grade == '_' for grade in grading):
                        click.secho('%s has not been graded yet. aborting!' % row[KEY_STUDENT_ID], fg='red')
                        f_info.print_info()
                        exit(1)
                        return

                    template.grading = grading
                    template.tests = [row[KEY_UE_PRE_EVAL_EX % d] for d in range(1, ep2.tests_for_exercise(ue) + 1)]
                    template.points = -1
                elif curr_ue_type == ExerciseType.Team:
                    points = row[KEY_UE_TA_POINTS]
                    if points == '_':
                        click.secho('%s has not been graded yet. aborting!' % row[KEY_STUDENT_ID], fg='red')
                        f_info.print_info()
                        exit(1)
                        return

                    template.points = points
                    template.grading = ''
                template.ex_type = curr_ue_type.name
                template.student_feedback = row[KEY_UE_FEEDBACK]
                template.group = group.name
                template.student_gender = stud_data[KEY_STUDENT_GENDER]

                issue = template.__str__()
                click.echo('Issue for %s - %s, %s\n' % (row[KEY_STUDENT_ID], stud_data[KEY_STUDENT_NAME_LAST].upper(),
                                                        stud_data[KEY_STUDENT_NAME_FIRST]))
                click.echo(issue.replace('\n\n', '\n'))
                click.echo('\n' + ('=' * 30) + '\n')
                issues += [(row[KEY_STUDENT_ID], issue)]

                row[KEY_UE_FEEDBACK] = escape_csv_string(row[KEY_UE_FEEDBACK])
                row[KEY_UE_REMARKS] = escape_csv_string(row[KEY_UE_REMARKS])

                writer.writerow(row)

    click.echo('Please enter the challenge, that has been printed at the beginning of the output.')
    c = click.prompt('Challenge')
    while c != challenge:
        click.secho('invalid challenge', fg='yellow', nl=True)
        c = click.prompt('Challenge')
    click.secho('challenge accepted', fg='green', nl=True)

    exceptions = []

    with click.progressbar(issues, label='Creating issues') as bar:
        for student_id, issue in bar:
            student_project = ep2.ue_repo(student_id)  # get project
            try:
                if curr_ue_type == ExerciseType.Normal:
                    title = 'Abgabe %d' % ue
                else:
                    title = 'Abgabe Teamaufgabe'
                ep2.create_project_issue(project=student_project, title=title, descrition=issue)
            except gitlab.GitlabCreateError as e:
                exceptions += [(e, student_project)]

    f_info.open_write(exercise_csv_file, True)
    shutil.move(exercise_csv_file_tmp, exercise_csv_file)
    f_info.delete(exercise_csv_file_tmp, True)

    if len(exceptions) > 0:
        click.secho('with errors:', fg='red', nl=True)
        for project, e in exceptions:
            click.secho('\t%s: %s' % (e, project), fg='red', nl=True)

    f_info.print_info()


@cli.group('list')
def list_grp():
    """Performs various list operations"""
    pass


@list_grp.command("ungraded")
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=click.INT)
@click.pass_context
def list_ungraded(ctx, ue, group):
    """This command lists all ungraded submission for a specific group and exercise."""
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    csv_file = group.pre_eval_csv(ue)
    empty = True
    curr_ue_type = ue_type(ue)

    fieldnames = pre_eval_csv_fieldnames(ep2,
                                         ue) if curr_ue_type == ExerciseType.Normal else pre_eval_csv_fieldnames_ta()

    try:
        with open(csv_file, 'r') as infile:
            reader = csv.DictReader(infile, fieldnames, KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file, fg='red')
                exit(1)

            for row in reader:  # iterate over attendance file
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % csv_file, fg='red')
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % csv_file, fg='red')
                    exit(1)

                if curr_ue_type == ExerciseType.Normal:
                    grading = row[KEY_UE_GRADING]
                    if any(grade == '_' for grade in grading):  # if not evaluated => list
                        click.echo(row[KEY_STUDENT_ID])
                        empty = False

                elif curr_ue_type == ExerciseType.Team:
                    if row[KEY_UE_TA_POINTS] == '_':  # if not evaluated => list
                        click.echo(row[KEY_STUDENT_ID])
                        empty = False
    except IOError:
        click.secho('no submission for ' + group.name + ' ue ' + ue, fg='red')
        exit(1)

    if empty:  # all work is done!
        click.secho('empty', fg='green')


if __name__ == '__main__':
    cli(obj={})
