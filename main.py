import logging

from greenhouse import GreenHouse

def setup():
    logging.basicConfig(level=logging.INFO)

    gh = GreenHouse("greenhouse")
    gh.run()

if __name__ == "__main__":
    setup()
