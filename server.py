from flask import Flask, request, jsonify
from flask_cors import CORS
from zeotap import (
    create_rule,
    combine_rules,
    evaluate_rule,
    serialize_ast,
    deserialize_ast,
)
import json
app = Flask(__name__)

app = Flask(__name__)
CORS(app)

@app.route("/create_rule", methods=["POST"])
def create_rule_endpoint():
    data = request.json
    print("jolla")
    rule_string = data.get("rule_string")
    print(rule_string)
    ast = create_rule(rule_string)
    return jsonify({"ast": serialize_ast(ast)})


@app.route("/combine_rules", methods=["POST"])
def combine_rules_endpoint():
    data = request.json
    rule_strings = data.get("rule_strings")
    combined_ast = combine_rules(rule_strings)
    return jsonify({"combined_ast": serialize_ast(combined_ast)})


@app.route("/evaluate_rule", methods=["POST"])
def evaluate_rule_endpoint():
    data = request.json
    ast_json = json.dumps(data.get("ast"))  # Convert dict to JSON string
    user_data = data.get("data")
    print("AST JSON:", ast_json)
    ast = deserialize_ast(ast_json)
    result = evaluate_rule(ast, user_data)
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(port=5000)
