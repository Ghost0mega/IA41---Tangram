from tangram.models.piece import Piece
from tangram.models.geometry import polygons_overlap


class Board:

    def __init__(self, pieces: list[Piece] | None = None):
        # Dictionnaire {nom_de_la_piece: instance_Piece} pour des accès rapides
        self.pieces: dict[str, Piece] = {}
        if pieces:
            for piece in pieces:
                self.add_piece(piece)

    def add_piece(self, piece: Piece) -> None:
        """Ajoute une pièce sur le plateau."""
        if piece.name in self.pieces:
            raise ValueError(f"Une pièce nommée '{piece.name}' existe déjà sur le plateau.")
        self.pieces[piece.name] = piece

    def remove_piece(self, name: str) -> Piece:
        """Retire une pièce du plateau par son nom."""
        if name not in self.pieces:
            raise KeyError(f"La pièce '{name}' n'est pas sur le plateau.")
        return self.pieces.pop(name)

    def get_piece(self, name: str) -> Piece:
        """Récupère une pièce du plateau par son nom."""
        if name not in self.pieces:
            raise KeyError(f"La pièce '{name}' n'est pas sur le plateau.")
        return self.pieces[name]

    def move_piece(self, name: str, new_position: tuple[float, float]) -> None:
        """Déplace une pièce sur le plateau."""
        piece = self.get_piece(name)
        piece.position = new_position

    def rotate_piece(self, name: str, angle_deg: float) -> None:
        """Pivote une pièce sur le plateau (ajoute à la rotation actuelle)."""
        piece = self.get_piece(name)
        piece.rotation_deg = (piece.rotation_deg + angle_deg) % 360.0

    def flip_piece(self, name: str) -> None:
        """Bascule l'état miroir d'une pièce sur le plateau."""
        piece = self.get_piece(name)
        piece.flip()

    def get_all_world_vertices(self) -> dict[str, list[tuple[float, float]]]:
        """Retourne les coordonnées absolues (monde) de toutes les pièces posées."""
        return {name: piece.get_world_vertices() for name, piece in self.pieces.items()}

    def check_collisions(self) -> list[tuple[str, str]]:
        """Retourne la liste des pairs de pièces qui se chevauchent."""
        collisions = []
        piece_names = list(self.pieces.keys())
        
        for i in range(len(piece_names)):
            for j in range(i + 1, len(piece_names)):
                name1, name2 = piece_names[i], piece_names[j]
                poly1 = self.pieces[name1].get_world_vertices()
                poly2 = self.pieces[name2].get_world_vertices()
                
                if polygons_overlap(poly1, poly2):
                    collisions.append((name1, name2))
                    
        return collisions