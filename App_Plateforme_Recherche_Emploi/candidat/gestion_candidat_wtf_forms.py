"""
    Fichier : gestion_candidat_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *


class FormWTFAjoutercandidat(FlaskForm):
    """
        Dans le formulaire "candidat_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_candidat_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom = StringField("Prénom", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                               Regexp(nom_candidat_regexp,
                                                      message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait d'union")])
    nom_candidat_wtf = StringField("Nom", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                      Regexp(nom_candidat_regexp,
                                                             message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait d'union")])
    email = StringField("Email", validators=[Length(min=6, max=50), Email(message="Adresse email invalide")])
    mot_de_passe = PasswordField("Mot de passe", validators=[Length(min=8, max=20, message="min 8 max 20")])
    telephone = StringField("Téléphone", validators=[Length(min=8, max=15, message="min 8 max 15")])
    date_de_naissance = DateField("Date de naissance", format='%Y-%m-%d', validators=[InputRequired("Date obligatoire")])
    adresse = StringField("Adresse", validators=[Length(min=2, max=100, message="min 2 max 100")])
    titre_profil = StringField("Titre du profil", validators=[Length(min=2, max=50, message="min 2 max 50")])
    resume = TextAreaField("Résumé")
    id_candidat = StringField("ID Candidat")  # Adding ID_Candidat field
    submit = SubmitField("Enregistrer candidat")


class FormWTFUpdatecandidat(FlaskForm):
    """
    Dans le formulaire "candidat_update_wtf.html", on impose que le champ soit rempli.
    Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    id_candidat = IntegerField("ID_Candidat")
    nom_candidat_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_candidat_update_wtf = StringField("Nom du candidat", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                         Regexp(nom_candidat_update_regexp,
                                                                                message="Pas de chiffres, de caractères "
                                                                                        "spéciaux, "
                                                                                        "d'espaces à double, de double "
                                                                                        "apostrophe, de double trait "
                                                                                        "d'union")
                                                                         ])
    prenom_candidat_update_wtf = StringField("Prénom du candidat")
    email_candidat_update_wtf = StringField("Email du candidat")
    mot_de_passe_candidat_update_wtf = PasswordField("Mot de passe du candidat")
    telephone_candidat_update_wtf = StringField("Téléphone du candidat")
    date_de_naissance_candidat_update_wtf = DateField("Date de naissance du candidat")
    adresse_candidat_update_wtf = StringField("Adresse du candidat")
    titre_profil_candidat_update_wtf = StringField("Titre de profil du candidat")
    resume_candidat_update_wtf = TextAreaField("Résumé du candidat")
    submit = SubmitField("Update candidat")




class FormWTFDeletecandidat(FlaskForm):
    """
        Dans le formulaire "candidat_delete_wtf.html"

        nom_candidat_delete_wtf : Champ qui reçoit la valeur du candidat, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "candidat".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_candidat".
    """
    nom_candidat_delete_wtf = StringField("Effacer ce candidat")
    submit_btn_del = SubmitField("Effacer candidat")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
