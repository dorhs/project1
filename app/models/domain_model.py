class Domain:
    def __init__(self, domain_name, status):
        self.domain_name = domain_name
        self.status = status

    def __repr__(self):
        return f'<Domain {self.domain_name}>'
