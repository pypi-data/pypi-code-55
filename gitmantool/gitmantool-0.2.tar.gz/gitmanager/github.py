from github import Github

from .settings import CredsManager


class GithubClient:
    
    def __init__(self, cfg):
        self.creds = CredsManager()
        self.TOKEN = self.creds.get_token("github")
        self.SRV = cfg.server
        self.USR = cfg.username
        self.REPO = cfg.repo
        self.link = cfg.link

        self.g = Github(self.TOKEN)
        repo = f"{self.USR}/{self.REPO}"
        self.r = self.g.get_repo(repo)


    # ─── COMMANDS ───────────────────────────────────────────────────────────────────

    def list_issues(self):
        for i in self.open_issues:        
            print(f" [{i.number}] {i.title}")

    def close_issue(self, id):
        issue = self.r.get_issue(number=int(id))
        issue.edit(state='closed')
    
    def show_issue(self, id):
        issue = self.r.get_issue(number=int(id))
        print(issue.url)
        print(issue.title)
        print(issue.body)

    def new_issue(self, labels):
        title = input("Input title: ")
        body = input("Input contents: \n")
        self.r.create_issue(title=title, body=body, labels=labels)
    
    # ─── PROPERTIES ─────────────────────────────────────────────────────────────────

    @property
    def open_issues(self):
        lista = []
        for i in self.r.get_issues():
            if i.milestone is not None:
                if i.milestone.state == "open":
                    lista.append(i)
        return lista