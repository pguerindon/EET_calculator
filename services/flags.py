from pathlib import Path


FLAGS_DIR = (
    Path(__file__).resolve().parent.parent
    / "flags"
)


def chemin_drapeau(
    codex,
):
    """
    Retourne le chemin du drapeau correspondant
    au CODEX.

    Si aucun drapeau correspondant n'existe,
    retourne le logo FIS.
    """

    if not codex:
        return FLAGS_DIR / "FIS.png"

    code = codex[:3].upper()

    fichier = FLAGS_DIR / f"{code}.png"

    if fichier.is_file():
        return fichier

    return FLAGS_DIR / "FIS.png"