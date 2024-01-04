### Convert HTTP exceptions in your custom exceptions

Usually it's a good idea to hide implementation details between layers. We can convert `requests` exceptions
to our custom exceptions by creating an `ExceptionHandler`.

```python
from api_client_framework.protocols import ExceptionHandler


class MyCustomPermissionDenied(Exception):
    ...


class CustomExceptionHandler(ExceptionHandler):
    def handle_exception(self, exception, response):
        # Convert this specific error to our custom error
        if exception.status_code == 400 and response.data["error_code"] == "permission_denied":
            raise MyCustomPermissionDenied()
        
        # Keep other exceptions untouched
        raise exception
```