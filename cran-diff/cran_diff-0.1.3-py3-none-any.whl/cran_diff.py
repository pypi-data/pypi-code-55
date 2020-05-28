import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Packages
from .models import Imports
from .models import Suggests
from .models import Exports
from .models import Arguments
from .models import News


def make_querymaker(connect_string):
    """Instantiates QueryMaker class"""
    engine = create_engine(connect_string)
    Session = sessionmaker(bind=engine)
    query_maker = QueryMaker(Session())
    return query_maker


class NotFoundError(Exception):
    pass


class QueryMaker():
    def __init__(self, session):
        self.session = session


    def get_names(self):
        """Gets unique names of all packages in database

        return: list of package names
        """ 
        names = self.session.query(Packages.name).distinct()
        names = [element for tupl in names for element in tupl]
        return names

    
    def check_name_and_version(self, package_name, versions):
        """Checks that package name and version number are in database.
        Exception is raised if either are not.

        :params 
        package_name: string for the package name
        versions: list of version number strings
        """
        for version in versions:
            results = (self.session.query(Packages.version)
                                .filter(Packages.name == package_name, Packages.version == version))
            results = [element for tupl in results for element in tupl]
            if len(results) == 0:
                raise NotFoundError()


    def get_latest_versions(self, package_name):
        """Lists all versions of given package in database

        :param package_name: string for the package name
        :return: a list of the package version numbers
        """
        versions = (self.session.query(Packages.version)
                            .filter(Packages.name == package_name)
                            .order_by(Packages.date.desc()))
        versions = [element for tupl in versions for element in tupl]
        if len(versions) == 0:
            raise NotFoundError()
        return versions


    def query_imports(self, package_name, versions):
        """Get dictionary of package imports
            
        :params
        package_name: string for the package name
        versions: list of version number strings
        
        :return: a dictionary of imports with their version number
        """
        self.check_name_and_version(package_name, versions)
        import_list = []
        for version in versions:
            result = (self.session.query(Imports.name, Imports.version)
                            .join(Packages, Packages.id == Imports.package_id)
                            .filter(Packages.name == package_name, Packages.version == version))
            import_list.append(dict(result))
        return import_list

        
    def query_suggests(self, package_name, versions):
        """Get dictionary of package suggests
            
        :params
        package_name: string for the package name
        versions: list of version number strings
        
        :return: a dictionary of suggests with their version number
        """
        self.check_name_and_version(package_name, versions)
        suggest_list = []
        for version in versions:
            result = (self.session.query(Suggests.name, Suggests.version)
                            .join(Packages, Packages.id == Suggests.package_id)
                            .filter(Packages.name == package_name, Packages.version == version))
            suggest_list.append(dict(result))
        return suggest_list


    def query_exports(self, package_name, versions):
        """Get list of package exports
            
        :params
        package_name: string for the package name
        versions: list of version number strings
        
        :return: a list of exports
        """
        self.check_name_and_version(package_name, versions)
        export_list = []
        for version in versions:
            result = (self.session.query(Exports.name, Exports.type)
                            .join(Packages, Packages.id == Exports.package_id)
                            .filter(Packages.name == package_name, Packages.version == version))
            export_list.append(dict(result))
        return export_list
       

    def query_arguments(self, package_name, versions):
        self.check_name_and_version(package_name, versions)
        function_list = []
        argument_list = []
        query = (self.session.query(Packages.version, Arguments.function, Arguments.name, Arguments.default)
            .filter(Packages.name == package_name, Packages.version.in_(versions))
            .join(Arguments, Arguments.package_id == Packages.id))
        result = query.all()
        for version in versions:
            functions = list(set([row[1] for row in result if row[0] == version]))
            function_list.append(functions)
            version_arguments = []
            for function in functions:
                arguments = [row[2:] for row in result if row[0] == version and row[1] == function]
                version_arguments.append(dict(arguments))
            argument_list.append(version_arguments)
        return function_list, argument_list


    def get_news(self):
        query = (self.session.query(Packages.name, Packages.version, Packages.date, Packages.title, Packages.description, News.category, News.text, News.type)
                .join(News, News.package_id == Packages.id))
        result = query.all()
        #Get list of dates, starting most recent
        dates = list(set([i[2].date() for i in result]))
        dates.sort(reverse = True)
        #Get all package updates and news for past five days
        new = {}
        updated = {}
        for date in dates[:5]:
            #Only include dates since update was applied (for now)
            if date < datetime.date(year = 2020, month = 5, day = 27):
                continue
            packages = list(set([i[0] for i in result if i[2].date() == date]))
            new_packages = []
            package_news = []
            for package in packages:
                package_data = [i for i in result if i[0] == package and i[2].date() == date]
                types = [i[-1] for i in package_data]
                #Check whether new package (and locate release version)
                if "new" in types:
                    release_data = [i for i in package_data if i[-1] == "new"][0]
                    package_dict = {"name": package}
                    package_dict.update({"initial_version": release_data[1]})
                    package_dict.update({"title": release_data[3]})
                    package_dict.update({"description": release_data[4]})
                    new_packages.append(package_dict)
                #Check for version updates
                if "update" in types:
                    update_data = [i for i in package_data if i[-1] == "update"]
                    update_versions = list(set([i[1] for i in update_data]))
                    for version in update_versions:
                        news = dict([i[5:7] for i in update_data if i[1] == version])
                        version_dict = {"name": package}
                        version_dict.update({"new_version": version})
                        categories = [i[5] for i in update_data if i[1] == version]
                        text = [i[6] for i in update_data if i[1] == version]
                        #Include version news if this exists
                        if categories[0] != "" or text[0] != "":
                            version_dict.update({"news": news})
                        package_news.append(version_dict)
            new.update({date.strftime('%Y/%m/%d'): new_packages})
            updated.update({date.strftime('%Y/%m/%d'): package_news})
        return new, updated


def get_diff(result_list):
    """Get dictionary of diffs for imports and suggests
        
    :params
    result_list: output from query_imports() or query_suggests()
    :return: a dictionary with added, removed and changed (version numbers) packages
    """
    set1 = set(result_list[0].items())
    set2 = set(result_list[1].items())
    diff1 = set1 - set2
    diff2 = set2 - set1
    # Check for version changes
    changed = []
    added = []
    removed = []
    for i in diff1:
        was_changed = False
        for j in diff2:
            if i[0] == j[0]:
                changed.append((i[0], i[1], j[1]))
                was_changed = True
                break
        if not was_changed:
            added.append(i)
    for i in diff2:
        was_changed = False
        for j in diff1:
            if i[0] == j[0]:
                was_changed = True
                break
        if not was_changed:
            removed.append(i)
    added = [list(elem) for elem in added]
    removed = [list(elem) for elem in removed]
    changed = [list(elem) for elem in changed]
    return {'added': added,
            'removed': removed,
            'changed': changed}


def get_export_diff(result_list):
    """Get dictionary of diffs for exports
        
    :params
    result_list: output from query_exports()
    :return: a dictionary with added and removed packages
    """
    set1 = set(result_list[0].items())
    set2 = set(result_list[1].items())
    diff1 = set1 - set2
    diff2 = set2 - set1
    #Check which exports have been added / removed
    added = []
    removed = []
    for i in diff1:
        added.append(i)
    for i in diff2:
        removed.append(i)
    added = [list(elem) for elem in added]
    removed = [list(elem) for elem in removed]
    return {'added': added,
            'removed': removed}


def get_argument_diff(function_list, argument_list):
    set1 = set(function_list[0])
    set2 = set(function_list[1])
    diff1 = set1 - set2
    diff2 = set2 - set1
    #Check which functions have been added / removed
    added = []
    removed = []
    for i in diff1:
        added.append(i)
    for i in diff2:
        removed.append(i)
    #Check argument difference for functions retained in latest version
    retained = set1 - diff1
    changed = []
    added_args = []
    removed_args = []
    for f in retained:
        new_function_id = function_list[0].index(f)
        old_function_id = function_list[1].index(f)
        set1 = set(argument_list[0][new_function_id].items())
        set2 = set(argument_list[1][old_function_id].items())
        diff1 = set1 - set2
        diff2 = set2 - set1
        #Check for added / removed arguments and changed defaults
        for i in diff1:
            was_changed = False
            for j in diff2:
                if i[0] == j[0]:
                    changed.append((f, i[0], j[1], i[1]))
                    was_changed = True
                    break
            if not was_changed:
                added_args.append((f, i[0]))
        for i in diff2:
            was_changed = False
            for j in diff1:
                if i[0] == j[0]:
                    was_changed = True
                    break
            if not was_changed:
                removed_args.append((f, i[0]))
    added_args = [list(elem) for elem in added_args]
    removed_args = [list(elem) for elem in removed_args]
    changed = [list(elem) for elem in changed]
    return {'added functions': added,
            'removed functions': removed,
            'new arguments': added_args,
            'removed arguments': removed_args,
            'argument default changes': changed}
