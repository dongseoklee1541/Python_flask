from flask import current_app
"""
if not current_app.elasticsearch :
if app.elasticsearch is None, and in that case return without doing anything.
This is so that when the Elasticsearch server isn't configured,
the application continues to run without the search capability and without giving any errors.
This is just as a matter of convenience during development or when running unit tests.
"""
def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    serach = current_app.elasticsearch.search(
        index = index,
        body = {'query': {'multi_match': {'query': query, 'fields': ['*']}},
               'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
