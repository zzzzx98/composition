import pymysql
import os

class F1:

    def __int__(self):
        pass

    #@staticmethod
    def _get_connection(self):

        usr = os.environ.get('DBUSER')
        pw = os.environ.get('DBPW')
        host = os.environ.get('DBHOST')

        conn = pymysql.connect(
            user="root",
            password="dbuserdbuser",
            host="localhost",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    #@staticmethod
    def get_qualifying(self,id):

        sql = "SELECT * FROM f22_databases.qualify where qualifyId = %s" % (id);
        conn = self._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        if result:
            return result
        else:
            return "Nothing Found."

    #@staticmethod
    def append_new_qualifying(self,data):
        if self.get_qualifying(data['qualifyId'])!="Nothing Found.":
            return ("already exist")
        sql = "INSERT INTO f22_databases.qualify VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)";
        conn = self._get_connection()
        cur = conn.cursor()
        try:
            conn.begin()
            res = cur.execute(sql, (data['qualifyId'],data['raceId'],data['driverId'],data['constructorId'],data['number'],data['position'],data['q1'],data['q2'],data['q3']))
            conn.commit()
            cur.close()
            conn.close()
            return "sucessfully add"
        except Exception as e:
            conn.rollback()
            return e

    #@staticmethod
    def delete_qualifying(self,id):
        sql = "DELETE FROM f22_databases.qualify where qualifyId = %s";
        conn = self._get_connection()
        cur = conn.cursor()
        try:
            conn.begin()
            res = cur.execute(sql, (id))
            conn.commit()
            cur.close()
            conn.close()
            return "Successfully deleted"
        except Exception as e:
            conn.rollback()
            return e

    #@staticmethod
    def update_qualifying(self,data):
        sql = "UPDATE f22_databases.qualify set raceId = %s, driverId = %s,constructorId = %s,number = %s,position = %s,q1 = %s,q2 = %s,q3 = %s where qualifyId = %s ;"
        conn = self._get_connection()
        cur = conn.cursor()
        try:
            conn.begin()
            res = cur.execute(sql, (data['raceId'],data['driverId'],data['constructorId'],data['number'],data['position'],data['q1'],data['q2'],data['q3'],data['qualifyId']))
            conn.commit()
            cur.close()
            conn.close()
            return "successfully update"
        except Exception as e:
            conn.rollback()
            return e
