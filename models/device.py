class DeviceModel:
    def __init__(self, mongo):
        self.mongo = mongo

    def get_device_by_id(self, device_id):
        return self.mongo.db.laptops.find_one({'_id': device_id})

    def get_all_devices(self):
        return self.mongo.db.laptops.find()

    def add_device(self, data):
        return self.mongo.db.laptops.insert_one(data).inserted_id

    def update_device(self, device_id, data):
        return self.mongo.db.laptops.update_one({'_id': device_id}, {'$set': data})

    def delete_device(self, device_id):
        return self.mongo.db.laptops.delete_one({'_id': device_id})