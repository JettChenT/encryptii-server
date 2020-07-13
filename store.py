import pymongo

# import datetime
class Store(object):
    """
        Store message in mongodb server
    """

    def __init__(self, url, user=0, pw=0):
        if user == 0 and pw == 0:
            self.client = pymongo.MongoClient(url)
        else:
            self.client = pymongo.MongoClient(url.format(us=user, password=pw))
        self.db = self.client.main
        self.collection = self.db.msgs

    def add(self, msg: dict):
        self.collection.insert_one(msg)

    def find(self, exp: dict)->dict:
        doc = self.collection.find_one(exp)
        return doc

    def desFind(self, exp: dict)->dict:
        doc = self.collection.find_one_and_delete(exp)
        return doc
