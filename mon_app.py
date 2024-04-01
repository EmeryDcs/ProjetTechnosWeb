# Projet réalisé en groupe avec Loïne Pommier

import os
import urllib.request
import cache_redis
import time

from flask import *
from models import Produit, Commande, CommandeProduit

app = Flask(__name__)

# --------------Partie 1 du projet----------------

#Affichage d'un formulaire pour créer une commande OU création d'une commande via un envoi de données JSON
@app.route('/order', methods=['POST', 'GET'])
def order():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'product' in data and 'id' in data['product'] and 'quantity' in data['product']:
                if data['product']['quantity'] >= 1:
                    produit = Produit.select().where(Produit.id == data['product']['id']).get()
                    print(produit.en_stock)
                    if (produit.en_stock) :
                        prix_total = Produit.select().where(Produit.id == data['product']['id']).get().prix * data['product']['quantity']
                        poids_livraison = Produit.select().where(Produit.id == data['product']['id']).get().poids * data['product']['quantity']
                        if poids_livraison < 500 :
                            prix_livraison = 5
                        elif poids_livraison < 2000 :
                            prix_livraison = 10
                        else : 
                            prix_livraison = 25

                        commande = Commande.create(
                            prix_total = prix_total,
                            carte_credit = "",
                            information_livraison = "",
                            transaction = "",
                            prix_livraison = prix_livraison
                        )
                        CommandeProduit.create(
                            commande = commande.id,
                            produit = data['product']['id'],
                            quantite = data['product']['quantity']
                        )
                        return redirect(url_for('order_resume', commande_id=commande.id), code=302)
                    else :
                        message_error = {
                            "error": {
                                'product': {
                                    "code": "out-of-inventory",
                                    "name": "Le produit demandé n'est pas en inventaire."
                                }
                            }
                        }
                        return message_error, 422
                else :
                    return "La quantité doit être supérieure à 0", 422
            else : #if 'product' in data and 'id' in data['product'] and 'quantity' in data['product']
                message_error = {
                    "error": {
                        'product': {
                            "code": "missing-field",
                            "name": "La création d'une commande nécessite un produit ou une quantité."
                        }
                    }
                }
                return message_error, 422
        else : #if request.is_json
            return 'Bad Request', 400
    else : #if request.method == 'POST'
        return render_template('order.html')

#Affichage de la commande
@app.route('/order/<int:commande_id>', methods=['GET'])
def order_resume(commande_id):
    try :
        commande = CommandeProduit.select().where(CommandeProduit.commande == commande_id).get()
        commande_dict = commande.to_dict()
        return "<pre>"+json.dumps(commande_dict, indent=4)+"</pre>"
    except CommandeProduit.DoesNotExist :
        return "La commande n'existe pas", 404
    
#Ajout d'adresse ou d'une carte de crédit à la commande
@app.route('/order/<int:commande_id>', methods=['PUT'])
def order_finalisation(commande_id):
    if request.is_json:
        if Commande.select().where(Commande.id == commande_id).exists() : #On vérifie que la commande existe
            commande = Commande.get(Commande.id == commande_id)
            data = request.get_json()
            if 'email' in data and 'information_livraison' in data : #On vérifie que l'on a bien un email et une adresse de livraison
                if ('country' and 'address' and 'postal_code' and 'city' and 'province') in data['information_livraison']:
                    print(data['information_livraison'])
                    commande.email = data['email']
                    commande.information_livraison = data['information_livraison']
                    commande.save()
                    return redirect(url_for('order_resume', commande_id=commande.id), code=302)
                else :
                    message_error = {
                        "error": {
                            'commande': {
                                "code": "missing-field",
                                "name": "La commande doit contenir une adresse de livraison valide."
                            }
                        }
                    }
                    return message_error, 422
            elif 'credit_card' in data : #On vérifie que l'on a bien une carte de crédit
                if commande.email == "" or commande.information_livraison == "" :
                    message_error = {
                        "error": {
                            'commande': {
                                "code": "missing-field",
                                "name": "La commande doit contenir un email et une adresse de livraison."
                            }
                        }
                    }
                    return message_error, 422
                elif commande.payer : #On vérifie que la commande n'a pas déjà été payé
                    message_error = {
                        "errors" : {
                            "order": {
                                "code": "already-paid",
                                "name": "La commande a déjà été payée."
                            }
                        }
                    }
                    return "La commande a déjà été payée", 422
                else :
                    url = 'http://dimprojetu.uqac.ca/~jgnault/shops/pay/'
                    data['amount_charged'] = commande.prix_total + commande.prix_livraison
                    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), {'Content-Type': 'application/json'})
                    try :
                        with urllib.request.urlopen(req) as response:
                            response_pay = response.read()
                            json_pay = json.loads(response_pay.decode('utf-8'))
                            commande.carte_credit = json_pay['credit_card']
                            commande.transaction = json_pay['transaction']
                            commande.payer = True
                            commande.save()
                            return redirect(url_for('order_resume', commande_id=commande.id), code=302)
                    except urllib.error.HTTPError as e: #On gère le renvoi de message d'erreur de l'API de paiement
                        message_error = {
                                    "error": {
                                        'commande': {
                                            "code": "payment-error",
                                            "name": "La carte de crédit à été décliné."
                                        }
                                    }
                                }
                        return message_error, 422
            else : #if 'email' in data and 'information_livraison' in data or 'credit_card' in data
                message_error = {
                    "error": {
                        'commande': {
                            "code": "missing-field",
                            "name": "Vous n'envoyez pas les bonnes données : mail et adresse de livraison ou carte de crédit."
                        }
                    }
                }
                return message_error, 422
        else : #if Commande.select().where(Commande.id == commande_id).exists()
            return "La commande n'existe pas", 404

#Affichage des produits
@app.route('/json', methods=['GET'])
def json_produits():
    produits = Produit.select()
    produits_dict = []
    for produit in produits :
        produits_dict.append(produit.to_dict())
    return "<pre>"+json.dumps(produits_dict, indent=4)+"</pre>"

def import_api():
    #Pour simplifier les appels d'API, nous avons décidé de supprimer les commandes et les produits déjà existants
    Produit.delete().execute() #On supprime les produits déjà existants
    Commande.delete().execute() #On supprime les commandes déjà existantes
    CommandeProduit.delete().execute() #On supprime les produits déjà existants dans les commandes

    url = 'http://dimprojetu.uqac.ca/~jgnault/shops/products/'

    response = urllib.request.urlopen(url)

    data = json.loads(response.read().decode('utf-8'))

    for produit in data['products']:
        Produit.create(
            id=int(produit['id']),
            type=clean_string(produit['type']),
            nom=clean_string(produit['name']),
            description=clean_string(produit['description']),
            image=clean_string(produit['image']),
            hauteur=produit['height'],
            poids=produit['weight'],
            prix=produit['price'],
            en_stock=produit['in_stock']
        )

def clean_string(s):
    return s.replace('\x00', '')

import_api()

# --------------Début d'une liaison avec des vues, ne pas prendre en compte.----------------
#SECRET_KEY = os.urandom(24)
# app.secret_key = SECRET_KEY

# @app.route('/')
# def index():
#     produits = Produit.select()
#     return render_template('index.html', produits=produits)

# @app.route('/produit/<int:produit_id>')
# def produit(produit_id):
#     produit = Produit.get(Produit.id == produit_id)
#     return render_template('produit.html', produit=produit)

# @app.route('/panier', methods=['GET', 'POST'])
# def panier():
#     if 'panier' not in session:
#         session['panier'] = []
#     if request.method == 'POST':
#         produit_id = request.form['produit_id']
#         produit = Produit.get_by_id(produit_id)
#         if produit.en_stock:
#             session['panier'].append({
#                 'id': produit.id,
#                 'nom': produit.nom,
#                 'prix': produit.prix,
#                 'quantite': 1
#             })
#             flash('Le produit a été ajouté à votre panier.', 'success')
#         else:
#             flash('Désolé, ce produit n\'est pas en stock.', 'danger')
#         return redirect(url_for('panier'))
#     else:
#         panier = session.get('panier', [])
#         total = sum(float(item['prix']) * float(item['quantite']) for item in panier)
#         return render_template('panier.html', panier=panier, total=total)
    
# @app.route('/commande', methods=['GET', 'POST'])
# def commande():
#     if 'panier' not in session:
#         flash('Votre panier est vide.', 'danger')
#         return redirect(url_for('index'))

#     panier = session['panier']
#     total = sum(float(item['prix']) * float(item['quantite']) for item in panier)

#     return render_template('commande.html', panier=panier, total=total)

# @app.route('/commander', methods=['POST'])
# def commander():
#     # Récupérer les données du formulaire
#     nom = request.form['nom']
#     adresse = request.form['adresse']
#     ville = request.form['ville']
#     code_postal = request.form['code_postal']
#     courriel = request.form['mail']
#     # carte_credit = request.form['carte_credit']
#     # expiration = request.form['expiration']
#     # cvv = request.form['cvv']

#     # Valider les données du formulaire
#     if not nom or not adresse or not ville or not code_postal or not courriel: # or not carte_credit or not expiration or not cvv:
#         flash('Veuillez remplir tous les champs du formulaire.')
#         return redirect(url_for('commande'))
    
#     panier = session['panier']
#     total = sum(float(item['prix']) * float(item['quantite']) for item in panier)

#     # Créer une nouvelle commande dans la base de données
#     commande = Commande.create(
#         nom=nom,
#         information_livraison=adresse + ', ' + ville + ', ' + code_postal,
#         email=courriel,
#         prix_total=total,
#         transaction = "",
#         prix_livraison = 0,
#         # carte_credit=carte_credit,
#         # expiration=expiration,
#         # cvv=cvv
#     )

#     for item in panier:
#         produit = Produit.get_by_id(item['id'])
#         CommandeProduit.create(commande=commande, produit=produit, quantite=item['quantite'])

#     # Vider le panier
#     session['panier'] = []

#     # Rediriger vers la page de confirmation
#     flash('Votre commande a été passée avec succès !')
#     return redirect(url_for('confirmer_commande', commande_id=commande.id))

# @app.route('/commande/<int:commande_id>', methods=['GET', 'POST'])
# def confirmer_commande(commande_id):
#     commande = Commande.get(Commande.id == commande_id)
#     produits = CommandeProduit.select().where(CommandeProduit.commande == commande)
#     total = commande.prix_total
#     if request.method == 'POST':
#         commande.payer = True
#         commande.save()
#         flash('La commande a été confirmée avec succès !', 'success')
#         return redirect(url_for('index'))
#     else : 
#         if commande.payer:
#             flash('La commande a déjà été confirmée.', 'warning')
#             return redirect(url_for('index')) # à changer pour afficher la commande
#     return render_template('confirmer_commande.html', commande=commande, produits=produits, total=total)
