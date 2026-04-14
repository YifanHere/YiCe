"""Custom exceptions for YiCe backend."""


class DataProviderError(Exception):
    """Base exception for data provider errors."""
    
    def __init__(self, provider: str, message: str, original_error: Exception = None):
        self.provider = provider
        self.original_error = original_error
        super().__init__(f"{provider} error: {message}")


class CacheError(Exception):
    """Base exception for cache-related errors."""
    
    def __init__(self, operation: str, message: str, original_error: Exception = None):
        self.operation = operation
        self.original_error = original_error
        super().__init__(f"Cache {operation} error: {message}")


class DataServiceError(Exception):
    """Base exception for data service errors."""
    
    def __init__(self, service: str, message: str, original_error: Exception = None):
        self.service = service
        self.original_error = original_error
        super().__init__(f"{service} error: {message}")


class RateLimitError(Exception):
    """Exception for rate limiting errors."""
    
    def __init__(self, message: str, retry_after: int = None):
        self.retry_after = retry_after
        if retry_after:
            message = f"{message} (retry after {retry_after} seconds)"
        super().__init__(message)


class ConfigurationError(Exception):
    """Exception for configuration errors."""
    
    def __init__(self, key: str, message: str = None):
        self.key = key
        if message:
            super().__init__(f"Configuration error for {key}: {message}")
        else:
            super().__init__(f"Configuration error for {key}")


class ValidationError(Exception):
    """Exception for data validation errors."""
    
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Validation error for {field}: {message}")