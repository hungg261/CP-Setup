from src.parser import OJ, CONFIG
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
    
    parser.add_argument(
        "-t", "--target",
        default="default",
        help="File extension (default: cpp)"
    )

    return parser.parse_args()

def Generate(args):
    oj = OJ(args.username)
    oj.init(args.link)
    
    formatter = {
        "username": oj.oj.username,
        "link": oj.oj.link,
        "id": oj.oj.id
    }

    with open(f"src/templates/{args.target}.txt", "r") as file:
        template = file.read()
        
    # format {}
    placeholders = ["username", "link", "id"]
    for key in placeholders:
        template = template.replace(f"{{{key}}}", f"__PLACEHOLDER_{key}__")

    template = template.replace("{", "{{").replace("}", "}}")

    for key in placeholders:
        template = template.replace(f"__PLACEHOLDER_{key}__", f"{{{key}}}")

    # format template
    content = template.format(**formatter)
    content = datetime.now().strftime(content)

    # output
    output_folder = CONFIG["oj"][oj.oj.name.lower()]
    output_file = output_folder + f"/{oj.oj.id}.{args.extension}"
    with open(output_file, "w") as newFile:
        newFile.write(content)

    print(f"Generated {output_file}")
    

if __name__ == "__main__":
    try:
        args = parse_args()
    except SystemExit:
        input("Invalid command, press [ENTER] to exit...")
        

    print("Link:", args.link)
    print("Username:", args.username)
    print("Extension:", args.extension)
    print("Target templates:", args.target)
    
    Generate(args)
    
    input("Press [ENTER] to exit...")