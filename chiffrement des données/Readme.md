**Chiffrement des données**
   
Ce programme utilise RSA pour chiffrer un fichier texte (source.txt) et sauvegarder son contenu chiffré dans un autre fichier (source_finale.txt). Ensuite, il copie ce fichier chiffré dans un répertoire de destination à l'aide de la bibliothèque shutil. Le processus comprend plusieurs étapes :

    1. Lecture du contenu du fichier source.
    2. Chiffrement du contenu à l'aide de la cryptographie RSA.
    3. Sauvegarde du contenu chiffré dans un fichier de sortie.
    4. Copie du fichier chiffré dans un répertoire de destination.

Prérequis

    - Python 3.x
    - Bibliothèque rsa pour la cryptographie RSA
    - Bibliothèque shutil pour la gestion des fichiers
