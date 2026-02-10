from typing import Optional

from sqlalchemy import select

from huapir.database.manager import DatabaseManager
from huapir.ioc.container import DependencyContainer
from huapir.multitenancy.models import Tenant, TenantMembership


class TenantService:
    """多租户服务：默认租户保障、成员关系与租户解析。"""

    def __init__(self, container: DependencyContainer):
        self.container = container
        self.db_manager = container.resolve(DatabaseManager)

    def ensure_default_tenant(self, tenant_id: str) -> None:
        with self.db_manager.session_scope() as session:
            existing = session.execute(
                select(Tenant).where(Tenant.tenant_id == tenant_id)
            ).scalar_one_or_none()
            if existing is not None:
                return
            session.add(Tenant(tenant_id=tenant_id, name=tenant_id))

    def user_belongs_to_tenant(self, tenant_id: str, user_id: str) -> bool:
        with self.db_manager.session_scope() as session:
            membership = session.execute(
                select(TenantMembership).where(
                    TenantMembership.tenant_id == tenant_id,
                    TenantMembership.user_id == user_id,
                    TenantMembership.is_active.is_(True),
                )
            ).scalar_one_or_none()
        return membership is not None

    def add_membership(self, tenant_id: str, user_id: str, role: str = "member") -> None:
        with self.db_manager.session_scope() as session:
            membership = session.execute(
                select(TenantMembership).where(
                    TenantMembership.tenant_id == tenant_id,
                    TenantMembership.user_id == user_id,
                )
            ).scalar_one_or_none()
            if membership is None:
                session.add(TenantMembership(tenant_id=tenant_id, user_id=user_id, role=role))
            else:
                membership.role = role
                membership.is_active = True

    def resolve_tenant_for_user(self, user_id: str) -> Optional[str]:
        with self.db_manager.session_scope() as session:
            membership = session.execute(
                select(TenantMembership)
                .where(TenantMembership.user_id == user_id, TenantMembership.is_active.is_(True))
                .limit(1)
            ).scalar_one_or_none()
        if membership is None:
            return None
        return membership.tenant_id
