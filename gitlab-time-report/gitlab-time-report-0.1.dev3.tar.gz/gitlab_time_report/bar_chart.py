import matplotlib.pyplot as plt
import numpy as np

from gitlab_time_report import chart


def time_user_week(issues):
    return None


def milestone_estimated_vs_recorded(issues):
    """Gets the total amount of spent hours and estimated hours per milestone in a GitLab project.

            :param issues: A list of GitLab issues.

            :return: A list of milestone names, a two dimensional list of spent and estimated hours per milestone
                     and a list of labels to display on the legend.
        """
    spent_time_milestone = {}
    estimated_time_milestone = {}
    for issue in issues:
        if issue.milestone is None:
            continue
        milestone = issue.milestone.get("title")
        spent_time = issue.time_stats().get("human_total_time_spent")
        estimated_time = issue.time_stats().get("human_time_estimate")
        if spent_time is None:
            spent_time = "0h"
        if estimated_time is None:
            estimated_time = "0h"
        spent_hours = chart.time_in_hours(spent_time)
        estimated_hours = chart.time_in_hours(estimated_time)
        if spent_time_milestone.get(milestone) is None:
            spent_time_milestone[milestone] = spent_hours
        else:
            spent_time_milestone[milestone] += spent_hours
        if estimated_time_milestone.get(milestone) is None:
            estimated_time_milestone[milestone] = estimated_hours
        else:
            estimated_time_milestone[milestone] += estimated_hours
    return (
        spent_time_milestone.keys(),
        [spent_time_milestone.values(), estimated_time_milestone.values()],
        ["Recorded Time", "Estimated Time"],
    )


def label_estimated_vs_recorded(issues):
    return None


class BarChart(chart.Chart):
    """Creates a bar chart from any given fitting data it receives."""

    def __init__(self, issues):
        """
            :param issues: A list of GitLab issues.
        """
        self.issues = issues

    def create_diagram(self, chart_type):
        """Builds a diagram in form of a bar chart and saves it as a png.

            :param chart_type: A string that contains the name of the requested chart type.

            :return: The name of the saved file.

            Calls the :py:func:`time_user_week` if called with the parameter 'time_user_week'.
            Calls the :py:func:`milestone_estimated_vs_recorded` if called with the parameter
            'milestone_estimated_vs_recorded'.
            Calls the :py:func:`label_estimated_vs_recorded` if called with the parameter label_estimated_vs_recorded.

            Creates diagrams with matplotlib. See https://matplotlib.org/users/index.html.
        """
        if chart_type == "time_user_week":
            self.title = "Time per User per Week"
            request_project_data = time_user_week
        elif chart_type == "milestone_estimated_vs_recorded":
            self.title = "Milestone Estimate vs. Recorded Time"
            request_project_data = milestone_estimated_vs_recorded
        elif chart_type == "label_estimated_vs_recorded":
            self.title = "Recorded vs. Estimated Time per Label"
            request_project_data = label_estimated_vs_recorded
        labels, bars, y_axis = request_project_data(self.issues)

        fig, ax = plt.subplots()
        ax.set_title(self.title)

        amount_bar_groups = len(labels)
        y_pos = np.arange(amount_bar_groups)
        height = 0.9 / amount_bar_groups
        starting_point = (amount_bar_groups / 2 - 0.5) * -height

        for bar_group in bars:
            ax.barh(y_pos + starting_point, bar_group, height)
            starting_point += height

        ax.set_yticks(y_pos - height)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()
        ax.legend(y_axis)

        file_name = f"{chart_type}.png"
        plt.tight_layout()
        plt.savefig(file_name)

        return file_name
