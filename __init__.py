import BSGraph

if __name__ == "__main__":
    open('outputPS2.txt', 'w').close()
    g = BSGraph.BSGraph()
    g.readActMovieFile("inputPS2.txt")
    g.displayActMov()
    readFile = open('promptsPS2.txt', 'r')
    for line in readFile:
        searchKeys = line.rstrip().split(":")
        if "searchActor" in line:
            g.displayMoviesOfActor(searchKeys[1].lstrip().rstrip())
        elif "searchMovie" in line:
            g.displayActorsOfMovie(searchKeys[1].lstrip().rstrip())
        elif "RMovies" in line:
            g.findMovieRelation(searchKeys[1].lstrip().rstrip(),searchKeys[2].lstrip().rstrip())
        elif "TMovies" in line:
            g.findMovieTransRelation(searchKeys[1].lstrip().rstrip(),searchKeys[2].lstrip().rstrip())