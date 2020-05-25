"""main entry for meteolab command-line interface"""

def main():
    from meteolab import Meteolab
    ret, fwds = Meteolab().run_command()
    return ret

if __name__ == "__main__":
    main()
