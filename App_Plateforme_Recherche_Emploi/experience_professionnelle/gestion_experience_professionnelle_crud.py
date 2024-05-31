"""Gestion des "routes" FLASK et des données pour les experience_professionnelle.
Fichier : gestion_experience_professionnelle_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from App_Plateforme_Recherche_Emploi import app
from App_Plateforme_Recherche_Emploi.database.database_tools import DBconnection
from App_Plateforme_Recherche_Emploi.erreurs.exceptions import *
from App_Plateforme_Recherche_Emploi.experience_professionnelle.gestion_experience_professionnelle_wtf_forms import FormWTFAjouterexperience_professionnelle
from App_Plateforme_Recherche_Emploi.experience_professionnelle.gestion_experience_professionnelle_wtf_forms import FormWTFDeleteexperience_professionnelle
from App_Plateforme_Recherche_Emploi.experience_professionnelle.gestion_experience_professionnelle_wtf_forms import FormWTFUpdateexperience_professionnelle

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /experience_professionnelle_afficher
    
    Test : ex : http://127.0.0.1:5575/experience_professionnelle_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_experience_professionnelle_sel = 0 >> tous les experience_professionnelle.
                id_experience_professionnelle_sel = "n" affiche le experience_professionnelle dont l'id est "n"
"""

class Exceptionexperience_professionnelleAfficher(Exception):
    pass


@app.route("/experience_professionnelle_afficher/<string:order_by>/<int:id_experience_professionnelle_sel>", methods=['GET', 'POST'])
def experience_professionnelle_afficher(order_by, id_experience_professionnelle_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_experience_professionnelle_sel == 0:
                    strsql_experience_professionnelle_afficher = """SELECT ID_Experience, FK_Candidat, Entreprise, Titre_Poste, Date_Debut, Date_Fin, Description FROM t_experience_professionnelle ORDER BY ID_Experience ASC"""
                    mc_afficher.execute(strsql_experience_professionnelle_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_experience_professionnelle"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du experience_professionnelle sélectionné avec un nom de variable
                    valeur_id_experience_professionnelle_selected_dictionnaire = {"value_id_experience_professionnelle_selected": id_experience_professionnelle_sel}
                    strsql_experience_professionnelle_afficher = """SELECT ID_Experience, FK_Candidat, Entreprise, Titre_Poste, Date_Debut, Date_Fin, Description  FROM t_experience_professionnelle WHERE ID_Experience = %(value_id_experience_professionnelle_selected)s"""

                    mc_afficher.execute(strsql_experience_professionnelle_afficher, valeur_id_experience_professionnelle_selected_dictionnaire)
                else:
                    strsql_experience_professionnelle_afficher = """SELECT ID_Experience, FK_Candidat, Entreprise, Titre_Poste, Date_Debut, Date_Fin, Description  FROM t_experience_professionnelle ORDER BY ID_Experience DESC"""

                    mc_afficher.execute(strsql_experience_professionnelle_afficher)

                data_experience_professionnelle = mc_afficher.fetchall()

                print("data_experience_professionnelle ", data_experience_professionnelle, " Type : ", type(data_experience_professionnelle))

                # Différencier les messages si la table est vide.
                if not data_experience_professionnelle and id_experience_professionnelle_sel == 0:
                    flash("""La table "experience_professionnelle" est vide. !!""", "warning")
                elif not data_experience_professionnelle and id_experience_professionnelle_sel > 0:
                    # Si l'utilisateur change l'id_experience_professionnelle dans l'URL et que le experience_professionnelle n'existe pas,
                    flash(f"Le experience professionnelle demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_experience_professionnelle" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données experience professionnelle affichés !!", "success")

        except Exception as Exception_experience_professionnelle_afficher:
            raise Exceptionexperience_professionnelleAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{experience_professionnelle_afficher.__name__} ; "
                                          f"{Exception_experience_professionnelle_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("experience_professionnelle/experience_professionnelle_afficher.html", data=data_experience_professionnelle)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /experience_professionnelle_ajouter
    
    Test : ex : http://127.0.0.1:5575/experience_professionnelle_ajouter
    
    Paramètres : sans
    
    But : Ajouter un experience_professionnelle pour un film
    
    Remarque :  Dans le champ "name_experience_professionnelle_html" du formulaire "experience_professionnelle/experience_professionnelle_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class Exceptionexperience_professionnelleAjouterWtf(Exception):
    pass


@app.route("/experience_professionnelle_ajouter", methods=['GET', 'POST'])
def experience_professionnelle_ajouter_wtf():
    form = FormWTFAjouterexperience_professionnelle()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                id_candidat = form.FK_Candidat.data
                entreprise = form.Entreprise.data
                titre_poste = form.Titre_Poste.data
                date_debut = form.Date_Debut.data
                date_fin = form.Date_Fin.data
                description = form.Description.data
                
                valeurs_insertion_dictionnaire = {
                    "value_id_candidat": id_candidat,
                    "value_entreprise": entreprise,
                    "value_titre_poste": titre_poste,
                    "value_date_debut": date_debut,
                    "value_date_fin": date_fin,
                    "value_description": description
                }

                strsql_insert_experience_professionnelle = """INSERT INTO t_experience_professionnelle 
                    (FK_Candidat, Entreprise, Titre_Poste, Date_Debut, Date_Fin, Description) 
                    VALUES (%(value_id_candidat)s, %(value_entreprise)s, %(value_titre_poste)s, 
                    %(value_date_debut)s, %(value_date_fin)s, %(value_description)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_experience_professionnelle, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Redirect to a relevant page after insertion, for example:
                # return redirect(url_for('some_view_function'))

        except Exception as Exception_experience_professionnelle_ajouter_wtf:
            raise Exceptionexperience_professionnelleAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{experience_professionnelle_ajouter_wtf.__name__} ; "
                                            f"{Exception_experience_professionnelle_ajouter_wtf}")

    return render_template("experience_professionnelle/experience_professionnelle_ajouter_wtf.html", form=form)



"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /experience_professionnelle_update
    
    Test : ex cliquer sur le menu "experience_professionnelle" puis cliquer sur le bouton "EDIT" d'un "experience_professionnelle"
    
    Paramètres : sans
    
    But : Editer(update) un experience_professionnelle qui a été sélectionné dans le formulaire "experience_professionnelle_afficher.html"
    
    Remarque :  Dans le champ "nom_experience_professionnelle_update_wtf" du formulaire "experience_professionnelle/experience_professionnelle_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


class Exceptionexperience_professionnelleUpdateWtf(Exception):
    pass


@app.route("/experience_professionnelle_update", methods=['GET', 'POST'])
def experience_professionnelle_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_experience_professionnelle"
    id_experience_professionnelle_update = request.values['id_experience_professionnelle_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateexperience_professionnelle()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur des champs depuis "experience_professionnelle_update_wtf.html" après avoir cliqué sur "SUBMIT".
            ID_Experience_update = form_update.ID_Experience.data
            FK_Candidat_update = form_update.FK_Candidat.data
            Entreprise_update = form_update.Entreprise.data
            Titre_Poste_update = form_update.Titre_Poste.data
            Date_Debut_update = form_update.Date_Debut.data
            Date_Fin_update = form_update.Date_Fin.data
            Description_update = form_update.Description.data

            valeur_update_dictionnaire = {
                "value_id_experience_professionnelle": id_experience_professionnelle_update,
                "value_ID_Experience": ID_Experience_update,
                "value_FK_Candidat": FK_Candidat_update,
                "value_Entreprise": Entreprise_update,
                "value_Titre_Poste": Titre_Poste_update,
                "value_Date_Debut": Date_Debut_update,
                "value_Date_Fin": Date_Fin_update,
                "value_Description": Description_update
            }

            str_sql_update_intituleexperience_professionnelle = """UPDATE t_experience_professionnelle SET 
                ID_Experience = %(value_ID_Experience)s,
                FK_Candidat = %(value_FK_Candidat)s,
                Entreprise = %(value_Entreprise)s,
                Titre_Poste = %(value_Titre_Poste)s,
                Date_Debut = %(value_Date_Debut)s,
                Date_Fin = %(value_Date_Fin)s,
                Description = %(value_Description)s
                WHERE ID_Experience = %(value_id_experience_professionnelle)s"""

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleexperience_professionnelle, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_experience_professionnelle_update"
            return redirect(url_for('experience_professionnelle_afficher', order_by="ASC", id_experience_professionnelle_sel=id_experience_professionnelle_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer les données du experience_professionnelle à mettre à jour
            str_sql_id_experience_professionnelle = "SELECT * FROM t_experience_professionnelle " \
                               "WHERE ID_Experience = %(value_id_experience_professionnelle)s"
            valeur_select_dictionnaire = {"value_id_experience_professionnelle": id_experience_professionnelle_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_experience_professionnelle, valeur_select_dictionnaire)
                experience_professionnelle_data = mybd_conn.fetchone()

            # Afficher les valeurs sélectionnées dans les champs du formulaire "experience_professionnelle_update_wtf.html"
            if experience_professionnelle_data:
                form_update.ID_Experience.data = experience_professionnelle_data["ID_Experience"]
                form_update.FK_Candidat.data = experience_professionnelle_data["FK_Candidat"]
                form_update.Entreprise.data = experience_professionnelle_data["Entreprise"]
                form_update.Titre_Poste.data = experience_professionnelle_data["Titre_Poste"]
                form_update.Date_Debut.data = experience_professionnelle_data["Date_Debut"]
                form_update.Date_Fin.data = experience_professionnelle_data["Date_Fin"]
                form_update.Description.data = experience_professionnelle_data["Description"]

    except Exception as Exception_experience_professionnelle_update_wtf:
        raise Exceptionexperience_professionnelleUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{experience_professionnelle_update_wtf.__name__} ; "
                                      f"{Exception_experience_professionnelle_update_wtf}")

    return render_template("experience_professionnelle/experience_professionnelle_update_wtf.html", form_update=form_update)





"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /experience_professionnelle_delete
    
    Test : ex. cliquer sur le menu "experience_professionnelle" puis cliquer sur le bouton "DELETE" d'un "experience_professionnelle"
    
    Paramètres : sans
    
    But : Effacer(delete) un experience_professionnelle qui a été sélectionné dans le formulaire "experience_professionnelle_afficher.html"
    
    Remarque :  Dans le champ "nom_experience_professionnelle_delete_wtf" du formulaire "experience_professionnelle/experience_professionnelle_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


class Exceptionexperience_professionnelleDeleteWtf(Exception):
    pass


@app.route("/experience_professionnelle_delete", methods=['GET', 'POST'])
def experience_professionnelle_delete_wtf():
    data_films_attribue_experience_professionnelle_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_experience_professionnelle"
    id_experience_professionnelle_delete = request.values['id_experience_professionnelle_btn_delete_html']

    # Objet formulaire pour effacer le experience_professionnelle sélectionné.
    form_delete = FormWTFDeleteexperience_professionnelle()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("experience_professionnelle_afficher", order_by="ASC", id_experience_professionnelle_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "experience_professionnelle/experience_professionnelle_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_experience_professionnelle_delete = session['data_films_attribue_experience_professionnelle_delete']
                print("data_films_attribue_experience_professionnelle_delete ", data_films_attribue_experience_professionnelle_delete)

                flash(f"Effacer le experience_professionnelle de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer experience_professionnelle" qui va irrémédiablement EFFACER le experience_professionnelle
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_experience_professionnelle": id_experience_professionnelle_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_experience_professionnelle = """DELETE FROM t_experience_professionnelle WHERE ID_Experience = %(value_id_experience_professionnelle)s"""
                str_sql_delete_idexperience_professionnelle = """DELETE FROM t_experience_professionnelle WHERE ID_Experience = %(value_id_experience_professionnelle)s"""
                # Manière brutale d'effacer d'abord la "fk_experience_professionnelle", même si elle n'existe pas dans la "t_experience_professionnelle_film"
                # Ensuite on peut effacer le experience_professionnelle vu qu'il n'est plus "lié" (INNODB) dans la "t_experience_professionnelle_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_experience_professionnelle, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idexperience_professionnelle, valeur_delete_dictionnaire)

                flash(f"experience_professionnelle définitivement effacé !!", "success")
                print(f"experience_professionnelle définitivement effacé !!")

                # afficher les données
                return redirect(url_for('experience_professionnelle_afficher', order_by="ASC", id_experience_professionnelle_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_experience_professionnelle": id_experience_professionnelle_delete}
            print(id_experience_professionnelle_delete, type(id_experience_professionnelle_delete))

            # Requête qui affiche tous les films_experience_professionnelle qui ont le experience_professionnelle que l'utilisateur veut effacer
            str_sql_experience_professionnelle_films_delete = """SELECT * FROM t_experience_professionnelle WHERE ID_Experience = %(value_id_experience_professionnelle)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_experience_professionnelle_films_delete, valeur_select_dictionnaire)
                data_films_attribue_experience_professionnelle_delete = mydb_conn.fetchall()
                print("data_films_attribue_experience_professionnelle_delete...", data_films_attribue_experience_professionnelle_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "experience_professionnelle/experience_professionnelle_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_experience_professionnelle_delete'] = data_films_attribue_experience_professionnelle_delete

                # Opération sur la BD pour récupérer "id_experience_professionnelle" et "intitule_experience_professionnelle" de la "t_experience_professionnelle"
                str_sql_id_experience_professionnelle = "SELECT * FROM t_experience_professionnelle WHERE ID_Experience = %(value_id_experience_professionnelle)s"

                mydb_conn.execute(str_sql_id_experience_professionnelle, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom experience_professionnelle" pour l'action DELETE
                data_nom_experience_professionnelle = mydb_conn.fetchone()
                print("data_nom_experience_professionnelle ", data_nom_experience_professionnelle, " type ", type(data_nom_experience_professionnelle), " experience_professionnelle ",
                      data_nom_experience_professionnelle["FK_Candidat"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "experience_professionnelle_delete_wtf.html"
            form_delete.nom_experience_professionnelle_delete_wtf.data = data_nom_experience_professionnelle["FK_Candidat"]

            # Le bouton pour l'action "DELETE" dans le form. "experience_professionnelle_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_experience_professionnelle_delete_wtf:
        raise Exceptionexperience_professionnelleDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{experience_professionnelle_delete_wtf.__name__} ; "
                                      f"{Exception_experience_professionnelle_delete_wtf}")

    return render_template("experience_professionnelle/experience_professionnelle_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_experience_professionnelle_delete)

