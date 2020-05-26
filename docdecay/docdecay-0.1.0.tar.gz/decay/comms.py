import datetime
from typing import List

from decay.analyzers import FileAnalysis
from decay.context import DocCheckerContext
from decay.feedback import warning, info
from decay.reports import OwnerReport, AdminReport


def send_results(all_file_analyses: List[FileAnalysis], context: DocCheckerContext):
    results = {}

    # sort in descending order by age.  If there is no date, set the date to something way in the past in the hopes
    #   that it appears near the bottom of the list.
    all_file_analyses.sort(key=lambda x: x.last_change or datetime.datetime.now() - datetime.timedelta(days=3650),
                           reverse=False)

    info(f"Post-processing {len(all_file_analyses)} checked files...", 0)
    # Group all the analyses into lists under each email recipient.
    for a in all_file_analyses:
        if not a.file_changed_recently and context.email_owner_if_stale:
            email = a.owner if a.owner else context.administrator
            if not email:
                warning(
                    "Found an old doc but there's no one to send it to.  Consider setting the --administrator "
                    "argument to ensure there is a recipient for any stale docs.", 1)
            else:
                if email not in results:
                    results[email] = []
                results[email].append(a)

    info(f"Sending {len(results)} owner report emails...", 1)
    for email, stale_file_analyses in results.items():
        owner_report = OwnerReport([email], context)
        owner_report.add_analysis(stale_file_analyses)
        owner_report.send()

    if context.administrator and context.admin_report:
        info(f"Sending admin email...", 1)
        admin_report = AdminReport([context.administrator], context)
        admin_report.add_analysis(all_file_analyses)
        admin_report.send()
