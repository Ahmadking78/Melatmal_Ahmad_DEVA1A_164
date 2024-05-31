"""Initialisation des variables d'environnement
    Auteur : OM 2023.03.21 Indispensable pour définir les variables indispensables dans tout le projet.
"""
import sys

from environs import Env
from flask import Flask

try:
    try:
        obj_env = Env()
        obj_env.read_env()
        HOST_MYSQL = obj_env("HOST_MYSQL")
        USER_MYSQL = obj_env("USER_MYSQL")
        PASS_MYSQL = obj_env("PASS_MYSQL")
        PORT_MYSQL = int(obj_env("PORT_MYSQL"))
        NAME_BD_MYSQL = obj_env("NAME_BD_MYSQL")
        NAME_FILE_DUMP_SQL_BD = obj_env("NAME_FILE_DUMP_SQL_BD")

        ADRESSE_SRV_FLASK = obj_env("ADRESSE_SRV_FLASK")
        DEBUG_FLASK = obj_env("DEBUG_FLASK")
        PORT_FLASK = obj_env("PORT_FLASK")
        SECRET_KEY_FLASK = obj_env("SECRET_KEY_FLASK")

        # OM 2022.04.11 Début de l'application
        app = Flask(__name__, template_folder="templates")
        print("app.url_map ____> ", app.url_map)

    except Exception as erreur:
        print(f"45677564530 init application variables d'environnement ou avec le fichier (son nom, son contenu)\n"
              f"{__name__}, "
              f"{erreur.args[0]}, "
              f"{repr(erreur)}, "
              f"{type(erreur)}")
        sys.exit()

    """
        Tout commence ici. Il faut "indiquer" les routes de l'applicationn.    
        Dans l'application les lignes ci-dessous doivent se trouver ici... soit après l'instanciation de la classe "Flask"
    """
    from App_Plateforme_Recherche_Emploi.database import database_tools
    from App_Plateforme_Recherche_Emploi.essais_wtf_forms import gestion_essai_wtf
    from App_Plateforme_Recherche_Emploi.essais_wtf_forms import gestion_wtf_forms_demo_select
    from App_Plateforme_Recherche_Emploi.demos_om_164 import routes_demos

    from App_Plateforme_Recherche_Emploi.erreurs import msg_avertissements

    from App_Plateforme_Recherche_Emploi.candidat import gestion_candidat_crud
    from App_Plateforme_Recherche_Emploi.candidat import gestion_candidat_wtf_forms

    from App_Plateforme_Recherche_Emploi.competence import gestion_competence_crud
    from App_Plateforme_Recherche_Emploi.competence import gestion_competence_wtf_forms

    from App_Plateforme_Recherche_Emploi.employeur import gestion_employeur_crud
    from App_Plateforme_Recherche_Emploi.employeur import gestion_employeur_wtf_forms

    from App_Plateforme_Recherche_Emploi.candidature import gestion_candidature_crud
    from App_Plateforme_Recherche_Emploi.candidature import gestion_candidature_wtf_forms

    from App_Plateforme_Recherche_Emploi.competences_candidat import gestion_competences_candidat_crud
    from App_Plateforme_Recherche_Emploi.competences_candidat import gestion_competences_candidat_wtf_forms

    from App_Plateforme_Recherche_Emploi.experience_professionnelle import gestion_experience_professionnelle_crud
    from App_Plateforme_Recherche_Emploi.experience_professionnelle import gestion_experience_professionnelle_wtf_forms

    from App_Plateforme_Recherche_Emploi.formation import gestion_formation_crud
    from App_Plateforme_Recherche_Emploi.formation import gestion_formation_wtf_forms

    from App_Plateforme_Recherche_Emploi.offre_emploi import gestion_offre_emploi_crud
    from App_Plateforme_Recherche_Emploi.offre_emploi import gestion_offre_emploi_wtf_forms

   

except Exception as Exception_init_App_Plateforme_Recherche_Emploi:
    print(f"4567756434 Une erreur est survenue {type(Exception_init_App_Plateforme_Recherche_Emploi)} dans"
          f"__init__ {Exception_init_App_Plateforme_Recherche_Emploi.args}")
    sys.exit()
