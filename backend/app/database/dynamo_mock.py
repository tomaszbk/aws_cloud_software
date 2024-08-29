class FakeTable:
    def __init__(self):
        self.table = []

    def put_item(self, Item):
        if Item in self.table:
            raise Exception("Item already exists!")
        self.table.append(Item)
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}
