from parser import OJ
import argparse
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser()

    # positional argument
    parser.add_argument(
        "link",
        help="Codeforces problem link"
    )

    # optional arguments
    parser.add_argument(
        "-u", "--username",
        default=None,
        help="Optional username"
    )

    parser.add_argument(
        "-e", "--extension",
        default="cpp",
        help="File extension (default: cpp)"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    print("Link:", args.link)
    print("Username:", args.username)
    print("Extension:", args.extension)
    
    oj = OJ(args.username)
    oj.init(args.link)
    
    formatter = {
        "username": oj.oj.username,
        "link": oj.oj.link,
        "id": oj.oj.id
    }

    with open("src/templates/setup1.txt", "r") as file:
        template = file.read()
        
    placeholders = ["username", "link", "id"]
    for key in placeholders:
        template = template.replace(f"{{{key}}}", f"__PLACEHOLDER_{key}__")

    template = template.replace("{", "{{").replace("}", "}}")

    for key in placeholders:
        template = template.replace(f"__PLACEHOLDER_{key}__", f"{{{key}}}")

    content = template.format(**formatter)
    content = datetime.now().strftime(content)

    output_file = f"src/{oj.oj.id}.{args.extension}"
    with open(output_file, "w") as newFile:
        newFile.write(content)

    print(f"Generated {output_file}")