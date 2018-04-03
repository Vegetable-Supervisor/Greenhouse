import logging

from greenhouse import GreenHouse

def setup():
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('greenhouse')

    gh = GreenHouse("greenhouse", log)
    gh.connect()
    gh.run_rest()


if __name__ == "__main__":
    setup()
