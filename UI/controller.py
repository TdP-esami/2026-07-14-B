import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self._genreValue = None
        self._movieValue = None

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        if self._genreValue is None:
            self._view.create_alert("Seleziona un genere dal menu a tendina.")
            return

        try:
            self._model.buildGraph(self._genreValue)

            self._view._txt_result.controls.append(
                ft.Text(f"Grafo correttamente creato per il genere {self._genreValue}.")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di vertici: {self._model.getNumNodi()}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di archi: {self._model.getNumEdges()}")
            )

            self._fillDDMovies()
            self._view.update_page()
        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione del grafo: {ex}")

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        try:
            num_components = self._model.getNumConnectedComponents()
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di componenti connesse: {num_components}")
            )

            movie_max_out, max_out_degree = self._model.getMovieWithMaxOutDegree()
            self._view._txt_result.controls.append(
                ft.Text(f"Film con maggior numero di archi uscenti: {movie_max_out} "
                        f"(archi uscenti: {max_out_degree})")
            )

            self._view._txt_result.controls.append(ft.Text(""))

            largest_component = self._model.getLargestConnectedComponent()
            self._view._txt_result.controls.append(
                ft.Text(f"Dimensione della componente connessa più grande: {len(largest_component)} film")
            )

            self._view._txt_result.controls.append(ft.Text(""))
            self._view._txt_result.controls.append(
                ft.Text("Dettagli dei film appartenenti alla componente connessa più grande:")
            )
            self._view._txt_result.controls.append(ft.Text(""))

            movie_info = self._model.getMovieInfoInLargestComponent()
            for title, num_actors in movie_info:
                self._view._txt_result.controls.append(
                    ft.Text(f"  - {title}: {num_actors} attori")
                )

            self._view.update_page()
        except Exception as ex:
            self._view.create_alert(f"Errore nella stampa delle info: {ex}")

    def handleTrovaSelezione(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        if self._movieValue is None:
            self._view.create_alert("Seleziona un film dal menu a tendina.")
            return

        try:
            N = int(self._view._txtInN.value)
            if N <= 0:
                self._view.create_alert("Inserisci un numero intero positivo per N.")
                return
        except (ValueError, TypeError):
            self._view.create_alert("Inserisci un valore numerico valido per N.")
            return

        try:
            best_selection, best_rating = self._model.getBestSelection(self._movieValue, N)

            if not best_selection:
                self._view._txt_result.controls.append(
                    ft.Text("Nessuna selezione trovata con i vincoli richiesti.")
                )
                self._view.update_page()
                return

            sorted_selection = sorted(best_selection, key=lambda m: m.Title)

            self._view._txt_result.controls.append(ft.Text("Lista (ordinata per titolo) dei film selezionati:"))
            self._view._txt_result.controls.append(ft.Text(""))

            for movie in sorted_selection:
                self._view._txt_result.controls.append(
                    ft.Text(f"  - {movie.Title}: anno {movie.Year}, {movie.get_num_actors()} attori nel cast")
                )

            self._view._txt_result.controls.append(ft.Text(""))
            self._view._txt_result.controls.append(
                ft.Text(f"Numero totale di film selezionati: {len(best_selection)}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Valutazione media complessiva della selezione: {best_rating:.2f}")
            )

            self._view.update_page()
        except Exception as ex:
            self._view.create_alert(f"Errore nella ricerca della selezione: {ex}")

    def _fillDDMovies(self):
        self._view._ddMovie.options.clear()
        all_movies = self._model.getAllMovies()

        movieOptions = list(
            map(lambda m: ft.dropdown.Option(data=m, key=str(m), on_click=self._choiceMovie), all_movies)
        )
        self._view._ddMovie.options = movieOptions

        self._view.update_page()

    def fillDDGenres(self):
        try:
            all_genres = self._model.getAllGenres()
        except Exception as ex:
            self._view.create_alert(f"Errore nel caricamento dei generi: {ex}")
            return

        genreOptions = list(map(lambda g: ft.dropdown.Option(data=g, key=str(g), on_click=self._choiceGenre),
                                all_genres))
        self._view._ddGenre.options = genreOptions

        self._view.update_page()

    def _choiceGenre(self, e):
        self._genreValue = e.control.data

    def _choiceMovie(self, e):
        self._movieValue = e.control.data