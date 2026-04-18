import inspect
from functools import wraps
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
def render(template_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get('request')
            if request is None:
                raise ValueError("The decorated function must have a 'request' parameter.")
            if inspect.iscoroutinefunction(func):
                context = await func(*args, **kwargs)
            else:
                context = func(*args, **kwargs)
            
            if context is None:
                context = {}

            return templates.TemplateResponse(
                request=request,
                name=template_name,
                context=context
            )
        return wrapper
    return decorator