from contextvars import ContextVar
from typing import Optional

request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)

def set_request_context(request_id: str, user_id: str):
    request_id_var.set(request_id)
    user_id_var.set(user_id)

def get_request_context() -> dict:
    return {
        "request_id": request_id_var.get(),
        "user_id": user_id_var.get()
    }