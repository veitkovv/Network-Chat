import asyncio
import ssl
import threading

from client.connection_manager import AsyncClientManager
from client.cli_args import CliArgs
from client.ui.console_ui.controller import ConsoleClient
from client.ui.qt_gui.controller import GuiClient
from client.ui.qt_gui.main import create_main_window


def create_loop(ui_controller, host, port, sc):
    """Цикл событий в главном потоке"""
    loop = asyncio.get_event_loop()
    client_instance = AsyncClientManager(loop, ui_controller)
    coro = loop.create_connection(lambda: client_instance, host, port, ssl=sc)
    loop.run_until_complete(coro)
    asyncio.async(client_instance.get_console_messages(loop))

    loop.run_forever()
    loop.close()


def create_thread_loop(ui_controller, host, port, sc):
    """Цикл событий не в главном потоке. Главный поток занят QT окном"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client_instance = AsyncClientManager(loop, ui_controller)
    coro = loop.create_connection(lambda: client_instance, host, port, ssl=sc)
    loop.run_until_complete(coro)
    asyncio.async(client_instance.get_gui_messages(loop))

    loop.run_forever()
    loop.close()


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
        ui_controller = GuiClient()  # сигналы в главный поток будут исходить из экземпляра этого класса.
        qt_thread = threading.Thread(target=create_thread_loop, args=(ui_controller, host, port, sc), daemon=True)
        qt_thread.start()
        create_main_window(ui_controller)
    else:
        ui_controller = ConsoleClient()
        create_loop(ui_controller, host, port, sc)
