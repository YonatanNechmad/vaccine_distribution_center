
class vaccines:
    # Hold the information on the vaccines currently in the inventory
    def __init__(self, _conn):
        self._conn = _conn

    def insert(self, vaccine):
        # vaccine.date serois take care
        self._conn.execute("""
            INSERT INTO vaccines (id ,date ,supplier ,quantity) VALUES (? ,? ,? ,? )
        """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])


class suppliers:
    # Holds the suppliers data
    def __init__(self, con):
        self._conn = con

    def insert(self, supplier):
        self._conn.execute("""
            INSERT INTO suppliers (id ,name ,logistic ) VALUES (? ,? ,? )
        """, [supplier.id, supplier.name, supplier.logistic])


class clinics:
    # Holds the information on the different clinics.
    def __init__(self, con):
        self._conn = con

    def insert(self, Clinic):
        self._conn.execute("""
            INSERT INTO clinics (id ,location ,demand ,logistic ) VALUES (? ,? ,? ,? )
        """, [Clinic.id, Clinic.location, Clinic.demand, Clinic.logistic])


class logistics:
    # Holds the information on the different delivery services.
    def __init__(self, con):
        self._conn = con

    def insert(self, Logistic):
        self._conn.execute("""
            INSERT INTO logistics (id ,name ,count_sent ,count_received ) VALUES (? ,? ,? ,? )
        """, [Logistic.id, Logistic.name, Logistic.count_sent, Logistic.count_received])

if __name__ == '__main__':
    None