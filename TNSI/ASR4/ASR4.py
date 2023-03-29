#!/usr/bin/env python
# coding: utf-8

# # ASR4 - Sécurisation des communications
# 
# # TP - Cryptographie 
# 
# La cryptographie est la science portant sur le **chiffrement** et le **déchiffrement** de données, c'est à dire de la transformation de celles-ci dans le but de les rendre incompréhensibles à quiconque ne dispose pas de la bonne **clé**. 
# 
# Nous allons à travers ce TP, en découvrir plusieurs méthodes.
# 

# ## 1 - Préparation
# 
# ### 1.1 - Échange de fichiers textes sur canal public
# 
# Ce TP a pour objectif de vous faire échanger des messages les uns avec les autres de manière sécurisée par le biais d'un cannal de discussion public. Nous allons pour cela utiliser un thread discord : 
# 
# > Q1 - Connectez-vous au serveur discord et rejoignez le thread CRYPTO.
# 
# Sur ce thread, vous allez vous échanger des messages sous la forme de fichiers textes. Les consignes suivantes sont à respecter :
# 
# - Un fichier a un **destinataire** spécifié dans le nom du fichier : `toto.txt` est destiné à Toto. 
# - Un fichier peut être **clair** ou **chiffré**, le nom d'un fichier chiffré est préfixé selon son protocole de chiffrement :
# 
# | Protocole de chiffrement | Préfixe          | Exemple        |
# | ------------------------ | ---------------- | -------------- |
# | Aucun                    |                  | `toto.txt`     |
# | César                    | `ces`            | `ces_toto.txt` |
# | XOR                      | `xor`            | `xor_toto.txt` |
# | Merkle                   | `mer`            | `mer_toto.txt` |
# | Diffie-Hellman           | `dhm`            | `dhm_toto.txt` |
# | RSA                      | `rsa`            | `rsa_toto.txt` |
# 
# - Excepté pour les méthodes de Merkle et Diffie-Hellman, un fichier commence par la ligne `Aujourd'hui il fait beau, Toto va à la plage.`.
# 
# > Q2 - Regroupez-vous par binomes puis échangez vous sur le thread un message clair en respectant les consignes.
# 
# ### 1.2 - Type bytes, encodage 
# 
# Le type Python `bytes` correspond à une **chaîne non-mutable et non-modifiable d'octets**, il d'agît d'un type de données très proches des données brutes manipulées dans une machine ou échangées sur un réseau. Travailler avec de tels objets plutôt qu'avec des chaînes de caractères permet de mieux apréhender les algorthmes de chiffrements que nous allons voir mais aussi de manipuler des fichiers n'étant pas forcément des textes. 
# 
# On peut construire des objets de ce type de plusieurs manières :

# In[5]:


# À partir de tableaux d'entiers entre 0 et 255

t = [65,123,235,55]
b = bytes(t)
t = list(b)

print(b)
print(len(b), b[0], b[1])
print()


# En encodant une chaîne de caractère en utf-8

s = "élève"
b = s.encode() 
s = b.decode()   # les méthodes encodes et décode peuvent prendre en argument le format d'encodage mais par défaut il s'agît de l'utf-8

print(b)
print(len(b), b[0], b[1])
print()

# À partir d'un entier qu'on écrit en base 256

n = 1025
b = int.to_bytes(n,2,'big')   # l'argument 2 sert à préciser le nombre d'octets à utiliser pour encoder l'entier 
n = int.from_bytes(b, 'big')  # dans les deux cas, l'argument 'big' sert à préciser qu'on lit le binaire de gauche à droite

print(b)
print(len(b), b[0], b[1])


# > Q3 - Convertir le tableau `[65,66,67]` en bytes et afficher le résultat, comment l'expliquer ?
# 
# > Q4 - Convertir le texte `"école"` en bytes et en afficher la taille. Pourquoi n'obtient-on pas 5 ? 
# 
# > Q5 - Convertir l'entier `2000` en un bytes `b` (2 octets) et afficher les valeurs de `b[1]` et `b[0]`. Retrouver ces valeurs par le calcul.

# In[ ]:





# Afin de lire et écrire dans nos fichiers textes en Python, nous utiliserons les fonctions suivantes : 

# In[7]:


def f_read(file_name: str):
    """chargement du fichier file_name dans un bytes"""
    f = open(file_name, 'rb')   # ouvre un flux de données binaires en lecture provenant de "toto.txt" 
    b = f.read()                # stocke le contenu du fichier dans un bytes b 
    f.close()                   # coupe le flux
    return b


def f_write(file_name:str, b:bytes):
    """sauvegarde du bytes b dans le fichier file_name"""
    f = open(file_name, 'wb')   # ouvre un flux de données binaires en lecture provenant de "toto.txt" 
    f.write(b)                  # stocke le contenu du fichier dans un bytes b 
    f.close()                   # coupe le flux


# > Q6 - Écrire un script Python comptant le nombre de lettres `'a'` dans un fichier texte.
# 
# > Q7 - Écrire un script Python générant un fichier texte `"hello.txt"` contenant le texte `"hello world!"`.
# 

# In[ ]:





# ### 1.3 - Données interprétées, données encodées, données chiffrées
# 
# Il est important avant de passer à la suite de bien distinguer les différentes formes sous lesquelles des données peuvent être manipulées. Pour cela, prenons l'exemple d'un lecteur de musique. 
# 
# - Données interprétées : pour notre logiciel, un fichier son est une suite de fréquences à transmette à un système son à intervalle de temps régulié. En Python, on pourrait imaginer garder en mémoire:
#  - le nombre `N:int` de sons joués par seconde ;
#  - un tableau `t:list[float]`, la liste de toutes des à jouer, dans l'ordre.
#  
#  
#  
# - Données encodées : pour garder en mémoire un fichier son sur un ordinateur, celui-ci doit être mis sous la forme d'une suite de bits ou encore d'une suites d'octets, on parle alors de fichier **encodé**. La méthode permettant de passer de données interprétées à des données encodées est appelé le **format d'encodage**, il donne généralement son extention au fichier.
#  - dans notre exemple, on peut encoder notre fichier au format mp3, wav, wma, midi, etc. ;
#  - pour encoder des nombres relatif, on peut utiliser le complément à deux sur un certain nombre de bits (ce n'est pas ce que fait Python) ;
#  - pour encoder des flottants, on utilise le format IEEE754 simple ou double ;
#  - pour encoder un texte, on peut utiliser selon le texte les formats ASCII, latin-$n$, UTF-8, UTF-16, UTF-32, etc.
#  
#  
#  
#  
# - Données chiffrées : si on veut envoyer par mail un fichier sensible `"top_secret.mp3"`, on a tout intérêt à le modifier de sorte qu'une personne malveillante qui intercepterait le mail ne puisse pas le lire sans en avoir l'autorisation. On va donc générer un nouveau fichier `"top_secret_crypte"` (l'extention n'a pas d'importance) à partir des octets de `"top_secret.mp3"` à l'aide d'un **algorithme de chiffrement**. C'est ce fichier que l'on va envoyer. Le destinataire, avec qui on se sera miis d'accord au préalable, devra alors déchiffrer le fichier avant de le lancer avec son propre lecteur.
# 
# 
# 
# ![Super schéma 1](encodage.jpg)

# ## 2 - Chiffrements symétriques
# 
# Un **algorithme de chiffrement symétrique** est une méthode permettant de chiffrer des données à l'aide d'une certaine **clée**, cette **même clée** étant nécessaire pour déchiffrer les données.
# 
# ### 2.1 - Chiffrement de César
# 
# ### Principe
# 
# Le chiffrement de César consiste, dans sa version historique, à effectuer un décalage d'un certain nombre des 26 lettres de l'alphabet dans le but de chiffrer un texte, chaque lettre étant remplacée par une autre. **La valeur du décalage constitue la clé du chiffrement**. 
# 
# Par exemple, avec un décalage de k=3 on transforme les lettre d'un message de la façon suivante :
# 
# | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z |
# |-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
# | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z | a | b | c |
# 
# Le message `"coucou"` est chiffré en `"frxfrx"`.
# 
# À l'inverse, une personne voulant déchiffrer un message devra alors savoir que le texte original a subi un décalage de 3 pour pouvoir le déchiffrer à l'aide du tableau inverse : 
# 
# | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z |
# |-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
# | x | y | z | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w |
# 
# Le message chiffré `"khoor"` se déchiffre ainsi en `"hello"`.
# 
# > Q1 - chiffrer le message `"bonjour"` avec la clé `k = 16`. 
# 
# ### Implémentation 
# 
# Informatiquement, il ne sert à rien de ne chiffrer que les lettres. Il est préférable de travailler sur les octets du fichier encodé.
# 
# > Q2.a - Écrire une fonction `cesar(b:bytes, k:int) -> bytes` prenant en argument une chaîne d'octets `b` et une clé entière `k` et renvoyant la chaîne d'octets obtenue en décalant les octets de `k` (après 255, on revient à 0). 
# 
# 

# In[ ]:





# > Q2.b - Ci-dessous se trouve un `bytes` chiffré à l'aide de cette fonction avec la clé `k = 149`. Avec quelle clé peut-on le déchiffrer ? 

# In[1]:


b = b'\xd7\x07\xf6\x0b\x04\xb5\xb6\xb5\xe9\n\xb5\xf6\x08\xb5\x07X>\n\x08\x08\xfe\xb5X5\xb5\xf9X>\xf8\xfd\xfe\xfb\xfb\x07\xfa\x07\xb5\x01\xfa\xb5\x02\xfa\x08\x08\xf6\xfc\xfa\xc3\xb5\xdf\xbc\xfa\x08\x05X=\x07\xfa\xb5\x06\n\xfa\xb5\t\n\xb5\t\xbc\xf6\x02\n\x08\xfa\x08\xb5\xf7\xfe\xfa\x03\xb5\xfa\t\xb5\xf7\x04\x03\xb5\xf8\x04\n\x07\xf6\xfc\xfa\xb5\x05\x04\n\x07\xb5\x01\xf6\xb5\x08\n\xfe\t\xfa\xb5\xb6'


# > Q3.a - À l'aide d'un éditeur de texte, écrire un message secret à destination de votre binome.
# 
# > Q3.b - Mettez vous d'accord (de manière discrète !) sur une clé de chiffrement partargée.
# 
# > Q3.c - Écrivez programme Python permettant de chiffrer votre message avec la clé choisie.
# 
# > Q3.d - Transmettez ce message à votre binome en passant par le canal public. 
# 
# > Q3.e - Écrivez programme Python permettant de déchiffrer le message de votre binome.

# In[2]:


##############
# CORRECTION #
##############


# ### 2.2 - Chiffrement XOR
# 
# ### Petit rappel de première : la fonction booléenne XOR 
# 
# On définit la fonction XOR (ou exclusif) par la table de vérité suivante : 
# 
# | x | y | x $\oplus$ y |
# | - | - | - |
# | 0 | 0 | 0 |
# | 0 | 1 | 1 |
# | 1 | 0 | 1 |
# | 1 | 1 | 0 |
# 
# Cette fonction possède une propriété intéressante pour le chiffrement de données binaires : 
# 
# *Quelques soient $x$ et $y$ $\in\mathbb{B}$,*
# $$
# (x\oplus y)\oplus y = x
# $$
# 
# On voit qu'un booléen $y$ peut servir de clé de chiffrement pour un autre booléen $x$. Dit comme cela ce n'est pas très intéressant, mais consirérons maintenant l'opération XOR sur un octet (8-bits). Étant donnés deux octets $X$ et $Y$, on obtient l'octet $X\oplus Y$ en effectuant l'opération XOR sur chacuns des 8 bits de $X$ et de $Y$.
# 
# Prenons un exemple : 
# 
# 
# $$
# \begin{array}{cc cccc cccc}
#  &&1&1&1&0& &0&1&0&1\\
# \oplus&&1&0&1&1& &0&0&0&1\\
# \hline
# =&&0&1&0&1& &0&1&0&0\\
# \end{array}
# $$
# 
# Biensur, la propriété valable pour les bits reste valable pour les octets, on a toujours *quelques soient les octets $X$ et $Y$,* 
# $$
# (X\oplus Y)\oplus Y = X
# $$
# 
# Vérifions le sur notre exemple
# 
# $$
# \begin{array}{cc cccc cccc}
#  &&1&1&1&0& &0&1&0&1\\
# \oplus&&1&0&1&1& &0&0&0&1\\
# \hline
# =&&0&1&0&1& &0&1&0&0\\
# \oplus&&1&0&1&1& &0&0&0&1\\
# \hline
# =&&1&1&1&0& &0&1&0&1\\
# \end{array}
# $$
# 
# En Python, l'opérateur XOR a pour symbole `^` et peut être utilisé entre deux entiers, l'opération étant effectuée bit par bit. 

# In[ ]:


X = 234
Y = 177
print(X^Y)


# > Q4.a - Vérifier que ce calcul correspond à l'exemple donné plus haut en coalculant les écritures binaire de 234, 177 et 91. 
# 
# > Q4.b - Vérifier la propriété $(X\oplus K) \oplus K = X$ avec quelques exemples.
# 
# ### Algorithme de chiffrement 
# 
# On se donne une clé `k` sous la forme d'une chaîne de caractère. Si on veut chiffrer une chaîne d'octets `b`, on procède comme suit : 
# 
# 1. convertir `k` en chaîne d'octets ;
# 2. pour chaque octet de `b` :
#  1. faire correspondre cet octet avec un octet de `k` (si `k` a trop peu d'octet, on repart au premier) ;
#  2. appliquer l'opération XOR ;
# 3. renvoyer la chaîne d'octets ainsi construite.
# 
# > Q5.a - Écrire une fonction `xor(b:bytes, k;str) -> bytes` réalisant cet algorithme.
#  

# In[3]:


##############
# CORRECTION #
##############


# > Q5.b - Ci-dessous se trouve un `bytes` chiffré à l'aide de cette fonction avec la clé `k = "martingale"`. Avec quelle clé peut-on le déchiffrer ? 

# In[4]:


b = b')\xa2\xdb\x17\x00\n\xa4\xc8\x01\x00\x03\x15R\x1b\x07N\t\x04L\x11J\x00\x00\x06\xaa\xc4\x13\x04L\x15\x0c\x12RUI,\x15\x00\x1a\nM@'

##############
# CORRECTION #
##############


# > 6.a. À l'aide d'un éditeur de texte, écrire autre un message secret à destination de votre binome.
# 
# > 6.b. Mettez vous d'accord (de manière discrète !) sur une clé de chiffrement partargée.
# 
# > 6.c. Écrivez programme Python permettant de chiffrer votre message avec la clé choisie.
# 
# > 6.d. Transmettez ce message à votre binome en passant par le canal public. 
# 
# > 7.e. Écrivez programme Python permettant de déchiffrer le message de votre binome.

# ## 3 - Chiffrements asymétriques
# 
# 
# Les chiffrements symétriques sont bien pratiques pour chiffrer des données, mais possèdent une faille majeure : pour s'échanger des messages à l'aide de tels algorithmes, la connaissance de la clé de chiffrement est nécessaire au destinataire afin de déchiffrer le message de l'émetteur. Pour les utiliser, on doit donc se mettre d'accord sur une clé commune. Or :
# 
# - pas question de se rencontrer physiquement ou d'utiliser un autre canal (cela déplace le problème) ;
# - pas question de partager la clé de chiffrement en clair (sinon n'importe qui pourra déchiffrer le message).
# 
# Nous allons voir trois méthodes permettant à deux interlocteurs de se mettre d'accord sur une clé de chiffrement de manère sécurisée, c'est à dire sans qu'un intervenant extérieur ne puisse deviner celle-ci.
# 
# Pour plus de clareté dans la suite, et afin de décrire les protocoles d'échange de clés, nous désignerons les protagonistes de l'échange avec les noms suivants :
# 
# - Alice est l'emettrice ;
# - Bob est le destinataire ; 
# - Eve est une personne cherchant à espionner la conversation entre Alice et Bob.
# 
# Dans tous les cas, Alice et Bob doivent réussir à se mettre d'accord sur une clé de chiffrement commune en communiquant sur un canal public, sans qu'Eve (qui peut intercepter leurs messages) ne puisse la deviner. 
# 
# ### 3.1 Méthode des puzzles de Merkle
# 
# Le principe des puzzle de Merkle est le suivant : 
# 
# 1. Alice génère un grand nombre (par exemple `N = 10000`) de triplets aléatoires `(identifiant, grande_clé, petite_clé)`. Les chiffres du tableau se-dessous sont des valeurs à respecter pour le TP. 
# 
# 
#  | chaîne        | utilité                                      | taille | code ASCII des caractères |
#  | ------------- | -------------------------------------------- |------- | ------------------------- |
#  | `identifiant` | sert à identifier les lignes de manière sûre | 12     | entre 33 et 126           |
#  | `grande_cle`  | proposition de clé commune                   | 16     | entre 33 et 126           |
#  | `petite_cle`  | clé servant à chiffrer la ligne              | 4      | entre 65 et 90            |
#  
# 2. Alice génère N lignes de la forme `"identifiant : <identifiant>, cle <grande_cle>"`, les encode et les chiffre avec la `petite_cle` correspondante (ici avec un chiffrement XOR). Elle concatène ses lignes et les sauvegarde dans un fichier chiffré.
# 
# 3. Alice envoie le fichier chiffré à Bob. 
# 
# 4. Bob choisit une ligne au hasard et casse le chiffrement de cette ligne par force brute (c'est à dire qu'il essaie toutes les combinaisons possibles de `petite_clé` dans le but d'obtenir un message commençant par `"identifiant : ..."`)
# 
# 6. Bob envoie à Alice et en clair l'`identifiant` de la ligne.
# 
# 7. Alice et Bob peuvent communiquer avec la `grande_clé` correspondante (Alice retrouvant la clé à l'aide de son identifiant).

# In[18]:


# exemple de lignes générées
t = [
  "identifiant : hdy-gà%jKY)=, cle : u7odiez97&'Rg:.L",
  "identifiant : dzfuhuez!;:2, cle : {ocids8_ndsi68uq",
  "identifiant : @iuezgd_5'(), cle : 6857651dsqhg87&&",
  "identifiant : !:;,diusqh[', cle : %%%doeuzhdez2342",
  "identifiant : 1sacrehasard, cle : cestvraimentfou!"     
]

# les lignes du tableau sont ensuite chiffrées (50 octets) avec les petites clés et converties en un seul bytes (N*50 octets) 


# ![Super schéma 2](merkle.jpg)
# 
# > Q1 - En imaginant que Bob mette environs 10 seconde à casser le chiffrement de la ligne qu'il a choisit, expliquer pourquoi Eve ne pourra pas facilement deviner la clé commune.
# 
# > Q2 - Écrire des fonctions Pythons permettant de réaliser les étapes 1, 2, 4 et 6 de la méthode.
# 
# 

# In[5]:


##############
# CORRECTION #
##############


from random import randint

def chaine_alea(n,a,b):
    """Renvoie un str aleatoire de taille n dont les caractères ont un code unicode entre a et b (inclus)"""
    pass # à compléter

def generer(N:int):
    """Renvoie un tableau de N triplets (id, K, k)"""
    pass # à compléter

def chiffrer(t)->bytes:
    """Renvoie une version chiffrée de t dont chaque case contient une chaîne de caractère respectant les spécifications"""
    pass # à compléter

def choix(b:bytes)->tuple:
    """choisit aléatoirement une ligne du tableau chiffré b, casse son chiffrement et renvoie la clé et son identifiant"""
    pass # à compléter

def retrouver(t, i):
    """Renvoie la grande clé du tableau t d'identifiant i"""
    pass # à compléter

# Tests
t = generer(10)
b = chiffrer(t)
i, K = choix(b)
print("clé choisie par Bob :", K.decode())
print("identifiant correspondant :", i.decode())
print("clé retrouvée par Alice :", retrouver(t, i.decode()))


# > Q3 - En passant par le canal public, utilisez cette méthode pour vous mettre d'accord avec votre binôme sur une clé de chiffrement puis échangez-vous quelques messages chiffrés à l'aide de cette clé.
# 
# 
# ### 3.2 La méthode Diffie-Hellman
# 
# ### Principe 
# 
# La méthode de Diffie-Hellman est une autre méthode permettant à Alice et Bob de se mettre d'accord sur une clé. Basée sur des propriétés arithmétiques, elle est à la fois plus rapide et plus sûre que la méthode des puzzles de Merkle. 
# 
# 
# Pour fonctionner, cette méthode nécessite l'utilisation d'une certaine fonction à deux variables $M$ telle que :
# 
# - $M(M(x,y),z) = M(M(x, z), z)$ ;
# - La connaîssance de $x$ et de $M(x, y)$ ne permet pas facilement de retrouver $y$.
# 
# On fait souvent dans cette méthode une analogie avec des couleurs. $M$ représente le mélange entre deux couleurs $x$ et $y$. 
# 
# > Q4 - Expliquer pourquoi le mélange de couleurs correspond bien aux attentes.
# 
# Voici le principe de la méthode, expliqué avec des couleurs : 
# 
# 1. Alice et Bob disposent d'une couleur publique, disons `jaune`, connue de tous ;
# 2. Ils choisissent chacun une couleur privée, disons `rouge` pour Alice et `bleu` pour Bob ;
# 3. Ils mélangent chacun leur couleur privée avec leur couleur publique et envoient le résultat à l'autre :
#  - Alice envoie `orange` à Bob ;
#  - Bob envoie `vert` à Alice ; 
# 4. Chacun ajoute sa couleur privée au mélange qu'il a reçu et obtient la même couleur finale `marron acajou`.
# 
# 
# ![Super schéma récapatulatif 3](diffie-hellman.jpg)
# 
# 
# > Q5 - Expliquer pourquoi Eve ne peut pas facilement obtenir cette même couleur commune.
# 
# 
# ### Implémentation 
# 
# En pratique, on peut utiliser comme fonction de mélange l'exponentiation modulaire, c'est à dire, étant donné un certain module $p\geq 2$ premier :
# 
# $$ M(g,a) = g^a \text{ mod } p $$
# 
# En effet, les propriétés de l'exponentiation modulaire (l'opération puissance modulo $n$) sont essentiellement les même que l'exponentiation classique et en particulier : 
# 
# $$ 
# \begin{align}
# M(M(g, a),b) &= (g^a)^b \text{ mod } p \\
#              &= g^{ab} \text{ mod } p \\
#              &=  (g^b)^a \text{ mod } p \\ 
#              &= M(M(g,b),a)
# \end{align}
# $$
# 
# En revanche, il est difficile (on ne sait pas le faire de manière efficace) de calculer un logarithme modulaire, c'est à dire de retrouver $a$ à partir de $g^a \text{ mod } p$.
# 
# Pour mettre en oeuvre la méthode on procède comme suit :
# - $p$ et $g$ sont des nombres publics ; 
#  - $p$ est le module du chiffrement ;
#  - $g$ est la base du chiffrement (`jaune` dans l'exemple) ;
# - Alice et Bob gènèrent des nombres privés respectivement $a$ et $b$ (`rouge` et `bleu` dans l'exemple).
# - Alice et Bob s'échangent $M(g, a)$ et $M(g, b)$ ;
# - La clé commune secrète est $M(M(g, a),b) = M(M(g,b),a)$
# 
# > Q6.a - À l'aide de la fonction `pow` (voir la <a href = "https://docs.python.org/fr/3/library/functions.html#pow">documentation</a>) écrire une fonction `melange(g: int, a:int, p:int)` générant un bytes de 4 octets encodant l'entier $g^a\text{ mod }p$.
# 
# Nous travaillerons avec les valeurs publiques `p = 1364603701` et `g = 382417751` (tous les nombres générés seront encodables sur 4 octets).
# 
# > Q6.b - Générez un nombre `a` aléatoire entre `0` et `p-1` : ce nombre est secret.
# 
# > Q6.c - À l'aide de votre fonction `melange` envoyez en clair à votre binome un fichier de 4 octets correspondant au mélange de votre clé privée `a` avec la clé publique `g`.
# 
# > Q6.d - Décodez le fichier de votre binome et mélanger le résultat avec votre propre clé privée. Le résultat est votre clé de chiffrement commune de 4 octets à interpréter comme un entier ou une chaîne de caractère en fonction d'algorithme de chiffrement souhaité.
# 

# In[ ]:


def melange(g:int, a:int, p:int)->bytes:
  pass # à compléter

p = 1364603701
g = 382417751


# ### 3.3 - Chiffrement RSA 
# 
# ### Principe
# 
# Le chiffrement RSA utilise également des propriétés arithmétiques des entiers pour fonctionner. Voici dans les grandes lignes son fonctionnement :
# 
# - Alice génère trois nombres, appelés clés RSA : $n$, $e$ et $d$. 
# - Le couple $K_{\text{Alice}}^{\text{pub}} = (n, e)$ constitue la **clé publique d'Alice**, elle la partage en clair avec tout le monde.
# - Le couple $K_{\text{Alice}}^{\text{priv}} = (n, d)$ constitue la **clé privée d'Alice**, elle ne la partage avec personne.
# 
# Ces trois nombres sont liés par la propriété suivante :
# $$ \forall m \leq n,\text{ }(m^e)^d \text{ mod }n = (m^d)^e\text{ mod }n = m $$
# 
# Propriété qu'on notera : 
# $$ \forall m \leq n, \text{ } K_{\text{Alice}}^\text{priv}.K_{\text{Alice}}^\text{pub}(m) = K_{\text{Alice}}^\text{pub}.K_{\text{Alice}}^\text{priv}(m) = m $$
# 
# Cette propriété offre deux possibilités très intéressantes : 
# 
# 1. Bob peut chiffrer un message $m$ à l'aide de la clé publique d'Alice : $m' = K_{\text{Alice}}^\text{pub}(m)$. Alice sera la seule personne capable de déchiffrer ce message à l'aide de sa clé privée : $m = K_{\text{Alice}}^\text{priv}(m')$.
# 
# 2. Alice peut chiffrer un message à l'aide de sa clé privée : $m' = K_{\text{Alice}}^\text{priv}(m)$. Toute personne pourra déchiffrer ce message à l'aide de la clé publique d'Alice : $m = K_{\text{Alice}}^\text{pub}(m')$.
# 
# 
# La première permet évidemment de communiquer de manière sûre de Bob vers Alice. Pour communiquer de manière sûre de Alice vers Bob, il suffit que Bob génère ces propres clés RSA $K_{\text{Bob}}^{\text{pub}}$ et $K_{\text{Alice}}^{\text{priv}}$.
# 
# La seconde paraît *a priori* moins utile puisque tout le monde peut déchiffrer le message. On peut cependant remarquer que lorsqu'Alice chiffre un message, tout utilisateur pouvant déchiffrer celui-ci à l'aide de la clé publique d'Alice est assuré que le chiffrement provient d'elle (elle est la seule à connaître sa clé privée). On appelle cela signer un message, nous en parlerons plus en détail dans la partie suivante.
# 
# 
# ![Super schéma récapitulatif +](rsa.jpg)
# 
# 
# 
# ### Implémentation
# 
# Vous avez à votre disposition un module RSA dont voici l'interface :
# 
# | fonction | description |
# | ------- | ----------- |
# | `generer_cles(taille:int) -> tuple` | gérère le triplet de clés RSA $(n, e, d)$ |
# | `exporter_cle(n:int, k:int) -> bytes` | transforme la clé $(n, k)$ où $k = e$ ou $d$ en bytes |
# | `importer_cle(b:bytes) -> tuple`  | transforme le bytes `b` en clé $(n, k)$ où $k = e$ ou $d$ |
# | `chiffrer(b:bytes, n:int, k:int) -> bytes` | chiffre le bytes `b` à l'aide de la clé $(n, k)$ où $k = e$ ou $d$ |
# | `dechiffrer(b:bytes, n:int, k:int) -> bytes`  | déchiffre le bytes `b` à l'aide de la clé $(n, k)$ où $k = e$ ou $d$ |
# 
# 
# > Q7.a - Téléchargez le module et importez-le dans un programme Python.
# 
# > Q7.b - Générez des clés $n_A$, $e_A$, $d_A$ puis sauvegardez-les dans deux fichiers `toto_pubkey.rsa` et `toto_privkey.rsa` (remplacez `toto` par votre prénom...) contenant les clés publiques $(n_A,e_A)$ et privées $(n_A,d_A)$.
# 
# > Q7.c - Partagez votre fichier de clé publique `toto_pubkey.rsa` sur le canal public. Tout le monde peut maintenant vous envoyer des messages chiffrés.
# 
# > Q7.d -  Téléchargez le fichier de clé publique de votre binome et importer la clé $(n_{B}, e_{B})$ dans un programme Python.  Vous pouvez maintenant envoyer des message chiffrés à votre binome.
# 
# En réalité, le chiffrement RSA est trop lent pour être utilisé afin de chiffrer un grand flux de données (discussion, vocale, vidéo, stream, remote play, etc.). 
# 
# Sa sureté et sa capacité à signer des messages en font cependant un excellent moyen d'échanger la clé commune d'une méthode de chiffrement symétrique (plus rapide). 
# 
# > Q8.a - Comment Alice et Bob peuvent utiliser RSA pour se mettre d'accord sur une clé de chiffrement XOR ? 
# 
# > Q8.b - Appliquer cette méthode avec votre binome.
# 
# 
# ## 4 - Authentification
# 
# ### 4.1 - L'attaque de l'homme du milieu
# 
# Considérons la procédure suivante : 
# 
# 1. Alice et Bob génèrent des clés RSA et se les partagent.
# 2. Grâce au chiffrement RSA, ils s'échangent de manière sécurisée un fichier contenant une clé de chiffrement xor.
# 3. Grâce à cette clé, ils communiquent de manière rapide et sécurisée. 
# 
# Une fois l'échange de clé effectué, Alice et Bob peuvent considérer que leur discussion est sécurisée. Cependant, on peut imaginer qu'Eve (qui veut intercepter la conversation entre les deux autres) se fasse passer lors de l'étape 1 passer pour Alice et / ou Bob. On appelle cela l'**attaque de l'homme du milieu**, plus de détail sur la [page wikipédia](https://fr.wikipedia.org/wiki/Attaque_de_l%27homme_du_milieu). 
# 
# Afin de contrer cette attaque, c'est à dire pour Alice et Bob de s'assurer qu'ils ont bien affaire l'un à l'autre on utilise les signatures RSA d'une troisière personne, dite **tiers de confiance**.
# 
# 
# ### 4.2 - Tiers de confiance et certificats d'authentifications
# 
# Plaçons nous du point de vue de Bob voulant s'assurer de l'identité d'Alice.
# 
# Plutôt que de se fier directement à la clé publique d'Ailce, Bob va passer par un tiers de confiance que l'on nommera Théo. Bob est sûr de l'identité de Théo et Théo est capable de s'assurer de l'identité de ses interloculteurs (par exemple en exigeant de rencontrer physiquement ceux-ci, en leur faisant passer un questionnaire, etc). L'échange de clé RSA se déroule alors de la manière suivante.
# 
# 1. Alice s'identifie ou s'est préalablement identifiée auprès de Théo. 
# 
# 2. Théo fournit à Alice un **certificat d'authentification** $s = K_{\text{Theo}}^\text{priv}.K_{\text{Alice}}^\text{pub}$ à Alice en signant la clé publique d'Alice avec sa propre clé privée. 
# 
# 3. Alice fournit à Bob ce certificat.
# 
# 4. Bob peut déchiffrer ce certificat signé par Théo à l'aide de la clé publique de celui-ci et vérifier qu'il s'agît bien de la clé publique d'Alice $$K_{\text{Theo}}^\text{pub}(s) = K_{\text{Theo}}^\text{pub}.K_{\text{Theo}}^\text{priv}.K_{\text{Alice}}^\text{pub} = K_{\text{Alice}}^\text{pub}$$
# 
# 
# ![Super schéma récapitulatif ++](authentification.jpg)
# 
# 
# Cette procédure se retrouve dans la vie courante. Lorsqu'on veut s'assurer de l'identité de quelqu'un, on lui demande généralement de présenter des documents officiels (carte d'identité, passeport). Ces documents sont produits par une autorité de confiance (ici une administration d'état). Ainsi, pour s'identifier auprès de Bob :
# 
# 1. Alice se présente ou s'est préalablement présentée à la préfecture qui vérifie son identité.
# 2. La préfecture délivre à Alice une carte d'identité.
# 3. Pour prouver à Bob son identité, Alice lui montre sa carte.
# 4. Bob peut constater que la photo de la carte correspond au visage d'Alice. 
# 
# Dans le domaine du web, le rôle de Théo (ou de la préfecture) est joué par une **autorité de certification**. La comission européenne publie et tient à jour une [liste de telles autoritées](https://esignature.ec.europa.eu/efda/tl-browser/#/screen/home), jugées de confiance.
# 
# > Q1 - Connectez-vous à un site web utilisant HTTPS puis (en cliquant sur le verrous à gauche de l'URL), trouver le certificat du site ainsi que l'autorité de certification l'ayant délivré.
