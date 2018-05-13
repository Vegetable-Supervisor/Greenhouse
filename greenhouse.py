import http
import io
import json
import logging
import time
import socket
import threading
import urllib.request
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, send_file, abort, request, jsonify, make_response
from flask_api import status

import modules.ssdp as ssdp

from supervisor import Supervisor
from configuration import Configuration

REST_PORT = 5943
REST_HOST = "0.0.0.0"
REST_URL = "https://{}:{}".format(REST_HOST, REST_PORT)


class GreenHouse:
    """A GreenHouse represents a connected greenhouse."""

    def __init__(self, name: str):
        """Create a connected GreenHouse.

        Keyword Arguments:
        name -- name of the GreenHouse to create
        """
        self.name = name
        self.usn = "greenhouse_{}_{}".format(self.name, time.time())
        self.logger = logging.getLogger(self.name)
        self.configuration = Configuration(
            name="greenhouse", description="not yet configured")
        self.app = Flask(self.name)
        self.ssdp_server = ssdp.SSDPServer()
        self.ssdp_server.register(
            manifestation="local",
            usn=self.usn,
            st="greenhouse",
            location=REST_URL,
            server=self.name,
        )

    def run(self):
        self.logger.info("starting SSDP advertiser")
        threading.Thread(target=self.run_ssdp_server, daemon=True).start()
        self.logger.info("starting REST API")
        self.run_rest()

    def run_ssdp_server(self):
        """Run the SSDP Advertiser."""
        self.ssdp_server.run()

    def run_rest(self):
        """Run the REST api, using HTTPS."""

        # Route Handlers

        @self.app.route("/name")
        def name():
            return self.configuration.name

        @self.app.route("/get_configuration")
        def get_configuration():
            r = make_response(json.dumps(self.configuration.__dict__))
            r.mimetype = 'application/json'
            return r

        @self.app.route("/push_configuration", methods=['POST'])
        def push_configuration():
            content = request.get_json()
            # TODO
            return content, status.HTTP_200_OK

        @self.app.route("/camera")
        def camera():
            """Returns the last picture taken from the camera."""
            try:
                return send_file("photo.jpg", mimetype='image/jpg')
            except FileNotFoundError:
                abort(404)

        self.app.run(ssl_context='adhoc')

    def _join_request(self):
        """Send a join request and wait for response. Returns True if and only if the Supervisor accepted the join request."""
        assert(self.supervisor)
        url = "http://" + str(self.supervisor.ip) + ":" + \
            str(self.supervisor.port) + "/join"  # TODO https
        post_fields = {'name': self.configuration.name}
        request = Request(url, urlencode(post_fields).encode())
        got = urlopen(request)
        if got.getcode() == http.HTTPStatus.ACCEPTED:
            return True
        return False
