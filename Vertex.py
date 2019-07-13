class Vertex:# Model for vertex
    def __init__(self,name,type,visited):
        self.type = type
        self.name = name
        self.visited = visited

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def getVisited(self):
        return self.visited