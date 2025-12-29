import re

class Codeforces:
    name = "Codeforces"
    
    def __init__(self, username: str = None):
        self.username = username
        self.id = None
        self.link = None

    def __repr__(self):
        print(self.username, self.id, self.link)
        return ""
    
    def parse(self, link: str):
        """
        https://codeforces.com/contest/{cid}/problem/{id}
        https://codeforces.com/problemset/problem/{cid}/{id}
        https://codeforces.com/gym/{gym_id}/problem/{id}
        """
        if link.endswith("/"):
            link = link[:-1]
            
        patterns = [
            # contest problem
            r"codeforces\.com/contest/(?P<cid>\d+)/problem/(?P<pid>[A-Z0-9]+)",
            # problemset
            r"codeforces\.com/problemset/problem/(?P<cid>\d+)/(?P<pid>[A-Z0-9]+)",
            # gym
            r"codeforces\.com/gym/(?P<cid>\d+)/problem/(?P<pid>[A-Z0-9]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, link)
            if match:
                self.id = match.group("cid") + match.group("pid")
                if "gym" in link:
                    self.id = "Gym_" + self.id
                    
                self.link = link
                return True

        return False

        
if __name__ == "__main__":
    user = Codeforces("hungg261")
    # user.parse("https://codeforces.com/contest/915/problem/C")
    user.parse("https://codeforces.com/gym/106289/problem/A")
    
    repr(user)