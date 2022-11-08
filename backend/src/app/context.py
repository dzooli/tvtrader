"""
    Application context definition

    File:       context.py
    Author:     Zoltan Fabian <zoltan.dzooli.fabian>
"""
import socket
from types import SimpleNamespace


class TvTraderContext(SimpleNamespace):
    """Application context class
    """
    _carbon_sock: socket.socket = None

    def __init__(self, **kwargs: any) -> None:
        super().__init__(**kwargs)

    @property
    def carbon_sock(self) -> socket.socket:
        """Getter for the Carbon connection socket

        Returns:
            socket.socket | None: Connection socket for the Carbon instance.
        """
        return self._carbon_sock

    @carbon_sock.setter
    def carbon_sock(self, sock: socket.socket) -> None:
        self._carbon_sock = sock

    @carbon_sock.deleter
    def carbon_sock(self):
        self._carbon_sock.shutdown()
        self._carbon_sock.close()
        del self._carbon_sock
