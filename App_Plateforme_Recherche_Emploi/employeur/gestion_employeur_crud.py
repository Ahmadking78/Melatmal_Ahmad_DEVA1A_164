"""Gestion des "routes" FLASK et des données pour les employeur.
Fichier : gestion_employeur_crud.py
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
from App_Plateforme_Recherche_Emploi.employeur.gestion_employeur_wtf_forms import FormWTFAjouteremployeur
from App_Plateforme_Recherche_Emploi.employeur.gestion_employeur_wtf_forms import FormWTFDeleteemployeur
from App_Plateforme_Recherche_Emploi.employeur.gestion_employeur_wtf_forms import FormWTFUpdateemployeur

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /employeur_afficher
    
    Test : ex : http://127.0.0.1:5575/employeur_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_employeur_sel = 0 >> tous les employeur.
                id_employeur_sel = "n" affiche le employeur dont l'id est "n"
"""

class ExceptionemployeurAfficher(Exception):
    pass


@app.route("/employeur_afficher/<string:order_by>/<int:id_employeur_sel>", methods=['GET', 'POST'])
def employeur_afficher(order_by, id_employeur_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_employeur_sel == 0:
                    strsql_employeur_afficher = """SELECT * FROM t_employeur ORDER BY ID_Employeur ASC"""
                    mc_afficher.execute(strsql_employeur_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_employeur"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du employeur sélectionné avec un nom de variable
                    valeur_id_employeur_selected_dictionnaire = {"value_id_employeur_selected": id_employeur_sel}
                    strsql_employeur_afficher = """SELECT *  FROM t_employeur WHERE ID_Employeur = %(value_id_employeur_selected)s"""

                    mc_afficher.execute(strsql_employeur_afficher, valeur_id_employeur_selected_dictionnaire)
                else:
                    strsql_employeur_afficher = """SELECT *  FROM t_employeur ORDER BY ID_Employeur DESC"""

                    mc_afficher.execute(strsql_employeur_afficher)

                data_employeur = mc_afficher.fetchall()

                print("data_employeur ", data_employeur, " Type : ", type(data_employeur)) 

                # Différencier les messages si la table est vide.
                if not data_employeur and id_employeur_sel == 0:
                    flash("""La table "t_employeur" est vide. !!""", "warning")
                elif not data_employeur and id_employeur_sel > 0:
                    # Si l'utilisateur change l'id_employeur dans l'URL et que le employeur n'existe pas,
                    flash(f"Le employeur demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_employeur" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données employeur affichés !!", "success")

        except Exception as Exception_employeur_afficher:
            raise ExceptionemployeurAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{employeur_afficher.__name__} ; "
                                          f"{Exception_employeur_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("employeur/employeur_afficher.html", data=data_employeur)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /employeur_ajouter
    
    Test : ex : http://127.0.0.1:5575/employeur_ajouter
    
    Paramètres : sans
    
    But : Ajouter un employeur pour un film
    
    Remarque :  Dans le champ "name_employeur_html" du formulaire "employeur/employeur_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class ExceptionemployeurAjouterWtf(Exception):
    pass

@app.route("/employeur_ajouter", methods=['GET', 'POST'])
def employeur_ajouter_wtf():
    form = FormWTFAjouteremployeur()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                valeurs_insertion_dictionnaire = {
                    "value_id_employeur": form.ID_Employeur.data,
                    "value_nom_entreprise": form.Nom_Entreprise.data,
                    "value_secteur": form.Secteur.data,
                    "value_email": form.Email.data,
                    "value_telephone": form.Telephone.data,
                    "value_adresse": form.Adresse.data,
                    "value_description": form.Description.data
                }

                strsql_insert_employeur = """INSERT INTO t_employeur 
                                             (ID_Employeur, Nom_Entreprise, Secteur, Email, Telephone, Adresse, Description) 
                                             VALUES 
                                             (%(value_id_employeur)s, %(value_nom_entreprise)s, %(value_secteur)s, 
                                             %(value_email)s, %(value_telephone)s, %(value_adresse)s, %(value_description)s)"""
                
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_employeur, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('employeur_afficher', order_by='ASC', id_employeur_sel=0))

        except Exception as Exception_employeur_ajouter_wtf:
            raise ExceptionemployeurAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                                f"{employeur_ajouter_wtf.__name__} ; "
                                                f"{Exception_employeur_ajouter_wtf}")

    return render_template("employeur/employeur_ajouter_wtf.html", form=form)




"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /employeur_update
    
    Test : ex cliquer sur le menu "employeur" puis cliquer sur le bouton "EDIT" d'un "employeur"
    
    Paramètres : sans
    
    But : Editer(update) un employeur qui a été sélectionné dans le formulaire "employeur_afficher.html"
    
    Remarque :  Dans le champ "nom_employeur_update_wtf" du formulaire "employeur/employeur_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class ExceptionemployeurUpdateWtf(Exception):
    pass

@app.route("/employeur_update", methods=['GET', 'POST'])
def employeur_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_employeur"
    id_employeur_update = request.values['id_employeur_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateemployeur()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur du champ depuis "employeur_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_employeur_update = form_update.Nom_Entreprise.data.lower()
            nom_entreprise = form_update.Nom_Entreprise.data
            secteur = form_update.Secteur.data
            email = form_update.Email.data
            telephone = form_update.Telephone.data
            adresse = form_update.Adresse.data
            description = form_update.Description.data
            id_employeur = form_update.ID_Employeur.data

            valeur_update_dictionnaire = {"value_name_employeur": name_employeur_update,
                                          "value_Nom_Entreprise": nom_entreprise,
                                          "value_Secteur": secteur,
                                          "value_Email": email,
                                          "value_Telephone": telephone,
                                          "value_Adresse": adresse,
                                          "value_Description": description,
                                          "value_id_employeur": id_employeur_update
                                          }

            str_sql_update_intituleemployeur = """UPDATE t_employeur SET 
            Nom_Entreprise = %(value_Nom_Entreprise)s, 
            Secteur = %(value_Secteur)s, 
            Email = %(value_Email)s, 
            Telephone = %(value_Telephone)s, 
            Adresse = %(value_Adresse)s, 
            Description = %(value_Description)s 
            WHERE ID_Employeur = %(value_id_employeur)s """

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleemployeur, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_employeur_update"
            return redirect(url_for('employeur_afficher', order_by="ASC", id_employeur_sel=id_employeur_update))
        
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_employeur" et "intitule_employeur" de la "t_employeur"
            str_sql_id_employeur = "SELECT ID_Employeur, Nom_Entreprise, Secteur, Email, Telephone, Adresse, Description FROM t_employeur " \
                                   "WHERE ID_Employeur = %(value_id_employeur)s"
            valeur_select_dictionnaire = {"value_id_employeur": id_employeur_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_employeur, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom employeur" pour l'UPDATE
                data_nom_employeur = mybd_conn.fetchone()

            print("data_nom_employeur ", data_nom_employeur, " type ", type(data_nom_employeur), " employeur ",
                  data_nom_employeur["Nom_Entreprise"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "employeur_update_wtf.html"
            form_update.ID_Employeur.data = data_nom_employeur["ID_Employeur"]
            form_update.Nom_Entreprise.data = data_nom_employeur["Nom_Entreprise"]
            form_update.Secteur.data = data_nom_employeur["Secteur"]
            form_update.Email.data = data_nom_employeur["Email"]
            form_update.Telephone.data = data_nom_employeur["Telephone"]
            form_update.Adresse.data = data_nom_employeur["Adresse"]
            form_update.Description.data = data_nom_employeur["Description"]

    except Exception as Exception_employeur_update_wtf:
        raise ExceptionemployeurUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                          f"{employeur_update_wtf.__name__} ; "
                                          f"{Exception_employeur_update_wtf}")

    return render_template("employeur/employeur_update_wtf.html", form_update=form_update)





"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /employeur_delete
    
    Test : ex. cliquer sur le menu "employeur" puis cliquer sur le bouton "DELETE" d'un "employeur"
    
    Paramètres : sans
    
    But : Effacer(delete) un employeur qui a été sélectionné dans le formulaire "employeur_afficher.html"
    
    Remarque :  Dans le champ "nom_employeur_delete_wtf" du formulaire "employeur/employeur_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""

class ExceptionemployeurDeleteWtf(Exception):
    pass

@app.route("/employeur_delete", methods=['GET', 'POST'])
def employeur_delete_wtf():
    data_films_attribue_employeur_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_employeur"
    id_employeur_delete = request.values['id_employeur_btn_delete_html']

    # Objet formulaire pour effacer le employeur sélectionné.
    form_delete = FormWTFDeleteemployeur()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("employeur_afficher", order_by="ASC", id_employeur_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "employeur/employeur_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_employeur_delete = session['data_films_attribue_employeur_delete']
                print("data_films_attribue_employeur_delete ", data_films_attribue_employeur_delete)

                flash(f"Effacer le employeur de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer employeur" qui va irrémédiablement EFFACER le employeur
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_employeur": id_employeur_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_employeur = """DELETE FROM t_employeur WHERE ID_Employeur = %(value_id_employeur)s"""
                str_sql_delete_idemployeur = """DELETE FROM t_employeur WHERE ID_Employeur = %(value_id_employeur)s"""
                # Manière brutale d'effacer d'abord la "fk_employeur", même si elle n'existe pas dans la "t_employeur_film"
                # Ensuite on peut effacer le employeur vu qu'il n'est plus "lié" (INNODB) dans la "t_employeur_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_employeur, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idemployeur, valeur_delete_dictionnaire)

                flash(f"employeur définitivement effacé !!", "success")
                print(f"employeur définitivement effacé !!")

                # afficher les données
                return redirect(url_for('employeur_afficher', order_by="ASC", id_employeur_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_employeur": id_employeur_delete}
            print(id_employeur_delete, type(id_employeur_delete))

            # Requête qui affiche tous les films_employeur qui ont le employeur que l'utilisateur veut effacer
            str_sql_employeur_films_delete = """SELECT * FROM t_employeur WHERE ID_Employeur = %(value_id_employeur)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_employeur_films_delete, valeur_select_dictionnaire)
                data_films_attribue_employeur_delete = mydb_conn.fetchall()
                print("data_films_attribue_employeur_delete...", data_films_attribue_employeur_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "employeur/employeur_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_employeur_delete'] = data_films_attribue_employeur_delete

                # Opération sur la BD pour récupérer "id_employeur" et "intitule_employeur" de la "t_employeur"
                str_sql_id_employeur = "SELECT * FROM t_employeur WHERE ID_Employeur = %(value_id_employeur)s"

                mydb_conn.execute(str_sql_id_employeur, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom employeur" pour l'action DELETE
                data_nom_employeur = mydb_conn.fetchone()
                print("data_nom_employeur ", data_nom_employeur, " type ", type(data_nom_employeur), " employeur ",
                      data_nom_employeur["Nom_Entreprise"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "employeur_delete_wtf.html"
            form_delete.nom_employeur_delete_wtf.data = data_nom_employeur["Nom_Entreprise"]

            # Le bouton pour l'action "DELETE" dans le form. "employeur_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_employeur_delete_wtf:
        raise ExceptionemployeurDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{employeur_delete_wtf.__name__} ; "
                                      f"{Exception_employeur_delete_wtf}")

    return render_template("employeur/employeur_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_employeur_delete)
