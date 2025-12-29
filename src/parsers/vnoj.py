class VNOJ:
    name = "VNOJ"
    
    def __init__(self, username: str = None):
        self.username = username
        self.id = None
        self.link = None
        self.organization = None
        
    def __repr__(self):
        print(self.username, self.id, self.link, self.organization)
        return ""
    
    def parse(self, link: str, in_organization: bool = False):
        """
        https://oj.vnoi.info/problem/{org}_{id}
        """
        if link.endswith("/"):
            link = link[:-1]
        
        id = link.rsplit("/")[-1]
        org = None
        if in_organization:
            if "_" not in id:
                return False
            
            org, id = id.split("_", maxsplit=1)
        
        self.link = link
        self.id = id
        self.organization = org
        return True
        
if __name__ == "__main__":
    user = VNOJ("hungg261")
    user.parse("https://oj.vnoi.info/problem/nvnamson_duhanh", True)
    
    repr(user)