import os

# 读取DATA_PATH环境变量，若未能找到则以当前工作目录为根文件夹存储在$PWD/data目录下。
DATA_PATH = os.path.abspath(
    os.environ.get("DATA_PATH", os.path.join(os.getcwd(), "data"))
)
# 支持覆盖配置路径，便于容器化与多环境部署。
CONFIG_FILE = os.path.abspath(
    os.environ.get("CONFIG_PATH", os.path.join(DATA_PATH, "config.yaml"))
)
# 统一数据库连接来源，支持 PostgreSQL/MySQL/SQLite。
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
# 按照规范插件应该在PLUGIN_PATH目录下存储对应的文件。
PLUGIN_PATH = os.path.join(DATA_PATH, "plugins")
DB_PATH = os.path.join(DATA_PATH, "db")

if os.path.exists(DATA_PATH) is False:
    os.makedirs(DATA_PATH)

if os.path.exists(PLUGIN_PATH) is False:
    os.makedirs(PLUGIN_PATH)

if os.path.exists(DB_PATH) is False:
    os.makedirs(DB_PATH)
