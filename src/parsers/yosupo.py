import re

class Yosupo:
    name = "Yosupo"

    def __init__(self, username: str = None):
        self.username = username
        self.id = None
        self.link = None

    def __repr__(self):
        return f"{self.username} {self.id} {self.link}"

    def parse(self, link: str):
        if link.endswith("/"):
            link = link[:-1]

        pattern = r"judge\.yosupo\.jp/problem/(?P<pid>[a-z0-9_]+)"

        match = re.search(pattern, link)
        if not match:
            return False

        self.id = match.group("pid")
        self.link = link
        return True


if __name__ == "__main__":
    user = Yosupo("hungg261")
    user.parse("https://judge.yosupo.jp/problem/aho_corasick")
    print(user)
