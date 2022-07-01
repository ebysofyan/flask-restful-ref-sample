from marshmallow import Schema, fields


class MovieSchemaValidator(Schema):
    title = fields.String(required=True)
    description = fields.String(required=False, allow_none=True)
    genre_id = fields.String(required=False, allow_none=True)
    year = fields.Integer(required=False)
    image_url = fields.String(required=False, allow_none=True)
    tags = fields.List(cls_or_instance=fields.String(required=False), required=False)
