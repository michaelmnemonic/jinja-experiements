from jinja2 import Environment, PackageLoader, select_autoescape
import yaml

def main():
    env = Environment(
        loader=PackageLoader("generate-yaml"),
        autoescape=select_autoescape()
    )

    # construct example deployment
    example_deployment = {
        "name": "Example deployment",
        "description": "This is an example deployment to test jinja templates",
        "functions": ["read_input_data", "validate_raw_input"]}

    template = env.get_template("deployment.yaml.j2")
    print(template.render(example_deployment))

if __name__ == "__main__":
    main()
