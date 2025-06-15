from jinja2 import Environment, PackageLoader, select_autoescape

def main():
    env = Environment(
        loader=PackageLoader("generate-yaml"),
        autoescape=select_autoescape()
    )


if __name__ == "__main__":
    main()
