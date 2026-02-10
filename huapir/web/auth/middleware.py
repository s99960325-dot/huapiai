from functools import wraps

from quart import g, jsonify, request

from huapir.config.global_config import GlobalConfig
from huapir.multitenancy.service import TenantService
from huapir.web.auth.services import AuthService


def require_auth(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        # 如果 query string 中包含 token，则使用该 token
        token = request.args.get("auth_token")
        if not token:
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"error": "No authorization header"}), 401
            token_type, token = auth_header.split()
            if token_type.lower() != "bearer":
                return jsonify({"error": "Invalid token type"}), 401
        try:
            auth_service: AuthService = g.container.resolve(AuthService)
            if not auth_service.verify_token(token):
                return jsonify({"error": "Invalid token"}), 401

            if g.container.has(GlobalConfig):
                config = g.container.resolve(GlobalConfig)
                if config.tenant.enabled and config.tenant.strict_mode:
                    tenant_id = request.headers.get("X-Tenant-ID")
                    user_id = request.headers.get("X-User-ID")
                    if not tenant_id or not user_id:
                        return jsonify({"error": "Missing tenant context headers"}), 403
                    if g.container.has(TenantService):
                        tenant_service = g.container.resolve(TenantService)
                        if not tenant_service.user_belongs_to_tenant(tenant_id, user_id):
                            return jsonify({"error": "Tenant access denied"}), 403

            return await f(*args, **kwargs)
        except Exception as e:
            raise e

    return decorated_function
