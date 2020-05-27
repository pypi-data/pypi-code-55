from .pubdoc import cli 

def main():
    cli(auto_envvar_prefix='PUBDOC')

def run() -> None:
    main()

if __name__ == "__main__":
    main()