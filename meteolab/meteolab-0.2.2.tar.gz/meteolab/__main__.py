"""main entry for meteolab command-line interface"""

def main():
    from meteolab import Meteolab
    return Meteolab().main()

if __name__ == "__main__":
    main()
