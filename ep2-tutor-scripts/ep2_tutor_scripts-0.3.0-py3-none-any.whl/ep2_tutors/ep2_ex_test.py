##!/usr/bin/env python3
# coding=utf-8
from __future__ import print_function

import random
import string

from ep2_core.common import *

from Cheetah.Template import Template

import csv

KEY_EX_TEST_ROLE = 'role'
KEY_EX_TEST_POINTS = 'points'
KEY_EX_TEST_LATE = 'late'
KEY_EX_TEST_TEAM = 'team'
KEY_EX_TEST_REMARKS = 'remarks'
KEY_EX_TEST_FEEDBACK = 'feedback'

TAG_NAME_EX_TEST = 'ex_test_%02d'
TAG_NAME_EX_TEST_LATE = 'ex_test_%02d_late'


def ex_test_csv_fieldnames():
    return [KEY_STUDENT_ID, KEY_EX_TEST_ROLE, KEY_EX_TEST_POINTS,
            KEY_EX_TEST_LATE, KEY_EX_TEST_TEAM , KEY_EX_TEST_REMARKS,
            KEY_EX_TEST_FEEDBACK]


class StudentIndex:

    def __init__(self, group: Ep2Group, ue: int, single: bool):
        current_ue_csv = group.exercise_test_csv(ue)

        self.students = group.student_list()
        self.group = group
        self.ue = ue
        self.single = single

        self.done = []
        try:
            with open(current_ue_csv, 'r') as infile:
                reader = csv.DictReader(infile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

                headers = next(reader, None)
                if not validate_headers(headers):
                    click.secho('Malformed file: %s. Invalid headers!' % current_ue_csv)
                    exit(1)

                for row in reader:
                    self.done += [row]
        except IOError:
            pass

        done_students = list(map(lambda x: x[KEY_STUDENT_ID], self.done))

        self.remaining = []
        for student_id in self.students:
            if student_id not in done_students:
                self.remaining += [student_id]

        self.teams = {}
        self.students_for_team = {}

        if single:
            return

        for row in self.done:
            student_id = row[KEY_STUDENT_ID]
            team = row[KEY_EX_TEST_TEAM % ue]
            if student_id == team:
                click.secho(('detected single exercise, if this is a mistake please delete %s/ex_test_%d.csv' % (group, ue)))
                self.single = True
                return
            self.teams[student_id] = team
            if team in self.students_for_team:
                self.students_for_team[team] += [student_id]
            else:
                self.students_for_team[team] = [student_id]

        if ue > 1:
            self.build_lookup_index(ue - 1)

    def build_lookup_index(self, prev_ue):
        previous_ue_csv = self.group.exercise_test_csv(prev_ue)

        done_students = map(lambda x: x[KEY_STUDENT_ID], self.done)
        previous = []
        try:
            with open(previous_ue_csv, 'r') as infile:
                reader = csv.DictReader(infile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

                headers = next(reader, None)
                if not validate_headers(headers):
                    click.secho('Malformed file: %s. Invalid headers!' % previous_ue_csv)
                    exit(1)

                for row in reader:
                    if row[KEY_EX_TEST_TEAM % prev_ue] == row[KEY_STUDENT_ID]:
                        click.secho('previous exercise was a single exercise, trying exercise before')
                        if prev_ue > 1:
                            self.teams = {}
                            self.build_lookup_index(prev_ue - 1)
                            return
                    if row[KEY_STUDENT_ID] not in done_students:
                        previous += [row]
        except IOError:
            pass

        for row in previous:
            student_id = row[KEY_STUDENT_ID]
            team = row[KEY_EX_TEST_TEAM % (prev_ue)]
            self.teams[student_id] = team
            if team in self.students_for_team:
                self.students_for_team[team] += [student_id]
            else:
                self.students_for_team[team] = [student_id]

    def team_members(self, student_id):
        if student_id not in self.teams:
            return []
        team = self.teams[student_id]
        colleagues = self.students_for_team[team]
        return list(filter(lambda x: x != student_id, colleagues))

    def mark_done(self, student_id):
        self.remaining.remove(student_id)
        self.done.append(student_id)

    def auto_fill_team(self, repo_owner):
        members = self.team_members(repo_owner)
        auto_fill_additionals: [str] = []

        for member in members:
            while member[0] == '0':
                member = member[1:]
                auto_fill_additionals += [member]

        return members + auto_fill_additionals

    def auto_fill_index(self):
        auto_fill_additionals: [str] = []

        for member in self.remaining:
            while member[0] == '0':
                member = member[1:]
                auto_fill_additionals += [member]

        return self.remaining + auto_fill_additionals


@click.group()
@click.option("--verbose/--silent", default=False, help='output extra information about the current steps')
@click.option("--sudo", required=False, default=None, help='Perform actions as a different user, ONLY usable by admins')
@click.pass_context
def cli(ctx, verbose, sudo):
    """Utility for ep2 tutors to keep track of submissions and grade ad-hoc exercises."""
    if verbose:
        click.echo("[DEBUG] Verbose output enabled!")

    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['SUDO'] = sudo


def team_name(members):
    return ''.join(sorted(members))


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=click.INT)
@click.option("--late/--on-time", default=False, help='if submission was late')
@click.confirmation_option(prompt='This will tag all repositories with the adhoc tags. Continue?')
@click.pass_context
def tag(ctx, group, ue: int, late):
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    group.tag_group((TAG_NAME_EX_TEST % ue) if not late else (TAG_NAME_EX_TEST_LATE % ue))


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=int)
@click.option("--late/--on-time", default=False, help='if submission was late')
@click.option("--idea/--no-idea", default=False,
              help="load project into the folder, that is monitored by IntelliJ Idea")
@click.option("--grade/--no-grade", default=False, help="also add grading with submission")
@click.option("--single/--team", default=False, help="type of the exercise, default is team")
@click.pass_context
def submission(ctx, group, ue, late, idea, grade, single):
    """Adds submissions of teams for a specific exercise to the corresponding CSV files."""
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)
    f_info = FileInformation('Submission')

    curr_adhoc_type = ex_test_type(ue)
    if curr_adhoc_type != (ExTestType.Single if single else ExTestType.Team):
        click.confirm('You have chosen exercise type %s even tough ad hoc exercise %s is marked as %s. Continue?' %
                      ('Single' if single else 'Team', ue, curr_adhoc_type.name), abort=True)

    index = StudentIndex(group, ue, single)

    single |= index.single

    if len(index.remaining) == 0:
        click.echo('No students remaining. Call ' + click.style('adhoc grade', bold=True) +
                   ' to change the grading of a student')
        return

    csv_file = group.exercise_test_csv(ue)
    csv_path = csv_file[:csv_file.rindex(os.sep)]  # needed to create parent dir

    try:
        os.makedirs(csv_path)
    except OSError:  # directory already exists
        pass

    append = os.path.exists(csv_file)  # if file already exists, don't rewrite header

    f_info.open_write(csv_file, True)

    with open(csv_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ex_test_csv_fieldnames(), lineterminator='\n')

        if not append:  # write header if file is new
            writer.writeheader()

        click.echo("Please enter submission information according to the prompts. Empty input to quit")

        # loop over input
        while len(index.remaining) > 0:

            # prompt owner of working repository
            repo_owner = prompt_manual("Mat.No. Repo", suffix=':   ', default="", show_default=False,
                                       type=click.Choice(index.auto_fill_index() + [""]), exit_condition=[''])

            if repo_owner.is_err():
                break

            repo_owner = repo_owner.ok()

            index.mark_done(repo_owner)
            if not single:
                auto_fill = index.auto_fill_team(repo_owner)

                if len(index.remaining) == 0:
                    click.secho('Invalid state: no student ids remaining!')
                    exit(1)

                if len(auto_fill) == 1:
                    editor = prompt_manual("Mat.No. Writer", type=click.Choice(index.auto_fill_index()), default=auto_fill[0],
                                           show_default=True, suffix=': ')
                else:
                    editor = prompt_manual("Mat.No. Writer", type=click.Choice(index.auto_fill_index()), show_default=True,
                                           suffix=': ')

                if editor.is_err():
                    break

                editor = editor.ok()

                index.mark_done(editor)
                if editor in auto_fill:
                    auto_fill.remove(editor)
                else:
                    auto_fill = []
                # allow for teams of 3 people

                if len(auto_fill) == 1:
                    third = prompt_manual("Mat.No. Third", suffix=':  ', type=click.Choice(index.auto_fill_index() + ['none']),
                                          default=auto_fill[0], show_default=True, exit_condition=['', 'none'])
                else:
                    third = prompt_manual("Mat.No. Third", suffix=':  ', type=click.Choice(index.auto_fill_index() + ['none']),
                                          default='none', show_default=False, exit_condition=['', 'none'])

                if third.is_err():
                    third = None
                else:
                    third = third.ok()

                if third is not None and third != 'none':
                    members = [(repo_owner, 'o'), (editor, 'e'), (third, 't')]
                    index.mark_done(third)
                else:
                    members = [(repo_owner, 'o'), (editor, 'e')]
            else:
                members = [(repo_owner, 'o')]

            team = team_name(map(lambda x: x[0], members))

            if idea:

                git_path = ep2.config.get("Local", "GitHome")
                uebung_path = os.path.join(git_path, "uebung")

                current_uebung = os.path.join(uebung_path, repo_owner)
                if not ep2.clone_or_update(current_uebung, ep2.ue_repo(repo_owner), TAG_NAME_EX_TEST_LATE % ue):
                    if not ep2.clone_or_update(current_uebung, ep2.ue_repo(repo_owner), TAG_NAME_EX_TEST % ue):
                        click.secho("Could not checkout submission from " + repo_owner +
                                    ", no tagged commit found", fg='red')
                    else:
                        ep2.idea_checkout(repo_owner)
                        click.secho('Project %s loaded into IntelliJ Idea' % repo_owner, fg='green')
                else:
                    ep2.idea_checkout(repo_owner)
                    click.secho('Project %s loaded into IntelliJ Idea' % repo_owner, fg='green')

            if grade:
                points = click.prompt("Points", type=click.IntRange(0, 4), show_choices=True)
            else:
                points = '_'

            for member in members:
                writer.writerow(
                    {KEY_STUDENT_ID: member[0], KEY_EX_TEST_ROLE: member[1], KEY_EX_TEST_POINTS: points,
                     KEY_EX_TEST_LATE: 1 if late else 0, KEY_EX_TEST_TEAM: team,
                     KEY_EX_TEST_REMARKS: '', KEY_EX_TEST_FEEDBACK: ''})

            click.secho('submission ok', fg='green')

    f_info.print_info()
    if not idea:
        click.echo('To checkout the repositories run ' + click.style('%s checkout' % EX_TEST_COMMAND_NAME, bold=True) + '.')
    if not grade:
        click.echo('To grade the exercises run ' + click.style('%s grade' % EX_TEST_COMMAND_NAME, bold=True) + '.')
        click.echo('To load the projects into IntelliJ IDEA run ' + click.style('ep2_util idea', bold=True) + '.')

    click.echo('Submit your results using ' + click.style('adhoc submit', bold=True) + '.')


def prompt_manual(prompt:str, suffix:str, type:click.Choice, show_default: bool, default:str = None,
                  exit_condition: [str] = []) -> Result[str, str]:
    prompt_result = click.prompt(prompt, prompt_suffix=suffix, show_default=show_default,
                         type=type, show_choices=False, default=default)

    if prompt_result in exit_condition:
        return Err('exit condition reached')

    verification_result = verify_and_normalize_student_id(prompt_result)

    while verification_result.is_err():
        prompt_result = click.prompt(prompt, prompt_suffix=suffix, show_default=show_default,
                                     type=type, show_choices=False, default=default)

        if prompt_result in exit_condition:
            return Err('exit condition reached')

        verification_result = verify_and_normalize_student_id(prompt_result)

    return verification_result


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero', type=click.INT)
@click.pass_context
def checkout(ctx, group, ue: int):
    """This command checks out all repositories of a group at the tag of the given exercise.

    To see the submissions, that have not yet been graded run:

        ep2_ex_test list ungraded --group <group> --ue <ue>
    """
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    git_path = ep2.config.get("Local", "GitHome")
    csv_path = group.exercise_test_csv(ue)
    uebung_path = os.path.join(git_path, "uebung")

    try:
        os.makedirs(uebung_path)
    except OSError:  # directory already exists
        pass

    if not os.path.exists(csv_path):
        click.secho("Could not find submissions file, please run 'submission' first or pull the tutor repo", fg='red')
        exit(1)

    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

        headers = next(reader, None)
        if not validate_headers(headers):
            click.secho('Malformed file: %s. Invalid headers!' % csv_path)
            exit(1)

        for row in reader:
            if KEY_INVALID in row:
                click.secho('Malformed file: %s' % csv_path, fg='red')
                exit(1)

            if not check_row(row):
                click.secho('Malformed file: %s. Missing column(s)!' % csv_path, fg='red')
                exit(1)

            if row[KEY_EX_TEST_ROLE] == 'o':
                current_uebung = os.path.join(uebung_path, row[KEY_STUDENT_ID])
                if not ep2.clone_or_update(current_uebung, ep2.ue_repo(row[KEY_STUDENT_ID]), TAG_NAME_EX_TEST_LATE % ue):
                    if not ep2.clone_or_update(current_uebung, ep2.ue_repo(row[KEY_STUDENT_ID]), TAG_NAME_EX_TEST % ue):
                        click.secho("Could not checkout submission from " + row[KEY_STUDENT_ID] +
                                    ", no tagged commit found", fg='red')

    click.echo('To grade the exercises run ' + click.style('%s grade' % EX_TEST_COMMAND_NAME, bold=True) + '.')
    click.echo('To load the projects into IntelliJ IDEA run ' + click.style('%s idea' % UTIL_COMMAND_NAME, bold=True) + '.')


@cli.command()
@click.option("--repo-owner", required=True, prompt=True, help='the matriculation number of the person, in whose '
                                                               'repository the exercise was written in',
              callback=validate_student_id)
@click.option("--points", required=True, prompt=True, help='points graded for this exercise', type=click.IntRange(0, 4))
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero')
@click.option("--remarks", prompt=True, default='', help='optional remarks for the lecturer')
@click.option("--feedback", prompt=True, default='', help='feedback for the students')
@click.pass_context
def grade(ctx, repo_owner, points, ue, group, remarks, feedback):
    """This command grades a single submission by updating the submissions CSV entry and creating an
    issue for the project in which the ad-hoc exercise was written in."""
    f_info = FileInformation('Grade')
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    csv_file = group.exercise_test_csv(ue)
    tmp_file = csv_file + ".tmp"  # tmp file for editing

    team = None

    with open(csv_file, 'r') as infile:
        reader = csv.DictReader(infile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

        headers = next(reader, None)
        if not validate_headers(headers):
            click.secho('Malformed file: %s. Invalid headers!' % csv_file)
            exit(1)

        for row in reader:
            if KEY_INVALID in row:
                click.secho('Malformed file: %s' % csv_file, fg='red')
                exit(1)

            if row[KEY_STUDENT_ID] == repo_owner:
                team = row[KEY_EX_TEST_TEAM]

    f_info.open_write(tmp_file, True)

    with open(csv_file, 'r') as infile:
        with open(tmp_file, 'w') as outfile:
            reader = csv.DictReader(infile, fieldnames=ex_test_csv_fieldnames(), restkey=KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file)
                f_info.print_info()
                exit(1)

            writer = csv.DictWriter(outfile, fieldnames=ex_test_csv_fieldnames(), lineterminator='\n')

            writer.writeheader()

            for row in reader:  # read and search for team members
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                if row[KEY_EX_TEST_TEAM] == team:  # if team matches, update points
                    row[KEY_EX_TEST_POINTS] = points
                    if remarks is not None and remarks != '':
                        row[KEY_EX_TEST_REMARKS] = escape_csv_string(remarks)
                    if feedback is not None and feedback != '':
                        row[KEY_EX_TEST_FEEDBACK] = escape_csv_string(feedback)
                writer.writerow(row)  # write row

    f_info.open_write(csv_file, True)
    shutil.move(tmp_file, csv_file)  # replace old file with tmp file
    f_info.delete(tmp_file, True)

    f_info.print_info()
    click.echo('Submit your results using ' + click.style('%s submit' % EX_TEST_COMMAND_NAME, bold=True) + '.')
    click.echo('For a list of ungraded exercises run ' + click.style('%s list ungraded' % EX_TEST_COMMAND_NAME, bold=True) + '.')


@cli.command()
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero')
@click.pass_context
def submit(ctx, group, ue):
    """Outputs all issues, that would be created, to verify them, before submission.

    To prevent accidental issue creation before validation, a challenge has to be entered, which is printed
    at the top of the output."""
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    f_info = FileInformation('Submit')

    challenge = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
    click.secho('Challenge %s' % challenge, bold=True)
    click.echo('\n' + ('=' * 30) + '\n')

    ex_test_csv_file = group.exercise_test_csv(ue)
    ex_test_csv_file_tmp = ex_test_csv_file + '.tmp'

    students = group.student_list()
    student_details = group.student_info()

    issues = []  # type: [(str, unicode)]

    template = Template(file=ep2.template_path('adhoc.tmpl'))

    template.tutor_gender = ep2.tutor_gender()
    template.group = group.name

    with open(ex_test_csv_file, 'r') as infile:
        f_info.open_write(ex_test_csv_file_tmp, True)
        with open(ex_test_csv_file_tmp, 'w') as outfile:
            reader = csv.DictReader(infile, ex_test_csv_fieldnames(), KEY_INVALID, strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % ex_test_csv_file)
                exit(1)

            writer = csv.DictWriter(outfile, ex_test_csv_fieldnames(), lineterminator='\n')

            writer.writeheader()

            for row in reader:
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % ex_test_csv_file)
                    f_info.print_info()
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % ex_test_csv_file, fg='red')
                    f_info.print_info()
                    exit(1)

                if row[KEY_EX_TEST_POINTS] == '_':
                    click.secho('%s has not been graded yet. aborting!' % row[KEY_STUDENT_ID], fg='red')
                    f_info.print_info()
                    exit(1)

                row[KEY_EX_TEST_FEEDBACK] = escape_csv_string(row[KEY_EX_TEST_FEEDBACK])
                row[KEY_EX_TEST_REMARKS] = escape_csv_string(row[KEY_EX_TEST_REMARKS])

                details = student_details[row[KEY_STUDENT_ID]]

                template.points = row[KEY_EX_TEST_POINTS]
                template.student_feedback = row[KEY_EX_TEST_FEEDBACK]
                template.student_gender = details[KEY_STUDENT_GENDER]
                template.attended = True

                students.remove(row[KEY_STUDENT_ID])

                issue = template.__str__()
                click.echo('Issue for student %s' % row[KEY_STUDENT_ID], nl=True)
                click.echo(issue.replace('\n\n', '\n'), nl=True)
                click.echo(('=' * 30), nl=True)
                issues += [(row[KEY_STUDENT_ID], issue)]

                writer.writerow(row)

    for student in students:
        details = student_details[student]

        template.attended = False
        template.student_feedback = None
        template.points = 0
        template.student_gender = details[KEY_STUDENT_GENDER]

        issue = template.__str__()
        click.echo('Issue for student %s' % student, nl=True)
        click.echo(issue.replace('\n\n', '\n'), nl=True)
        click.echo(('=' * 30), nl=True)
        issues += [(student, issue)]

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
                ep2.create_project_issue(project=student_project, title='Übungstest %s' % ue, descrition=issue)
            except gitlab.GitlabCreateError as e:
                exceptions += [(e, student_project)]

    if len(exceptions) > 0:
        click.secho('with errors:', fg='red', nl=True)
        for project, e in exceptions:
            click.secho('\t%s: %s' % (e, project), fg='red', nl=True)
    else:
        click.secho('ok', nl=True, fg='green')

    f_info.open_write(ex_test_csv_file, True)
    shutil.move(ex_test_csv_file_tmp, ex_test_csv_file)
    f_info.delete(ex_test_csv_file_tmp, True)

    f_info.print_info()


@cli.group('list')
def list_grp():
    """Performs various (maybe in the future) list operations"""
    pass


@list_grp.command("ungraded")
@click.option("--group", required=True, prompt=True, help='name of the group')
@click.option("--ue", required=True, prompt=True, help='number of the exercise, WITHOUT leading zero')
@click.pass_context
def list_ungraded(ctx, ue, group):
    """This command lists all ungraded submission for a specific group and exercise."""
    ep2 = Ep2(verbose=ctx.obj["VERBOSE"], sudo=ctx.obj["SUDO"])
    group = ep2.group(group)

    csv_file = group.exercise_test_csv(ue)
    empty = True

    try:
        with open(csv_file, 'r') as infile:
            reader = csv.DictReader(infile, fieldnames=ex_test_csv_fieldnames(), strict=True)

            headers = next(reader, None)
            if not validate_headers(headers):
                click.secho('Malformed file: %s. Invalid headers!' % csv_file)
                exit(1)

            for row in reader:
                if KEY_INVALID in row:
                    click.secho('Malformed file: %s' % csv_file)
                    exit(1)

                if not check_row(row):
                    click.secho('Malformed file: %s. Missing column(s)!' % csv_file, fg='red')
                    exit(1)

                if row[KEY_EX_TEST_POINTS] == '_' and row[KEY_EX_TEST_ROLE] == 'o':
                    click.echo(row[KEY_STUDENT_ID])
                    empty = False
    except IOError:
        click.secho('no submission for ' + group.name + ' ue ' + ue, fg='red')
        exit(1)

    if empty:
        click.secho('empty', fg='green')


if __name__ == '__main__':
    cli(obj={})
