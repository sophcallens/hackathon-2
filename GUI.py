import flet as ft
import random as rd

class Taquin:
    def __init__(self, page: ft.Page):
        self.page = page
        self.plateau_gagnant = ["1", "2", "3", "4", "5", "6", "7", "8", ""]
        self.plateau = ["1", "2", "3", "4", "5", "6", "7", "8", ""]
        rd.shuffle(self.plateau)
    
        self.titre = [ft.Text(value="Jeu du Taquin",text_align="center", width=160)]
        self.cases = [ft.TextField(value=i, text_align="center", width=50, read_only=True, on_click=self.move_case) for i in self.plateau]

        self.initialisation()


    def initialisation(self):
        grille = ft.GridView(controls=self.cases, runs_count=3, run_spacing=5, spacing=5, width=160)
        reset_button = [ft.IconButton(icon=ft.icons.REFRESH, on_click=self.reset)]

        self.page.add(ft.Column(controls = [ft.Row(self.titre), grille, ft.Row(reset_button)]))
        self.page.update()

    def reset(self, event):
        rd.shuffle(self.plateau)
        for i in range(len(self.cases)) : 
            self.cases[i].value = self.plateau[i]
        self.page.update()

    def move_case(self, event):
        i_clique = self.cases.index(event.control)
        for i in range(len(self.cases)) :
            if self.cases[i].value == "" :
                i_vide = i

        coups_possibles = []
        if i_vide % 3 > 0: 
            coups_possibles.append(i_vide - 1)
        if i_vide % 3 < 2: 
            coups_possibles.append(i_vide + 1)
        if i_vide >= 3: 
            coups_possibles.append(i_vide - 3)
        if i_vide < len(self.cases) - 3: 
            coups_possibles.append(i_vide + 3)

        if i_clique in coups_possibles:
            self.cases[i_vide].value = self.cases[i_clique].value
            self.cases[i_clique].value = ""
            self.page.update()

            self.verification()
    
    def verification(self):
        if [case.value for case in self.cases] == self.plateau_gagnant:
            dialog = ft.AlertDialog(title=ft.Text("C'est gagné !!!"))
            self.page.add(dialog)

            dialog.open = True
            self.page.update()
    

def jouer(page: ft.Page):
    page.title = "Jeu du Taquin"
    Taquin(page)

ft.app(target=jouer)
