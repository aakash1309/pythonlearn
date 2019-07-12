import Vertex
import MyQueue
class Graph:
    def __init__(self):
        self.vertList = []
        self.numActors = 0
        self.edges = []
        self.numMovies = 0

    def addVertex(self,name,type):
        newVertex = Vertex.Vertex(name,type,False)
        self.vertList.append(newVertex)
        if type == "Actor":
            self.numActors = self.numActors + 1
        else:
            self.numMovies = self.numMovies + 1
        return newVertex

    def getVertex(self,name):
        for x in self.vertList:
            if x.getName() == name:
                return x
        return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,fname,ftype,tname,ttype):
        nvf = self.getVertex(fname)
        nvt = self.getVertex(tname)
        if nvf == None:
            nvf = self.addVertex(fname,ftype)
        if nvt == None:
            nvt = self.addVertex(tname,ttype)
        newEdge = []
        newEdge.append(nvf);
        newEdge.append(nvt);
        self.edges.append(newEdge);
        return

    def getActors(self):
        actorList = []
        for x in self.vertList:
            if x.getType() == "Actor":
                actorList.append(x.getName())
        return actorList

    def getMovies(self):
        movieList = []
        for x in self.vertList:
            if x.getType() == "Movie":
                movieList.append(x.getName())
        return movieList

    def isVertexPresentInEdge(self,name,edge):
        i=0;
        while i < len(edge):
            if edge[i].getName() == name:
                return i
            i=i+1
        return -1
    def getNeighbours(self,name):
        neighbourList = []
        for edge in self.edges:
            thing_index = self.isVertexPresentInEdge(name,edge)
            if thing_index != -1:
                neighbourList.append(edge[abs(thing_index-1)])
        return neighbourList

    def readActMovieFile(self,inputFile):
        f = open(inputFile, "r")
        for x in f:
            x = x.rstrip().split("/")
            if 2 > len(x):
                continue
            else:
                i = 1;
                while i < len(x):
                    self.addEdge(x[0].lstrip().rstrip(), "Movie", x[i].lstrip().rstrip(), "Actor");
                    i = i + 1;
        f.close()

    def displayActMov(self):
        file = open('outputPS2.txt', 'a+')
        file.write("--------Function displayActMov --------\n")
        file.write("Total no. of movies: %d\r" % self.numMovies)
        file.write("Total no. of actors: %d\r\n" % self.numActors)
        file.write("List of movies:\n")
        file.writelines(["%s\n" % item for item in self.getMovies()])
        file.write("\n");
        file.write("List of Actors:\n")
        file.writelines(["%s\n" % item for item in self.getActors()])
        file.write("-----------------------------------------")
        file.close()

    def displayMoviesOfActor(self,actor):
        file = open('outputPS2.txt', 'a+')
        file.write("\n--------Function displayMoviesOfActor--------\n")
        file.write("Actor name: %s\r" % actor)
        file.write("List of movies:\n")
        movieList = self.getNeighbours(actor);
        if len(movieList) == 0:
            file.write("No Actors Found For This Movie");
        file.writelines(["%s\n" % item.getName() for item in movieList])
        file.write("-----------------------------------------")
        file.close()


    def displayActorsOfMovie(self,movie):
        file = open('outputPS2.txt', 'a+')
        file.write("\n--------Function displayActorsOfMovie --------\n")
        file.write("Movie name: %s\r" % movie)
        file.write("List of Actors:\n")
        actorList = self.getNeighbours(movie);
        if len(actorList) == 0:
            file.write("No Movies Found For This Actor");
        file.writelines(["%s\n" % item.getName() for item in actorList])
        file.write("-----------------------------------------")
        file.close()

    def findMovieRelation(self, movA, movB):
        file = open('outputPS2.txt', 'a+')
        file.write("\n--------Function findMovieRelation --------\n")
        file.write("Movie A: %s\r" % movA)
        file.write("Movie B: %s\r" % movB)
        movANeighbours = set(self.getNeighbours(movA));
        movBNeighbours = set(self.getNeighbours(movB));
        commonMembers = movANeighbours.intersection(movBNeighbours)
        if len(commonMembers) > 0:
            file.write("Related: Yes, ")
            file.writelines(["%s " % item.getName() for item in commonMembers])
        else:
            file.write("Related: No");
        file.write("\n-----------------------------------------")
        file.close()

    def findMovieTransRelationRecursive(self, movA, movB):
        file = open('outputPS2.txt', 'a+')
        file.write("\n--------Function findMovieTransRelation --------\n")
        file.write("Movie A: %s\r" % movA)
        file.write("Movie B: %s\r" % movB)
        path=""
        path = self.findPath(movA,movB,path)
        if path == None:
            file.write("Related: No");
            file.write("\n-----------------------------------------")
        else:
            file.write("Related: Yes, ")
            file.write(path)
            file.write("\n----------------------------------------")
        file.close()

    def findPathRecursive(self, movA, movB,path):
        if movA == movB:
            return path + movA
        else:
            path = path + movA + " > "
        if movA == movB:
            return path
        for node in self.getNeighbours(movA):
            if node.getName() not in path:
                newpath = self.findPath(node.getName(), movB, path)
                if newpath: return newpath
        return None


    def findMovieTransRelation(self,movA,movB):
        file = open('outputPS2.txt', 'a+')
        file.write("\n--------Function findMovieTransRelation --------\n")
        file.write("Movie A: %s\r" % movA)
        file.write("Movie B: %s\r" % movB)
        for i in self.vertList:
            if i.getName() == movA:
                i.visited = True
            else:
                i.visited = False
        q = MyQueue.MyQueue();
        temp_path = [movA]
        q.enqueue(temp_path)
        while q.IsEmpty() == False:
            tmp_path = q.dequeue()
            last_node = tmp_path[len(tmp_path) - 1]
            if last_node == movB:
                file.write("Related: Yes, %s" %tmp_path.pop(0))
                file.writelines([" > %s" % item for item in tmp_path])
                file.write("\n----------------------------------------")
                file.close()
                return
            for link_node in self.getNeighbours(last_node):
                if not link_node.getVisited():
                    link_node.visited = True
                    new_path = tmp_path + [link_node.getName()]
                    q.enqueue(new_path)
        file.write("Related: No");
        file.write("\n-----------------------------------------")
        file.close()
