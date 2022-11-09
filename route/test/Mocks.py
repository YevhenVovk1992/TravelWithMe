class UserMock:
    """
        Mock for the user. Using in access check
    """
    def has_perm(self, *args, **kwargs):
        return True


class InsertedIdMock:
    """
        Mock method in the CollectionMock
    """
    def inserted_id(self):
        return 'ID from MongoMock'


class CollectionMock:
    """
        Mock method in the MongoMock
    """
    def insert_one(self, *args, **kwargs):
        return InsertedIdMock()


class MongoMock:
    """
        Mock class for database emulation
    """

    def __init__(self, *args, **kwargs):
        pass

    def close(self):
        pass

    def __getitem__(self, item):
        return {'event_users': CollectionMock()}