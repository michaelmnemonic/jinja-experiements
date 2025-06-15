from jinja2 import Environment, PackageLoader, select_autoescape
import yaml

def load_list_of_functions(file_path):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            list_of_functions = data["functions"]
            return list_of_functions
        except yaml.YAMLError as exc:
            print(exc)

def main():
    env = Environment(
        loader=PackageLoader("generate-yaml"),
        autoescape=select_autoescape()
    )

    # read list of functions
    list_of_functions = load_list_of_functions("data/functions.yaml")

    # construct example deployment
    example_deployment = {
        "name": "Example deployment",
        "description": "This is an example deployment to test jinja templates",
        "functions": ["read_input_data", "validate_raw_input"]}

    # in and outputs are the combined in and outputs of functions
    input = {}
    for thisFunction in example_deployment["functions"]:
        input.update(list_of_functions[thisFunction]["input"])

    example_deployment.update({"input": input})
    
    template = env.get_template("deployment.yaml.j2")
    print(template.render(example_deployment))

if __name__ == "__main__":
    main()
