document
    .getElementById("calculer")
    .addEventListener(
        "click",
        calculer
    );

function todToUs(tod)
{
    const [hh, mm, reste] =
        tod.split(":");

    const [ss, frac = "0"] =
        reste.split(".");

    return (
        parseInt(hh) * 3600 * 1000000
        +
        parseInt(mm) * 60 * 1000000
        +
        parseInt(ss) * 1000000
        +
        parseInt(
            frac
                .padEnd(
                    6,
                    "0"
                )
                .substring(
                    0,
                    6
                )
        )
    );
}

function usToTod(us, precision)
{
    const hh =
        Math.floor(
            us / 3600000000
        );

    us %= 3600000000;

    const mm =
        Math.floor(
            us / 60000000
        );

    us %= 60000000;

    const ss =
        Math.floor(
            us / 1000000
        );

    us %= 1000000;

    const facteur =
        Math.pow(
            10,
            6 - precision
        );

    const frac =
        Math.floor(
            us / facteur
        );

    return (
        hh.toString().padStart(2, "0")
        + ":"
        + mm.toString().padStart(2, "0")
        + ":"
        + ss.toString().padStart(2, "0")
        + "."
        + frac
            .toString()
            .padStart(
                precision,
                "0"
            )
    );
}

function durationToUs(duree)
{
    const [hh, mm, reste] =
        duree.split(":");

    const [ss, frac = "0"] =
        reste.split(".");

    return (
        parseInt(hh) * 3600 * 1000000
        +
        parseInt(mm) * 60 * 1000000
        +
        parseInt(ss) * 1000000
        +
        parseInt(
            frac
                .padEnd(
                    6,
                    "0"
                )
                .substring(
                    0,
                    6
                )
        )
    );
}

function usToDuration(
    us,
    precision
)
{
    const hh =
        Math.floor(
            us / 3600000000
        );

    us %= 3600000000;

    const mm =
        Math.floor(
            us / 60000000
        );

    us %= 60000000;

    const ss =
        Math.floor(
            us / 1000000
        );

    us %= 1000000;

    const facteur =
        Math.pow(
            10,
            6 - precision
        );

    const frac =
        Math.floor(
            us / facteur
        );

    return (
        hh
            .toString()
            .padStart(
                2,
                "0"
            )
        + ":"
        +
        mm
            .toString()
            .padStart(
                2,
                "0"
            )
        + ":"
        +
        ss
            .toString()
            .padStart(
                2,
                "0"
            )
        + "."
        +
        frac
            .toString()
            .padStart(
                precision,
                "0"
            )
    );
}

function calculer()
{
    const depart =
        document
            .getElementById(
                "heure_depart"
            )
            .value.trim();

    const arrivee =
        document
            .getElementById(
                "heure_arrivee"
            )
            .value.trim();

    const temps =
        document
            .getElementById(
                "temps_course"
            )
            .value.trim();

    const message =
        document
            .getElementById(
                "message_validation"
            );

    const nbValeurs =
        (depart !== "" ? 1 : 0)
        +
        (arrivee !== "" ? 1 : 0)
        +
        (temps !== "" ? 1 : 0);

    //
    // Validations
    //

    if (
        depart !== ""
        &&
        !todValide(depart)
    )
    {
        message.innerHTML =
            TXT.erreur_tod;

        message.style.color =
            "red";

        return;
    }

    if (
        arrivee !== ""
        &&
        !todValide(arrivee)
    )
    {
        message.innerHTML =
            TXT.erreur_tod;

        message.style.color =
            "red";

        return;
    }

    if (
        temps !== ""
        &&
        !dureeValide(temps)
    )
    {
        message.innerHTML =
            TXT.erreur_duree;

        message.style.color =
            "red";

        return;
    }

    if (nbValeurs < 2)
    {
        message.innerHTML =
            TXT.erreur_deux_valeurs;

        message.style.color =
            "red";

        return;
    }

    //
    // Calcul déjà effectué
    //

    if (nbValeurs === 3)
    {
        message.innerHTML =
            TXT.calcul_ok;

        message.style.color =
            "green";

        return;
    }

    //
    // Départ + Arrivée -> Temps
    //

    if (
        depart !== ""
        &&
        arrivee !== ""
    )
    {
        const departUs =
            todToUs(depart);

        const arriveeUs =
            todToUs(arrivee);

        if (
            arriveeUs <
            departUs
        )
        {
            message.innerHTML =
                TXT.erreur_arrivee;

            message.style.color =
                "red";

            return;
        }

        const tempsUs =
            arriveeUs -
            departUs;

        const precisionTemps =
            parseInt(
                document
                    .getElementById(
                        "precision_temps"
                    )
                    .value
            );

        document
            .getElementById(
                "temps_course"
            )
            .value =
            usToDuration(
                tempsUs,
                precisionTemps
            );

        message.innerHTML =
            TXT.calcul_ok;

        message.style.color =
            "green";

        return;
    }

    //
    // Départ + Temps -> Arrivée
    //

    if (
        depart !== ""
        &&
        temps !== ""
    )
    {
        const departUs =
            todToUs(
                depart
            );

        const tempsUs =
            durationToUs(
                temps
            );

        const arriveeUs =
            departUs +
            tempsUs;

        const precisionTod =
            parseInt(
                document
                    .getElementById(
                        "precision_tod"
                    )
                    .value
            );

        document
            .getElementById(
                "heure_arrivee"
            )
            .value =
            usToTod(
                arriveeUs,
                precisionTod
            );

        message.innerHTML =
            TXT.calcul_ok;

        message.style.color =
            "green";

        return;
    }

    //
    // Arrivée + Temps -> Départ
    //

    if (
        arrivee !== ""
        &&
        temps !== ""
    )
    {
        const arriveeUs =
            todToUs(
                arrivee
            );

        const tempsUs =
            durationToUs(
                temps
            );

        const departUs =
            arriveeUs -
            tempsUs;

        if (
            departUs < 0
        )
        {
            message.innerHTML =
                TXT.erreur_negative;

            message.style.color =
                "red";

            return;
        }

        const precisionTod =
            parseInt(
                document
                    .getElementById(
                        "precision_tod"
                    )
                    .value
            );

        document
            .getElementById(
                "heure_depart"
            )
            .value =
            usToTod(
                departUs,
                precisionTod
            );

        message.innerHTML =
            TXT.calcul_ok;

        message.style.color =
            "green";

        return;
    }
}

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

function formaterDuree(chiffres, precision)
{
    let max = 6 + precision;

    chiffres = chiffres.substring(0, max);

    let resultat = "";

    if (chiffres.length >= 1)
        resultat += chiffres.substring(
            0,
            Math.min(2, chiffres.length)
        );

    if (chiffres.length > 2)
        resultat += ":" + chiffres.substring(
            2,
            Math.min(4, chiffres.length)
        );

    if (chiffres.length > 4)
        resultat += ":" + chiffres.substring(
            4,
            Math.min(6, chiffres.length)
        );

    if (chiffres.length > 6)
        resultat += "." + chiffres.substring(6);

    return resultat;
}

function formaterChampTOD(idChamp)
{
    document
        .getElementById(idChamp)
        .addEventListener(
            "input",
            function()
            {
                let precision =
                    parseInt(
                        document
                            .getElementById(
                                "precision_tod"
                            )
                            .value
                    );

                let chiffres =
                    this.value.replace(
                        /\D/g,
                        ""
                    );

                this.value =
                    formaterTemps(
                        chiffres,
                        precision
                    );
            }
        );
}

function mettreAJourTOD()
{
    const precision =
        parseInt(
            document
                .getElementById(
                    "precision_tod"
                )
                .value
        );

    [
        "heure_depart",
        "heure_arrivee"
    ]
    .forEach(
        function(id)
        {
            let champ =
                document.getElementById(id);

            let chiffres =
                champ.value.replace(
                    /\D/g,
                    ""
                );

            if (chiffres.length > 6)
            {
                let partieFixe =
                    chiffres.substring(0, 6);

                let decimales =
                    chiffres.substring(6);

                decimales =
                    decimales.padEnd(
                        precision,
                        "0"
                    );

                chiffres =
                    partieFixe +
                    decimales;
            }

            champ.value =
                formaterTemps(
                    chiffres,
                    precision
                );
        }
    );
}

function mettreAJourDuree()
{
    const precision =
        parseInt(
            document
                .getElementById(
                    "precision_temps"
                )
                .value
        );

    let champ =
        document.getElementById(
            "temps_course"
        );

    let chiffres =
        champ.value.replace(
            /\D/g,
            ""
        );

    if (chiffres.length > 6)
    {
        let partieFixe =
            chiffres.substring(0, 6);

        let decimales =
            chiffres.substring(6);

        decimales =
            decimales.padEnd(
                precision,
                "0"
            );

        chiffres =
            partieFixe +
            decimales;
    }

    champ.value =
        formaterDuree(
            chiffres,
            precision
        );
}

function todValide(tod)
{
    const morceaux = tod.match(
        /^(\d{2}):(\d{2}):(\d{2})(\.\d+)?$/
    );

    if (!morceaux)
        return false;

    const hh = parseInt(morceaux[1]);
    const mm = parseInt(morceaux[2]);
    const ss = parseInt(morceaux[3]);

    return (
        hh < 24 &&
        mm < 60 &&
        ss < 60
    );
}

function dureeValide(duree)
{
    const morceaux = duree.match(
        /^(\d{2}):(\d{2}):(\d{2})(\.\d+)?$/
    );

    if (!morceaux)
        return false;

    const mm = parseInt(morceaux[2]);
    const ss = parseInt(morceaux[3]);

    return (
        mm < 60 &&
        ss < 60
    );
}

formaterChampTOD("heure_depart");
formaterChampTOD("heure_arrivee");

document
    .getElementById("heure_depart")
    .addEventListener(
        "input",
        function()
        {
            let precision =
                parseInt(
                    document
                        .getElementById(
                            "precision_tod"
                        )
                        .value
                );

            let chiffres =
                this.value.replace(
                    /\D/g,
                    ""
                );

            this.value =
                formaterTemps(
                    chiffres,
                    precision
                );
        }
    );

//
// Formatage Heure de départ
//

document
    .getElementById("heure_depart")
    .addEventListener(
        "input",
        function ()
        {
            let precision =
                parseInt(
                    document
                        .getElementById(
                            "precision_tod"
                        )
                        .value
                );

            let chiffres =
                this.value.replace(
                    /\D/g,
                    ""
                );

            this.value =
                formaterTemps(
                    chiffres,
                    precision
                );
        }
    );

//
// Formatage Heure d'arrivée
//

document
    .getElementById("heure_arrivee")
    .addEventListener(
        "input",
        function ()
        {
            let precision =
                parseInt(
                    document
                        .getElementById(
                            "precision_tod"
                        )
                        .value
                );

            let chiffres =
                this.value.replace(
                    /\D/g,
                    ""
                );

            this.value =
                formaterTemps(
                    chiffres,
                    precision
                );
        }
    );

//
// Formatage Temps de course
//

document
    .getElementById("temps_course")
    .addEventListener(
        "input",
        function ()
        {
            let precision =
                parseInt(
                    document
                        .getElementById(
                            "precision_temps"
                        )
                        .value
                );

            let chiffres =
                this.value.replace(
                    /\D/g,
                    ""
                );

            this.value =
                formaterDuree(
                    chiffres,
                    precision
                );
        }
    );

document
    .getElementById("effacer")
    .addEventListener(
        "click",
        function ()
        {
            document
                .getElementById(
                    "heure_depart"
                )
                .value = "";

            document
                .getElementById(
                    "heure_arrivee"
                )
                .value = "";

            document
                .getElementById(
                    "temps_course"
                )
                .value = "";

            document
                .getElementById(
                    "message_validation"
                )
                .innerHTML = "";
        }
    );

document
    .getElementById(
        "precision_tod"
    )
    .addEventListener(
        "change",
        function ()
        {
            sessionStorage.setItem(
                "precision_tod",
                this.value
            );

            mettreAJourTOD();
        }
    );

document
    .getElementById(
        "precision_temps"
    )
    .addEventListener(
        "change",
        function ()
        {
            sessionStorage.setItem(
                "precision_temps",
                this.value
            );

            mettreAJourDuree();
        }
    );

//
// Restauration des précisions
//

const precisionTodSauvee =
    sessionStorage.getItem(
        "precision_tod"
    );

if (precisionTodSauvee)
{
    document
        .getElementById(
            "precision_tod"
        )
        .value =
        precisionTodSauvee;
}

const precisionTempsSauvee =
    sessionStorage.getItem(
        "precision_temps"
    );

if (precisionTempsSauvee)
{
    document
        .getElementById(
            "precision_temps"
        )
        .value =
        precisionTempsSauvee;
}