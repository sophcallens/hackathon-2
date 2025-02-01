import random as rd

class Plateau:
    def __init__(self, plateau: list[str]):
        self.plateau = plateau
        self.plateau_gagnant = ["1", "2", "3", "4", "5", "6", "7", "8", ""]

    def voisins(self) -> list:
        voisins = []
        i_vide = self.plateau.index("")
        
        # Mouvements possibles
        moves = []
        if i_vide % 3 > 0:
            moves.append(i_vide - 1)  # Gauche
        if i_vide % 3 < 2:
            moves.append(i_vide + 1)  # Droite
        if i_vide >= 3:
            moves.append(i_vide - 3)  # Haut
        if i_vide < 6:
            moves.append(i_vide + 3)  # Bas
        
        for i_possible in moves:
            nouveau_plateau = self.plateau.copy()
            nouveau_plateau[i_vide], nouveau_plateau[i_possible] = (
                nouveau_plateau[i_possible],
                nouveau_plateau[i_vide],
            )
            voisins.append(Plateau(nouveau_plateau))
        
        return voisins

    def resolu(self) -> bool:
        return self.plateau == self.plateau_gagnant


class TaquinSolver:
    def __init__(self, plateau_depart: Plateau):
        self.plateau_depart = plateau_depart

    def solve(self) -> list[Plateau]:
        file = [self.plateau_depart]
        distances = {self.plateau_depart: 0}
        sommets_visites = {}

        while file != []:
            plateau_courant = file.pop(0)
            distance_courante = distances[plateau_courant]

            if plateau_courant.resolu():
                return self.reconstruire_chemin(plateau_courant, sommets_visites)

            for voisin in plateau_courant.voisins():
                nouvelle_distance = distance_courante + 1

                if voisin not in distances or nouvelle_distance < distances[voisin]:
                    distances[voisin] = nouvelle_distance
                    sommets_visites[voisin] = plateau_courant
                    file.append(voisin)

        return []

    def reconstruire_chemin(self, plateau_final: Plateau, sommets_visites: dict) -> list[Plateau]:
        chemin = [plateau_final]
        while plateau_final in sommets_visites:
            plateau_final = sommets_visites[plateau_final]
            chemin.append(plateau_final)
        chemin.reverse()
        return chemin




def afficher_plateau(plateau: Plateau):
    """Affiche un plateau sous forme 3x3."""
    for i in range(0, 9, 3):
        print(plateau.plateau[i:i + 3])
    print()


plateau_initial = Plateau(["1", "2", "3", "4", "5", "6", "7", "8", ""])
rd.shuffle(plateau_initial.plateau)

print("Plateau initial :")
afficher_plateau(plateau_initial)

solver = TaquinSolver(plateau_initial)
chemin_solution = solver.solve()

if chemin_solution:
    print(f"Solution trouvée en {len(chemin_solution) - 1} mouvements.\n")
    for i, etape in enumerate(chemin_solution):
        print(f"Étape {i}:")
        afficher_plateau(etape)
else:
    print("Aucune solution trouvée.")

