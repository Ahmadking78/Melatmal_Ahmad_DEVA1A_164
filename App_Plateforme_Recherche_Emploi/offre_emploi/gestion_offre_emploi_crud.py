"""Gestion des "routes" FLASK et des données pour les offre_emploi.
Fichier : gestion_offre_emploi_crud.py
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
from App_Plateforme_Recherche_Emploi.offre_emploi.gestion_offre_emploi_wtf_forms import FormWTFAjouteroffre_emploi
from App_Plateforme_Recherche_Emploi.offre_emploi.gestion_offre_emploi_wtf_forms import FormWTFDeleteoffre_emploi
from App_Plateforme_Recherche_Emploi.offre_emploi.gestion_offre_emploi_wtf_forms import FormWTFUpdateoffre_emploi

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /offre_emploi_afficher
    
    Test : ex : http://127.0.0.1:5575/offre_emploi_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_offre_emploi_sel = 0 >> tous les offre_emploi.
                id_offre_emploi_sel = "n" affiche le offre_emploi dont l'id est "n"
"""

class Exceptionoffre_emploiAfficher(Exception):
    pass

@app.route("/offre_emploi_afficher/<string:order_by>/<int:id_offre_emploi_sel>", methods=['GET', 'POST'])
def offre_emploi_afficher(order_by, id_offre_emploi_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_offre_emploi_sel == 0:
                    strsql_offre_emploi_afficher = """SELECT ID_Offre, FK_Employeur, Titre, Description, Date_Publication, Date_Expiration, Type_Contrat, Localisation, Salaire FROM t_offre_emploi ORDER BY ID_Offre ASC"""
                    mc_afficher.execute(strsql_offre_emploi_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_offre_emploi"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du offre_emploi sélectionné avec un nom de variable
                    valeur_id_offre_emploi_selected_dictionnaire = {"value_id_offre_emploi_selected": id_offre_emploi_sel}
                    strsql_offre_emploi_afficher = """SELECT ID_Offre, FK_Employeur, Titre, Description, Date_Publication, Date_Expiration, Type_Contrat, Localisation, Salaire  FROM t_offre_emploi WHERE ID_Offre = %(value_id_offre_emploi_selected)s"""

                    mc_afficher.execute(strsql_offre_emploi_afficher, valeur_id_offre_emploi_selected_dictionnaire)
                else:
                    strsql_offre_emploi_afficher = """SELECT ID_Offre, FK_Employeur, Titre, Description, Date_Publication, Date_Expiration, Type_Contrat, Localisation, Salaire  FROM t_offre_emploi ORDER BY ID_Offre DESC"""

                    mc_afficher.execute(strsql_offre_emploi_afficher)

                data_offre_emploi = mc_afficher.fetchall()

                print("data_offre_emploi ", data_offre_emploi, " Type : ", type(data_offre_emploi))

                # Différencier les messages si la table est vide.
                if not data_offre_emploi and id_offre_emploi_sel == 0:
                    flash("""La table "offre_emploi" est vide. !!""", "warning")
                elif not data_offre_emploi and id_offre_emploi_sel > 0:
                    # Si l'utilisateur change l'id_offre_emploi dans l'URL et que le offre_emploi n'existe pas,
                    flash(f"Le offre emploi demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_offre_emploi" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données offre emploi affichés !!", "success")

        except Exception as Exception_offre_emploi_afficher:
            raise Exceptionoffre_emploiAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{offre_emploi_afficher.__name__} ; "
                                          f"{Exception_offre_emploi_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("offre_emploi/offre_emploi_afficher.html", data=data_offre_emploi)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /offre_emploi_ajouter
    
    Test : ex : http://127.0.0.1:5575/offre_emploi_ajouter
    
    Paramètres : sans
    
    But : Ajouter un offre_emploi pour un film
    
    Remarque :  Dans le champ "name_offre_emploi_html" du formulaire "offre_emploi/offre_emploi_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class Exceptionoffre_emploiAjouterWtf(Exception):
    pass

@app.route("/offre_emploi_ajouter", methods=['GET', 'POST'])
def offre_emploi_ajouter_wtf():
    form = FormWTFAjouteroffre_emploi()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                ID_Offre = form.ID_Offre.data
                FK_Employeur = form.FK_Employeur.data
                Titre = form.Titre.data
                Description = form.Description.data
                Date_Publication = form.Date_Publication.data
                Date_Expiration = form.Date_Expiration.data
                Type_Contrat = form.Type_Contrat.data
                Localisation = form.Localisation.data
                Salaire = form.Salaire.data
                
                valeurs_insertion_dictionnaire = {
                    "ID_Offre": ID_Offre,
                    "FK_Employeur": FK_Employeur,
                    "Titre": Titre,
                    "Description": Description,
                    "Date_Publication": Date_Publication,
                    "Date_Expiration": Date_Expiration,
                    "Type_Contrat": Type_Contrat,
                    "Localisation": Localisation,
                    "Salaire": Salaire
                }

                strsql_insert_offre_emploi = """INSERT INTO t_offre_emploi (ID_Offre, FK_Employeur, Titre, Description, Date_Publication, Date_Expiration, Type_Contrat, Localisation, Salaire) 
                                                VALUES (%(ID_Offre)s, %(FK_Employeur)s, %(Titre)s, %(Description)s, %(Date_Publication)s, %(Date_Expiration)s, %(Type_Contrat)s, %(Localisation)s, %(Salaire)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_offre_emploi, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('offre_emploi_afficher', order_by='ASC', id_offre_emploi_sel=0))

        except Exception as Exception_offre_emploi_ajouter_wtf:
            raise Exceptionoffre_emploiAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{offre_emploi_ajouter_wtf.__name__} ; "
                                            f"{Exception_offre_emploi_ajouter_wtf}")

    return render_template("offre_emploi/offre_emploi_ajouter_wtf.html", form=form)



"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /offre_emploi_update
    
    Test : ex cliquer sur le menu "offre_emploi" puis cliquer sur le bouton "EDIT" d'un "offre_emploi"
    
    Paramètres : sans
    
    But : Editer(update) un offre_emploi qui a été sélectionné dans le formulaire "offre_emploi_afficher.html"
    
    Remarque :  Dans le champ "nom_offre_emploi_update_wtf" du formulaire "offre_emploi/offre_emploi_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class Exceptionoffre_emploiUpdateWtf(Exception):
    pass


@app.route("/offre_emploi_update", methods=['GET', 'POST'])
def offre_emploi_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_offre_emploi"
    id_offre_emploi_update = request.values['id_offre_emploi_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateoffre_emploi()
    try:
        if request.method == "POST" and form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "offre_emploi_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.

            valeur_update_dictionnaire = {
                "value_ID_Offre": id_offre_emploi_update,
                "value_FK_Employeur": form_update.FK_Employeur.data,
                "value_Titre": form_update.Titre.data,
                "value_Description": form_update.Description.data,
                "value_Date_Publication": form_update.Date_Publication.data,
                "value_Date_Expiration": form_update.Date_Expiration.data,
                "value_Type_Contrat": form_update.Type_Contrat.data,
                "value_Localisation": form_update.Localisation.data,
                "value_Salaire": form_update.Salaire.data
            }

            str_sql_update_intituleoffre_emploi = """UPDATE t_offre_emploi SET 
                ID_Offre = %(value_ID_Offre)s,
                FK_Employeur = %(value_FK_Employeur)s,
                Titre = %(value_Titre)s,
                Description = %(value_Description)s,
                Date_Publication = %(value_Date_Publication)s,
                Date_Expiration = %(value_Date_Expiration)s,
                Type_Contrat = %(value_Type_Contrat)s,
                Localisation = %(value_Localisation)s,
                Salaire = %(value_Salaire)s
                WHERE ID_Offre = %(value_ID_Offre)s"""

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleoffre_emploi, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_offre_emploi_update"
            return redirect(url_for('offre_emploi_afficher', order_by="ASC", id_offre_emploi_sel=id_offre_emploi_update))
        
        elif request.method == "GET":
            # Opération sur la BD pour récupérer les données du offre_emploi à mettre à jour
            str_sql_id_offre_emploi = "SELECT * FROM t_offre_emploi " \
                                   "WHERE ID_Offre = %(value_id_offre_emploi)s"
            valeur_select_dictionnaire = {"value_id_offre_emploi": id_offre_emploi_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_offre_emploi, valeur_select_dictionnaire)
                offre_emploi_data = mybd_conn.fetchone()

            # Afficher les valeurs sélectionnées dans les champs du formulaire "offre_emploi_update_wtf.html"
            form_update.ID_Offre.data = offre_emploi_data["ID_Offre"]
            form_update.FK_Employeur.data = offre_emploi_data["FK_Employeur"]
            form_update.Titre.data = offre_emploi_data["Titre"]
            form_update.Description.data = offre_emploi_data["Description"]
            form_update.Date_Publication.data = offre_emploi_data["Date_Publication"]
            form_update.Date_Expiration.data = offre_emploi_data["Date_Expiration"]
            form_update.Type_Contrat.data = offre_emploi_data["Type_Contrat"]
            form_update.Localisation.data = offre_emploi_data["Localisation"]
            form_update.Salaire.data = offre_emploi_data["Salaire"]

    except Exception as Exception_offre_emploi_update_wtf:
        raise Exceptionoffre_emploiUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                          f"{offre_emploi_update_wtf.__name__} ; "
                                          f"{Exception_offre_emploi_update_wtf}")

    return render_template("offre_emploi/offre_emploi_update_wtf.html", form_update=form_update, offre_emploi_data=offre_emploi_data)




"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /offre_emploi_delete
    
    Test : ex. cliquer sur le menu "offre_emploi" puis cliquer sur le bouton "DELETE" d'un "offre_emploi"
    
    Paramètres : sans
    
    But : Effacer(delete) un offre_emploi qui a été sélectionné dans le formulaire "offre_emploi_afficher.html"
    
    Remarque :  Dans le champ "nom_offre_emploi_delete_wtf" du formulaire "offre_emploi/offre_emploi_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""

class Exceptionoffre_emploiDeleteWtf(Exception):
    pass


@app.route("/offre_emploi_delete", methods=['GET', 'POST'])
def offre_emploi_delete_wtf():
    data_films_attribue_offre_emploi_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_offre_emploi"
    id_offre_emploi_delete = request.values['id_offre_emploi_btn_delete_html']

    # Objet formulaire pour effacer le offre_emploi sélectionné.
    form_delete = FormWTFDeleteoffre_emploi()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("offre_emploi_afficher", order_by="ASC", id_offre_emploi_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "offre_emploi/offre_emploi_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_offre_emploi_delete = session['data_films_attribue_offre_emploi_delete']
                print("data_films_attribue_offre_emploi_delete ", data_films_attribue_offre_emploi_delete)

                flash(f"Effacer le offre_emploi de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer offre_emploi" qui va irrémédiablement EFFACER le offre_emploi
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_offre_emploi": id_offre_emploi_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_offre_emploi = """DELETE FROM t_offre_emploi WHERE ID_Offre = %(value_id_offre_emploi)s"""
                str_sql_delete_idoffre_emploi = """DELETE FROM t_offre_emploi WHERE ID_Offre = %(value_id_offre_emploi)s"""
                # Manière brutale d'effacer d'abord la "fk_offre_emploi", même si elle n'existe pas dans la "t_offre_emploi_film"
                # Ensuite on peut effacer le offre_emploi vu qu'il n'est plus "lié" (INNODB) dans la "t_offre_emploi_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_offre_emploi, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idoffre_emploi, valeur_delete_dictionnaire)

                flash(f"offre_emploi définitivement effacé !!", "success")
                print(f"offre_emploi définitivement effacé !!")

                # afficher les données
                return redirect(url_for('offre_emploi_afficher', order_by="ASC", id_offre_emploi_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_offre_emploi": id_offre_emploi_delete}
            print(id_offre_emploi_delete, type(id_offre_emploi_delete))

            # Requête qui affiche tous les films_offre_emploi qui ont le offre_emploi que l'utilisateur veut effacer
            str_sql_offre_emploi_films_delete = """SELECT * FROM t_offre_emploi WHERE ID_Offre = %(value_id_offre_emploi)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_offre_emploi_films_delete, valeur_select_dictionnaire)
                data_films_attribue_offre_emploi_delete = mydb_conn.fetchall()
                print("data_films_attribue_offre_emploi_delete...", data_films_attribue_offre_emploi_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "offre_emploi/offre_emploi_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_offre_emploi_delete'] = data_films_attribue_offre_emploi_delete

                # Opération sur la BD pour récupérer "id_offre_emploi" et "intitule_offre_emploi" de la "t_offre_emploi"
                str_sql_id_offre_emploi = "SELECT * FROM t_offre_emploi WHERE ID_Offre = %(value_id_offre_emploi)s"

                mydb_conn.execute(str_sql_id_offre_emploi, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom offre_emploi" pour l'action DELETE
                data_nom_offre_emploi = mydb_conn.fetchone()
                print("data_nom_offre_emploi ", data_nom_offre_emploi, " type ", type(data_nom_offre_emploi), " offre_emploi ",
                      data_nom_offre_emploi["FK_Employeur"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "offre_emploi_delete_wtf.html"
            form_delete.nom_offre_emploi_delete_wtf.data = data_nom_offre_emploi["FK_Employeur"]

            # Le bouton pour l'action "DELETE" dans le form. "offre_emploi_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_offre_emploi_delete_wtf:
        raise Exceptionoffre_emploiDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{offre_emploi_delete_wtf.__name__} ; "
                                      f"{Exception_offre_emploi_delete_wtf}")

    return render_template("offre_emploi/offre_emploi_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_offre_emploi_delete)