"""
This module is used to build objects which could be used by moic.cli.utils method
For example the print_issue function
"""
from datetime import datetime

from jira.resources import Comment, Issue, IssueType, Status

from moic.base import settings
from moic.plugins.jira.utils.parser import JiraDocument


class JiraIssue:
    """
    JiraIssue Class represents a normalized issue based on a Jira.Issue resource
    """

    def __init__(self, raw: Issue):
        """
        Init object method

        Args:
            raw (Issue): A Jira Issue
        """
        self.raw = raw
        self.key = raw.key
        self.summary = raw.fields.summary
        self.type = JiraIssueType(raw.fields.issuetype)
        self.reporter = raw.fields.reporter if hasattr(raw.fields, "reporter") else ""
        self.decription = raw.fields.description if hasattr(raw.fields, "description") else ""
        self.status = JiraStatus(raw.fields.status)
        self.assignee = raw.fields.assignee if hasattr(raw.fields, "assignee") and raw.fields.assignee else ""
        self.peer = (
            raw.raw["fields"][settings.get("custom_fields.peer")]["displayName"]
            if settings.get("custom_fields.peer") in raw.raw["fields"]
            and raw.raw["fields"][settings.get("custom_fields.peer")]
            else ""
        )
        self.points = (
            raw.raw["fields"][settings.get("custom_fields.story_points")]
            if settings.get("custom_fields.story_points") in raw.raw["fields"]
            else ""
        )
        self.subtasks = [JiraIssue(i) for i in raw.fields.subtasks] if hasattr(raw.fields, "subtasks") else []

    def __repr__(self):
        """
        Representation method
        """
        return f"<JiraIssue key={self.key}, summary={self.summary}>"


class JiraComment:
    """
    JiraComment Class represents a normalized issue comment based on Jira.Comment resource
    """

    def __init__(self, raw: Comment):
        """
        Init method

        Args:
            raw (Status): A Jira Comment
        """
        self.raw = raw
        self.id = raw.id
        self.author = raw.author.displayName
        self.body = [e.rendered for e in JiraDocument(raw.body).elements]
        self.created = datetime.strptime(raw.created.split(".")[0], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y %H:%M:%S")

    def __repr__(self):
        """
        Representation method
        """
        return f"<JiraComment id={self.id}, author={self.author}>"


class JiraIssueType:
    """
    JiraIssueType Class represents a normalized issue type based on Jira.IssueType resource
    """

    def __init__(self, raw: IssueType):
        """
        Init method

        Args:
            raw (Status): A Jira IssueType
        """
        self.raw = raw
        self.id = raw.id
        self.description = raw.description
        self.name = raw.name

    def __repr__(self):
        """
        Representation method
        """
        return f"<JiraIssueType id={self.id}, name={self.name}>"


class JiraStatus:
    """
    JiraStatus Class represents a normalized status based on a Jira.Status resource
    """

    def __init__(self, raw: Status):
        """
        Init method

        Args:
            raw (Status): A Jira Status
        """
        self.raw = raw
        self.id = raw.id
        self.name = raw.name
        self.description = raw.description
        self.category = raw.statusCategory.key
        self.color = raw.statusCategory.colorName

    def __repr__(self):
        """
        Representation method
        """
        return f"<JiraStatus id={self.id}, name={self.name}>"
