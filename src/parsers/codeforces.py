import re

class Codeforces:
    name = "Codeforces"

    def __init__(self, username: str = None):
        self.username = username
        self.id = None
        self.link = None

    def __repr__(self):
        return f"{self.username} {self.id} {self.link}"

    def parse(self, link: str):
        if link.endswith("/"):
            link = link[:-1]

        patterns = [
            r"codeforces\.com/group/(?P<group>[A-Za-z0-9]+)/contest/(?P<cid>\d+)/problem/(?P<pid>[A-Z0-9]+)",
            r"codeforces\.com/contest/(?P<cid>\d+)/problem/(?P<pid>[A-Z0-9]+)",
            r"codeforces\.com/problemset/problem/(?P<cid>\d+)/(?P<pid>[A-Z0-9]+)",
            r"codeforces\.com/gym/(?P<cid>\d+)/problem/(?P<pid>[A-Z0-9]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, link)
            if match:
                cid = match.group("cid")
                pid = match.group("pid")

                if "group" in match.groupdict():
                    self.id = f"Group_{match.group('group')}_{cid}{pid}"
                elif "gym" in link:
                    self.id = f"Gym_{cid}{pid}"
                else:
                    self.id = cid + pid

                self.link = link
                return True

        return False


if __name__ == "__main__":
    user = Codeforces("hungg261")
    user.parse("https://codeforces.com/group/MWSDmqGsZm/contest/223340/problem/A")
    print(user)
