import asyncio
import ssl

from client.connection_manager import AsyncClientManager
from client.cli_args import CliArgs
from client.ui.console_ui.controller import ConsoleClient
from client.ui.qt_gui.controller import GuiClient

if __name__ == '__main__':
    cli_args = CliArgs()
    cli_args.get_cli_params()
    host = cli_args.host
    port = cli_args.port
    gui = cli_args.gui

    # SSL load
    sc = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sc.load_cert_chain('protocol\cert\chat.cert', 'protocol\cert\chat.key')

    if gui:
        ui_controller = GuiClient()
    else:
        ui_controller = ConsoleClient()

    loop = asyncio.get_event_loop()
    client_instance = AsyncClientManager(loop, ui_controller)
    coro = loop.create_connection(lambda: client_instance, host, port, ssl=sc)
    asyncio.async(client_instance.run_ui(loop))
    loop.run_until_complete(coro)

    loop.run_forever()
    loop.close()
