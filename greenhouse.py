import modules.ssdp as ssdp
from flask import Flask, send_file, abort, request
import urllib.request
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import http

from supervisor import Supervisor

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
            return False

        discovery_resp = resps[0]
        self.supervisor = Supervisor(discovery_resp.location)

        self.logger.info("discovered supervisor at {}".format(self.supervisor.location))


        # Join Step
        joined = self._join_request()
        if not joined:
            self.logger.info("could not join supervisor")
            return False

        self.logger.info("join accepted")
        return True

    def run(self):
        """Run the REST api, using HTTPS."""
        assert(self.supervisor)

        # Only allow Supervisor's IP to access REST API
        @self.app.before_request
        def limit_remote_addr():
            if request.remote_addr != self.supervisor.ip:
                abort(http.HTTPStatus.FORBIDDEN)

        # Route Handlers

        @self.app.route("/name")
        def name():
            return self.name

        @self.app.route("/camera")
        def camera():
            """Returns the last picture taken from the camera."""
            return send_file("photo.jpg", mimetype='image/jpg')

        self.app.run(ssl_context='adhoc')

    def _join_request(self):
        """Send a join request and wait for response. Returns True if and only if the Supervisor accepted the join request."""
        assert(self.supervisor)
        url = "http://" + str(self.supervisor.ip) + ":" + str(self.supervisor.port) + "/join" # TODO https
        post_fields = {'name': self.name}
        request = Request(url, urlencode(post_fields).encode())
        got = urlopen(request)
        if got.getcode() == http.HTTPStatus.ACCEPTED:
            return True
        return False
