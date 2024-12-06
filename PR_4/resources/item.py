from flask import Blueprint, request
from schemas import ItemSchema
from models.item import ItemModel
from db import db

item_blueprint = Blueprint("item", __name__)
item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


@item_blueprint.route('/', methods=['POST'])
def create_item():
    item_data = request.get_json()
    item = item_schema.load(item_data)
    new_item = ItemModel(**item)

    try:
        db.session.add(new_item)
        db.session.commit()
    except Exception as e:
        return {"message": f"Error occurred: {str(e)}"}, 500

    return item_schema.dump(new_item), 201


@item_blueprint.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = ItemModel.query.get_or_404(item_id)
    return item_schema.dump(item)


@item_blueprint.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item_data = request.get_json()
    item = ItemModel.query.get_or_404(item_id)

    item.name = item_data.get('name', item.name)
    item.price = item_data.get('price', item.price)
    item.store_id = item_data.get('store_id', item.store_id)

    db.session.commit()
    return item_schema.dump(item)


@item_blueprint.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = ItemModel.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return {"message": "Item deleted successfully"}


@item_blueprint.route('/', methods=['GET'])
def get_all_items():
    items = ItemModel.query.all()
    return item_list_schema.dump(items)
