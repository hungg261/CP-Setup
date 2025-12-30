from src.parser import OJ, CONFIG

from datetime import datetime
import subprocess
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(
        description="CP Setup tool"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate
    gen_parser = subparsers.add_parser("generate", help="Generate a new CP file")
    gen_parser.add_argument(
        "link",
        help="Codeforces problem link or other OJ link"
    )
    gen_parser.add_argument(
        "-u", "--username",
        default=None,
        help="Optional username"
    )
    gen_parser.add_argument(
        "-e", "--extension",
        default="cpp",
        help="File extension (default: cpp)"
    )
    gen_parser.add_argument(
        "-t", "--target",
        default="default",
        help="Target template (default: default)"
    )

    # open
    open_parser = subparsers.add_parser("open", help="Open a file or folder")
    open_parser.add_argument(
        "-o", "--open",
        required=True,
        help="Path to file or folder to open"
    )

    return parser.parse_args()

def open_and_highlight(filepath):
    abs_path = os.path.abspath(filepath)
    command = f'explorer /select,"{abs_path}"'
    
    try:
        subprocess.run(command, shell=True)
    except FileNotFoundError:
        print("Error: Windows Explorer not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

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

    open_and_highlight(output_file)
    print(f"Generated {output_file}")
    

if __name__ == "__main__":
    try:
        args = parse_args()
    except SystemExit:
        input("Invalid command, press [ENTER] to exit...")
        
    
    if args.command == "open":
        subprocess.run("explorer /n, \"{}\"".format(os.path.abspath(CONFIG["oj"][args.open.lower()])), shell=True)
        os._exit(0)

    print("Link:", args.link)
    print("Username:", args.username)
    print("Extension:", args.extension)
    print("Target templates:", args.target)
    
    Generate(args)
    
    input("Press [ENTER] to exit...")