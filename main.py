from dialogic.dialog_connector import DialogConnector
from dialogic.server.flask_server import FlaskServer


from dm import make_dm
import scenarios

import logging
logging.basicConfig(level=logging.DEBUG)


dm = make_dm()
connector = DialogConnector(
    dialog_manager=dm,
    alice_native_state='session',  # use built-in session state in Alice
)
server = FlaskServer(connector=connector)

handler = connector.serverless_alice_handler

if __name__ == '__main__':
    server.parse_args_and_run()
