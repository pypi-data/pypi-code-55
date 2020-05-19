#!/usr/bin/python3.6
from src.imports import *
from src.utils import get_config

config = get_config()
webhook = config["teams"]["webhook"]

@click.group()
def cli():
    pass

@cli.command()
def getProjects():
    selected_project = questionary.select(
        "Please select the project you'll be working on",
        choices=jira_client.get_projects_names()
    ).ask()
    return selected_project

@cli.command()
def getIssues():
    #! For this command to work you need to manually add the project variable
    #! Or use the getProjects function
    project = ''
    selected_issue = questionary.select(
        "Please select the issue you'll be working on",
        choices=jira_client.get_issues_project(project)
    ).ask()
    click.echo(selected_issue)

@cli.command()
def sendMessage():
    try:
        # * You must create the connectorcard object with the Microsoft Webhook URL
        myTeamsMessage = pymsteams.connectorcard(webhook)

        # * Add text to the message.
        myTeamsMessage.text("This message was sent using Leona")

        # * create the section
        myMessageSection = pymsteams.cardsection()

        # * Section Title
        myMessageSection.title("Feature started")

        # * Activity Elements
        myMessageSection.activityTitle(
            "User " + " started working on the feature: issue_key")
        myMessageSection.activitySubtitle("my activity subtitle")
        myMessageSection.activityImage(
            "https://img.favpng.com/24/25/19/github-repository-version-control-source-code-png-favpng-C3CZbFLHhkc9CB2Qu0CbHEY4W.jpg")
        myMessageSection.activityText("This is my activity Text")

        # * Facts are key value pairs displayed in a list.

        # * Add your section to the connector card object before sending
        myTeamsMessage.addSection(myMessageSection)
        # * send the message.
        myTeamsMessage.send()
        click.echo('Message sent succesfully')
    except Exception as e:
        click.echo('Something Failed : {0}'.format(e))

@cli.command()
def pr():
    # !This code gets all the default reviewers of a specific repository
    # !In this case the repository is leona
    reviewers_name, reviewers_uuid = bitbucket_client.get_reviewers('leona')
    title_prompt = (Input(prompt="Enter the title of the pull request: "))
    description_prompt = (Input(prompt="Enter the description of the pull request: "))
    reviewers_prompt = (Check(prompt="Select the reviewers: ", choices = reviewers_name))
    title_result = title_prompt.launch()
    description_result = description_prompt.launch()
    reviewers_result = reviewers_prompt.launch()
    formated_uuid = bitbucket_client.get_formated_uuid(reviewers_result,reviewers_name, reviewers_uuid)
    branch_name = bitbucket.client.get_current_branch_name()    
    repo_name = bitbucket_client.get_current_repo_name()
    response = bitbucket_client.create_pull_request(title_result, description_result, branch_name, formated_uuid, repo_name)
    click.echo('Pull Request Created succesfully')

@cli.command()
def commitsLog():
    repo_names = ['flowy_iac','flowy_gizmo_configurator_web', 'flowy_api_ts','flowy_form_mobile','flowy_core','flowy_form_web',
                  'flowy_analytics_api','flowy_developer_documentation','flowy_api','flowy_agent','flowy_analytics_web']
    authors, messages, dates, diffs, diffs_data, diffs_stats_data, hashs, lines_added, lines_removed = ([] for i in range(9))
    selected_repo = questionary.select(
        "Please select the issue you'll be working on",
        choices=repo_names
    ).ask()
    
    commits_response = bitbucket_client.get_commits(selected_repo)
    for commit in commits_response['values']:
        authors.append(commit['author']['user']['display_name'])
        messages.append(commit['message'])
        dates.append(commit['date'])
        diffs.append(commit['links']['diff']['href'])
        hashs.append(commit['hash'])
    
    diffs_data = bitbucket_client.get_diffs_data(diffs)
    lines_added, lines_removed = bitbucket_client.get_diffs_stats(hashs,selected_repo)
    log = [{'author': a, 'message': b, 'date': c, 'diff': d, 'lines_added': e, 'lines_removed': f}
           for (a, b, c, d, e, f) in zip(authors, messages, dates, diffs_data, lines_added, lines_removed)]
    mylog = DataFrame(log)
    writer = ExcelWriter('%s_commit_logs.xlsx' % selected_repo)
    mylog.to_excel(writer)
    writer.close()
    click.echo('The excel file has been created succesfully!')

@cli.command()
def jiraLogs():
    projects, keys, issue_name, issue_status, issue_description, issue_summary, issue_assignee, issue_updated = ([] for i in range(8))
   
    selected_project = questionary.select(
        "Please select the project you'll be working on",
        choices=jira_client.get_projects_names()
    ).ask()
        
    issues_data = jira_client.get_all_issues(selected_project, ["key", "summary", "status", "assignee", "updated"])
    
    for issue in issues_data:
        issue_name.append(issue.key)
        issue_status.append(issue.fields.status.name)
        issue_description.append(issue.fields.status.description)
        issue_summary.append(issue.fields.summary)
        issue_assignee.append(str(issue.fields.assignee))
        issue_updated.append(issue.fields.updated)

    log = [{'name': i, 'description': j, 'summary': v, 'assignee': x, 'updated': y,'status': z}
           for (i, j, v, x, y, z) in zip(issue_name, issue_description, issue_summary, issue_assignee, issue_updated,issue_status)]
    
    mylog = DataFrame(log)
    writer = ExcelWriter('%s_jira_logs.xlsx' % selected_project, engine='xlsxwriter')
    mylog.to_excel(writer, sheet_name='logs')
    writer.close()
    click.echo('The excel file has been created succesfully!')

@cli.command()
@click.option('-r','--registry')
@click.option('-t','--tag')
@click.option('-v','--version')
@click.option('-d','--dockerfile')
def build(registry,tag,version,dockerfile):
    command = 'docker build --no-cache -t %s/%s:%s -f %s .' % (registry,tag,version,dockerfile)
    os.system(command)

@cli.command(context_settings={"ignore_unknown_options": True})
@click.option('-r','--registry')
@click.option('-t','--tag')
@click.option('-v','--version')
@click.option('-df','--dockerfile')
@click.argument('options', nargs=-1, type=click.Path())
def build_prod(registry,tag,version,dockerfile, options):
    opt = ''
    for option in options:
        opt += '%s ' % option
    opt = opt[:-1]
    command = 'docker build --no-cache -t %s/%s:%s %s -f %s .' % (registry,tag,version,opt,dockerfile)
    click.echo(command)
    os.system(command)

@cli.command()
@click.option('-r','--registry')
@click.option('-t','--tag') 
@click.option('-v','--version')
def push(registry,tag,version):
    command = 'docker login -u hlcndev0ps -p h1cn2019! && docker push %s/%s:%s' % (registry,tag,version)
    try:
        os.system(command)
    except Exception as e:
        click.echo('Job Failed! : {0}'.format(e))
        sys.exit(-1)
    logout = 'docker logout'
    os.system(logout)

@cli.command()
@click.option('-r','--registry')
@click.option('-t','--tag')
@click.option('-v','--version')
def test(registry, tag, version):
    command = """docker run %s/%s:%s bash -c 'yarn test-ci'""" % (registry, tag, version)
    os.system(command)

@cli.command()
@click.option('-p','--password')
@click.option('-s','--service')
def deploy(password, service):
    command = """ANSIBLE_HOST_KEY_CHECKING=false ansible-playbook /etc/ansible/playbook.yml -i /etc/ansible/hosts --extra-vars 'ansible_sudo_pass=%s' -e service_name=%s""" % (password, service)
    os.system(command)