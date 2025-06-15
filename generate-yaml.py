from jinja2 import Environment, PackageLoader, select_autoescape
import yaml

# Function to load a list of functions from a YAML file
def load_list_of_functions(file_path):
    with open(file_path, 'r') as file:
        try:
            # Parse the YAML file and extract the list of functions
            data = yaml.safe_load(file)
            list_of_functions = data["functions"]
            return list_of_functions
        except yaml.YAMLError as exc:
            # Print any errors encountered during parsing
            print(exc)

def main():
    # Set up the Jinja2 environment for template rendering
    env = Environment(
        loader=PackageLoader("generate-yaml"),
        autoescape=select_autoescape(),
        lstrip_blocks = True,
        trim_blocks= True
    )

    # Load the list of functions from the YAML file
    list_of_functions = load_list_of_functions("data/functions.yaml")

    # Construct an example deployment with a detailed description
    example_deployment = {
        "name": "Example deployment",
        "description": "This is an example deployment to test Jinja templates. This description is intentionally very long to test breaking of text into several lines. It includes various details and explanations to ensure that the template handles longer text blocks effectively. By adding more content, we can see how the text wraps and whether it maintains readability and structure. This process is crucial for understanding how templates manage and display extensive information without losing format or clarity. Additionally, it helps in identifying any potential issues with text overflow or alignment in the rendered output.",
        "functions": ["read_input_data", "validate_raw_input"]  # List of functions to be included in the deployment
    }

    # Initialize dictionaries for input and output
    input = {}
    output = {}

    # Combine the inputs and outputs of all specified functions
    for thisFunction in example_deployment["functions"]:
        input.update(list_of_functions[thisFunction]["input"])
        output.update(list_of_functions[thisFunction]["output"])

    # Identify and remove internal interfaces (inputs and outputs that are the same)
    interfaces_to_remove = []
    for thisInput in input:
        if thisInput in output:
            interfaces_to_remove.append(thisInput)
    for this_interface_to_remove in interfaces_to_remove:
        input.pop(this_interface_to_remove)
        output.pop(this_interface_to_remove)

    # Update the example deployment with the finalized inputs and outputs
    example_deployment.update({"input": input})
    example_deployment.update({"output": output})
    
    # Load the Jinja2 template for the deployment YAML
    template = env.get_template("deployment.yaml.j2")

    # Write the rendered template to a YAML file
    with open(example_deployment["name"].lower().replace(" ", "_") + ".yaml", "w") as file:
        file.write(template.render(example_deployment))

if __name__ == "__main__":
    main()
