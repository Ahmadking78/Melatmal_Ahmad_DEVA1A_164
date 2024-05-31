"""
    Fichier : gestion_competences_candidat_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *


class FormWTFAjoutercompetences_candidat(FlaskForm):
    """
    Form for adding competences candidat.
    """
    FK_Candidat = StringField("FK Candidat", validators=[DataRequired()])
    FK_Competence = StringField("FK Competence", validators=[DataRequired()])
    Niveau = StringField("Niveau", validators=[DataRequired()])

    submit = SubmitField("Enregistrer competences_candidat")



class FormWTFUpdatecompetences_candidat(FlaskForm):
    """
        Dans le formulaire "competences_candidat_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    FK_Candidat = StringField("FK Candidat", validators=[Length(min=2, max=20, message="min 2 max 20")])
    FK_Competence = StringField("FK Competence", validators=[Length(min=2, max=20, message="min 2 max 20")])
    Niveau = StringField("Niveau", validators=[Length(min=2, max=20, message="min 2 max 20")])
    submit = SubmitField("Update competences_candidat")



class FormWTFDeletecompetences_candidat(FlaskForm):
    """
        Dans le formulaire "competences_candidat_delete_wtf.html"

        nom_competences_candidat_delete_wtf : Champ qui reçoit la valeur du competences_candidat, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "competences_candidat".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_competences_candidat".
    """
    nom_competences_candidat_delete_wtf = StringField("Effacer ce competences_candidat")
    submit_btn_del = SubmitField("Effacer competences_candidat")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
