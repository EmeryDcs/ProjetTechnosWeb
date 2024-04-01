from flask import *
from peewee import PostgresqlDatabase
from peewee import (
    Model,
    PrimaryKeyField,
    CharField,
    DecimalField,
    BooleanField,
    ForeignKeyField,
    IntegerField
)

DB_HOST = 'localhost'
DB_USER = 'admin'
DB_PASSWORD = 'pass'
DB_PORT = 5432
DB_NAME = 'db-tp-python'

db = PostgresqlDatabase('my_database', user='my_user', password='my_password', host='localhost', port=5432)

class Produit(Model):
    id = PrimaryKeyField()
    nom = CharField()
    type = CharField()
    description = CharField()
    prix = DecimalField()
    en_stock = BooleanField()
    hauteur = DecimalField()
    poids = DecimalField()
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
    prix_total = DecimalField()
    email = CharField(null=True)
    carte_credit = CharField()
    information_livraison = CharField()
    payer = BooleanField(default = False)
    transaction = CharField(null = True)
    prix_livraison = DecimalField(null = True)

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

    class Meta:
        database = db

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