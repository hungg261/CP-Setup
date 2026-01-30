import re

class SPOJ:
    name = "SPOJ"

    def __init__(self, username: str = None):
        self.username = username
        self.id = None
        self.link = None

    def __repr__(self):
        return f"{self.username} {self.id} {self.link}"

    def parse(self, link: str):
        if link.endswith("/"):
            link = link[:-1]

        pattern = r"spoj\.com/problems/(?P<pid>[A-Z0-9_]+)"

        match = re.search(pattern, link)
        if not match:
            return False

        pid = match.group("pid")
        self.id = f"{pid}"
        self.link = link
        return True


if __name__ == "__main__":
    user = SPOJ("hungg")
    user.parse("https://www.spoj.com/problems/CLFLARR")
    print(user)
