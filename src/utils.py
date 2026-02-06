from pathlib import Path
import subprocess
import os

def open_and_highlight(filepath):
    abs_path = os.path.abspath(filepath)
    command = f'explorer /select,"{abs_path}"'
    
    try:
        subprocess.run(command, shell=True)
    except FileNotFoundError:
        print("Error: Windows Explorer not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

import subprocess
from pathlib import Path

def clean(path):
    preview = subprocess.run(
        ["git", "clean", "-fdn"],
        cwd=path,
        capture_output=True,
        text=True,
        check=True
    )

    lines = preview.stdout.strip().splitlines()
    if not lines:
        print("Nothing to clean.")
        return

    flagged = False

    for line in lines:
        file_path = line.replace("Would remove ", "").strip()
        suffix = Path(file_path).suffix

        if suffix not in {".exe", ".o"}:
            print(f"[*] {line} (***)")
            flagged = True
        else:
            print(line)

    if flagged:
        print("\n(***) = not .exe or .o files!")

    ans = input("\nDelete these files? (y/n): ")
    if ans.lower() != "y":
        print("Aborted.")
        return

    subprocess.run(
        ["git", "clean", "-fd"],
        cwd=path,
        check=True
    )

def commit_each(path):
    path = Path(path).resolve()

    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=path,
        capture_output=True,
        text=True,
        check=True
    )
    
    subprocess.run(["git", "restore", "--staged", "."], cwd=path, check=True)
    
    files = []
    for line in result.stdout.splitlines():
        file_path = line.split(maxsplit=1)[1]
        file_path = Path(file_path).name
        
        if file_path.endswith((".cpp", ".py")):
            files.append(file_path)

    if not files:
        print("No .cpp or .py changes to commit.")
        return

    committed = False
    
    print(f"Found {len(files)} changed .cpp/.py files:")
    for file in files:
        print(f"[*] {file}")
    print()
        
    isProceed = input("Proceed to commit each separately? (y/n): ")
    if isProceed.lower() != "y":
        print("Aborted committing files.")
        return

    for file in files:
        subprocess.run(["git", "add", file], cwd=path, check=True)

        commit = subprocess.run(
            ["git", "commit", "-m", f"Auto commit"],
            cwd=path
        )

        if commit.returncode == 0:
            committed = True

    if committed:
        subprocess.run(["git", "push"], cwd=path, check=True)