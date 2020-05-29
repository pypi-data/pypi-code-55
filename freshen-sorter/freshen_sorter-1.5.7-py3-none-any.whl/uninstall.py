from context_menu import windows_menus
from context_menu import menus

def uninstall():
    windows_menus.delete_key(os.path.join(windows_menus.context_registry_format('DIRECTORY_BACKGROUND'), 'Sort Files'))


if __name__ == "__main__":
    if is_admin():
        uninstall()
    else:
        windows_menus.run_admin()
