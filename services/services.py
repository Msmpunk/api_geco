# Import the necessary modules
from bson.json_util import dumps
from models.device import DeviceModel
from schemas.schemas import DeviceSchema

# Function to retrieve an item by its ID
def get_item(mongo, item_id):
    # Create a DeviceModel instance
    device_model = DeviceModel(mongo)
    # Retrieve the item from the database using the DeviceModel
    item = device_model.get_device_by_id(item_id)
    return item

# Function to retrieve all items
def get_all_items(mongo):
    # Create a DeviceModel instance
    device_model = DeviceModel(mongo)
    # Retrieve all devices from the database using the DeviceModel
    laptops = device_model.get_all_devices()
    # Convert the result to JSON format
    return dumps(laptops)

# Function to add a new item
def add_item(mongo, data):
    # Create a DeviceModel instance
    device_model = DeviceModel(mongo)
    # Add the new item to the database using the DeviceModel
    new_item_id = device_model.add_device(data)
    # Retrieve the newly added item from the database using the DeviceModel
    new_item = device_model.get_device_by_id(new_item_id)
    # Convert the '_id' field to a string for JSON serialization
    new_item['_id'] = str(new_item['_id'])
    return new_item

# Function to update an existing item
def update_item(mongo, item_id, data):
    # Create a DeviceModel instance
    device_model = DeviceModel(mongo)
    # Update the item in the database using the DeviceModel
    device_model.update_device(item_id, data)
    # Retrieve the updated item from the database
    updated_item = device_model.get_device_by_id(item_id)
    return updated_item

# Function to delete an item
def delete_item(mongo, item_id):
    # Create a DeviceModel instance
    device_model = DeviceModel(mongo)
    # Delete the item from the database using the DeviceModel
    device_model.delete_device(item_id)
