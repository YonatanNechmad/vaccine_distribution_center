import sqlite3
import atexit
import sys
from myDAOs import vaccines
from myDAOs import suppliers
from myDAOs import clinics
from myDAOs import logistics
from myDTOs import Vaccine

if __name__ == '__main__':
    None


class _Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = vaccines(self._conn)
        self.suppliers = suppliers(self._conn)
        self.clinics = clinics(self._conn)
        self.logistics = logistics(self._conn)
        self.summery = [0, 0, 0, 0]
        self.idToNextVaccine = 0

    def close_db(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE vaccines (
        id          INT     PRIMARY KEY,
        date        DATE    NOT NULL,
        supplier    INT     REFERENCES suppliers(id),
        quantity    INT     NOT NULL
        );
            
        CREATE TABLE suppliers (
        id          INT     PRIMARY KEY,
        name        STRING    NOT NULL,
        logistic    INT     REFERENCES logistics(id)
        );
            
        CREATE TABLE clinics (
        id          INT     PRIMARY KEY,
        location    STRING    NOT NULL,
        demand      INT     NOT NULL,
        logistic    INT     REFERENCES logistics(id)
        );
            
        CREATE TABLE logistics (
        id              INT     PRIMARY KEY,
        name            STRING    NOT NULL,
        count_sent      INT     NOT NULL,
        count_received  INT     NOT NULL );
        """)

    def setSum(self, summery, idToNextVaccine):
        self.summery = summery
        self.idToNextVaccine = idToNextVaccine + 1

    def receiveShipment(self, name, amount, date):
        # update logistics receive
        c = self._conn.cursor()
        currLogistic = c.execute("""
            SELECT logistic FROM suppliers Where name = ?
            """, [name]).fetchone()

        logisticCurrNum = c.execute("""
            SELECT count_received FROM logistics Where id = ?
            """, [currLogistic[0]]).fetchone()

        cNum = int(logisticCurrNum[0]) + amount
        self._conn.execute("""
            UPDATE logistics SET count_received = ? WHERE id = ?
            """, [cNum, currLogistic[0]])

        # update vaccines
        supplierNum = c.execute("""
                    SELECT id FROM suppliers Where name = ?
                """, [name]).fetchone()

        self.vaccines.insert(Vaccine(self.idToNextVaccine, date, int(supplierNum[0]), amount))
        self.idToNextVaccine = self.idToNextVaccine + 1

        # write in output
        self.summery[0] = self.summery[0] + amount
        self.summery[2] = self.summery[2] + amount

        receiveWrite = "{},{},{},{}".format(*self.summery)

        with open(sys.argv[3], "a") as output:  # check 'w+'
            output.write(receiveWrite)

    def sendShipment(self, location, amount):
        # DELETE FROM vaccines WHERE quantity=0

        # decrease demand in clinic
        c = self._conn.cursor()
        _clinic = c.execute("""
                    SELECT * FROM clinics Where location= ?
                """, [location]).fetchone()

        demClinic = int(_clinic[2]) - amount

        self._conn.execute("""
                    UPDATE clinics SET demand = ? WHERE id = ?
                """, [demClinic, _clinic[0]])

        # update the logistic of location

        currLogistic = c.execute("""
                    SELECT logistic FROM clinics Where location = ?
                    """, [location]).fetchone()

        numToLog = c.execute("""
                SELECT count_sent FROM logistics Where id = ?
                """, [currLogistic[0]]).fetchone()

        thisCurr = int(numToLog[0]) + amount

        self._conn.execute("""
                UPDATE logistics SET count_sent = ? WHERE id = ?
                """, [thisCurr, currLogistic[0]])

        # decrease inventory of vaccine

        rememberAmount = amount

        while amount > 0:
            vList = c.execute("""
                        SELECT * FROM vaccines ORDER BY date LIMIT 1
                        """).fetchone()
            if amount >= vList[3]:
                amount = amount - int(vList[3])
                self._conn.execute("""
                        DELETE FROM vaccines WHERE id =?
                """, [vList[0]])
            else:
                currNum = int(vList[3]) - amount
                self._conn.execute("""
                            UPDATE  vaccines SET quantity = ? WHERE id =?
                            """, [currNum, vList[0]])
                amount = 0

        self.summery[0] = self.summery[0] - rememberAmount
        self.summery[1] = self.summery[1] - rememberAmount
        self.summery[3] = self.summery[3] + rememberAmount

        receiveWrite = "{},{},{},{}".format(*self.summery)

        with open(sys.argv[3], "a") as output:  # check 'w+'
            output.write(receiveWrite)


repo = _Repository()
atexit.register(repo.close_db)
