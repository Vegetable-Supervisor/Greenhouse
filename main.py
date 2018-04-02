import logging

from greenhouse import GreenHouse

def main():
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('greenhouse')

    gh = GreenHouse("greenhouse", log)
    gh.Connect()


if __name__ == "__main__":
    main()
