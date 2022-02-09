class Human:
    type = str()

    def __init__(self, height, weight=0) -> None:
        self.type = 'homo sapiens'
        self.height = height
        self.weight = weight

    def getHeight(self):
        return self.height

    def getWeight(self):
        return self.weight

    def setHeight(self, height):
        self.height = height

    def setWeight(self, weight):
        self.weight = weight
