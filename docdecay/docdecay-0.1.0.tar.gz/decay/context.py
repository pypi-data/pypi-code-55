from argparse import ArgumentParser
import argparse
from email_validator import validate_email, EmailNotValidError


class DocCheckerContext:
    def __init__(self, args: argparse.Namespace, parser: ArgumentParser):
        self.github_branch = args.github_branch
        self.github_repo = args.github_repo
        self.github_repo_owner = args.github_owner
        self.github_repo_path = args.github_repo_folder
        self.github_token = args.github_access_token
        self.doc_is_stale_after_days = args.stale_age_in_days
        self.email_owner_if_stale = args.email_owner
        self.sendgrid_api_key = args.sendgrid_api_key
        self.from_email = args.from_email
        self.admin_report = args.admin_report
        self.administrator = args.administrator
        self.extensions = args.extensions.split(",")

        if self.admin_report is True and not self.administrator:
            parser.error(
                "With 'admin_report' set, you must specify an administrator email using 'administrator' argument")

        if self.administrator:
            try:
                valid = validate_email(self.administrator)
                self.administrator = valid.email
            except EmailNotValidError as e:
                parser.error(f"{self.administrator} is not a valid email address: " + str(e))

        if self.from_email:
            try:
                valid = validate_email(self.from_email)
                self.from_email = valid.email
            except EmailNotValidError as e:
                parser.error(f"{self.from_email} is not a valid email address: " + str(e))

        if self.email_owner_if_stale or self.admin_report:
            if not self.sendgrid_api_key:
                parser.error(f"You must specify a sendgrid token if you are sending owner or admin reports via email")

            if not self.from_email:
                parser.error(f"You must specify a 'from' email if you are sending owner or admin reports via email")
