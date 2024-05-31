"""
    Fichier : gestion_offre_emploi_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""


from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *


class FormWTFAjouteroffre_emploi(FlaskForm):
    """
    Dans le formulaire "offre_emploi_ajouter_wtf.html" on impose que le champ soit rempli.
    Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    ID_Offre = StringField("ID Offre")
    FK_Employeur = StringField("FK Employeur")
    Titre = StringField("Titre")
    Description = StringField("Description")
    Date_Publication = DateField("Date de publication")
    Date_Expiration = DateField("Date d'expiration")
    Type_Contrat = StringField("Type de contrat")
    Localisation = StringField("Localisation")
    Salaire = FloatField("Salaire")
    submit = SubmitField("Enregistrer offre_emploi")



class FormWTFUpdateoffre_emploi(FlaskForm):
    """
    Dans le formulaire "offre_emploi_update_wtf.html" on impose que le champ soit rempli.
    Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    ID_Offre = IntegerField("ID_Offre")
    FK_Employeur = IntegerField("FK_Employeur")
    Titre = StringField("Titre")
    Description = TextAreaField("Description")
    Date_Publication = DateField("Date_Publication")
    Date_Expiration = DateField("Date_Expiration")
    Type_Contrat = StringField("Type_Contrat")
    Localisation = StringField("Localisation")
    Salaire = DecimalField("Salaire", places=2)
    submit = SubmitField("Update offre_emploi")



class FormWTFDeleteoffre_emploi(FlaskForm):
    """
        Dans le formulaire "offre_emploi_delete_wtf.html"

        nom_offre_emploi_delete_wtf : Champ qui reçoit la valeur du offre_emploi, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "offre_emploi".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_offre_emploi".
    """
    nom_offre_emploi_delete_wtf = StringField("Effacer ce offre_emploi")
    submit_btn_del = SubmitField("Effacer offre_emploi")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
