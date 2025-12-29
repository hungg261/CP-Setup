class MarisaOJ:
    name = "MarisaOJ"
    
    def __init__(self, username: str = None):        
        self.username = username
        self.id = None
        self.link = None
        
    def __repr__(self):
        print(self.username, self.id, self.link)
        return ""
    
    def parse(self, link: str):
        """
        https://marisaoj.com/problem/{id}
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
    user = MarisaOJ("hungg261")
    user.parse("https://marisaoj.com/problem/349")
    
    repr(user)