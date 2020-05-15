import math
from . import areas

def ρ(As, b, d):
    """
        Ποσοστό διαμήκους οπλισμού

    Args:
        As (float): Reinforcement area
        b (float): Section width
        d (float): Section effective depth

    Returns:
        float:
    """
    return As / (b * d)


def ρw(nw, diaw, b, s, α=math.pi/2):
    """
        Ποσοστό εγκάρσιου οπλισμού

    Args:
        nw (float): Τμήσεις συνδετήρα
        diaw (float): Διάμετρος συνδετήρα
        b (float): Section width
        s (float): Space between transverse reinforcement
        α (float): Transverse reinforcement angle

    Returns:
        float:
    """
    Asw = nw * areas.As(diaw)
    return Asw / (b * s * math.sin(α))


def ω(As: float, b: float, d: float, fy: float, fc: float):
    """
        Μηχανικά ποσοστά οπλισμού

    Args:
        As (float): Reinforcement area
        b (float): Section width
        d (float): Section effective depth
        fy (float):
        fc (float):

    Returns:
        float:
    """
    return As / (b * d) * (fy / fc)
