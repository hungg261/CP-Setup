from src.parser import OJ, CONFIG
from src.utils import clean, open_and_highlight, commit_each

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
    gen_parser = subparsers.add_parser("generate", aliases=["gen"],
                                       help="Generate a new CP file")
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
    open_parser = subparsers.add_parser("open",
                                        help="Open a file or folder")
    open_parser.add_argument(
        "-o", "--open",
        required=False,
        help="Path to file or folder to open"
    )
    
    open_parser.add_argument(
        "-g", "--git",
        required=False,
        help="Path to file or folder to open in Git Bash"
    )
    
    # git
    git_parser = subparsers.add_parser("git",
                                          help="Commit each changed .cpp and .py file separately")
    git_parser.add_argument(
        "-c", "--commit",
        required=False,
        help="Path to the commit target folder"
    )
    
    git_parser.add_argument(
        "-m", "--message",
        required=False,
        help="Commit message"
    )
    
    git_parser.add_argument(
        "-cl", "--clean",
        required=False,
        help="Path to the clean target folder"
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
    output_fname = output_folder + f"/{oj.oj.id}"
    output_file = output_fname + f".{args.extension}"
    
    handlingDupFile = "1"
    if os.path.exists(output_file):
        handlingDupFile = input(f"""\n[!!!] File already exists!\n
1. Replace
2. Create new version
3. Skip
> """).strip()
    
    if handlingDupFile == "1" or handlingDupFile == "2":
        if handlingDupFile == "2":
            fcounter = 2
            output_fname += f"_v{fcounter}"
            output_file = output_fname + f".{args.extension}"
            
            while os.path.exists(output_file):
                output_file = output_file.replace(f"_v{fcounter}", f"_v{fcounter + 1}")
                fcounter += 1
        
        with open(output_file, "w") as newFile:
            newFile.write(content)
        print(f"Generated {output_file}")
                
    isOpened = input("""Choose your opening method\n")
1. Open in Code::Blocks
2. Open in Explorer
3. Don't open
> """)
    if isOpened == "1":
        subprocess.Popen([r"C:\Program Files\CodeBlocks\codeblocks.exe", output_file])
    elif isOpened == "2":
        open_and_highlight(output_file)
    

if __name__ == "__main__":
    try:
        args = parse_args()
    except SystemExit:
        input("Invalid command, press [ENTER] to exit...")
        os._exit(1)
        
    
    if args.command == "open":
        oj_name = args.open or args.git

        if not oj_name:
            print("Error: No OJ specified")
            os._exit(1)

        oj_key = oj_name.lower()

        if oj_key not in CONFIG["oj"]:
            print(f"Error: Unknown OJ '{oj_name}'")
            os.exit(1)

        path = os.path.abspath(CONFIG["oj"][oj_key])

        if args.git:
            subprocess.Popen([
                r"C:\Program Files\Git\git-bash.exe",
                f"--cd={path}"
            ])
        else:
            subprocess.run(
                f'explorer /n,"{path}"',
                shell=True
            )

        os._exit(0)
        
    elif args.command == "git":
        if args.commit is None and args.clean is None:
            print("Error: No commit or clean path specified")
            os._exit(1)
            
        if args.clean is not None:
            oj_key = args.clean.lower()
            if oj_key not in CONFIG["oj"]:
                print(f"Error: Unknown OJ '{args.clean}'")
                os._exit(1)
            
            path = os.path.abspath(CONFIG["oj"][oj_key])
            clean(path)
            os._exit(0)
            
        oj_key = args.commit.lower()
        if oj_key not in CONFIG["oj"]:
            print(f"Error: Unknown OJ '{args.commit}'")
            os._exit(1)
        
        path = os.path.abspath(CONFIG["oj"][oj_key])
        print(path)
        
        if args.message is not None:
            commit_each(path, str(args.message))
        else:
            commit_each(path)
        
    elif args.command in ["generate", "gen"]:
        print("Link:", args.link)
        print("Username:", args.username)
        print("Extension:", args.extension)
        print("Target templates:", args.target)
        
        Generate(args)
    else:
        print("Error: Unknown command")
        os._exit(1)