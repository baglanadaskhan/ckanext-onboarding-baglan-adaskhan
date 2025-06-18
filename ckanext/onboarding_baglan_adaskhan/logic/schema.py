import ckan.logic.schema as schema


@schema.validator_args
def dataset_review_schema(not_empty, review_status_flow_validator):
    schema = {
        "id": [not_empty],
        "review_status": [not_empty, review_status_flow_validator],
    }
    return schema
