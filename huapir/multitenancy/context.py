import contextlib
import contextvars
from typing import Dict, Iterator, Optional

tenant_context: contextvars.ContextVar[dict[str, str]] = contextvars.ContextVar(
    "tenant_context", default={}
)


def set_tenant_context(tenant_id: str, user_id: Optional[str] = None) -> contextvars.Token:
    context = {"tenant_id": tenant_id}
    if user_id:
        context["user_id"] = user_id
    return tenant_context.set(context)


def get_tenant_context() -> dict[str, str]:
    return dict(tenant_context.get())


@contextlib.contextmanager
def use_tenant_context(tenant_id: str, user_id: Optional[str] = None) -> Iterator[None]:
    token = set_tenant_context(tenant_id, user_id=user_id)
    try:
        yield
    finally:
        tenant_context.reset(token)
