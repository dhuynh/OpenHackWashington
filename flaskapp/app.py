from flask import Flask, make_response
app = Flask(__name__)
from classes import QueryBuilder

@app.route('/query')
def query(query):
    try:
        search = query.args.get("search")
    except AttributeError:
        return make_response()
    try:
        qtype = query.args.get("queryType")
    except AttributeError:
        qtype = None
    if qtype is None:
        qb = QueryBuilder(query, qtype)
    else:
        qb = QueryBuilder(query)

if __name__ == '__main__':
    app.run()

