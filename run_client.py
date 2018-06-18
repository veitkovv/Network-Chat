import asyncio
import ssl

from client.manager import AsyncClientManager
from client.cli_args import CliArgs
from client.ui.console_ui import ConsoleClient
from client.ui.qt_gui_client import QtGuiClient

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
        ui_instance = QtGuiClient()
    else:
        ui_instance = ConsoleClient()

    loop = asyncio.get_event_loop()
    client_instance = AsyncClientManager(loop, ui_instance)
    coro = loop.create_connection(lambda: client_instance, host, port, ssl=sc)
    loop.run_until_complete(coro)

    asyncio.async(client_instance.get_console_messages(loop))

    loop.run_forever()
    loop.close()
