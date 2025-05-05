from dataclasses import dataclass

from model.artObject import ArtObject


@dataclass
class Arco:
    o1: ArtObject #l'oggetto 1, che sarebbe il nodo1 è un OGGETTO OPERA D'ARTE
    o2: ArtObject #secondo nodo
    peso: int #peso dell'arco, che sarebbe il numero di esibizioni in cui le due opere d'arte sono statee esposte insieme
