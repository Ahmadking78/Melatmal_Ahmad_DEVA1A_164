--
-- les requêtes pour mon table CANDIDAT `t_candidat`
--
#Pour récupérer un candidat par son ID : 
SELECT ID_Candidat, Nom, Prenom, Email, Mot_de_passe, Telephone, Date_de_naissance, Adresse, Titre_profil, Resume 
FROM t_candidat 
WHERE ID_Candidat = 1;

#Création (Create) :
INSERT INTO t_candidat (Nom, Prenom, Email, Mot_de_passe, Telephone, Date_de_naissance, Adresse, Titre_profil, Resume) 
VALUES ('<nom>', '<prenom>', '<email>', '<mot_de_passe>', '<telephone>', '<date_de_naissance>', '<adresse>', '<titre_profil>', '<resume>');

#Mise à jour (Update) :
UPDATE t_candidat 
SET Nom='<nouveau_nom>', Prenom='<nouveau_prenom>', Email='<nouvel_email>', Mot_de_passe='<nouveau_mot_de_passe>', 
Telephone='<nouveau_telephone>', Date_de_naissance='<nouvelle_date_de_naissance>', Adresse='<nouvelle_adresse>', 
Titre_profil='<nouveau_titre_profil>', Resume='<nouveau_resume>' 
WHERE ID_Candidat = 1;

#Suppression (Delete) :
DELETE FROM t_candidat WHERE ID_Candidat = 1;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------



--
-- les requêtes pour mon table Candidature `t_candidature`
--
#Pour récupérer une candidature par son ID :
SELECT * FROM t_candidature WHERE ID_Candidature = 1;

#Création (Create) :
INSERT INTO t_candidature (FK_Candidat, FK_Offre, Date_Candidature, Lettre_Motivation, Statut) 
VALUES (1, 3, '2024-03-10', 'Dear Hiring Manager,\nI am writing to express my interest in the Supply Chain Manager position at Logistics Solutions Inc. I have extensive experience in logistics and inventory management, and I am confident in my ability to drive efficiency and optimize processes in your organization.\n\nSincerely, [Candidate]', 'Pending');

#Mise à jour (Update) :
UPDATE t_candidature 
SET FK_Candidat = 2, FK_Offre = 8, Date_Candidature = '2024-03-19', 
Lettre_Motivation = 'Dear Hiring Manager,\nI am excited to apply for the Venture Capital Analyst position at TechStart Ventures. With my strong financial analysis skills and passion for technology, I am eager to evaluate investment opportunities and support the growth of technology startups.\n\nBest regards, [Candidate]', Statut = 'Pending'
WHERE ID_Candidature = 10;

#Suppression (Delete) :
DELETE FROM t_candidature WHERE ID_Candidature = 3;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------



--
-- les requêtes pour mon table Competence `t_competence`
--
#Lecture (Read) :
SELECT * FROM t_competence;

SELECT * FROM t_competence WHERE ID_Competence = 1;

#Création (Create) :
INSERT INTO t_competence (Nom_Competence, Description) 
VALUES ('<nom_competence>', '<description>');

#Mise à jour (Update) :
UPDATE t_competence 
SET Nom_Competence = '<nouveau_nom_competence>', Description = '<nouvelle_description>' 
WHERE ID_Competence = 1;

#Suppression (Delete) :
DELETE FROM t_competence WHERE ID_Competence = 1;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------



--
-- les requêtes pour mon table Competences_Candidat `t_competences_candidat`
--
#Lecture (Read) :
SELECT * FROM t_competences_candidat WHERE FK_Candidat = 1;

SELECT * FROM t_competences_candidat WHERE FK_Candidat = 1 AND FK_Competence = 3;

#Création (Create) :
INSERT INTO t_competences_candidat (FK_Candidat, FK_Competence, Niveau) 
VALUES (1, 3, 'Intermediate');

#Mise à jour (Update) :
UPDATE t_competences_candidat 
SET Niveau = 'Advanced' 
WHERE FK_Candidat = 1 AND FK_Competence = 3;

#Suppression (Delete) :
DELETE FROM t_competences_candidat WHERE FK_Candidat = 1 AND FK_Competence = 3;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------



--
-- les requêtes pour mon table Employeur `t_employeur`
--
#Lecture (Read) :
SELECT * FROM t_employeur WHERE ID_Employeur = 1;

#Création (Create) :
INSERT INTO t_employeur (Nom_Entreprise, Secteur, Email, Telephone, Adresse, Description) 
VALUES ('<nom_entreprise>', '<secteur>', '<email>', '<telephone>', '<adresse>', '<description>');

#Mise à jour (Update) :
UPDATE t_employeur 
SET Nom_Entreprise = '<nouveau_nom_entreprise>', Secteur = '<nouveau_secteur>', 
Email = '<nouveau_email>', Telephone = '<nouveau_telephone>', Adresse = '<nouvelle_adresse>', 
Description = '<nouvelle_description>' 
WHERE ID_Employeur = 1;

#Suppression (Delete) :
DELETE FROM t_employeur WHERE ID_Employeur = 1;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------



--
-- les requêtes pour mon table Experience Professionnelle `t_experience_professionnelle`
--
#Lecture (Read) :
SELECT * FROM t_experience_professionnelle WHERE FK_Candidat = 1;

#Création (Create) :
INSERT INTO t_experience_professionnelle (FK_Candidat, Entreprise, Titre_Poste, Date_Debut, Date_Fin, Description) 
VALUES (1, '<entreprise>', '<titre_poste>', '<date_debut>', '<date_fin>', '<description>');

#Mise à jour (Update) :
UPDATE t_experience_professionnelle 
SET Entreprise = '<nouvelle_entreprise>', Titre_Poste = '<nouveau_titre_poste>', 
Date_Debut = '<nouvelle_date_debut>', Date_Fin = '<nouvelle_date_fin>', 
Description = '<nouvelle_description>' 
WHERE ID_Experience = 1;

#Suppression (Delete) :
DELETE FROM t_experience_professionnelle WHERE ID_Experience = 1;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------


--
-- les requêtes pour mon table Formation `t_formation`
--
#Lecture (Read) :
SELECT * FROM t_formation WHERE FK_Candidat = 1;

#Création (Create) :
INSERT INTO t_formation (FK_Candidat, Etablissement, Diplome, Domaine, Date_Debut, Date_Fin, Description) 
VALUES (1, '<etablissement>', '<diplome>', '<domaine>', '<date_debut>', '<date_fin>', '<description>');

#Mise à jour (Update) :
UPDATE t_formation 
SET Etablissement = '<nouvel_etablissement>', Diplome = '<nouveau_diplome>', Domaine = '<nouveau_domaine>', 
Date_Debut = '<nouvelle_date_debut>', Date_Fin = '<nouvelle_date_fin>', Description = '<nouvelle_description>' 
WHERE ID_Formation = 1;

#Suppression (Delete) :
DELETE FROM t_formation WHERE ID_Formation = 1;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------


--
-- les requêtes pour mon table Offre Emploi `t_offre_emploi`
--
#Lecture (Read) :
SELECT * FROM t_offre_emploi WHERE FK_Employeur = 1;

#Création (Create) :
INSERT INTO t_offre_emploi (FK_Employeur, Titre, Description, Date_Publication, Date_Expiration, Type_Contrat, Localisation, Salaire) 
VALUES (1, '<titre>', '<description>', '<date_publication>', '<date_expiration>', '<type_contrat>', '<localisation>', <salaire>);

#Mise à jour (Update) :
UPDATE t_offre_emploi 
SET Titre = '<nouveau_titre>', Description = '<nouvelle_description>', Date_Publication = '<nouvelle_date_publication>', 
Date_Expiration = '<nouvelle_date_expiration>', Type_Contrat = '<nouveau_type_contrat>', Localisation = '<nouvelle_localisation>', 
Salaire = <nouveau_salaire> 
WHERE ID_Offre = 1;

#Suppression (Delete) :
DELETE FROM t_offre_emploi WHERE ID_Offre = 1;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------



