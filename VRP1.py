import pandas as pd
import math
from collections import defaultdict
from datetime import datetime as dt
import os
import time

class Locaion():
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.long = longitude

class Order(object):
    def __init__(self, order_id, due_time, lat, long):
        self.delivery_id = order_id
        self.due_time = due_time
        self.location = Locaion(lat, long)

class Store(object):
    def __init__(self, store_id, lat, long):
        self.store_id = store_id
        self.location = Locaion(lat, long)

class VRP(object):
    def __init__(self, stores_data=None, orders_data=None, path=None):
        self.stores = defaultdict(Store)
        self.oreders = defaultdict(Order)
        self.path = path
        self.populte_data(stores_data, orders_data, path)

    def populte_data(self, stores_data, orders_data, path):
        print("Start Reading Stores data".center(50,"-"))
        store_df = pd.read_csv(os.path.join(path,stores_data))
        store_df.apply(self.populate_stores, axis=1)
        print("{} Stores were read.".format(len(stores_data)))
        print("Start Reading Orders data".center(50, "-"))
        oreder_df = pd.read_csv(os.path.join(path, orders_data))
        oreder_df.apply(self.populate_orders, axis=1)
        print("{} Orders were read.".format(len(oreder_df)))


    def solve_VRP(self):
        tic = time.time()
        solution = self.naive_solution(self.stores, self.oreders)
        self.print_the_solution(solution)
        tac = time.time()
        print("The total time sepent for the solution is : {} seconds.".format((tac - tic)*1000))

    def populate_stores(self, row):
        col = row.to_dict()
        st_id = col['store_id']
        lat = col['latitude']
        long = col['longitude']

        if st_id and lat and long:
            store = Store(st_id, lat, long)
            self.stores[st_id] = store
        return True

    def populate_orders(self, row):
        col = row.to_dict()
        del_id = col['delivery_id']
        due_date = dt.strptime(col['due_at'], '%Y-%m-%d %H:%M:%S')
        lat = col['latitude']
        long = col['longitude']

        if del_id and due_date and lat and long:
            order = Order(del_id, due_date, lat, long)
            self.oreders[del_id] = order
        return True

    @staticmethod
    def travel_time(point1, point2):
        return math.sqrt((point1.lat - point2.lat) ^ 2 + (point1.long - point2) ^ 2) * 5

    @staticmethod
    def naive_solution(orders, solutions):
        pass

    @staticmethod
    def print_the_solution(solutio):
        pass

if __name__ == '__main__':
    vrp = VRP("stores_data.csv", "deliveries_data.csv", "./")
    vrp.solve_VRP()
