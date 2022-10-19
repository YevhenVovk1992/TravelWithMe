from pymongo import MongoClient

from utils.GetEnviromentVariable import get_environment_variables


env = get_environment_variables()
CONNECTION_STRING = env('MONGO_CONNECTION_STRING')


class MongoConnect:

    def __init__(self, str_connect, database):
        self.str_connect = str_connect
        self.database = database
        self.client = None

    def __enter__(self):
        self.client = MongoClient(self.str_connect)
        database = self.client[self.database]
        return database

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.client.close()


if __name__ == "__main__":

    with MongoConnect(CONNECTION_STRING, 'test') as db:
        data = {'pending_users': [6, 9], 'approved_users': [3]}
        collection = db['event_users']
        data_id = collection.insert_one(data).inserted_id
        print(data_id)


