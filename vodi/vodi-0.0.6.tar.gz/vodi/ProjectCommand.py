from vodi import Projects

class ProjectCommand():
    def printAll(self):
        Projects.printAllProjects()

    def print(self, project):
        Projects.printProject(project)