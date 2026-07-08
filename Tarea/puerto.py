import json
class Puerto:
    list = []
    def __init__(self)-> None:
        self.id = str
        self.material = str

    def load(filename: str):
        with open(filename, 'r', encoding = 'utf-8' ) as f:
            data = json.load(f)
            for v in data["ports"]:
                new = Puerto()
                new.id = (v["id"])
                new.material =(v["material"])
                Puerto.list.append(new)
