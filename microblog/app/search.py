from flask import current_app
"""
if not current_app.elasticsearch :
if app.elasticsearch is None, and in that case return without doing anything.
This is so that when the Elasticsearch server isn't configured,
the application continues to run without the search capability and without giving any errors.
This is just as a matter of convenience during development or when running unit tests.
"""
def add_to_index(index, model): # add는 추가와 modified까지 가능하다
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)
    """
    if attempt to add an entry with an existing id, then Elasticsearch  replaces
    the old entry with the new one.
    """

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index = index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
               'from': (page - 1) * per_page, 'size': per_page}) # 'fields' : ['*'] 는 es가 모든 필드를 보도록 지시 함(multi_match)
    ids = [int(hit['_id']) for hit in search['hits']['hits']] # a list of id elements for the search results
    return ids, search['hits']['total']['value'] # id 번호들과, 찾아낸 총 개수

