"""Gestion des "routes" FLASK et des données pour les competences_candidat.
Fichier : gestion_competences_candidat_crud.py
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
from App_Plateforme_Recherche_Emploi.competences_candidat.gestion_competences_candidat_wtf_forms import FormWTFAjoutercompetences_candidat
from App_Plateforme_Recherche_Emploi.competences_candidat.gestion_competences_candidat_wtf_forms import FormWTFDeletecompetences_candidat
from App_Plateforme_Recherche_Emploi.competences_candidat.gestion_competences_candidat_wtf_forms import FormWTFUpdatecompetences_candidat

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /competences_candidat_afficher
    
    Test : ex : http://127.0.0.1:5575/competences_candidat_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_competences_candidat_sel = 0 >> tous les competences_candidat.
                id_competences_candidat_sel = "n" affiche le competences_candidat dont l'id est "n"
"""

class Exceptioncompetences_candidatAfficher(Exception):
    pass

@app.route("/competences_candidat_afficher/<string:order_by>/<int:id_competences_candidat_sel>", methods=['GET', 'POST'])
def competences_candidat_afficher(order_by, id_competences_candidat_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_competences_candidat_sel == 0:
                    strsql_competences_candidat_afficher = """SELECT FK_Candidat, FK_Competence, Niveau FROM t_competences_candidat ORDER BY FK_Candidat ASC"""
                    mc_afficher.execute(strsql_competences_candidat_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_competences_candidat"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du competences_candidat sélectionné avec un nom de variable
                    valeur_id_competences_candidat_selected_dictionnaire = {"value_id_competences_candidat_selected": id_competences_candidat_sel}
                    strsql_competences_candidat_afficher = """SELECT FK_Candidat, FK_Competence, Niveau  FROM t_competences_candidat WHERE FK_Candidat = %(value_id_competences_candidat_selected)s"""

                    mc_afficher.execute(strsql_competences_candidat_afficher, valeur_id_competences_candidat_selected_dictionnaire)
                else:
                    strsql_competences_candidat_afficher = """SELECT FK_Candidat, FK_Competence, Niveau  FROM t_competences_candidat ORDER BY FK_Candidat DESC"""

                    mc_afficher.execute(strsql_competences_candidat_afficher)

                data_competences_candidat = mc_afficher.fetchall()

                print("data_competences_candidat ", data_competences_candidat, " Type : ", type(data_competences_candidat))

                # Différencier les messages si la table est vide.
                if not data_competences_candidat and id_competences_candidat_sel == 0:
                    flash("""La table "t_competences_candidat" est vide. !!""", "warning")
                elif not data_competences_candidat and id_competences_candidat_sel > 0:
                    # Si l'utilisateur change l'id_competences_candidat dans l'URL et que le competences_candidat n'existe pas,
                    flash(f"Le competences candidat demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_competences_candidat" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données competences candidat affichés !!", "success")

        except Exception as Exception_candidat_afficher:
            raise Exceptioncompetences_candidatAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{competences_candidat_afficher.__name__} ; "
                                          f"{Exception_candidat_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("competences_candidat/competences_candidat_afficher.html", data=data_competences_candidat)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /competences_candidat_ajouter
    
    Test : ex : http://127.0.0.1:5575/competences_candidat_ajouter
    
    Paramètres : sans
    
    But : Ajouter un competences_candidat pour un film
    
    Remarque :  Dans le champ "name_competences_candidat_html" du formulaire "competences_candidat/competences_candidat_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class Exceptioncompetences_candidatAjouterWtf(Exception):
    pass


@app.route("/competences_candidat_ajouter", methods=['GET', 'POST'])
def competences_candidat_ajouter_wtf():
    form = FormWTFAjoutercompetences_candidat()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                FK_Candidat = form.FK_Candidat.data
                FK_Competence = form.FK_Competence.data
                Niveau = form.Niveau.data

                valeurs_insertion_dictionnaire = {
                    "value_FK_Candidat": FK_Candidat,
                    "value_FK_Competence": FK_Competence,
                    "value_Niveau": Niveau
                }

                strsql_insert_competences_candidat = """INSERT INTO t_competences_candidat (FK_Candidat, FK_Competence, Niveau) VALUES (%(value_FK_Candidat)s, %(value_FK_Competence)s, %(value_Niveau)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_competences_candidat, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")

                return redirect(url_for('competences_candidat_afficher', order_by='DESC', id_competences_candidat_sel=0))

        except Exception as Exception_competences_candidat_ajouter_wtf:
            raise Exceptioncompetences_candidatAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{competences_candidat_ajouter_wtf.__name__} ; "
                                            f"{Exception_competences_candidat_ajouter_wtf}")

    return render_template("competences_candidat/competences_candidat_ajouter_wtf.html", form=form)



"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /competences_candidat_update
    
    Test : ex cliquer sur le menu "competences_candidat" puis cliquer sur le bouton "EDIT" d'un "competences_candidat"
    
    Paramètres : sans
    
    But : Editer(update) un competences_candidat qui a été sélectionné dans le formulaire "competences_candidat_afficher.html"
    
    Remarque :  Dans le champ "nom_competences_candidat_update_wtf" du formulaire "competences_candidat/competences_candidat_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class Exceptioncompetences_candidatUpdateWtf(Exception):
    pass

@app.route("/competences_candidat_update", methods=['GET', 'POST'])
def competences_candidat_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_competences_candidat"
    id_competences_candidat_update = request.values['id_competences_candidat_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatecompetences_candidat()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur des champs depuis "competences_candidat_update_wtf.html" après avoir cliqué sur "SUBMIT".
            FK_Candidat_update = form_update.FK_Candidat.data
            FK_Competence_update = form_update.FK_Competence.data
            Niveau_update = form_update.Niveau.data

            valeur_update_dictionnaire = {
                "value_id_competences_candidat": id_competences_candidat_update,
                "value_FK_Candidat": FK_Candidat_update,
                "value_FK_Competence": FK_Competence_update,
                "value_Niveau": Niveau_update
            }

            str_sql_update_intitulecompetences_candidat = """UPDATE t_competences_candidat SET 
                FK_Candidat = %(value_FK_Candidat)s,
                FK_Competence = %(value_FK_Competence)s,
                Niveau = %(value_Niveau)s
                WHERE FK_Candidat = %(value_id_competences_candidat)s"""

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulecompetences_candidat, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_competences_candidat_update"
            return redirect(url_for('competences_candidat_afficher', order_by="ASC", id_competences_candidat_sel=id_competences_candidat_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer les données du competences_candidat à mettre à jour
            str_sql_id_competences_candidat = "SELECT * FROM t_competences_candidat " \
                               "WHERE FK_Candidat = %(value_id_competences_candidat)s"
            valeur_select_dictionnaire = {"value_id_competences_candidat": id_competences_candidat_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_competences_candidat, valeur_select_dictionnaire)
                competences_candidat_data = mybd_conn.fetchone()

            # Afficher les valeurs sélectionnées dans les champs du formulaire "competences_candidat_update_wtf.html"
            if competences_candidat_data:
                form_update.FK_Candidat.data = competences_candidat_data["FK_Candidat"]
                form_update.FK_Competence.data = competences_candidat_data["FK_Competence"]
                form_update.Niveau.data = competences_candidat_data["Niveau"]

    except Exception as Exception_competences_candidat_update_wtf:
        raise Exceptioncompetences_candidatUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{competences_candidat_update_wtf.__name__} ; "
                                      f"{Exception_competences_candidat_update_wtf}")

    return render_template("competences_candidat/competences_candidat_update_wtf.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /competences_candidat_delete
    
    Test : ex. cliquer sur le menu "competences_candidat" puis cliquer sur le bouton "DELETE" d'un "competences_candidat"
    
    Paramètres : sans
    
    But : Effacer(delete) un competences_candidat qui a été sélectionné dans le formulaire "competences_candidat_afficher.html"
    
    Remarque :  Dans le champ "nom_competences_candidat_delete_wtf" du formulaire "competences_candidat/competences_candidat_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""

class Exceptioncompetences_candidatDeleteWtf(Exception):
    pass


@app.route("/competences_candidat_delete", methods=['GET', 'POST'])
def competences_candidat_delete_wtf():
    data_films_attribue_competences_candidat_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_competences_candidat"
    id_competences_candidat_delete = request.values['id_competences_candidat_btn_delete_html']

    # Objet formulaire pour effacer le competences_candidat sélectionné.
    form_delete = FormWTFDeletecompetences_candidat()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("competences_candidat_afficher", order_by="ASC", id_competences_candidat_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "competences_candidat/competences_candidat_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_competences_candidat_delete = session['data_films_attribue_competences_candidat_delete']
                print("data_films_attribue_competences_candidat_delete ", data_films_attribue_competences_candidat_delete)

                flash(f"Effacer le competences_candidat de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer competences_candidat" qui va irrémédiablement EFFACER le competences_candidat
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_competences_candidat": id_competences_candidat_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_competences_candidat = """DELETE FROM t_competences_candidat WHERE FK_Candidat = %(value_id_competences_candidat)s"""
                str_sql_delete_idcompetences_candidat = """DELETE FROM t_competences_candidat WHERE FK_Candidat = %(value_id_competences_candidat)s"""
                # Manière brutale d'effacer d'abord la "fk_competences_candidat", même si elle n'existe pas dans la "t_competences_candidat_film"
                # Ensuite on peut effacer le competences_candidat vu qu'il n'est plus "lié" (INNODB) dans la "t_competences_candidat_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_competences_candidat, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idcompetences_candidat, valeur_delete_dictionnaire)

                flash(f"competences_candidat définitivement effacé !!", "success")
                print(f"competences_candidat définitivement effacé !!")

                # afficher les données
                return redirect(url_for('competences_candidat_afficher', order_by="ASC", id_competences_candidat_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_competences_candidat": id_competences_candidat_delete}
            print(id_competences_candidat_delete, type(id_competences_candidat_delete))

            # Requête qui affiche tous les films_competences_candidat qui ont le competences_candidat que l'utilisateur veut effacer
            str_sql_competences_candidat_films_delete = """SELECT FK_Candidat, FK_Competence FROM t_competences_candidat WHERE FK_Candidat = %(value_id_competences_candidat)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_competences_candidat_films_delete, valeur_select_dictionnaire)
                data_films_attribue_competences_candidat_delete = mydb_conn.fetchall()
                print("data_films_attribue_competences_candidat_delete...", data_films_attribue_competences_candidat_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "competences_candidat/competences_candidat_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_competences_candidat_delete'] = data_films_attribue_competences_candidat_delete

                # Opération sur la BD pour récupérer "id_competences_candidat" et "intitule_competences_candidat" de la "t_competences_candidat"
                str_sql_id_competences_candidat = "SELECT FK_Candidat, FK_Competence FROM t_competences_candidat WHERE FK_Candidat = %(value_id_competences_candidat)s"

                mydb_conn.execute(str_sql_id_competences_candidat, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom competences_candidat" pour l'action DELETE
                data_nom_competences_candidat = mydb_conn.fetchone()
                print("data_nom_competences_candidat ", data_nom_competences_candidat, " type ", type(data_nom_competences_candidat), " competences_candidat ",
                      data_nom_competences_candidat["FK_Candidat"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "competences_candidat_delete_wtf.html"
            form_delete.nom_competences_candidat_delete_wtf.data = data_nom_competences_candidat["FK_Candidat"]

            # Le bouton pour l'action "DELETE" dans le form. "competences_candidat_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_competences_candidat_delete_wtf:
        raise Exceptioncompetences_candidatDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{competences_candidat_delete_wtf.__name__} ; "
                                      f"{Exception_competences_candidat_delete_wtf}")

    return render_template("competences_candidat/competences_candidat_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_competences_candidat_delete)
