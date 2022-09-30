from types import SimpleNamespace
import socket


class TvTraderContext(SimpleNamespace):
    _carbon_sock = None

    def __init__(self, **kwargs: any) -> None:
        super().__init__(**kwargs)

    @property
    def carbon_sock(self):
        return self._carbon_sock

    @carbon_sock.setter
    def carbon_sock(self, sock: socket.socket) -> None:
        self._carbon_sock = sock

    @carbon_sock.deleter
    def carbon_sock(self):
        self._carbon_sock.shutdown()
        self._carbon_sock.close()
        del self._carbon_sock
