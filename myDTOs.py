class Vaccine:
    # Hold the information on the vaccine
    def __init__(self, id, date, supplier, quantity):
        self.id = int(id)
        self.date = date
        self.supplier = int(supplier)
        self.quantity = int(quantity)


class Supplier:
    # Holds the supplier data
    def __init__(self, id, name, logistics):
        self.id = id
        self.name = name
        self.logistic = logistics


class Clinic:
    # Holds the information on the clinic.
    def __init__(self, id, location, demand, logistic):
        self.id = id
        self.location = location
        self.demand = demand
        self.logistic = logistic


class Logistic:
    # Holds the information on the deliver
    def __init__(self, id, name, count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received


if __name__ == '__main__':
    None
