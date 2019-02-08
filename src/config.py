import sys
import json

class Config:
    def __init__(self):
        pass

    def load_json(self, filename):
        data = {}
        try:
            with open(filename, encoding='utf-8') as file:
                data = json.loads(file.read())
        except:
            print('NOPE! Config failed to read file', filename)
            print(sys.exc_info())
        return data

    def save_json(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)
