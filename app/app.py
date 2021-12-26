import os
import json
import boto3
from boto3.dynamodb.conditions import Key

from flask import Flask, jsonify, request, make_response

from .utils import get_timestamp

app = Flask(__name__)

FAVOURITE_COMPANIES_TABLE = os.environ["FAVOURITE_COMPANIES_TABLE"]
client = boto3.client("dynamodb", region_name="eu-west-1")


def get_item_by_id(id):
    resp = client.get_item(
        TableName=FAVOURITE_COMPANIES_TABLE, Key={"org_id": {"S": id}}
    )
    return resp.get("Item")


def query_attribute_table(key_conditions) -> list:
    resp = client.query(
        TableName=FAVOURITE_COMPANIES_TABLE,
        KeyConditionExpression=Key("favourite_org_id").eq(key_conditions),
    )
    return resp["Items"]


@app.route("/")
def hello():
    print(FAVOURITE_COMPANIES_TABLE)

    return {"Hello World!": FAVOURITE_COMPANIES_TABLE}


@app.route("/favourite_companies")
def get_users():

    table = client.scan(TableName=FAVOURITE_COMPANIES_TABLE)
    # if not request.args:
    return (json.dumps(table["Items"]), 200, {"Content-Type": "application/json"})

    # favourite_org_id = request.args.get("favourite_org_id")
    # if favourite_org_id:
    #     resp = client.query(
    #         TableName=FAVOURITE_COMPANIES_TABLE,
    #         KeyConditionExpression=Key("favourite_org_id").eq(favourite_org_id),
    #     )
    #     items = query_attribute_table(favourite_org_id)
    #     return jsonify(resp["Items"])

    # org_id_recieved = request.args.get("org_id")
    # if org_id_recieved:
    #     items = query_attribute_table(
    #         {
    #             "org_id": {
    #                 "ComparisonOperator": "EQ",
    #                 "AttributeValueList": [{"S": org_id_recieved}],
    #             }
    #         }
    #     )
    #     return jsonify(items)


""" SINGLE ITEM METHODS"""


@app.route("/favourite_company/get/<string:org_id>")
def get_user(org_id):

    item = get_item_by_id(org_id)
    if not item:
        return jsonify({"error": "User does not exist"}), 404

    return jsonify(item)


@app.route("/favourite_company/delete/<string:org_id>", methods=["DELETE"])
def delete_user(org_id):
    item = get_item_by_id(org_id)
    if not item:
        return jsonify({"error": "User does not exist"}), 404

    client.delete_item(
        TableName=FAVOURITE_COMPANIES_TABLE, Key={"org_id": {"S": org_id}}
    )
    return jsonify({"success": f"Deleted item: {item}"})


@app.route("/favourite_company/create", methods=["POST"])
def create_user():
    org_id = request.json.get("org_id")
    favourite_org_id = request.json.get("favourite_org_id")
    if not org_id or not favourite_org_id:
        return jsonify({"error": "Please provide org_id and favourite_org_id"}), 400

    item = {
        "org_id": {"S": org_id},
        "favourite_org_id": {"S": favourite_org_id},
        "date": {"S": get_timestamp()},
    }

    resp = client.put_item(TableName=FAVOURITE_COMPANIES_TABLE, Item=item)

    return jsonify(item)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)
