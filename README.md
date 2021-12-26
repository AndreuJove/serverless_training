# Serverless Framework Python Flask API service backed by DynamoDB on AWS

This template demonstrates how to develop and deploy a simple Python Flask API service, backed by DynamoDB, running on AWS Lambda using the traditional Serverless Framework.

### Prerequisites

In order to package your dependencies locally with `serverless-python-requirements`, you need to have `Python3.8` installed locally. You can create and activate a dedicated virtual environment with the following command:

```bash
python3.8 -m venv ./venv
source ./venv/bin/activate
```

### Endpoints requested

- `GET /favourite_company/<org_id>`
  List all items with the `org_id` provided

- `POST /favourite_company/create`
  Method to create an item in the database

### Extra endpoints

- `GET /favourite_companies`
  List all items of the table.

- `DELETE /favourite_company/delete/<org_id>/<favourite_org_id>`
  Delete the item of the database with the `org_id` and the `favourite_org_id` provided.
