import sqlite3


class Model:

    database = 'readhotmaildb.db'
    def __init__(self):
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        
        
    def createDB(self):

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        
        
        
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fingerprint (
                ID INTEGER PRIMARY KEY,
                Group1 TEXT,
                Group2 TEXT,
                Device1 TEXT,
                Device2 TEXT,
                Device3 TEXT,
                GPU TEXT,
                R6408 TEXT,
                R35661 TEXT,
                R36349 TEXT,
                Random TEXt
                
            )
            ''')
        
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS browser (
                ID INTEGER PRIMARY KEY,
                Browser_type TEXT,
                Proxy_type TEXT,
                Proxy_ip TEXT,
                Proxy_port TEXT,
                Proxy_user TEXT,
                Proxy_pass TEXT,
                Profile_name TEXT
                
            )
            ''')



        cursor.execute('''
            CREATE TABLE IF NOT EXISTS account (
                ID INTEGER PRIMARY KEY,
                Profile_name TEXT,
                Password TEXT,
                Access_token TEXT,
                Refresh_token TEXT,
                Error TEXT,
                Status TEXT,
                Browser_id INTEGER,
                Fingerprint_id INTEGER ,
                FOREIGN KEY (Browser_id) REFERENCES browser(ID) ON DELETE CASCADE,
                FOREIGN KEY (Fingerprint_id) REFERENCES fingerprint(ID) ON DELETE CASCADE        
            )
            ''')
        conn.commit()
        
    # def writeDB(self, table, data):
    #     records = [(item['id'], item['profile_name'], item['password'], item['browser'], item['proxy_host'], 
    #                 item['proxy_port'],item['proxy_username'],item['proxy_password'],
    #                 item['access_token'], item['refresh_token'], item['error'], item['status']) for item in data]
    #     self.cursor.executemany(f'''
    #         INSERT OR REPLACE INTO {table} 
    #         (ID,Profile_name, password, Browser, Proxy_host, Proxy_port, Proxy_username, Proxy_password, Access_token, Refresh_token, Error, Status)
    #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    #     ''', records)
        
    #     self.conn.commit()
        # self.conn.close()
    def writeDB(self, table, records):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        for record in records:
            keys = ', '.join(record.keys())
            placeholders = ', '.join(['?'] * len(record))
            values = tuple(record.values())

            cursor.execute(f'''
                INSERT OR REPLACE INTO {table} ({keys})
                VALUES ({placeholders})
            ''', values)
        conn.commit()
   
        
        
    def updateDB(self,table,id,data:dict):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        fields = ', '.join([f"{key} = ?" for key in data.keys()])
        values = list(data.values())
        values.append(id)
        sql = f"UPDATE {table} SET {fields} WHERE ID = ?"
        cursor.execute(sql, values)
        conn.commit()


    def readDB(self,table):
        self.cursor.execute(f'SELECT * FROM {table}')
        rows = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]

        result = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            result.append(row_dict)

        return result
            
    def disconnectDB(self):
        self.conn.close()
        
    def getProfilePage(self, limit, offset):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()       
        cursor.execute('''
            SELECT 
                account.ID as Profile_id,account.*, browser.ID as Browser_id, browser.*
            FROM account
            JOIN browser ON account.Browser_id = browser.ID
            LIMIT ? OFFSET ?
        ''', (limit, offset)
        )

        rows = cursor.fetchall()
        


        column_names = [desc[0] for desc in cursor.description]
        print(column_names)
        result = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            result.append(row_dict)

        return result