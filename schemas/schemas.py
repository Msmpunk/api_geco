from marshmallow import Schema, fields, validate

# Schema for the technical details of a device
class TechnicalDetailsSchema(Schema):
    processor = fields.Str(required=True)
    ram = fields.Str(required=True)
    storage = fields.Str(required=True)
    operating_system = fields.Str(required=True)  # Correct the field name

# Schema for a device
class DeviceSchema(Schema):
    _id = fields.Int(default=lambda: None)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    marca = fields.Str(required=True)
    modelo = fields.Str(required=True)
    serial_number = fields.Str(required=True)
    state = fields.Str(required=True)
    register_date = fields.DateTime(required=True)
    location = fields.Str(required=True)
    technical_details = fields.Nested(TechnicalDetailsSchema, required=True)
