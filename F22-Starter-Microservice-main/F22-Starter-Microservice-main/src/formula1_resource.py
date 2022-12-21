import pymysql
import os
import json

class Formula1Resource():

    def __int__(self):
        pass


    def _get_connection(self):

        # usr = os.environ.get('DBUSER')
        # pw = os.environ.get('DBPW')
        # h = os.environ.get('DBHOST')

        usr = "admin"
        pw = "dbuserdbuser"
        h = "circuits.cdlehdu4ibgc.us-east-1.rds.amazonaws.com"

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    def get_by_key(self, key):

        sql = "SELECT name, location, country FROM microservice1.circuits where `circuitRef`=%s";
        conn = self._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        if res == 1:
            result = cur.fetchone()
        else:
            result = "Nothing found"

        return result

    def create_by_template(self, new_resource):
        print(new_resource['circuitRef'])
        if self.get_by_key(new_resource['circuitRef'])!="Nothing found":
            return ("already exist")
        sql = "insert into microservice1.circuits(circuitId, circuitRef, name, location, country, lat, lng, alt, url) values ((SELECT MAX(circuitID) FROM microservice1.circuits c)+1,"
        for k, v in new_resource.items():
            sql += '"' + str(v) + '", '
        sql = sql[0:-2]
        sql += ')'
        print(sql)
        conn = self._get_connection()
        cursor = conn.cursor()
        res = cursor.execute(sql)

        if res != 0:
            result = new_resource['circuitRef']
        else:
            result = 0

        return result

    def update_by_key(self, ref, new_resource):
        sql = "update microservice1.circuits set name=%s, location=%s, country=%s, lat=%s, lng=%s, alt=%s, url=%s where circuitRef=%s"
        conn = self._get_connection()
        cursor = conn.cursor()
        res = cursor.execute(sql, (new_resource['name'],
                                   new_resource['location'],
                                   new_resource['country'],
                                   new_resource['lat'],
                                   new_resource['lng'],
                                   new_resource['alt'],
                                   new_resource['url'],
                                   ref
                                   ))
        if res != 0:
            result = 'Succeed'
        else:
            result = "Noooooo"

        return result

    def delete_by_ref(self, ref):
        sql = "delete from microservice1.circuits where circuitRef=%s"
        conn = self._get_connection()
        cursor = conn.cursor()
        res = cursor.execute(sql, args=ref)

        if res != 0:
            result = 1
        else:
            result = 0

        return result

    def get_by_template(self, q, limit=None, offset=None):
        # print(q['field'], q['val'], q['limit'], q['offset'])
        sql = "SELECT circuitRef, name, location, country FROM microservice1.circuits where "+ q['field'] + " = %s limit " + limit+ " offset " + offset
        # sql2 = "select * from microservice1.circuits where country='China' limit 2 offset 0"
        conn = self._get_connection()
        cursor = conn.cursor()
        s = cursor.mogrify(sql, (q['val']))
        print(s)
        res = cursor.execute(sql, (q['val']))
        # r = {'data':[], 'links':[]}
        # r['links'] = {'prev':[], 'cur':[], 'next':[]}
        if res >0:
            result = cursor.fetchall()

        else:
            result = "Nothing found"
        # r['data'] = result

        return result



if __name__ == "__main__":
    svc = Formula1Resource()
    q = {
        "field": "country",
        "val": "China",
    }

    q2 = {
        "name": "nyy2",
        "location": "Shanghai",
        "country": "China",
        "lat": 0,
        "lng": 0,
        "alt": 0,
        "url": "qwerty"
    }
    res = svc.get_by_template(q, limit='1', offset='1')
    print(json.dumps(res, default=str))