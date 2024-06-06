"""Gestion des "routes" FLASK et des données pour les candidature.
Fichier : gestion_candidature_crud.py
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
from App_Plateforme_Recherche_Emploi.candidature.gestion_candidature_wtf_forms import FormWTFAjoutercandidature
from App_Plateforme_Recherche_Emploi.candidature.gestion_candidature_wtf_forms import FormWTFDeletecandidature
from App_Plateforme_Recherche_Emploi.candidature.gestion_candidature_wtf_forms import FormWTFUpdatecandidature

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /candidature_afficher
    
    Test : ex : http://127.0.0.1:5575/candidature_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_candidature_sel = 0 >> tous les candidature.
                id_candidature_sel = "n" affiche le candidature dont l'id est "n"
"""

class ExceptioncandidatureAfficher(Exception):
    pass

@app.route("/candidature_afficher/<string:order_by>/<int:id_candidature_sel>", methods=['GET', 'POST'])
def candidature_afficher(order_by, id_candidature_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_candidature_sel == 0:
                    strsql_candidature_afficher = """SELECT ID_Candidature, FK_Candidat, FK_Offre, Date_Candidature, Lettre_Motivation, Statut FROM t_candidature ORDER BY ID_Candidature ASC"""
                    mc_afficher.execute(strsql_candidature_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_candidature"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du candidature sélectionné avec un nom de variable
                    valeur_id_candidature_selected_dictionnaire = {"value_id_candidature_selected": id_candidature_sel}
                    strsql_candidature_afficher = """SELECT ID_Candidature, FK_Candidat, FK_Offre, Date_Candidature, Lettre_Motivation, Statut  FROM t_candidature WHERE ID_Candidature = %(value_id_candidature_selected)s"""

                    mc_afficher.execute(strsql_candidature_afficher, valeur_id_candidature_selected_dictionnaire)
                else:
                    strsql_candidature_afficher = """SELECT ID_Candidature, FK_Candidat, FK_Offre, Date_Candidature, Lettre_Motivation, Statut  FROM t_candidature ORDER BY ID_Candidature DESC"""

                    mc_afficher.execute(strsql_candidature_afficher)

                data_candidature = mc_afficher.fetchall()

                print("data_candidature ", data_candidature, " Type : ", type(data_candidature))

                # Différencier les messages si la table est vide.
                if not data_candidature and id_candidature_sel == 0:
                    flash("""La table "t_candidature" est vide. !!""", "warning")
                elif not data_candidature and id_candidature_sel > 0:
                    # Si l'utilisateur change l'id_candidature dans l'URL et que le candidature n'existe pas,
                    flash(f"Le candidature demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_candidature" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données candidature affichés !!", "success")

        except Exception as Exception_candidature_afficher:
            raise ExceptioncandidatureAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{candidature_afficher.__name__} ; "
                                          f"{Exception_candidature_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("candidature/candidature_afficher.html", data=data_candidature)



"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /candidature_ajouter
    
    Test : ex : http://127.0.0.1:5575/candidature_ajouter
    
    Paramètres : sans
    
    But : Ajouter un candidature pour un film
    
    Remarque :  Dans le champ "name_candidature_html" du formulaire "candidature/candidature_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class ExceptioncandidatureAjouterWtf(Exception):
    pass


@app.route("/candidature_ajouter", methods=['GET', 'POST'])
def candidature_ajouter_wtf():
    form = FormWTFAjoutercandidature()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                ID_Candidature = form.ID_Candidature.data
                FK_Candidat = form.FK_Candidat.data
                FK_Offre = form.FK_Offre.data
                Date_Candidature = form.Date_Candidature.data
                Lettre_Motivation = form.Lettre_Motivation.data
                Statut = form.Statut.data

                valeurs_insertion_dictionnaire = {
                    "value_ID_Candidature": ID_Candidature,
                    "value_FK_Candidat": FK_Candidat,
                    "value_FK_Offre": FK_Offre,
                    "value_Date_Candidature": Date_Candidature,
                    "value_Lettre_Motivation": Lettre_Motivation,
                    "value_Statut": Statut
                }

                strsql_insert_candidature = """INSERT INTO t_candidature 
                                               (ID_Candidature, FK_Candidat, FK_Offre, Date_Candidature, Lettre_Motivation, Statut) 
                                               VALUES 
                                               (%(value_ID_Candidature)s, %(value_FK_Candidat)s, %(value_FK_Offre)s, %(value_Date_Candidature)s, 
                                               %(value_Lettre_Motivation)s, %(value_Statut)s)"""
                
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_candidature, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('candidature_afficher', order_by='ASC', id_candidature_sel=0))

        except Exception as Exception_candidature_ajouter_wtf:
            raise ExceptioncandidatureAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                                  f"{candidature_ajouter_wtf.__name__} ; "
                                                  f"{Exception_candidature_ajouter_wtf}")

    return render_template("candidature/candidature_ajouter_wtf.html", form=form)




"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /candidature_update
    
    Test : ex cliquer sur le menu "candidature" puis cliquer sur le bouton "EDIT" d'un "candidature"
    
    Paramètres : sans
    
    But : Editer(update) un candidature qui a été sélectionné dans le formulaire "candidature_afficher.html"
    
    Remarque :  Dans le champ "nom_candidature_update_wtf" du formulaire "candidature/candidature_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class ExceptioncandidatureUpdateWtf(Exception):
    pass

@app.route("/candidature_update", methods=['GET', 'POST'])
def candidature_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_candidature"
    id_candidature_update = request.values['id_candidature_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatecandidature()
    try:
        if request.method == "POST" and form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "candidature_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.

            valeur_update_dictionnaire = {
                "value_ID_Candidature": form_update.ID_Candidature.data,
                "value_FK_Candidat": form_update.FK_Candidat.data,
                "value_FK_Offre": form_update.FK_Offre.data,
                "value_Date_Candidature": form_update.Date_Candidature.data,
                "value_Lettre_Motivation": form_update.Lettre_Motivation.data,
                "value_Statut": form_update.Statut.data
            }

            str_sql_update_intitulecandidature = """UPDATE t_candidature SET 
                                                   FK_Candidat = %(value_FK_Candidat)s,
                                                   FK_Offre = %(value_FK_Offre)s,
                                                   Date_Candidature = %(value_Date_Candidature)s,
                                                   Lettre_Motivation = %(value_Lettre_Motivation)s,
                                                   Statut = %(value_Statut)s
                                                   WHERE ID_Candidature = %(value_ID_Candidature)s"""

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulecandidature, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_candidature_update"
            return redirect(url_for('candidature_afficher', order_by="ASC", id_candidature_sel=id_candidature_update))
        
        elif request.method == "GET":
            # Opération sur la BD pour récupérer les données du candidature à mettre à jour
            str_sql_id_candidature = "SELECT * FROM t_candidature " \
                                   "WHERE ID_Candidature = %(value_id_candidature)s"
            valeur_select_dictionnaire = {"value_id_candidature": id_candidature_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_candidature, valeur_select_dictionnaire)
                candidature_data = mybd_conn.fetchone()

            # Remplir les champs du formulaire avec les données existantes
            form_update.ID_Candidature.data = candidature_data["ID_Candidature"]
            form_update.FK_Candidat.data = candidature_data["FK_Candidat"]
            form_update.FK_Offre.data = candidature_data["FK_Offre"]
            form_update.Date_Candidature.data = candidature_data["Date_Candidature"]
            form_update.Lettre_Motivation.data = candidature_data["Lettre_Motivation"]
            form_update.Statut.data = candidature_data["Statut"]

    except Exception as Exception_candidature_update_wtf:
        raise ExceptioncandidatureUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                          f"{candidature_update_wtf.__name__} ; "
                                          f"{Exception_candidature_update_wtf}")

    return render_template("candidature/candidature_update_wtf.html", form_update=form_update)





"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /candidature_delete
    
    Test : ex. cliquer sur le menu "candidature" puis cliquer sur le bouton "DELETE" d'un "candidature"
    
    Paramètres : sans
    
    But : Effacer(delete) un candidature qui a été sélectionné dans le formulaire "candidature_afficher.html"
    
    Remarque :  Dans le champ "nom_candidature_delete_wtf" du formulaire "candidature/candidature_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""

class ExceptioncandidatureDeleteWtf(Exception):
    pass


@app.route("/candidature_delete", methods=['GET', 'POST'])
def candidature_delete_wtf():
    data_films_attribue_candidature_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_candidature"
    id_candidature_delete = request.values['id_candidature_btn_delete_html']

    # Objet formulaire pour effacer le candidature sélectionné.
    form_delete = FormWTFDeletecandidature()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("candidature_afficher", order_by="ASC", id_candidature_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "candidature/candidature_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_candidature_delete = session['data_films_attribue_candidature_delete']
                print("data_films_attribue_candidature_delete ", data_films_attribue_candidature_delete)

                flash(f"Effacer le candidature de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer candidature" qui va irrémédiablement EFFACER le candidature
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_candidature": id_candidature_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_candidature = """DELETE FROM t_candidature WHERE ID_Candidature = %(value_id_candidature)s"""
                str_sql_delete_idcandidature = """DELETE FROM t_candidature WHERE ID_Candidature = %(value_id_candidature)s"""
                # Manière brutale d'effacer d'abord la "fk_candidature", même si elle n'existe pas dans la "t_candidature_film"
                # Ensuite on peut effacer le candidature vu qu'il n'est plus "lié" (INNODB) dans la "t_candidature_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_candidature, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idcandidature, valeur_delete_dictionnaire)

                flash(f"candidature définitivement effacé !!", "success")
                print(f"candidature définitivement effacé !!")

                # afficher les données
                return redirect(url_for('candidature_afficher', order_by="ASC", id_candidature_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_candidature": id_candidature_delete}
            print(id_candidature_delete, type(id_candidature_delete))

            # Requête qui affiche tous les films_candidature qui ont le candidature que l'utilisateur veut effacer
            str_sql_candidature_films_delete = """SELECT * FROM t_candidature WHERE ID_Candidature = %(value_id_candidature)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_candidature_films_delete, valeur_select_dictionnaire)
                data_films_attribue_candidature_delete = mydb_conn.fetchall()
                print("data_films_attribue_candidature_delete...", data_films_attribue_candidature_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "candidature/candidature_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_candidature_delete'] = data_films_attribue_candidature_delete

                # Opération sur la BD pour récupérer "id_candidature" et "intitule_candidature" de la "t_candidature"
                str_sql_id_candidature = "SELECT * FROM t_candidature WHERE ID_candidature = %(value_id_candidature)s"

                mydb_conn.execute(str_sql_id_candidature, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom candidature" pour l'action DELETE
                data_nom_candidature = mydb_conn.fetchone()
                print("data_nom_candidature ", data_nom_candidature, " type ", type(data_nom_candidature), " candidature ",
                      data_nom_candidature["FK_Candidat"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "candidature_delete_wtf.html"
            form_delete.nom_candidature_delete_wtf.data = data_nom_candidature["FK_Candidat"]

            # Le bouton pour l'action "DELETE" dans le form. "candidature_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_candidature_delete_wtf:
        raise ExceptioncandidatureDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{candidature_delete_wtf.__name__} ; "
                                      f"{Exception_candidature_delete_wtf}")

    return render_template("candidature/candidature_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_candidature_delete)
