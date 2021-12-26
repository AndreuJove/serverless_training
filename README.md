# Serverless Framework Python Flask API service backed by DynamoDB on AWS

Python Flask API service, backed by DynamoDB, running on AWS Lambda using the traditional Serverless Framework.

## Endpoints requested:

- ##### `GET /favourite_company/<org_id>`

  List all items with the `org_id` provided.

- ##### `POST /favourite_company/create`
  Method to create an item in the database.

Example:

```bash
curl -H "Content-Type: application/json" -u username:apikey -X POST https://woo6lrrukc.execute-api.eu-west-1.amazonaws.com/api/favourite_company/create -d '{"org_id": "amazon", "favourite_org_id": "facebook"}'

```

## Extra endpoints:

- ##### GET `/favourite_companies`

  List all items of the table.

- ##### DELETE `/favourite_company/delete/<org_id>/<favourite_org_id>`
  Delete the item of the database with the `org_id` and the `favourite_org_id` provided.

### Development

```bash
sls wsgi serve
```

### Deploy:

```bash
sls deploy
```

### Configuration AWS credentials for serverless framework:

```bash
serverless config credentials --provider aws --key {key} --secret {secret}
```

Check the credentials:

```
cat ~/.aws/credentials
```

### Serverless plugins used:

To install them:

```bash
serverless plugin install -n serverless-python-requirements
```

```bash
serverless plugin install -n serverless-wsgi
```

```bash
serverless plugin install -n serverless-basic-authentication
```
