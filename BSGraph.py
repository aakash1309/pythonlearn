import Vertex
import MyQueue
class BSGraph:# Graph implementation
    def __init__(self):
        self.ActMov = []
        self.edges = []

    def addVertex(self,name,type): # This adds a vertex to the graph. This vertex can be either an actor or a movie
        newVertex = Vertex.Vertex(name,type,False)
        self.ActMov.append(newVertex)
        return newVertex

    def getVertex(self,name):# Returns the vertex if present in the graph
        for x in self.ActMov:
            if x.getName() == name:
                return x
        return None

    def addEdge(self,fname,ftype,tname,ttype):# Creates a vertices if not present, 
        nvf = self.getVertex(fname)           # uses addVertex method to create a vetex and creates a edge b/w these vertice
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

    def getActors(self):# Returns all the actors present in the graph
        actorList = []
        for x in self.ActMov:
            if x.getType() == "Actor":
                actorList.append(x.getName())
        return actorList

    def getMovies(self):# Returns all the movies present in the graph
        movieList = []
        for x in self.ActMov:
            if x.getType() == "Movie":
                movieList.append(x.getName())
        return movieList

    def isVertexPresentInEdge(self,name,edge):# Checks if the edge contains the input vertex
        i=0;
        while i < len(edge):
            if edge[i].getName() == name:
                return i
            i=i+1
        return -1
    def getNeighbours(self,name):# Returns all the vertecies that are direct neighbour to this vertex
        neighbourList = []
        for edge in self.edges:
            thing_index = self.isVertexPresentInEdge(name,edge)
            if thing_index != -1:
                neighbourList.append(edge[abs(thing_index-1)])
        return neighbourList

    def readActMovieFile(self,inputFile):#Reads the input file and creates the graph
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

    def displayActMov(self):# outputs all the actors, movies and their count
        movies = self.getMovies()
        actors = self.getActors()
        file = open('outputPS2.txt', 'a+')
        file.write("--------Function displayActMov --------\n")
        file.write("Total no. of movies: %d\n" % len(movies))
        file.write("Total no. of actors: %d\n" % len(actors))
        file.write("List of movies:\n")
        file.writelines(["%s\n" % item for item in movies])
        file.write("\n");
        file.write("List of Actors:\n")
        file.writelines(["%s\n" % item for item in actors])
        file.write("-----------------------------------------")
        file.close()

    def displayMoviesOfActor(self,actor):# Outputs all the movies that the actor has played role in.
        file = open('outputPS2.txt', 'a+')
        file.write("\n--------Function displayMoviesOfActor--------\n")
        file.write("Actor name: %s\n" % actor)
        file.write("List of movies:\n")
        movieList = self.getNeighbours(actor);
        if len(movieList) == 0:
            file.write("No Actors Found For This Movie");
        file.writelines(["%s\n" % item.getName() for item in movieList])
        file.write("-----------------------------------------")
        file.close()


    def displayActorsOfMovie(self,movie):# Outputs all the actors that have taken part in the movie.
        file = open('outputPS2.txt', 'a+')
        file.write("\n--------Function displayActorsOfMovie --------\n")
        file.write("Movie name: %s\n" % movie)
        file.write("List of Actors:\n")
        actorList = self.getNeighbours(movie);
        if len(actorList) == 0:
            file.write("No Movies Found For This Actor");
        file.writelines(["%s\n" % item.getName() for item in actorList])
        file.write("-----------------------------------------")
        file.close()

    def findMovieRelation(self, movA, movB):# Outputs all the common actors b/w the two movies.
        file = open('outputPS2.txt', 'a+')
        file.write("\n--------Function findMovieRelation --------\n")
        file.write("Movie A: %s\n" % movA)
        file.write("Movie B: %s\n" % movB)
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

    def findMovieTransRelation(self,movA,movB):# finds path between 2 movies using BFS.
        file = open('outputPS2.txt', 'a+')
        file.write("\n--------Function findMovieTransRelation --------\n")
        file.write("Movie A: %s\n" % movA)
        file.write("Movie B: %s\n" % movB)
        for i in self.ActMov:
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
