from .model import Model
import sqlite3





class Account(Model):
    table = 'account'
    def __init__(self):
        self.model = Model()
        self.model.__init__()
        self.cursor = self.model.cursor

    def readAccount(self):
        # return self.model.readDB(self.table)
        conn = sqlite3.connect(self.model.database)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table}")
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return data

    def writeAccount(self, data):
        self.model.writeDB(table=self.table,records=data)


    def readAccountForID(self, ID):
        conn = sqlite3.connect(self.model.database)
        cursor = conn.cursor()
        idProfile = int(ID)
        cursor.execute(f'SELECT * FROM {self.table} WHERE ID=?',(idProfile,))
        row = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description]

        row_dict = dict(zip(column_names, row))

        return row_dict

    def updateAccount(self, ID, data:dict):
        check = self.model.updateDB(table=self.table,ID=ID,data=data)