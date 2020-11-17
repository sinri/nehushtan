from mysql.MySQLKit import MySQLKit
from mysql.MySQLKitConfig import MySQLKitConfig
from tests.config import MYSQL_CONFIG

MySQLKit(MySQLKitConfig(MYSQL_CONFIG))
