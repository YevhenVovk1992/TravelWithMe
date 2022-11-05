from pymongo import MongoClient

from utils.GetEnviromentVariable import get_environment_variables


class MongoConnect:
    env = get_environment_variables()
    __CONNECTION_STRING = env('MONGO_CONNECTION_STRING')
    __CONNECTION_DB = 'TravelWithMe_DB'

    def __init__(self):
        self.__database = MongoConnect.__CONNECTION_DB
        self.__str_connect = MongoConnect.__CONNECTION_STRING
        self.client = None

    def __enter__(self):
        self.client = MongoClient(self.__str_connect)
        database = self.client[self.__database]
        return database

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.client.close()



if __name__ == "__main__":

    with MongoConnect() as db:
        data = {'pending_users': [6, 9], 'approved_users': [3]}
        collection = db['event_users']
        data_id = collection.insert_one(data).inserted_id
        print(data_id)


