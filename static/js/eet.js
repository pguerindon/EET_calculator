const btnCalculer = document.getElementById("btn_calculer");

function formaterTemps(chiffres, precision)
{
    let max = 6 + precision;

    chiffres = chiffres.substring(0, max);

    let resultat = "";

    if (chiffres.length >= 1)
        resultat += chiffres.substring(0, Math.min(2, chiffres.length));

    if (chiffres.length > 2)
        resultat += ":" + chiffres.substring(2, Math.min(4, chiffres.length));

    if (chiffres.length > 4)
        resultat += ":" + chiffres.substring(4, Math.min(6, chiffres.length));

    if (chiffres.length > 6)
        resultat += "." + chiffres.substring(6);

    return resultat;
}


function tempsComplet(temps, precision)
{
    const chiffres = temps.replace(/\D/g, "");

    return chiffres.length === (6 + precision);
}


function convertirTempsEnSecondes(temps)
{
    const morceaux = temps.split(":");

    if (morceaux.length !== 3)
        throw "temps invalide";

    const hh = parseInt(morceaux[0]);
    const mm = parseInt(morceaux[1]);
    const secFrac = parseFloat(morceaux[2]);

    return (
        hh * 3600 +
        mm * 60 +
        secFrac
    );
}


function mettreAJourDeltas()
{

    const precisionTE =
        parseInt(
            document.getElementById(
                "precision_te"
            ).value
        );

    const precisionTM =
        parseInt(
            document.getElementById(
                "precision_tm"
            ).value
        );

    const precisionDelta =
        Math.max(
            precisionTE,
            precisionTM
        );
    document
        .querySelectorAll(".ligne")
        .forEach(ligne =>
        {
            const tm =
                ligne.querySelector(".tm")
                     .value.trim();

            const te =
                ligne.querySelector(".te")
                     .value.trim();

            const cellule =
                ligne.querySelector(".delta-cell");

            cellule.innerHTML = "";
            cellule.className = "delta-cell delta";

            if (
                !tempsComplet(
                    tm,
                    parseInt(
                        document.getElementById(
                            "precision_tm"
                        ).value
                    )
                )
            )
            {
                return;
            }

            if (
                !tempsComplet(
                    te,
                    precisionTE
                )
            )
            {
                return;
            }

            try
            {
                const tmSec =
                    convertirTempsEnSecondes(tm);

                const teSec =
                    convertirTempsEnSecondes(te);

                const delta =
                    tmSec - teSec;

                cellule.innerHTML =
                    (delta >= 0 ? "+" : "") +
                    delta.toFixed(
                        precisionDelta
                    );

                if (Math.abs(delta) > 1)
                {
                    cellule.className =
                        "delta-cell delta-warning";
                }
            }
            catch
            {
            }
        });
}

function mettreAJourEtatCalcul()
{
    let nbDossards = 0;
    let nbTMComplets = 0;
    let nbTEComplets = 0;
    let nbTEVides = 0;

    const precisionTM =
        parseInt(
            document.getElementById(
                "precision_tm"
            ).value
        );

    const precisionTE =
        parseInt(
            document.getElementById(
                "precision_te"
            ).value
        );

    document
        .querySelectorAll(".ligne")
        .forEach(
            ligne =>
            {
                ligne.classList.remove(
                    "ligne-eet"
                );

                const dossard =
                    ligne.querySelector(".dossard")
                         .value.trim();

                const tm =
                    ligne.querySelector(".tm")
                         .value.trim();

                const te =
                    ligne.querySelector(".te")
                         .value.trim();

                if (dossard !== "")
                {
                    nbDossards++;
                }

                if (
                    tempsComplet(
                        tm,
                        precisionTM
                    )
                )
                {
                    nbTMComplets++;
                }

                if (
                    tempsComplet(
                        te,
                        precisionTE
                    )
                )
                {
                    nbTEComplets++;
                }

                if (te === "")
                {
                    nbTEVides++;
                }

                if (
                    dossard !== "" &&
                    tempsComplet(
                        tm,
                        precisionTM
                    ) &&
                    te === ""
                )
                {
                    ligne.classList.add(
                        "ligne-eet"
                    );
                }
            }
        );

    const grilleValide =
    (
        nbDossards === 11 &&
        nbTMComplets === 11 &&
        nbTEComplets === 10 &&
        nbTEVides === 1
    );

    const message =
        document.getElementById(
            "message_validation"
        );

    if (grilleValide)
    {
        message.innerHTML =
            "✓ " + TXT.grille_valide;

        message.style.color =
            "green";
    }
    else
    {
        message.innerHTML = "";
    }

    if (btnCalculer)
    {
        btnCalculer.disabled =
            !grilleValide;
    }

    console.log(
        "Dossards :", nbDossards,
        "TM :", nbTMComplets,
        "TE :", nbTEComplets,
        "TE vides :", nbTEVides,
        "Grille valide :", grilleValide
    );
}

document.addEventListener(
    "input",
    function(event)
    {
        if (
            event.target.classList.contains("tm") ||
            event.target.classList.contains("te")
        )
        {
            let precision;

            if (
                event.target.classList.contains("tm")
            )
            {
                precision =
                    parseInt(
                        document.getElementById(
                            "precision_tm"
                        ).value
                    );
            }
            else
            {
                precision =
                    parseInt(
                        document.getElementById(
                            "precision_te"
                        ).value
                    );
            }

            let chiffres =
                event.target.value.replace(
                    /\D/g,
                    ""
                );

            event.target.value =
                formaterTemps(
                    chiffres,
                    precision
                );

            let longueurAttendue =
                6 + precision;

            if (
                chiffres.length ===
                longueurAttendue
            )
            {
                const champs =
                    Array.from(
                        document.querySelectorAll(
                            ".dossard, .tm, .te"
                        )
                    );

                const index =
                    champs.indexOf(
                        event.target
                    );

                if (
                    index >= 0 &&
                    index < champs.length - 1
                )
                {
                    champs[
                        index + 1
                    ].focus();

                    champs[
                        index + 1
                    ].select();
                }
            }
        }
        mettreAJourDeltas();
        mettreAJourEtatCalcul();
    }
);

const checkbox =
    document.getElementById(
        "resultat_sous_grille"
    );

if (checkbox)
{
    //
    // Restauration du choix
    //
    const resultatDessous =
        localStorage.getItem(
            "resultat_sous_grille"
        ) === "true";

    checkbox.checked =
        resultatDessous;

    document
        .querySelector(
            ".conteneur"
        )
        .classList
        .toggle(
            "resultat-dessous",
            resultatDessous
        );

    //
    // Changement de mode
    //
    checkbox.addEventListener(
        "change",
        function()
        {
            document
                .querySelector(
                    ".conteneur"
                )
                .classList
                .toggle(
                    "resultat-dessous",
                    this.checked
                );

            localStorage.setItem(
                "resultat_sous_grille",
                this.checked
            );
        }
    );
}

function changerLangue()
{
    document.getElementById(
        "btn_langue"
    ).click();
}

document.addEventListener(
    "DOMContentLoaded",
    () =>
    {
        mettreAJourDeltas();
        mettreAJourEtatCalcul();
    }
);