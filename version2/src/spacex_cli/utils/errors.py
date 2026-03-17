class SpaceXCLIError(Exception):
    """Базовое исключение CLI."""


class NetworkError(SpaceXCLIError):
    """Ошибка сетевого соединения."""


class NotFoundError(SpaceXCLIError):
    """Ресурс не найден (404)."""

    def __init__(self, resource: str, identifier: str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"Not found: {resource}/{identifier}")


class APIError(SpaceXCLIError):
    """Непредвиденная HTTP-ошибка."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"SpaceX API error {status_code}: {message}")


class ValidationError(SpaceXCLIError):
    """Некорректный ввод пользователя."""
