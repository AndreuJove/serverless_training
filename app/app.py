from boto3 import client
from flask import Flask, jsonify, request, make_response

from .utils import get_timestamp
from .constants import FAVOURITE_COMPANIES_TABLE, FAVOURITE_ORG_ID, ORG_ID


app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
client = client("dynamodb", region_name="eu-west-1")


hey = lambda x: x
print(hey)


@app.route("/favourite_companies", methods=["GET"])
def get_all_favourite_companies():
    table = client.scan(TableName=FAVOURITE_COMPANIES_TABLE)
    return jsonify(table["Items"]), 200, {"Content-Type": "application/json"}


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

    if not resp["Items"]:
        return jsonify({"error": f"There is no company with org_id: {org_id}"}), 400

    return jsonify(resp["Items"])


@app.route(
    "/favourite_company/delete/<string:org_id>/<string:favourite_org_id>",
    methods=["DELETE"],
)
def delete_company(org_id, favourite_org_id):
    resp = client.get_item(
        TableName=FAVOURITE_COMPANIES_TABLE,
        Key={
            ORG_ID: {"S": org_id},
            FAVOURITE_ORG_ID: {"S": favourite_org_id},
        },
    )

    if not resp.get("Item"):
        return (
            jsonify(
                {
                    "error": f"There is no company with org_id: {org_id} and favourite_org_id: {favourite_org_id}."
                }
            ),
            400,
        )

    _ = client.delete_item(
        TableName=FAVOURITE_COMPANIES_TABLE,
        Key={
            ORG_ID: {"S": org_id},
            FAVOURITE_ORG_ID: {"S": favourite_org_id},
        },
    )

    return jsonify(
        {
            "success": f"Deleted company with org_id: {org_id} and favourite_org_id: {favourite_org_id}."
        }
    )


@app.route("/favourite_company/create", methods=["POST"])
def create_user():
    org_id = request.json.get(ORG_ID)
    favourite_org_id = request.json.get(FAVOURITE_ORG_ID)
    if not org_id or not favourite_org_id:
        return (
            jsonify(
                {
                    "error": "Please provide org_id and favourite_org_id in the request body."
                }
            ),
            400,
        )

    item = {
        ORG_ID: {"S": org_id},
        FAVOURITE_ORG_ID: {"S": favourite_org_id},
        "date": {"S": get_timestamp()},
    }

    _ = client.put_item(TableName=FAVOURITE_COMPANIES_TABLE, Item=item)

    return jsonify(
        {
            "success": f"Created company with org_id: {org_id} and favourite_org_id: {favourite_org_id}"
        }
    )


@app.errorhandler(404)
def resource_not_found(_):
    return make_response(jsonify(error_handled="Not found!"), 404)
