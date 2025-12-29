class CSES:
    name = "CSES"
    
    def __init__(self, username: str = None):
        self.username = username
        self.id = None
        self.link = None
        
    def __repr__(self):
        print(self.username, self.id, self.link)
        return ""
    
    def parse(self, link: str):
        """
        https://cses.fi/problemset/task/{id}
        """
        if link.endswith("/"):
            link = link[:-1]
        
        id = link.rsplit("/")[-1]
        if id.isdigit():
            self.link = link
            self.id = id
            return True
        
        return False
        
if __name__ == "__main__":
    user = CSES("hungg261")
    user.parse("https://cses.fi/problemset/task/2190/")
    
    repr(user)