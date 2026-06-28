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

function validerGrille()
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
        .forEach(ligne =>
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

            /*
             * Ligne EET :
             * Dossard présent
             * TM complet
             * TE vide
             */

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
        });

    const grilleValide =
    (
        nbDossards === 11 &&
        nbTMComplets === 11 &&
        nbTEComplets === 10 &&
        nbTEVides === 1
    );

    console.log(
        "nbDossards=",
        nbDossards,
        "nbTMComplets=",
        nbTMComplets,
        "nbTEComplets=",
        nbTEComplets,
        "nbTEVides=",
        nbTEVides
    );

    console.log(
        "grilleValide=",
        grilleValide
    );

    const message =
        document.getElementById(
            "message_validation"
        );

    if (
        document.getElementById(
            "resultat-panel"
        ) !== null
    )
    {
        message.innerHTML = "";
        return;
    }
    if (nbTEVides > 1)
    {
        message.innerHTML =
            TXT.erreur_plusieurs_te;
    }

    else if (
        nbTEVides === 0 &&
        !resultatAffiche
    )
    {
        message.innerHTML =
            TXT.erreur_aucun_te;
    }
    else if (nbTMComplets < 11)
    {
        message.innerHTML =
            TXT.erreur_tm;
    }
    else if (nbTEComplets < 10)
    {
         message.innerHTML =
            TXT.erreur_references;
    }
    else if (grilleValide)
    {
        message.innerHTML =
            "✓ " + TXT.grille_valide;
    }

    if (grilleValide)
    {
        message.style.color = "green";
    }
    else
    {
        message.style.color = "red";
    }


    document
        .getElementById(
            "btn_calculer"
        )
        .disabled = !grilleValide;

}

function chargerExempleFIS()
{
    document.getElementById(
        "precision_te"
    ).value = "4";

    document.getElementById(
        "precision_tm"
    ).value = "4";

    const donnees =
    [
        ["1","10:00:50.3548","10:00:50.1292"],
        ["2","10:01:52.0189","10:01:52.1921"],
        ["3","10:02:49.4978","10:02:49.4920"],
        ["4","10:03:50.6148","10:03:50.9812"],
        ["5","10:04:49.2741","10:04:49.8729"],
        ["6","10:05:50.4702","10:05:50.5129"],
        ["7","10:06:48.9125","10:06:48.8615"],
        ["8","10:07:51.5814",""],
        ["9","10:08:49.8751","10:08:50.0002"],
        ["10","10:09:49.2459","10:09:49.4278"],
        ["11","10:10:50.3954","10:10:50.3473"]
    ];

    document
        .querySelectorAll(".ligne")
        .forEach(
            (ligne, index) =>
            {
                ligne.querySelector(
                    ".dossard"
                ).value =
                    donnees[index][0];

                ligne.querySelector(
                    ".tm"
                ).value =
                    donnees[index][1];

                ligne.querySelector(
                    ".te"
                ).value =
                    donnees[index][2];
            }
        );

    mettreAJourDeltas();
    validerGrille();
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
        validerGrille();
    }
);


document
    .getElementById("btn_effacer")
    .addEventListener(
        "click",
        function()
        {
            //
            // Champs
            //
            document
                .querySelectorAll(".dossard, .tm, .te")
                .forEach(champ =>
                {
                    champ.value = "";
                });

            //
            // Deltas
            //
            document
                .querySelectorAll(".delta-cell")
                .forEach(cell =>
                {
                    cell.textContent = "";
                    cell.className =
                        "delta-cell delta";
                });

            //
            // Somme des deltas
            //
            const total =
                document.querySelector(
                    ".delta-total"
                );

            if (total)
            {
                total.textContent = "";
            }

            //
            // Ligne EET
            //
            document
                .querySelectorAll(".ligne")
                .forEach(ligne =>
                {
                    ligne.classList.remove(
                        "ligne-eet-calculee"
                    );
                });

            document
                .querySelectorAll(".te")
                .forEach(champ =>
                {
                    champ.classList.remove(
                        "te-eet"
                    );
                });

            //
            // Panneau résultat
            //
            const panel =
                document.getElementById(
                    "resultat-panel"
                );

            if (panel)
            {
                panel.remove();
            }

            document
                .querySelector(
                    ".conteneur"
                )
                .classList
                .remove(
                    "resultat-dessous"
                );


            //
            // Message
            //
            document.getElementById(
                "message_validation"
            ).textContent = "";

            //
            // Bouton calcul
            //
            document.getElementById(
                "btn_calculer"
            ).disabled = true;

            
        }
    );

document
    .getElementById(
        "btn_exemple_fis"
    )
    .addEventListener(
        "click",
        function()
        {
            chargerExempleFIS();
        }
    )

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