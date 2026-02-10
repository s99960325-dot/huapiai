import os
from contextlib import contextmanager
from typing import Generator, Optional

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from huapir.config import DATABASE_URL, DB_PATH
from huapir.ioc.container import DependencyContainer
from huapir.logger import get_logger

logger = get_logger("DB")

# 创建Base类，用于所有ORM模型
Base = declarative_base()
metadata = MetaData()


class DatabaseManager:
    """数据库管理器，负责管理数据库连接和会话。支持 SQLite / PostgreSQL / MySQL。"""

    def __init__(self, container: DependencyContainer, database_url: Optional[str] = None, is_debug: bool = False):
        self.container = container
        self.engine = None
        self.session_factory = None
        self.data_dir = DB_PATH
        self.db_path = os.path.join(self.data_dir, "kirara.db")
        self.database_url = database_url or DATABASE_URL or None
        self.is_debug = is_debug

    def initialize(self):
        """初始化数据库连接"""
        os.makedirs(self.data_dir, exist_ok=True)

        if self.database_url:
            db_url = self.database_url
        else:
            db_url = f"sqlite:///{self.db_path}"

        connect_args: dict = {}
        engine_kw: dict = {"echo": self.is_debug}
        if db_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
            engine_kw["connect_args"] = connect_args
        else:
            # PostgreSQL / MySQL: 连接池与健康检查
            engine_kw["pool_pre_ping"] = True
            engine_kw["pool_size"] = 5
            engine_kw["max_overflow"] = 10
        self.engine = create_engine(db_url, **engine_kw)

        self.session_factory = sessionmaker(bind=self.engine, autocommit=False, autoflush=False, expire_on_commit=False)
        self._run_migrations()
        logger.info(f"Database initialized at {self.engine.url}")

    def _run_migrations(self):
        assert self.engine is not None
        """运行数据库迁移"""
        try:
            # 获取 alembic.ini 的路径
            package_dir = os.path.dirname(os.path.dirname(__file__))
            alembic_ini_path = os.path.join(package_dir, "alembic.ini")
            
            # 如果配置文件不存在，说明是作为包安装的，使用默认配置
            if not os.path.exists(alembic_ini_path):
                alembic_cfg = Config()
                alembic_cfg.set_main_option("script_location", os.path.join(package_dir, "alembic"))
            else:
                alembic_cfg = Config(alembic_ini_path)
                
            alembic_cfg.set_main_option("sqlalchemy.url", str(self.engine.url))

            # 检查是否需要迁移
            with self.engine.connect() as connection:
                context = MigrationContext.configure(connection)
                current_rev = context.get_current_revision()
                
                script = ScriptDirectory.from_config(alembic_cfg)
                head_rev = script.get_current_head()

                if current_rev != head_rev:
                    logger.info("Running database migrations...")
                    command.upgrade(alembic_cfg, "head")
                    logger.info("Database migrations completed")
                else:
                    logger.info("Database schema is up to date")

        except Exception as e:
            logger.error(f"Error during database migration: {e}")
            raise

    def get_session(self) -> Session:
        """获取数据库会话，调用方负责 commit/rollback 与 close。"""
        if not self.session_factory:
            self.initialize()
        assert self.session_factory is not None
        return self.session_factory()

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """提供事务作用域：成功则 commit，异常则 rollback，最后关闭 session。"""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def shutdown(self):
        """关闭数据库连接"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
