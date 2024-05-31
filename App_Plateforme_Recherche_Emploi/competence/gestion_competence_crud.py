"""Gestion des "routes" FLASK et des données pour les competence.
Fichier : gestion_competenceure_crud.py
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
from App_Plateforme_Recherche_Emploi.competence.gestion_competence_wtf_forms import FormWTFAjoutercompetence
from App_Plateforme_Recherche_Emploi.competence.gestion_competence_wtf_forms import FormWTFDeletecompetence
from App_Plateforme_Recherche_Emploi.competence.gestion_competence_wtf_forms import FormWTFUpdatecompetence

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /competence_afficher
    
    Test : ex : http://127.0.0.1:5575/competence_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_competence_sel = 0 >> tous les competence.
                id_competence_sel = "n" affiche le competence dont l'id est "n"
"""

class ExceptioncompetenceAfficher(Exception):
    pass


@app.route("/competence_afficher/<string:order_by>/<int:id_competence_sel>", methods=['GET', 'POST'])
def competence_afficher(order_by, id_competence_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_competence_sel == 0:
                    strsql_competence_afficher = """SELECT * FROM t_competence ORDER BY ID_Competence ASC"""
                    mc_afficher.execute(strsql_competence_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_competence"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du competence sélectionné avec un nom de variable
                    valeur_id_competence_selected_dictionnaire = {"value_id_competence_selected": id_competence_sel}
                    strsql_competence_afficher = """SELECT *  FROM t_competence WHERE ID_Competence = %(value_id_competence_selected)s"""

                    mc_afficher.execute(strsql_competence_afficher, valeur_id_competence_selected_dictionnaire)
                else:
                    strsql_competence_afficher = """SELECT *  FROM t_competence ORDER BY ID_Competence DESC"""

                    mc_afficher.execute(strsql_competence_afficher)

                data_competence = mc_afficher.fetchall()

                print("data_competence ", data_competence, " Type : ", type(data_competence))

                # Différencier les messages si la table est vide.
                if not data_competence and id_competence_sel == 0:
                    flash("""La table "t_competence" est vide. !!""", "warning")
                elif not data_competence and id_competence_sel > 0:
                    # Si l'utilisateur change l'id_competence dans l'URL et que le competence n'existe pas,
                    flash(f"Le competence demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_competence" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données competence affichés !!", "success")

        except Exception as Exception_competence_afficher:
            raise ExceptioncompetenceAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{competence_afficher.__name__} ; "
                                          f"{Exception_competence_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("competence/competence_afficher.html", data=data_competence)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /competence_ajouter
    
    Test : ex : http://127.0.0.1:5575/competence_ajouter
    
    Paramètres : sans
    
    But : Ajouter un competence pour un film
    
    Remarque :  Dans le champ "name_competence_html" du formulaire "competence/competence_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class ExceptioncompetenceAjouterWtf(Exception):
    pass

@app.route("/competence_ajouter", methods=['GET', 'POST'])
def competence_ajouter_wtf():
    form = FormWTFAjoutercompetence()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                id_competence = form.ID_Competence.data
                name_competence = form.nom_competence_wtf.data
                description_competence = form.description_competence.data
                
                valeurs_insertion_dictionnaire = {
                    "value_ID_Competence": id_competence,
                    "value_nom_competence": name_competence,
                    "value_description_competence": description_competence
                }

                strsql_insert_competence = """INSERT INTO t_competence (ID_Competence, Nom_Competence, Description)
                                              VALUES (%(value_ID_Competence)s, %(value_nom_competence)s, %(value_description_competence)s)"""
                
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_competence, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('competence_afficher', order_by='ASC', id_competence_sel=0))

        except Exception as Exception_competence_ajouter_wtf:
            raise Exception(f"fichier : {Path(__file__).name}  ;  "
                            f"competence_ajouter_wtf ; "
                            f"{Exception_competence_ajouter_wtf}")

    return render_template("competence/competence_ajouter_wtf.html", form=form)




"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /competence_update
    
    Test : ex cliquer sur le menu "competence" puis cliquer sur le bouton "EDIT" d'un "competence"
    
    Paramètres : sans
    
    But : Editer(update) un competence qui a été sélectionné dans le formulaire "competence_afficher.html"
    
    Remarque :  Dans le champ "nom_competence_update_wtf" du formulaire "competence/competence_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class ExceptioncompetenceUpdateWtf(Exception):
    pass

@app.route("/competence_update", methods=['GET', 'POST'])
def competence_update_wtf():
    id_competence_update = request.values['id_competence_btn_edit_html']
    form_update = FormWTFUpdatecompetence()
    try:
        if request.method == "POST" and form_update.submit.data:
            Nom_Competence_update = form_update.Nom_Competence_update_wtf.data
            Description_competence_update = form_update.Description_competence_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_competence": id_competence_update,
                "value_Nom_Competence": Nom_Competence_update,
                "value_Description_competence": Description_competence_update,
            }

            str_sql_update_intitulecompetence = """UPDATE t_competence SET 
                Nom_competence = %(value_Nom_Competence)s, 
                Description = %(value_Description_competence)s
                WHERE ID_Competence = %(value_id_competence)s"""

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulecompetence, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            return redirect(url_for('competence_afficher', order_by="ASC", id_competence_sel=id_competence_update))
        
        elif request.method == "GET":
            str_sql_id_competence = "SELECT * FROM t_competence WHERE ID_Competence = %(value_id_competence)s"
            valeur_select_dictionnaire = {"value_id_competence": id_competence_update}
            
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_competence, valeur_select_dictionnaire)
                competence_data = mybd_conn.fetchone()

            if competence_data:
                form_update.ID_Competence_update_wtf.data = competence_data["ID_Competence"]
                form_update.Nom_Competence_update_wtf.data = competence_data["Nom_Competence"]
                form_update.Description_competence_update_wtf.data = competence_data["Description"]

    except Exception as Exception_competence_update_wtf:
        raise ExceptioncompetenceUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{competence_update_wtf.__name__} ; "
                                      f"{Exception_competence_update_wtf}")

    return render_template("competence/competence_update_wtf.html", form_update=form_update)




"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /competence_delete
    
    Test : ex. cliquer sur le menu "competence" puis cliquer sur le bouton "DELETE" d'un "competence"
    
    Paramètres : sans
    
    But : Effacer(delete) un competence qui a été sélectionné dans le formulaire "competence_afficher.html"
    
    Remarque :  Dans le champ "nom_competence_delete_wtf" du formulaire "competence/competence_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""

class ExceptioncompetenceDeleteWtf(Exception):
    pass


@app.route("/competence_delete", methods=['GET', 'POST'])
def competence_delete_wtf():
    data_films_attribue_competence_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_competence"
    id_competence_delete = request.values['id_competence_btn_delete_html']

    # Objet formulaire pour effacer le competence sélectionné.
    form_delete = FormWTFDeletecompetence()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("competence_afficher", order_by="ASC", id_competence_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "competence/competence_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_competence_delete = session['data_films_attribue_competence_delete']
                print("data_films_attribue_competence_delete ", data_films_attribue_competence_delete)

                flash(f"Effacer le competence de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer competence" qui va irrémédiablement EFFACER le competence
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_competence": id_competence_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_competence = """DELETE FROM t_competence WHERE ID_Competence = %(value_id_competence)s"""
                str_sql_delete_idcompetence = """DELETE FROM t_competence WHERE ID_Competence = %(value_id_competence)s"""
                # Manière brutale d'effacer d'abord la "fk_competence", même si elle n'existe pas dans la "t_competence_film"
                # Ensuite on peut effacer le competence vu qu'il n'est plus "lié" (INNODB) dans la "t_competence_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_competence, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idcompetence, valeur_delete_dictionnaire)

                flash(f"competence définitivement effacé !!", "success")
                print(f"competence définitivement effacé !!")

                # afficher les données
                return redirect(url_for('competence_afficher', order_by="ASC", id_competence_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_competence": id_competence_delete}
            print(id_competence_delete, type(id_competence_delete))

            # Requête qui affiche tous les films_competence qui ont le competence que l'utilisateur veut effacer
            str_sql_competence_films_delete = """SELECT * FROM t_competence WHERE ID_Competence = %(value_id_competence)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_competence_films_delete, valeur_select_dictionnaire)
                data_films_attribue_competence_delete = mydb_conn.fetchall()
                print("data_films_attribue_competence_delete...", data_films_attribue_competence_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "competence/competence_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_competence_delete'] = data_films_attribue_competence_delete

                # Opération sur la BD pour récupérer "id_competence" et "intitule_competence" de la "t_competence"
                str_sql_id_competence = "SELECT * FROM t_competence WHERE ID_Competence = %(value_id_competence)s"

                mydb_conn.execute(str_sql_id_competence, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom competence" pour l'action DELETE
                data_nom_competence = mydb_conn.fetchone()
                print("data_nom_competence ", data_nom_competence, " type ", type(data_nom_competence), " competence ",
                      data_nom_competence["Nom_Competence"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "competence_delete_wtf.html"
            form_delete.nom_competence_delete_wtf.data = data_nom_competence["Nom_Competence"]

            # Le bouton pour l'action "DELETE" dans le form. "competence_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_competence_delete_wtf:
        raise ExceptioncompetenceDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{competence_delete_wtf.__name__} ; "
                                      f"{Exception_competence_delete_wtf}")

    return render_template("competence/competence_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_competence_delete)
