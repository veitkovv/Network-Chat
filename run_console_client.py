from client.manager import AsyncClientManager
from client.cli_args import GetHostAndPort
import asyncio
import ssl

if __name__ == '__main__':
    cli_args = GetHostAndPort()
    cli_args.get_cli_params()
    host = cli_args.host
    port = cli_args.port

    sc = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sc.load_cert_chain('protocol\cert\chat.cert', 'protocol\cert\chat.key')

    loop = asyncio.get_event_loop()
    client_instance = AsyncClientManager(loop)
    coro = loop.create_connection(lambda: client_instance, host, port, ssl=sc)
    loop.run_until_complete(coro)

    asyncio.async(client_instance.get_console_messages(loop))

    loop.run_forever()
    loop.close()
