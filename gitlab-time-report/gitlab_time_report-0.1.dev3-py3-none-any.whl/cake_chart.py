import matplotlib.pyplot as plt

from gitlab_time_report import chart


def time_user(issues):
    """Gets the total amount of spent hours by user in a GitLab project.

        :param issues: A list of GitLab issues.

        :return: A list of user names and a list of spent hours by user.
    """
    time_per_user = {}
    for issue in issues:
        for note in issue.notes.list(all=True):
            if note.system:
                name = note.author.get("name")
                message = note.body
                prefix, time_data = message.split(" ", 1)
                if prefix == "added":
                    modifier = 1
                elif prefix == "subtracted":
                    modifier = -1
                else:
                    continue
                spent_time = time_data.split(" of time spent at ", 1)[0]
                hours = chart.time_in_hours(spent_time) * modifier
                if time_per_user.get(name) is None:
                    time_per_user[name] = hours
                else:
                    time_per_user[name] += hours
    return time_per_user.keys(), time_per_user.values()


def time_label(issues):
    """Gets the total amount of spent hours per issue label in a GitLab project.

            :param issues: A list of GitLab issues.

            :return: A list of label names and a list of spent hours per label.
        """
    time_per_label = {}
    for issue in issues:
        spent_time = issue.time_stats().get("human_total_time_spent")
        if spent_time is None:
            spent_time = "0h"
        hours = chart.time_in_hours(spent_time)
        for issue_label in issue.labels:
            if time_per_label.get(issue_label) is None:
                time_per_label[issue_label] = hours
            else:
                time_per_label[issue_label] += hours
    return time_per_label.keys(), time_per_label.values()


def get_values(slices):
    """Returns the :py:func:`format_value`.

        :param slices: A list of spent hours as floats.

        :return: :py:func:`format_value`.
    """

    def format_value(pct):
        """Formats floats, by rounding it to two digits after the comma.

            :param pct: Spent hours as float.

            :return: Formatted float.
        """
        total = sum(slices)
        val = round(pct * total / 100)
        return f"{val:.2f}"

    return format_value


class CakeChart(chart.Chart):
    """Creates a cake chart from any given fitting data it receives."""

    def __init__(self, issues):
        """
            :param issues: A list of GitLab issues.
        """
        self.issues = issues

    def create_diagram(self, chart_type):
        """Builds a diagram in form of a cake chart and saves it as a png.

            :param chart_type: A string that contains the name of the requested chart type.

            :return: The name of the saved file.

            Calls the :py:func:`time_user` if called with the parameter 'time_user'.
            Calls the :py:func:`time_label` if called with the parameter 'time_label'.
            Calls the :py:func:`get_values` to receive formatted numbers to display on the drawn cake chart.

            Creates diagrams with matplotlib. See https://matplotlib.org/users/index.html.
        """
        if chart_type == "time_user":
            self.title = "Time per User [hours]"
            request_project_data = time_user
        elif chart_type == "time_label":
            self.title = "Time per Label [hours]"
            request_project_data = time_label
        labels, slices = request_project_data(self.issues)

        fig, ax = plt.subplots()
        ax.set_title(self.title)

        plt.pie(
            slices, autopct=get_values(slices), shadow=True,
        )

        ax.legend(labels, loc="upper right", bbox_to_anchor=(1.35, 1.1))

        file_name = f"{chart_type}.png"
        plt.savefig(file_name)

        return file_name
