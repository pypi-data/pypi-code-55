import argparse
import os

from termcolor import colored
from termcolor import cprint

development_mode = False

global development_dir, project_path, app_path, template_dir, project_name, app_name


def main():
    # Instantiate the parser
    global development_dir, project_path, app_path, project_name, app_name, template_dir
    parser = argparse.ArgumentParser(prog="newdjango", description="Django Project and App creation")

    base_dir = os.environ['HOME']

    # Add arguments
    parser.add_argument('-d', '--devdir', type=str, default=os.path.join(base_dir, 'Development'), dest='devdir',
                        help='The base development dir to create your project in.')
    parser.add_argument('-t', '--tempdir', type=str, dest='templatedir',
                        help='The directory where your APP template files are stored.')
    parser.add_argument('-p', '--proj', type=str, default='', dest='projectname',
                        help='The name of your Django PROJECT')
    parser.add_argument('-a', '--app', type=str, default='', dest='appname', help='The name of your Django APP.')
    parser.add_argument('-b', '--bootstrap', type=bool, default=False, dest='bootstrap',
                        help='"True" means you want Bootstrap')
    parser.add_argument('-m', '--materializecss', type=bool, default=False, dest='materializecss',
                        help='"True" means you want Materializecss')

    # Parse the arguments
    args = parser.parse_args()

    if development_mode:
        development_dir = os.path.join(base_dir, 'Development/MyDjango')
        template_dir = os.path.join(base_dir, 'Development/MyTemplates', 'new_app_structure')
        project_name = 'SampleProject'.lower()
        project_path = os.path.join(development_dir, project_name)
        app_name = f'app_core'.lower()
        app_path = os.path.join(project_path, str(app_name).lower())
    elif not development_mode:
        development_dir = os.path.join(base_dir, args.devdir)
        template_dir = os.path.join(base_dir, 'Development/MyTemplates', args.templatedir)
        project_name = args.projectname
        project_path = os.path.join(development_dir, project_name)
        app_name = f"app_{str(args.appname).capitalize()}"
        app_path = os.path.join(project_path, str(app_name).lower())

    comfirm_text = colored(
        f'Successfully created...\n\n'
        f'your project: {project_name}\n'
        f'your app: {app_name}\n'
        f'in path: {project_path}\n'
    )
    not_confirm_text = colored('\nCanceled creating your Django project.\n', 'red', attrs=['blink', 'bold'])
    wrong_text = colored('Please enter "y" or "Y" to confirm, or "n" or "N" to cancel, next time you run this command',
                         'green', attrs=['blink', 'bold'])
    question = colored(
        f'\n\nCreation Dir: {development_dir}\n'
        f'Project name: {project_name}\n'
        f'App name: {app_name}\n\n'
        f'Is this correct?: "y" or "n":', 'yellow', attrs=['blink', 'bold']
    )

    def create_django_project():
        if not os.path.exists(project_path):
            os.makedirs(project_path)
            os.system(f'django-admin startproject base {project_path}')
        else:
            cprint('Your project already exists...', 'red', attrs=['bold'])

    def create_django_app():
        os.chdir(project_path)
        if template_dir:
            os.system(f'python3 manage.py startapp --template={template_dir} {app_name}')
        else:
            os.system(f'python3 manage.py startapp {app_name}')

    def create_venv():
        os.chdir(project_path)
        os.system(f"python3 -m venv {project_name}_env")
        os.system(f"python3 -m pip install django-import-export django-icons django-widget-tweaks")
        os.system(f"python3 -m pip install -r {app_path}/requirements.txt")
        os.system(f"pipreqs {project_path}")

    def rename_files():
        templatetags_dir = os.path.join(app_path, 'templatetags')
        os.rename(f"{templatetags_dir}/APPNAME_tags.py", f"{templatetags_dir}/{str(app_name).lower()}_tags.py")
        os.rename(f"{app_path}/static/APPNAME", f"{app_path}/static/{app_name}")
        os.rename(f"{app_path}/static/{app_name}/css/app.sass", f"{app_path}/static/{app_name}/css/{app_name}.sass")
        os.rename(f"{app_path}/static/{app_name}/js/app.js", f"{app_path}/static/{app_name}/js/{app_name}.js")
        os.rename(f"{app_path}/templates/APPNAME", f"{app_path}/templates/{app_name}")
        os.rename(f"{app_path}/templates/{app_name}/base_bs.html", f"{app_path}/templates/{app_name}/base.html")

    def change_appname_in_files():
        files_to_modify = [
            f'{project_path}/base/settings.py',
            f'{project_path}/base/urls.py',
            f'{app_path}/admin.py',
            f'{app_path}/apps.py',
            f'{app_path}/forms.py',
            f'{app_path}/models.py',
            f'{app_path}/urls.py',
            f'{app_path}/views.py',
            f'{app_path}/views.py',
            f'{app_path}/templates/{app_name}/base.html',
            f'{app_path}/templates/{app_name}/base_m.html',
            f'{app_path}/templates/{app_name}/home.html',
        ]

        lowertexttofind = 'appname'
        lowertexttoreplace = app_name.lower()
        captexttofind = 'Appname'
        captexttoreplace = args.appname.capitalize()

        for file in files_to_modify:
            with open(file, "r") as inputfile:
                filedata = inputfile.read()
            cap_filedata = filedata.replace(captexttofind, captexttoreplace)
            with open(file, "w") as newfile:
                newfile.write(cap_filedata)
            cprint(f"Properly named all Django app files with '{str(app_name).capitalize()}'.", "green", attrs=['bold'])

        for file in files_to_modify:
            with open(file, "r") as inputfile:
                filedata = inputfile.read()
            lower_filedata = filedata.replace(lowertexttofind, lowertexttoreplace)
            with open(file, "w") as newfile:
                newfile.write(lower_filedata)
            cprint(f"Properly named all Django app files with '{str(app_name).capitalize()}'.", "green", attrs=['bold'])

    correct = input(question)

    if correct == "y" or correct == "Y":
        create_django_project()
        create_django_app()
        rename_files()
        change_appname_in_files()
        create_venv()
        cprint(comfirm_text)
    elif correct == "n" or correct == "N":
        startover = input('Would you like to startover? "y/Y" or "n/N": ')
        if startover == "y" or startover == "Y":
            main()
        elif startover == "n" or startover == "N":
            cprint(not_confirm_text)
            pass
    else:
        cprint(wrong_text)


if __name__ == "__main__":
    main()
