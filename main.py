import logging

from greenhouse import GreenHouse

def setup():
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('greenhouse')

    gh = GreenHouse("greenhouse", log)
    connected = gh.connect()

    if not connected:
        log.info("Could not connect GreenHouse to Supervisor.")
        return

    gh.run()

if __name__ == "__main__":
    setup()
