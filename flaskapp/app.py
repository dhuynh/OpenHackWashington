from flask import Flask, make_response, jsonify, request, render_template
app = Flask(__name__, template_folder="static")
from json import dumps
from jinja2 import Environment, PackageLoader, select_autoescape
import jinja2
import os
from classes import QueryBuilder, ConfigManager
from pprint import pprint
config_path = "configs"
template_loader = jinja2.FileSystemLoader("static")
template_env = Environment(loader=template_loader)
template = template_env.get_template("index.html")
import json

baseurl = "https://duyssearch.search.windows.net/"
with open(os.path.join(config_path, "index_config.json"), "r") as index:
    index_config = json.load(index)
@app.route('/query')
def query():
    try:
        search = request.args.get("search")
    except AttributeError:
        response = simple_response(400, {"message": "include 'search' in params"})
        return response

    try:
        qtype = request.args.get("querytype")
        if qtype not in ["full", "simple", None]:
            return simple_response(400, {"message": "query type is either full or simple"})
    except AttributeError:
        qtype = None

    try:
        sortby = request.args.get("sortby")
        acceptable = [c["name"] for c in index_config["fields"]]
        acceptable.append(None)
        if sortby not in acceptable:
            return simple_response(400, {"message": "wrong query params. Acceptable sortby: %s" % ", ".join(
                [c["name"] for c in index_config["fields"]])})
    except AttributeError:
        sortby = None



    qb = QueryBuilder()
    df = qb.hitsearch(search, sortby, qtype)


    return render_template(template_name_or_list="index.html",
                           tables=[df.to_html(classes='table table-hover', header="true")],
                           titles=df.columns.values, num_hits=str(df.shape[0]))
    # return simple_response(200, hits)


def simple_response(status, content):
    pprint(content)
    return make_response(jsonify(content), status)

if __name__ == '__main__':
    app.run()

