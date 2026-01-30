class AtCoder:
    name = "AtCoder"

    def __init__(self, username: str = None):
        self.username = username
        self.id = None
        self.link = None

    def __repr__(self):
        return f"{self.username} {self.id} {self.link}"

    def parse(self, link: str):
        if link.endswith("/"):
            link = link[:-1]

        if "atcoder.jp/contests/" not in link or "/tasks/" not in link:
            return False

        pid = link.rsplit("/", 1)[-1]

        self.link = link
        self.id = pid
        return True


if __name__ == "__main__":
    user = AtCoder("hungg261")
    user.parse("https://atcoder.jp/contests/abc357/tasks/abc357_f")
    print(user)
