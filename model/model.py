import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._movies = []
        self._bestSelection = []
        self._bestAvgRating = 0.0

    def buildGraph(self, genre):
        self._graph.clear()

        self._movies = DAO.getMoviesByGenre(genre)

        for movie in self._movies:
            DAO.getActorsForMovie(movie) # popolo il film con gli attori

        self._graph.add_nodes_from(self._movies)

        for i in range(len(self._movies)):
            for j in range(i + 1, len(self._movies)):
                f1 = self._movies[i]
                f2 = self._movies[j]

                if not (f1.Actors & f2.Actors):
                    continue

                if f1.Year is None or f2.Year is None:
                    # se l'anno non è noto per uno dei due film, inseriamo comunque l'arco in entrambe le direzioni.
                    self._graph.add_edge(f1, f2)
                    self._graph.add_edge(f2, f1)
                elif f1.Year < f2.Year:
                    self._graph.add_edge(f1, f2)
                elif f2.Year < f1.Year:
                    self._graph.add_edge(f2, f1)
                else:
                    # stesso anno, aggiungo entrambi i versi
                    self._graph.add_edge(f1, f2)
                    self._graph.add_edge(f2, f1)

    def getNumConnectedComponents(self):
        return nx.number_weakly_connected_components(self._graph)

    def getLargestConnectedComponent(self):
        if len(self._graph.nodes) == 0:
            return []

        components = list(nx.weakly_connected_components(self._graph))
        largest = max(components, key=len)
        return list(largest)

    def getMovieInfoInLargestComponent(self):
        largest_component = self.getLargestConnectedComponent()

        result = []
        for movie in largest_component:
            result.append((movie.Title, movie.get_num_actors()))

        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def getMovieWithMaxOutDegree(self):
        if len(self._graph.nodes) == 0:
            return None, 0

        max_out_degree = -1
        best_movie = None
        for node, out_degree in self._graph.out_degree():
            if out_degree > max_out_degree:
                max_out_degree = out_degree
                best_movie = node
        return best_movie, max_out_degree

    def getBestSelection(self, starting_movie, N):

        if starting_movie not in self._graph.nodes:
            return [], 0.0

        starting_component = self._getConnectedComponent(starting_movie)
        if starting_component is None:
            return [], 0.0

        all_components = list(nx.weakly_connected_components(self._graph))
        remaining_components = [c for c in all_components if c != starting_component]

        self._bestSelection = []
        self._bestAvgRating = 0.0

        parziale = [starting_movie]
        self._ricorsione(parziale, N, remaining_components)

        return self._bestSelection, self._bestAvgRating

    def _ricorsione(self, parziale, N, comp_rimanenti):
        # condizione di terminazione: parziale è lunga N
        if len(parziale) == N:
            total_rating = self._getTotalAvgRating(parziale)
            if total_rating > self._bestAvgRating:
                self._bestAvgRating = total_rating
                self._bestSelection = copy.deepcopy(parziale)
            return

        # se non ci sono più componenti disponibili, o non ne restano abbastanza da
        # raggiungere N elementi, posso interrompere questo ramo della ricorsione
        if not comp_rimanenti or N - len(parziale) > len(comp_rimanenti):
            return

        next_component = comp_rimanenti[0]

        # opzione 1: non prendo nessun film da questa componente
        self._ricorsione(parziale, N, comp_rimanenti[1:])

        # opzione 2: prendo il film con rating maggiore da questa componente
        best_movie = self._getMovieWithMaxRating(next_component)

        if best_movie is not None:
            parziale.append(best_movie)
            self._ricorsione(parziale, N, comp_rimanenti[1:])
            parziale.pop()

    def _getConnectedComponent(self, movie):
        components = list(nx.weakly_connected_components(self._graph))
        for component in components:
            if movie in component:
                return component
        return None

    def _getMovieWithMaxRating(self, movies):
        best_movie = None
        max_rating = -1.0
        for movie in movies:
            if movie.AvgRating > max_rating:
                max_rating = movie.AvgRating
                best_movie = movie
        return best_movie

    def _getTotalAvgRating(self, movies):
        return sum(movie.AvgRating for movie in movies)

    def getAllGenres(self):
        return DAO.getAllGenres()

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getAllMovies(self):
        return self._graph.nodes