import modules.ssdp as ssdp
from flask import Flask
from flask import send_file
import urllib.request
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import http

class GreenHouse:
    """A GreenHouse represents a connected greenhouse."""

    def __init__(self, name, logger):
        self.name = name
        self.logger = logger
        self.app = Flask(self.name)

    def connect(self):
        """Perform the connection establishment to a Supervisor in the same LAN."""

        # Discovery Step
        resps = list(ssdp.discover("vegetable-supervisor"))

        # for now support only one supervisor
        if len(resps) != 1:
            self.logger.info("detected {} supervisors, GreenHouse only supports one supervisor".format(len(resps)))
            return

        discovery_resp = resps[0]
        self.logger.info("discovered supervisor at {}".format(discovery_resp.location))

        self.supervisor_address = discovery_resp.location

        # Join Step
        while not self._send_join_request():
            # TODO : retry timer
            pass

        self.logger.info("join accepted")

    def run_rest(self):
        """Run the REST api, using HTTPS."""

        # Route Handlers
        @self.app.route("/")
        def hello():
            return self.name

        @self.app.route("/camera")
        def camera():
            """Returns the last picture taken from the camera."""
            return send_file("photo.jpg", mimetype='image/jpg')

        self.app.run(ssl_context='adhoc')

    def _send_join_request(self):
        assert(self.supervisor_address)
        url = "http://" + self.supervisor_address + "/join" # TODO https
        post_fields = {'name': self.name}
        request = Request(url, urlencode(post_fields).encode())
        got = urlopen(request)
        if got.getcode() == http.HTTPStatus.ACCEPTED:
            return True
        return False
