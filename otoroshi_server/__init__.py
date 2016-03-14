from os import environ
from autobahn.twisted.wamp import ApplicationRunner
from otoroshi_server.component import OtoroshiComponent


runner = ApplicationRunner(
    environ.get('AUTOBAHN_ROUTER', u"ws://127.0.0.1:8080/ws"),
    u"otoroshi",
    debug=False
)
runner.run(OtoroshiComponent)
