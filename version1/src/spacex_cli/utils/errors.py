class SpaceXCLIError(Exception):
    """Base CLI exception."""


class NetworkError(SpaceXCLIError):
    """Network connection error."""


class NotFoundError(SpaceXCLIError):
    """Resource not found (404)."""

    def __init__(self, resource: str, identifier: str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"Not found: {resource}/{identifier}")


class APIError(SpaceXCLIError):
    """Unexpected HTTP error."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"SpaceX API error {status_code}: {message}")


class ValidationError(SpaceXCLIError):
    """Invalid user input."""
