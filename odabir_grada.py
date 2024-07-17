import json

class Gradovi:
    GRADOVI = "./gradovi.json"
    def __init__(self, city, zip, region, municipality):
        self.city = city
        self.zip = zip
        self.region = region
        self.municipality = municipality
        
    
    @classmethod  #ucitavamo sve iz biblioteke track.json i smestamo u jedan niz track
    def load_city(cls):
        with open(cls.GRADOVI, "r", encoding="utf-8") as f:
            grad = json.load(f)
            g = []
            for i in grad:
                t = Gradovi(i["city"],i["zip"], i["region"], i["municipality"])
                g.append(t)
            return g   

