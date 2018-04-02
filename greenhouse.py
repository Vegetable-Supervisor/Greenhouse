import modules.ssdp as ssdp

class GreenHouse:
    """A GreenHouse represents a connected greenhouse."""

    def __init__(self, name, logger):
        self.name = name
        self.logger = logger

    def Connect(self):
        """Connect to a Vegetable-Supervisor in the LAN."""

        # Discovery step
        resps = list(ssdp.discover("vegetable-supervisor"))

        # for now support only one supervisor
        if len(resps) != 1:
            self.logger.info("detected {} supervisors, GreenHouse only supports one supervisor".format(len(resps)))
            return

        discovery_resp = resps[0]
        self.logger.info("discovered supervisor at {}".format(discovery_resp.location))
