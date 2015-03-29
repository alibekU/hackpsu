import pymongo
import logging

class Database:
    logging.basicConfig(filename='web.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    
    def __init__(self, dbName):
        self._dbName = dbName
        self._connection = None

        try:
            self._connection = pymongo.MongoClient('localhost',27017)
        except (pymongo.errors.OperationFailure, pymongo.errors.ConnectionFailure), e:
            logging.error('Problem with db connection: %s' % e)
    
    def getPeople(self):
        try:
            return self._connection[self._dbName]['people'].find()
        except pymongo.errors.OperationFailure, e:
            logging.error('Database getPeople operation failed: %s' % e)

    def addPerson(self, data):
        try:
            collection = self._connection[self._dbName]['people']
            new_person = {}

            for key,value in data.items():
                new_person[key] = value
            collection.update()

