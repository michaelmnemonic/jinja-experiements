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
    # Load Template
    env = Environment(
        loader=PackageLoader("generate-yaml"),
        autoescape=select_autoescape(),
        lstrip_blocks = True,
        trim_blocks= True
    )

    # read list of functions
    list_of_functions = load_list_of_functions("data/functions.yaml")

    # construct example deployment
    example_deployment = {
        "name": "Example deployment",
        "description": "This is an example deployment to test Jinja templates. This description is intentionally very long to test breaking of text into several lines. It includes various details and explanations to ensure that the template handles longer text blocks effectively. By adding more content, we can see how the text wraps and whether it maintains readability and structure. This process is crucial for understanding how templates manage and display extensive information without losing format or clarity. Additionally, it helps in identifying any potential issues with text overflow or alignment in the rendered output.",
        "functions": ["read_input_data", "validate_raw_input"]}

    # in and outputs are the combined in and outputs of all functions
    input = {}
    output = {}
    for thisFunction in example_deployment["functions"]:
        input.update(list_of_functions[thisFunction]["input"])
        output.update(list_of_functions[thisFunction]["output"])

    # ...except if in- and output are the same, these are assumed to be internal and therefore removed from the deployment
    interfaces_to_remove = []
    for thisInput in input:
        if thisInput in output:
            interfaces_to_remove.append(thisInput)
    for this_interface_to_remove in interfaces_to_remove:
        input.pop(this_interface_to_remove)
        output.pop(this_interface_to_remove)

    # Assign in- and outputs
    example_deployment.update({"input": input})
    example_deployment.update({"output": output})
    
    # Render template and write to file
    template = env.get_template("deployment.yaml.j2")
    with open(example_deployment["name"].lower().replace(" ", "_") + ".yaml", "w") as file:
        file.write(template.render(example_deployment))

if __name__ == "__main__":
    main()
