"""gitlab-recurrring-issues

This tool looks a repo for creating recurring issues.
It's starts from one existing issue with a special tag:

- recurring::hourly  ## for tests ?
- recurring::daily
- recurring::weekly
- recurring::monthly
- recurring::yearly

Then group by issue name (if multiple issues with the same name) and search for
the most recent issue for a given issue name.

Then looks at issue creation date

If the issue creation date is older than the recurring period, creates a new
one with same name and copy some parameters:
- title
- description
- assignee
- tags (including recuring tag)
- weight
- confidential
- if there is a due date in the source issue, looks for interval between source
  creation date and source due date and add a due date for the new issue
  with same interval
...
"""
import argparse
import os

import pendulum
import gitlab


def main():
    """entrypoint script."""
    parser = argparse.ArgumentParser(description="Git lab bot for recurring issues.")
    parser.add_argument(
        "--private-token",
        dest="private_token",
        action="store_true",
        default=False,
        help="Use private token instead of CI_JOB_TOKEN",
    )
    args = parser.parse_args()

    if args.private_token:
        gitlab_client = gitlab.Gitlab(
            "https://gitlab.com/", private_token=os.environ["GITLAB_PRIVATE_TOKEN"]
        )
    else:
        gitlab_client = gitlab.Gitlab(
            "https://gitlab.com/", job_token=os.environ["CI_JOB_TOKEN"]
        )
    gitlab_client.auth()

    project = gitlab_client.projects.get(os.environ["CI_PROJECT_ID"])
    # volontarly we do not filter on opened issues because we may want to
    # clone a closed issue (ex: the task is done, marqued closed and we want
    # to creates a new one for the next week)
    for recurring_tag, period_add in (
        ("recurring::hourly", {"hours": 1}),
        ("recurring::daily", {"days": 1}),
        ("recurring::weekly", {"weeks": 1}),
        ("recurring::monthly", {"months": 1}),
        ("recurring::yearly", {"years": 1}),
    ):
        print(recurring_tag)
        issues = project.issues.list(
            labels=[recurring_tag,], order_by="created_at", sort="desc"
        )  # ])
        unique_labels_done = []
        for issue in issues:
            start_date = pendulum.parse(issue.created_at)

            print("%s:%s:%s" % (issue.title, start_date, start_date.add(**period_add)))
            # issue.created_at = start_date.add(days=-2).isoformat()
            # issue.save()
            if (
                start_date.add(**period_add) < pendulum.now()
                and issue.title not in unique_labels_done
            ):
                # we should create a new issue for this one
                print("create new issue for %s" % issue.title)
                new_issue = project.issues.create(
                    {
                        "title": issue.title,
                        "description": issue.description,
                        "labels": issue.labels,
                        "assignee": issue.assignee,
                        "weight": issue.weight,
                        "confidential": issue.confidential,
                    }
                )
                if issue.due_date is not None:
                    new_due_date = pendulum.now() + (
                        pendulum.parse(issue.due_date) - start_date
                    )
                    new_issue.due_date = new_due_date.date()
                    new_issue.save()
                # close the previous issue:
                # TODO: close the issue except when there is a tag to avoid closing
                print("close old issue %s" % issue.title)
                issue.state_event = "close"
                issue.save()
            unique_labels_done.append(issue.title)
