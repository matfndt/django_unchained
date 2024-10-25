import ast
from dataclasses import field

def parse_model(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read(), filename=file_path)
    
    models = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            model_name = node.name
            fields = {}
            for stmt in node.body:
                if isinstance(stmt, ast.Assign):
                    field_name = stmt.targets[0].id
                    field_type = stmt.value.func.id if isinstance(stmt.value, ast.Call) else None
                    fields[field_name] = field_type
            models[model_name] = fields
    return models


def generate_rust_code(models):
    rust_code = ""
    for model_name, fields in models.items():
        rust_code += f"#[derive(Serialize, Deserialize)]\n"
        rust_code += f"pub struct {model_name} {{\n"
        for field_name, field_type in fields.items():
            rust_type = "String" if field_type == "str" else field_type  # Simplified type conversion
            rust_code += f"    pub {field_name}: {rust_type},\n"
        rust_code += "}\n\n"
    return rust_code