import re
import json


class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type  # "operator" or "operand"
        self.value = value  # Operand value or operator type
        self.left = left  # Left child Node
        self.right = right  # Right child Node

    def __repr__(self):
        if self.node_type == "operand":
            return f"Operand({self.value})"
        else:
            return f"Operator({self.value}, {self.left}, {self.right})"


def parse_expression(expression):
    tokens = re.split(r"(\s+AND\s+|\s+OR\s+|\s*[\(\)\=><]\s*)", expression)
    tokens = [token.strip() for token in tokens if token.strip()]
    return tokens


def build_ast(tokens):
    def parse_subexpression(tokens):
        if not tokens:
            return None, tokens

        token = tokens.pop(0)
        if token == "(":
            left, tokens = parse_subexpression(tokens)
            op = tokens.pop(0)  # This should be 'AND' or 'OR'
            right, tokens = parse_subexpression(tokens)
            tokens.pop(0)  # Pop the closing ')'
            return Node("operator", op, left, right), tokens
        elif token == ")":
            return None, tokens
        elif token in ("AND", "OR"):
            return None, tokens
        else:
            # Handle operand nodes (expect format: "attribute operator value")
            value = token
            if tokens and tokens[0] in ("=", ">", "<"):
                op = tokens.pop(0)
                if tokens:
                    val = tokens.pop(0)
                    value = f"{value} {op} {val}"
            return Node("operand", value), tokens

    ast, remaining_tokens = parse_subexpression(tokens)
    return ast


def create_rule(rule_string):
    tokens = parse_expression(rule_string)
    ast = build_ast(tokens)
    return ast


def serialize_ast(ast):
    return json.dumps(ast, default=lambda o: o.__dict__)


def deserialize_ast(ast_json):
    def from_dict(d):
        node = Node(d["node_type"], d.get("value"), None, None)
        if "left" in d:
            node.left = from_dict(d["left"])
        if "right" in d:
            node.right = from_dict(d["right"])
        return node

    data = json.loads(ast_json)
    return from_dict(data)


def combine_rules(rule_strings):
    if not rule_strings:
        return None

    asts = [create_rule(rule) for rule in rule_strings]
    combined_ast = asts[0]

    for ast in asts[1:]:
        combined_ast = Node("operator", "OR", combined_ast, ast)

    return combined_ast


def evaluate_node(node, data):
    if node is None:
        return False  # or handle as appropriate

    if node.node_type == "operand":
        # Assuming node.value is in the format: "attribute operator value"
        parts = node.value.split()
        if len(parts) != 3:
            raise ValueError(f"Unexpected operand format: {node.value}")
        attr, op, val = parts
        val = val.strip("'")  # Remove quotes if value is a string
        if op == "=":
            return data.get(attr) == val
        elif op == ">":
            return data.get(attr) > float(val)
        elif op == "<":
            return data.get(attr) < float(val)
    elif node.node_type == "operator":
        left_result = evaluate_node(node.left, data)
        right_result = evaluate_node(node.right, data)
        if node.value == "AND":
            return left_result and right_result
        elif node.value == "OR":
            return left_result or right_result
    return False


def evaluate_rule(ast, data):
    return evaluate_node(ast, data)


def test_rule_engine():
    rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

    ast1 = create_rule(rule1)
    ast2 = create_rule(rule2)

    combined_ast = combine_rules([rule1, rule2])

    test_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
    print(evaluate_rule(ast1, test_data))  # Expected: True
    print(evaluate_rule(combined_ast, test_data))  # Expected: True
