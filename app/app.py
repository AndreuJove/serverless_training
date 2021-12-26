import json

from boto3 import client
from flask import Flask, jsonify, request, make_response

from .utils import get_timestamp
from .constants import FAVOURITE_COMPANIES_TABLE, FAVOURITE_ORG_ID, ORG_ID


app = Flask(__name__)
client = client("dynamodb", region_name="eu-west-1")


@app.route("/favourite_companies", methods=["GET"])
def get_all_favourite_companies():
    table = client.scan(TableName=FAVOURITE_COMPANIES_TABLE)
    return (json.dumps(table["Items"]), 200, {"Content-Type": "application/json"})


@app.route("/favourite_company/<string:org_id>", methods=["GET"])
def get_company(org_id):
    resp = client.query(
        TableName=FAVOURITE_COMPANIES_TABLE,
        KeyConditions={
            ORG_ID: {
                "ComparisonOperator": "EQ",
                "AttributeValueList": [{"S": org_id}],
            }
        },
    )
    return jsonify(resp["Items"])


@app.route(
    "/favourite_company/delete/<string:org_id>/<string:favourite_org_id>",
    methods=["DELETE"],
)
def delete_company(org_id, favourite_org_id):
    client.batch_write_item(
        RequestItems={
            FAVOURITE_COMPANIES_TABLE: [
                {
                    "DeleteRequest": {
                        "Key": {
                            ORG_ID: {"S": org_id},
                            FAVOURITE_ORG_ID: {"S": favourite_org_id},
                        }
                    }
                }
            ]
        }
    )

    return jsonify(
        {
            "success": f"Deleted company with org_id: {org_id} and favourite_org_id: {favourite_org_id}"
        }
    )


@app.route("/favourite_company/create", methods=["POST"])
def create_user():
    org_id = request.json.get(ORG_ID)
    favourite_org_id = request.json.get(FAVOURITE_ORG_ID)
    if not org_id or not favourite_org_id:
        return jsonify({"error": "Please provide org_id and favourite_org_id"}), 400

    item = {
        ORG_ID: {"S": org_id},
        FAVOURITE_ORG_ID: {"S": favourite_org_id},
        "date": {"S": get_timestamp()},
    }

    _ = client.put_item(TableName=FAVOURITE_COMPANIES_TABLE, Item=item)

    return jsonify(item)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)
