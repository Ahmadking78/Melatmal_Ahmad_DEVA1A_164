# Module 164 Melatmal_Ahmad_DEVA1A_Recherche_de_Emploi 2024.06.07

# Installation de mon projet CRUD Python

Ce guide détaille les étapes nécessaires pour installer et exécuter mon projet CRUD Python sur votre machine locale.

## Prérequis

Avant de commencer, assurez-vous d'avoir les logiciels suivants installés sur votre système :

- Python (version 3.12.2)
- pip (le gestionnaire de paquets Python)

## Installation

1. Clonez ce dépôt GitHub en utilisant la commande suivante :

    ```
    git clone https://github.com/votre-utilisateur/votre-projet.git
    ```

    Ou téléchargez le dossier zip à partir du lien GitHub et extrayez-le sur votre machine.

2. Accédez au répertoire de votre projet :

    ```
    cd Melatmal_Ahmad_DEVA1A_164
    ```

3. Installez les dépendances en utilisant pip et le fichier requirements.txt :

    ```
    pip install -r requirements.txt
    ```

4. Importez la base de données dans votre système de gestion de bases de données MySQL :

    Utilisez le fichier `database/Melatmal_Ahmad_DEVA1A_Recherche_de_Emploi_164_2024.sql` pour créer la base de données.

## Structure des fichiers

Tous les fichiers nécessaires au bon fonctionnement du projet se trouvent dans le répertoire `database/`, y compris :

- Cahier des Charges
- Dictionnaire des Données
- Modèle Conceptuel de Données (MCD)
- Modèle Logique de Données (MLD)
- La base de données .SQL
- Toutes les requêtes .SQL nécessaires

## Fichier .env

Le fichier `.env` contient toutes les informations de connexion à la base de données ainsi que d'autres paramètres nécessaires à l'application. Voici un exemple de contenu :

```plaintext
# Serveur MySql
HOST_MYSQL="localhost"
USER_MYSQL="root"
PASS_MYSQL=""
PORT_MYSQL=3306
```

Si vous utilisez PHPMyAdmin, vous pouvez laisser les champs tels qu'ils sont, sauf si vous avez défini un mot de passe pour votre base de données, auquel cas vous devez spécifier ce mot de passe dans le champ PASS_MYSQL.

Si vous utilisez une autre base de données comme Laragon, XAMPP, ou tout autre système de gestion de bases de données, veuillez remplir tous les champs en fonction de votre configuration. Par exemple, vous devrez spécifier le bon HOST_MYSQL, USER_MYSQL, PASS_MYSQL et PORT_MYSQL.


## Exécution

1. Une fois l'installation terminée et la base de données importée, vous pouvez exécuter l'application en utilisant le fichier run_mon_app.py :

    ```
    python run_mon_app.py
    ```


2. L'application devrait maintenant être accessible depuis votre navigateur à l'adresse http://localhost:port (remplacez "port" par le numéro de port sur lequel l'application s'exécute).