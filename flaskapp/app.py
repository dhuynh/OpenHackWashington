from flask import Flask, make_response, jsonify, request, render_template
app = Flask(__name__, template_folder="static")
from json import dumps
from jinja2 import Environment, PackageLoader, select_autoescape
import jinja2
from classes import QueryBuilder, ConfigManager
from pprint import pprint
config_path = "configs"
template_loader = jinja2.FileSystemLoader("static")
template_env = Environment(loader=template_loader)
template = template_env.get_template("index.html")

baseurl = "https://duyssearch.search.windows.net/"

@app.route('/query')
def query():
    try:
        search = request.args.get("search")
    except AttributeError:
        response = simple_response(400, {"message": "include 'search' in params"})
        return response

    try:
        qtype = request.args.get("queryType")
    except AttributeError:
        qtype = None

    try:
        sortby = request.args.get("sortBy")
    except AttributeError:
        sortby = None

    if qtype is None:
        qb = QueryBuilder(qtype)
    else:
        qb = QueryBuilder()

    hits = qb.hitsearch(search, sortby, qtype)
    return render_template(template_name_or_list="index.html", hits=hits)
    # return simple_response(200, hits)

@app.route("/configs/<config_name>", methods=["POST", "DELETE", "EDIT"])
def manage_config(config_name):
    cm = ConfigManager(config_path=config_path)
    url=""
    if config_name == "indexer":
        url = baseurl + "indexers/myindexer"

    if request.method == "POST":
        cm.post_config(url=url)
    elif request.method == "DELETE":
        cm.delete_config(url=url)

def simple_response(status, content):
    pprint(content)
    return make_response(jsonify(content), status)

if __name__ == '__main__':
    app.run()

