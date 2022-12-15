import mysql.connector


class DB:
    def __init__(self, **kwargs) -> None:
        self.cnx = mysql.connector.connect(host=kwargs.get('host'),
                                           user=kwargs.get('user'),
                                           passwd=kwargs.get('pwd'),
                                           database=kwargs.get('db'))
        self.cnx.autocommit = True
        self.cursor = self.cnx.cursor(buffered=True, dictionary=True)
