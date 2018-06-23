import asyncio
import ssl

from server.cli_args import GetHostAndPort
from server.manager import AsyncServerManager
from server.core.chat_controller import ChatController

if __name__ == "__main__":
    cli_args = GetHostAndPort()  # args parse
    cli_args.get_cli_params()
    HOST, PORT = cli_args.host, cli_args.port

    chat_controller = ChatController()

    loop = asyncio.get_event_loop()

    sc = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sc.load_cert_chain('protocol\cert\chat.cert', 'protocol\cert\chat.key')

    coro = loop.create_server(lambda: AsyncServerManager(chat_controller), HOST, PORT, ssl=sc)

    server = loop.run_until_complete(coro)

    start_msg = 'Serving connections on: {}:{}'.format(*server.sockets[0].getsockname())
    print(start_msg)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        stop_msg = 'Stopping server: {}:{}'.format(*server.sockets[0].getsockname())
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
