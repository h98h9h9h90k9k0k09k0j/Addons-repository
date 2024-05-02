"""Client-specific Exceptions for websocket-distributed addon."""

from __future__ import annotations


class SocketClientException(Exception):
    """Generic Matter exception."""


class TransportError(SocketClientException):
    """Exception raised to represent transport errors."""


class ConnectionClosed(TransportError):
    """Exception raised when the connection is closed."""


class CannotConnect(TransportError):
    """Exception raised when failed to connect the client."""


class ConnectionFailed(TransportError):
    """Exception raised when an established connection fails."""


class NotConnected(MatterClientException):
    """Exception raised when not connected to client."""


class InvalidState(SocketClientException):
    """Exception raised when data gets in invalid state."""


class InvalidMessage(SocketClientException):
    """Exception raised when an invalid message is received."""


class InvalidServerVersion(SocketClientException):
    """Exception raised when connected to server with incompatible version."""
