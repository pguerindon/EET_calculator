from pathlib import Path


FLAGS_DIR = (
    Path(__file__).resolve().parent.parent
    / "flags"
)


def chemin_drapeau(
    nation,
):
    """
    Retourne le chemin du drapeau correspondant
    au code nation.

    Retourne None si la nation est absente
    ou si aucun drapeau correspondant n'existe.
    """

    if not nation:
        return None

    code = nation[:3].upper()

    fichier = FLAGS_DIR / f"{code}.png"

    if fichier.is_file():
        return fichier

    return None