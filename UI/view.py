import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP - Esame del 14 Luglio 2026 - Traccia B"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        # graphical elements
        self._title = None
        self._txt_result = None

        self._ddGenre = None
        self._btnCreaGrafo = None
        self._btnStampaInfo = None

        self._ddMovie = None
        self._txtInN = None
        self._btnTrovaSelezione = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - Esame del 14 Luglio 2026 - Traccia B", color="blue", size=24)
        self._page.controls.append(self._title)

        # riga 1: selezione genere + creazione grafo + stampa info
        self._ddGenre = ft.Dropdown(label="Genere")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                                on_click=self._controller.handleCreaGrafo)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa Info",
                                                 on_click=self._controller.handleStampaInfo)

        row1 = ft.Row([ft.Container(self._ddGenre, width=180),
                       ft.Container(self._btnCreaGrafo, width=180),
                       ft.Container(self._btnStampaInfo, width=180)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # riga 2: selezione film, N, ricerca selezione
        self._ddMovie = ft.Dropdown(label="Film")
        self._txtInN = ft.TextField(label="Numero di film")
        self._btnTrovaSelezione = ft.ElevatedButton(text="Trova selezione film",
                                                     on_click=self._controller.handleTrovaSelezione)

        row2 = ft.Row([ft.Container(self._ddMovie, width=220),
                       ft.Container(self._txtInN, width=150),
                       ft.Container(self._btnTrovaSelezione, width=220)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        self._page.controls.append(self._txt_result)
        self._page.update()

        # popolo il menu a tendina dei generi
        self._controller.fillDDGenres()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
