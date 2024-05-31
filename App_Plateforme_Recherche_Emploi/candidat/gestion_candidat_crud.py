"""Gestion des "routes" FLASK et des données pour les candidat.
Fichier : gestion_candidat_crud.py
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
from App_Plateforme_Recherche_Emploi.candidat.gestion_candidat_wtf_forms import FormWTFAjoutercandidat
from App_Plateforme_Recherche_Emploi.candidat.gestion_candidat_wtf_forms import FormWTFDeletecandidat
from App_Plateforme_Recherche_Emploi.candidat.gestion_candidat_wtf_forms import FormWTFUpdatecandidat

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /candidat_afficher
    
    Test : ex : http://127.0.0.1:5575/candidat_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_candidat_sel = 0 >> tous les candidat.
                id_candidat_sel = "n" affiche le candidat dont l'id est "n"
"""

class ExceptioncandidatAfficher(Exception):
    pass


@app.route("/candidat_afficher/<string:order_by>/<int:id_candidat_sel>", methods=['GET', 'POST'])
def candidat_afficher(order_by, id_candidat_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_candidat_sel == 0:
                    strsql_candidat_afficher = """SELECT ID_Candidat, Nom, Prenom, Email, Mot_de_passe, Telephone, Date_de_naissance, Adresse, Titre_profil, Resume FROM t_candidat ORDER BY ID_Candidat ASC"""
                    mc_afficher.execute(strsql_candidat_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_candidat"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du candidat sélectionné avec un nom de variable
                    valeur_id_candidat_selected_dictionnaire = {"value_id_candidat_selected": id_candidat_sel}
                    strsql_candidat_afficher = """SELECT ID_Candidat, Nom, Prenom, Email, Mot_de_passe, Telephone, Date_de_naissance, Adresse, Titre_profil, Resume  FROM t_candidat WHERE ID_Candidat = %(value_id_candidat_selected)s"""

                    mc_afficher.execute(strsql_candidat_afficher, valeur_id_candidat_selected_dictionnaire)
                else:
                    strsql_candidat_afficher = """SELECT ID_Candidat, Nom, Prenom, Email, Mot_de_passe, Telephone, Date_de_naissance, Adresse, Titre_profil, Resume  FROM t_candidat ORDER BY ID_Candidat DESC"""

                    mc_afficher.execute(strsql_candidat_afficher)

                data_candidat = mc_afficher.fetchall()

                print("data_candidat ", data_candidat, " Type : ", type(data_candidat))

                # Différencier les messages si la table est vide.
                if not data_candidat and id_candidat_sel == 0:
                    flash("""La table "t_candidat" est vide. !!""", "warning")
                elif not data_candidat and id_candidat_sel > 0:
                    # Si l'utilisateur change l'id_candidat dans l'URL et que le candidat n'existe pas,
                    flash(f"Le candidat demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_candidat" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données candidat affichés !!", "success")

        except Exception as Exception_candidat_afficher:
            raise ExceptioncandidatAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{candidat_afficher.__name__} ; "
                                          f"{Exception_candidat_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("candidat/candidat_afficher.html", data=data_candidat)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /candidat_ajouter
    
    Test : ex : http://127.0.0.1:5575/candidat_ajouter
    
    Paramètres : sans
    
    But : Ajouter un candidat pour un film
    
    Remarque :  Dans le champ "name_candidat_html" du formulaire "candidat/candidat_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

class ExceptioncandidatAjouterWtf(Exception):
    pass

@app.route("/candidat_ajouter", methods=['GET', 'POST'])
def candidat_ajouter_wtf():
    form = FormWTFAjoutercandidat()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                prenom = form.prenom.data
                nom = form.nom_candidat_wtf.data
                email = form.email.data
                mot_de_passe = form.mot_de_passe.data
                telephone = form.telephone.data
                date_de_naissance = form.date_de_naissance.data
                adresse = form.adresse.data
                titre_profil = form.titre_profil.data
                resume = form.resume.data
                id_candidat = form.id_candidat.data

                valeurs_insertion_dictionnaire = {
                    "value_prenom": prenom,
                    "value_nom": nom,
                    "value_email": email,
                    "value_mot_de_passe": mot_de_passe,
                    "value_telephone": telephone,
                    "value_date_de_naissance": date_de_naissance,
                    "value_adresse": adresse,
                    "value_titre_profil": titre_profil,
                    "value_resume": resume,
                    "value_id_candidat": id_candidat
                }

                strsql_insert_candidat = """INSERT INTO t_candidat (ID_Candidat, Prenom, Nom, Email, Mot_de_passe, Telephone, Date_de_naissance, Adresse, Titre_profil, Resume) 
                                            VALUES (%(value_id_candidat)s, %(value_prenom)s, %(value_nom)s, %(value_email)s, %(value_mot_de_passe)s, %(value_telephone)s, 
                                            %(value_date_de_naissance)s, %(value_adresse)s, %(value_titre_profil)s, %(value_resume)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_candidat, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('candidat_afficher', order_by='ASC', id_candidat_sel=0))

        except Exception as Exception_candidat_ajouter_wtf:
            raise ExceptioncandidatAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                              f"{candidat_ajouter_wtf.__name__} ; "
                                              f"{Exception_candidat_ajouter_wtf}")

    return render_template("candidat/candidat_ajouter_wtf.html", form=form)




"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /candidat_update
    
    Test : ex cliquer sur le menu "candidat" puis cliquer sur le bouton "EDIT" d'un "candidat"
    
    Paramètres : sans
    
    But : Editer(update) un candidat qui a été sélectionné dans le formulaire "candidat_afficher.html"
    
    Remarque :  Dans le champ "nom_candidat_update_wtf" du formulaire "candidat/candidat_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""
class ExceptioncandidatUpdateWtf(Exception):
    pass

@app.route("/candidat_update", methods=['GET', 'POST'])
def candidat_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_candidat"
    id_candidat_update = request.values['id_candidat_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatecandidat()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur des champs depuis "candidat_update_wtf.html" après avoir cliqué sur "SUBMIT".
            id_candidat = form_update.id_candidat.data
            name_candidat_update = form_update.nom_candidat_update_wtf.data
            prenom_candidat_update = form_update.prenom_candidat_update_wtf.data
            email_candidat_update = form_update.email_candidat_update_wtf.data
            mot_de_passe_candidat_update = form_update.mot_de_passe_candidat_update_wtf.data
            telephone_candidat_update = form_update.telephone_candidat_update_wtf.data
            date_de_naissance_candidat_update = form_update.date_de_naissance_candidat_update_wtf.data
            adresse_candidat_update = form_update.adresse_candidat_update_wtf.data
            titre_profil_candidat_update = form_update.titre_profil_candidat_update_wtf.data
            resume_candidat_update = form_update.resume_candidat_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_candidat": id_candidat,
                "value_name_candidat": name_candidat_update,
                "value_prenom_candidat": prenom_candidat_update,
                "value_email_candidat": email_candidat_update,
                "value_mot_de_passe_candidat": mot_de_passe_candidat_update,
                "value_telephone_candidat": telephone_candidat_update,
                "value_date_de_naissance_candidat": date_de_naissance_candidat_update,
                "value_adresse_candidat": adresse_candidat_update,
                "value_titre_profil_candidat": titre_profil_candidat_update,
                "value_resume_candidat": resume_candidat_update
            }

            str_sql_update_intitulecandidat = """UPDATE t_candidat SET 
                Nom = %(value_name_candidat)s, 
                Prenom = %(value_prenom_candidat)s,
                Email = %(value_email_candidat)s,
                Mot_de_passe = %(value_mot_de_passe_candidat)s,
                Telephone = %(value_telephone_candidat)s,
                Date_de_naissance = %(value_date_de_naissance_candidat)s,
                Adresse = %(value_adresse_candidat)s,
                Titre_profil = %(value_titre_profil_candidat)s,
                Resume = %(value_resume_candidat)s
                WHERE ID_Candidat = %(value_id_candidat)s"""

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulecandidat, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_candidat_update"
            return redirect(url_for('candidat_afficher', order_by="ASC", id_candidat_sel=id_candidat_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer les données du candidat à mettre à jour
            str_sql_id_candidat = "SELECT * FROM t_candidat " \
                               "WHERE ID_Candidat = %(value_id_candidat)s"
            valeur_select_dictionnaire = {"value_id_candidat": id_candidat_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_candidat, valeur_select_dictionnaire)
                data_nom_candidat = mybd_conn.fetchone()

            # Afficher les valeurs sélectionnées dans les champs du formulaire "candidat_update_wtf.html"
            form_update.id_candidat.data = data_nom_candidat["ID_Candidat"]
            form_update.nom_candidat_update_wtf.data = data_nom_candidat["Nom"]
            form_update.prenom_candidat_update_wtf.data = data_nom_candidat["Prenom"]
            form_update.email_candidat_update_wtf.data = data_nom_candidat["Email"]
            form_update.mot_de_passe_candidat_update_wtf.data = data_nom_candidat["Mot_de_passe"]
            form_update.telephone_candidat_update_wtf.data = data_nom_candidat["Telephone"]
            form_update.date_de_naissance_candidat_update_wtf.data = data_nom_candidat["Date_de_naissance"]
            form_update.adresse_candidat_update_wtf.data = data_nom_candidat["Adresse"]
            form_update.titre_profil_candidat_update_wtf.data = data_nom_candidat["Titre_profil"]
            form_update.resume_candidat_update_wtf.data = data_nom_candidat["Resume"]

    except Exception as Exception_candidat_update_wtf:
        raise ExceptioncandidatUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{candidat_update_wtf.__name__} ; "
                                      f"{Exception_candidat_update_wtf}")

    return render_template("candidat/candidat_update_wtf.html", form_update=form_update)




"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /candidat_delete
    
    Test : ex. cliquer sur le menu "candidat" puis cliquer sur le bouton "DELETE" d'un "candidat"
    
    Paramètres : sans
    
    But : Effacer(delete) un candidat qui a été sélectionné dans le formulaire "candidat_afficher.html"
    
    Remarque :  Dans le champ "nom_candidat_delete_wtf" du formulaire "candidat/candidat_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""

class ExceptioncandidatDeleteWtf(Exception):
    pass

@app.route("/candidat_delete", methods=['GET', 'POST'])
def candidat_delete_wtf():
    data_films_attribue_candidat_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_candidat"
    id_candidat_delete = request.values['id_candidat_btn_delete_html']

    # Objet formulaire pour effacer le candidat sélectionné.
    form_delete = FormWTFDeletecandidat()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("candidat_afficher", order_by="ASC", id_candidat_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "candidat/candidat_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_candidat_delete = session['data_films_attribue_candidat_delete']
                print("data_films_attribue_candidat_delete ", data_films_attribue_candidat_delete)

                flash(f"Effacer le candidat de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer candidat" qui va irrémédiablement EFFACER le candidat
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_candidat": id_candidat_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_candidat = """DELETE FROM t_candidat WHERE ID_Candidat = %(value_id_candidat)s"""
                str_sql_delete_idcandidat = """DELETE FROM t_candidat WHERE ID_Candidat = %(value_id_candidat)s"""
                # Manière brutale d'effacer d'abord la "fk_candidat", même si elle n'existe pas dans la "t_candidat_film"
                # Ensuite on peut effacer le candidat vu qu'il n'est plus "lié" (INNODB) dans la "t_candidat_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_candidat, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idcandidat, valeur_delete_dictionnaire)

                flash(f"candidat définitivement effacé !!", "success")
                print(f"candidat définitivement effacé !!")

                # afficher les données
                return redirect(url_for('candidat_afficher', order_by="ASC", id_candidat_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_candidat": id_candidat_delete}
            print(id_candidat_delete, type(id_candidat_delete))

            # Requête qui affiche tous les films_candidat qui ont le candidat que l'utilisateur veut effacer
            str_sql_candidat_films_delete = """SELECT ID_Candidat, Nom, Prenom, Email, Mot_de_passe, Telephone, Date_de_naissance, Adresse, Titre_profil, Resume FROM t_candidat WHERE ID_Candidat = %(value_id_candidat)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_candidat_films_delete, valeur_select_dictionnaire)
                data_films_attribue_candidat_delete = mydb_conn.fetchall()
                print("data_films_attribue_candidat_delete...", data_films_attribue_candidat_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "candidat/candidat_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_candidat_delete'] = data_films_attribue_candidat_delete

                # Opération sur la BD pour récupérer "id_candidat" et "intitule_candidat" de la "t_candidat"
                str_sql_id_candidat = "SELECT ID_Candidat, Nom, Prenom, Email, Mot_de_passe, Telephone, Date_de_naissance, Adresse, Titre_profil, Resume FROM t_candidat WHERE ID_Candidat = %(value_id_candidat)s"

                mydb_conn.execute(str_sql_id_candidat, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom candidat" pour l'action DELETE
                data_nom_candidat = mydb_conn.fetchone()
                print("data_nom_candidat ", data_nom_candidat, " type ", type(data_nom_candidat), " candidat ",
                      data_nom_candidat["Nom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "candidat_delete_wtf.html"
            form_delete.nom_candidat_delete_wtf.data = data_nom_candidat["Nom"]

            # Le bouton pour l'action "DELETE" dans le form. "candidat_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_candidat_delete_wtf:
        raise ExceptioncandidatDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{candidat_delete_wtf.__name__} ; "
                                      f"{Exception_candidat_delete_wtf}")

    return render_template("candidat/candidat_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_candidat_delete)
