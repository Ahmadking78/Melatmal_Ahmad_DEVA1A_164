"""Gestion des "routes" FLASK et des données pour les formation.
Fichier : gestion_formation_crud.py
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
from App_Plateforme_Recherche_Emploi.formation.gestion_formation_wtf_forms import FormWTFAjouterformation
from App_Plateforme_Recherche_Emploi.formation.gestion_formation_wtf_forms import FormWTFDeleteformation
from App_Plateforme_Recherche_Emploi.formation.gestion_formation_wtf_forms import FormWTFUpdateformation

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /formation_afficher
    
    Test : ex : http://127.0.0.1:5575/formation_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_formation_sel = 0 >> tous les formation.
                id_formation_sel = "n" affiche le formation dont l'id est "n"
"""

class ExceptionformationAfficher(Exception):
    pass

@app.route("/formation_afficher/<string:order_by>/<int:id_formation_sel>", methods=['GET', 'POST'])
def formation_afficher(order_by, id_formation_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_formation_sel == 0:
                    strsql_formation_afficher = """SELECT ID_Formation, FK_Candidat, Etablissement, Diplome, Domaine, Date_Debut, Date_Fin, Description FROM t_formation ORDER BY ID_Formation ASC"""
                    mc_afficher.execute(strsql_formation_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_formation"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du formation sélectionné avec un nom de variable
                    valeur_id_formation_selected_dictionnaire = {"value_id_formation_selected": id_formation_sel}
                    strsql_formation_afficher = """SELECT ID_Formation, FK_Candidat, Etablissement, Diplome, Domaine, Date_Debut, Date_Fin, Description  FROM t_formation WHERE ID_Formation = %(value_id_formation_selected)s"""

                    mc_afficher.execute(strsql_formation_afficher, valeur_id_formation_selected_dictionnaire)
                else:
                    strsql_formation_afficher = """SELECT ID_Formation, FK_Candidat, Etablissement, Diplome, Domaine, Date_Debut, Date_Fin, Description  FROM t_formation ORDER BY ID_Formation DESC"""

                    mc_afficher.execute(strsql_formation_afficher)

                data_formation = mc_afficher.fetchall()

                print("data_formation ", data_formation, " Type : ", type(data_formation))

                # Différencier les messages si la table est vide.
                if not data_formation and id_formation_sel == 0:
                    flash("""La table "t_formation" est vide. !!""", "warning")
                elif not data_formation and id_formation_sel > 0:
                    # Si l'utilisateur change l'id_formation dans l'URL et que le formation n'existe pas,
                    flash(f"Le formation demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_formation" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données formation affichés !!", "success")

        except Exception as Exception_formation_afficher:
            raise ExceptionformationAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{formation_afficher.__name__} ; "
                                          f"{Exception_formation_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("formation/formation_afficher.html", data=data_formation)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /formation_ajouter
    
    Test : ex : http://127.0.0.1:5575/formation_ajouter
    
    Paramètres : sans
    
    But : Ajouter un formation pour un film
    
    Remarque :  Dans le champ "name_formation_html" du formulaire "formation/formation_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class ExceptionformationAjouterWtf(Exception):
    pass


@app.route("/formation_ajouter", methods=['GET', 'POST'])
def formation_ajouter_wtf():
    form = FormWTFAjouterformation()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                id_formation = form.ID_Formation.data
                fk_candidat = form.FK_Candidat.data
                etablissement = form.Etablissement.data
                diplome = form.Diplome.data
                domaine = form.Domaine.data
                date_debut = form.Date_Debut.data
                date_fin = form.Date_Fin.data
                description = form.Description.data
                
                valeurs_insertion_dictionnaire = {
                    "value_id_formation": id_formation,
                    "value_fk_candidat": fk_candidat,
                    "value_etablissement": etablissement,
                    "value_diplome": diplome,
                    "value_domaine": domaine,
                    "value_date_debut": date_debut,
                    "value_date_fin": date_fin,
                    "value_description": description
                }

                strsql_insert_formation = """INSERT INTO t_formation (ID_Formation, FK_Candidat, Etablissement, Diplome, Domaine, Date_Debut, Date_Fin, Description) VALUES (%(value_id_formation)s, %(value_fk_candidat)s, %(value_etablissement)s, %(value_diplome)s, %(value_domaine)s, %(value_date_debut)s, %(value_date_fin)s, %(value_description)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_formation, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Redirect to the page to view all formations
                return redirect(url_for('formation_afficher', order_by='ASC', id_formation_sel=0))

        except Exception as Exception_formation_ajouter_wtf:
            raise ExceptionformationAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{formation_ajouter_wtf.__name__} ; "
                                            f"{Exception_formation_ajouter_wtf}")

    return render_template("formation/formation_ajouter_wtf.html", form=form)



"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /formation_update
    
    Test : ex cliquer sur le menu "formation" puis cliquer sur le bouton "EDIT" d'un "formation"
    
    Paramètres : sans
    
    But : Editer(update) un formation qui a été sélectionné dans le formulaire "formation_afficher.html"
    
    Remarque :  Dans le champ "nom_formation_update_wtf" du formulaire "formation/formation_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class ExceptionformationUpdateWtf(Exception):
    pass


@app.route("/formation_update", methods=['GET', 'POST'])
def formation_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_formation"
    id_formation_update = request.values['id_formation_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateformation()
    try:
        if request.method == "POST" and form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "formation_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.

            valeur_update_dictionnaire = {
                "ID_Formation": form_update.ID_Formation.data,
                "FK_Candidat": form_update.FK_Candidat.data,
                "Etablissement": form_update.Etablissement.data,
                "Diplome": form_update.Diplome.data,
                "Domaine": form_update.Domaine.data,
                "Date_Debut": form_update.Date_Debut.data,
                "Date_Fin": form_update.Date_Fin.data,
                "Description": form_update.Description.data
            }

            str_sql_update_intituleformation = """UPDATE t_formation SET 
                                                  FK_Candidat = %(FK_Candidat)s,
                                                  Etablissement = %(Etablissement)s,
                                                  Diplome = %(Diplome)s,
                                                  Domaine = %(Domaine)s,
                                                  Date_Debut = %(Date_Debut)s,
                                                  Date_Fin = %(Date_Fin)s,
                                                  Description = %(Description)s
                                                  WHERE ID_Formation = %(ID_Formation)s"""

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleformation, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_formation_update"
            return redirect(url_for('formation_afficher', order_by="ASC", id_formation_sel=id_formation_update))
        
        elif request.method == "GET":
            # Opération sur la BD pour récupérer les données du formation à mettre à jour
            str_sql_id_formation = "SELECT * FROM t_formation " \
                                   "WHERE ID_Formation = %(value_id_formation)s"
            valeur_select_dictionnaire = {"value_id_formation": id_formation_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_formation, valeur_select_dictionnaire)
                formation_data = mybd_conn.fetchone()

            # Afficher les valeurs sélectionnées dans les champs du formulaire "formation_update_wtf.html"
            if formation_data:
                form_update.ID_Formation.data = formation_data["ID_Formation"]
                form_update.FK_Candidat.data = formation_data["FK_Candidat"]
                form_update.Etablissement.data = formation_data["Etablissement"]
                form_update.Diplome.data = formation_data["Diplome"]
                form_update.Domaine.data = formation_data["Domaine"]
                form_update.Date_Debut.data = formation_data["Date_Debut"]
                form_update.Date_Fin.data = formation_data["Date_Fin"]
                form_update.Description.data = formation_data["Description"]

    except Exception as Exception_formation_update_wtf:
        raise ExceptionformationUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                          f"{formation_update_wtf.__name__} ; "
                                          f"{Exception_formation_update_wtf}")

    return render_template("formation/formation_update_wtf.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /formation_delete
    
    Test : ex. cliquer sur le menu "formation" puis cliquer sur le bouton "DELETE" d'un "formation"
    
    Paramètres : sans
    
    But : Effacer(delete) un formation qui a été sélectionné dans le formulaire "formation_afficher.html"
    
    Remarque :  Dans le champ "nom_formation_delete_wtf" du formulaire "formation/formation_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""

class ExceptionformationDeleteWtf(Exception):
    pass


@app.route("/formation_delete", methods=['GET', 'POST'])
def formation_delete_wtf():
    data_films_attribue_formation_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_formation"
    id_formation_delete = request.values['id_formation_btn_delete_html']

    # Objet formulaire pour effacer le formation sélectionné.
    form_delete = FormWTFDeleteformation()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("formation_afficher", order_by="ASC", id_formation_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "formation/formation_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_formation_delete = session['data_films_attribue_formation_delete']
                print("data_films_attribue_formation_delete ", data_films_attribue_formation_delete)

                flash(f"Effacer le formation de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer formation" qui va irrémédiablement EFFACER le formation
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_formation": id_formation_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_formation = """DELETE FROM t_formation WHERE ID_Formation = %(value_id_formation)s"""
                str_sql_delete_idformation = """DELETE FROM t_formation WHERE ID_Formation = %(value_id_formation)s"""
                # Manière brutale d'effacer d'abord la "fk_formation", même si elle n'existe pas dans la "t_formation_film"
                # Ensuite on peut effacer le formation vu qu'il n'est plus "lié" (INNODB) dans la "t_formation_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_formation, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idformation, valeur_delete_dictionnaire)

                flash(f"formation définitivement effacé !!", "success")
                print(f"formation définitivement effacé !!")

                # afficher les données
                return redirect(url_for('formation_afficher', order_by="ASC", id_formation_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_formation": id_formation_delete}
            print(id_formation_delete, type(id_formation_delete))

            # Requête qui affiche tous les films_formation qui ont le formation que l'utilisateur veut effacer
            str_sql_formation_films_delete = """SELECT * FROM t_formation WHERE ID_Formation = %(value_id_formation)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_formation_films_delete, valeur_select_dictionnaire)
                data_films_attribue_formation_delete = mydb_conn.fetchall()
                print("data_films_attribue_formation_delete...", data_films_attribue_formation_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "formation/formation_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_formation_delete'] = data_films_attribue_formation_delete

                # Opération sur la BD pour récupérer "id_formation" et "intitule_formation" de la "t_formation"
                str_sql_id_formation = "SELECT * FROM t_formation WHERE ID_Formation = %(value_id_formation)s"

                mydb_conn.execute(str_sql_id_formation, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom formation" pour l'action DELETE
                data_nom_formation = mydb_conn.fetchone()
                print("data_nom_formation ", data_nom_formation, " type ", type(data_nom_formation), " formation ",
                      data_nom_formation["FK_Candidat"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "formation_delete_wtf.html"
            form_delete.nom_formation_delete_wtf.data = data_nom_formation["FK_Candidat"]

            # Le bouton pour l'action "DELETE" dans le form. "formation_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_formation_delete_wtf:
        raise ExceptionformationDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{formation_delete_wtf.__name__} ; "
                                      f"{Exception_formation_delete_wtf}")

    return render_template("formation/formation_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_formation_delete)
