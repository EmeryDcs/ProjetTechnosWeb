import time

from flask import *
from peewee import PostgresqlDatabase
from peewee import (
    Model,
    PrimaryKeyField,
    CharField,
    FloatField,
    BooleanField,
    ForeignKeyField,
    IntegerField
)

DB_HOST = "db"
DB_USER = 'user'
DB_PASSWORD = 'pass'
DB_PORT = 5432
DB_NAME = 'dbtp'

db = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

class Produit(Model):
    id = PrimaryKeyField()
    nom = CharField()
    type = CharField()
    description = CharField()
    prix = FloatField()
    en_stock = BooleanField()
    hauteur = FloatField()
    poids = FloatField()
    image = CharField()

    def to_dict(self): # Convertir un objet en dictionnaire
        return {
            'id': self.id,
            'nom': self.nom,
            'type': self.type,
            'description': self.description,
            'prix': self.prix,
            'en_stock': self.en_stock,
            'hauteur': self.hauteur,
            'poids': self.poids,
            'image': self.image
        }

    class Meta:
        database = db

class Commande(Model):
    id = PrimaryKeyField()
    prix_total = FloatField()
    email = CharField(null=True)
    carte_credit = CharField()
    information_livraison = CharField()
    payer = BooleanField(default = False)
    transaction = CharField(null = True)
    prix_livraison = FloatField(null = True)

    class Meta:
        database = db

class CommandeProduit(Model): # Table de liaison entre Commande et Produit, permet de gérer plusieurs produits pour une commande
    commande = ForeignKeyField(Commande)
    produit = ForeignKeyField(Produit)
    quantite = IntegerField()

    def to_dict(self): # Convertir un objet en dictionnaire
        print('carte_credit', self.commande.carte_credit),
        return {
            'order' :{
                'id': self.commande.id,
                'prix_total': self.commande.prix_total,
                'email': self.commande.email,
                'carte_credit': json.loads(self.commande.carte_credit.replace("'", "\"")) if self.commande.carte_credit else None,
                'information_livraison': json.loads(self.commande.information_livraison.replace("'", "\"")) if self.commande.information_livraison else None,
                'payer': self.commande.payer,
                'transaction': json.loads(self.commande.transaction.replace("'", "\"")) if self.commande.transaction else None,
                'produit': {
                    'id': self.produit.id,
                    'quantite': self.quantite,
                },
                'prix_livraison': self.commande.prix_livraison
            }
        }
    
    def to_dict_product(self):
        return {
            'id': self.produit.id,
            'quantite': self.quantite,
        }

    class Meta:
        database = db

time.sleep(1) # Attente de 5 secondes pour laisser le temps à la base de données de démarrer

db.connect()

db.create_tables([Produit, Commande, CommandeProduit], safe=True)

# Cette fonction n'est plus nécessaire
# def init_db():
#     produits = [
#         {
#             'nom': 'Brown eggs',
#             'description': 'Raw organic brown eggs in a basket',
#             'prix': 28.1,
#             'en_stock': True,
#             'poids': 400,
#             'image': '0.jpg'
#         },
#         {
#             'nom': 'Sweet fresh stawberry',
#             'description': 'Sweet fresh stawberry on the wooden table',
#             'prix': 29.45,
#             'en_stock': True,
#             'poids': 299,
#             'image': '1.jpg'
#         }
#     ]
#     for produit in produits:
#         Produit.create(**produit)