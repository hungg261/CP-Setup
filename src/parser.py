import json
from parsers import codeforces, cses, marisaoj, vnoj

def load_config(path = "src/config.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{path} not found")
    except json.JSONDecodeError:
        print(f"{path} is not valid JSON")
    return None
    
CONFIG = load_config("src/config.json")

def getOJ(link: str):
    link = link.lower()
    table: dict = CONFIG["oj_patterns"]
    
    for oj, patterns in table.items():
        for pattern in patterns:
            if pattern in link:
                return oj
    
    return None

class OJ:
    def __init__(self, username: str = None):
        self.username = username
        self.oj = None
        
    def init(self, link: str):
        if link.endswith("/"):
            link = link[:-1]
        
        oj_name = getOJ(link)
        if oj_name is None:
            return
        
        match oj_name:
            case "codeforces":
                self.oj = codeforces.Codeforces()
            case "cses":
                self.oj = cses.CSES()
            case "marisaoj":
                self.oj = marisaoj.MarisaOJ()
            case "vnoj":
                self.oj = vnoj.VNOJ()
            case _:
                return
        
        self.username = CONFIG["username"][oj_name]
        self.oj.username = self.username
        
        self.oj.parse(link)
    
if __name__ == "__main__":
    user = OJ(None)
    user.init("https://codeforces.com/gym/106289/problem/A")
    user.init("https://cses.fi/problemset/task/2190/")
    repr(user.oj)