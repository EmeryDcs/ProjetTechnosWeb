# Projet Technos Web

Ce projet vise à développer une API web grâce à Flask et Peewee.

# Réalisé par :

Ce projet a été réalisé par Emery Descours et Loïne Pommier
Codes permanents : 
DESE11119900
POML14570300

## Fonctionnalités

- Fonctionnalité 1 : Affichage des produits via un GET sur /json
- Fonctionnalité 2 : Création d'une commande via un POST sur /order
- Fonctionnalité 3 : Mise à jour de la commande via un PUT sur /order/{id}

## Exemples via Postman fonctionnels :

POST http://127.0.0.1:5000/order envoi du JSON suivant : 
{
    "product": {
        "id": 3, "quantity": 3
    }
}

PUT http://127.0.0.1:5000/order/1 envoi du JSON suivant : 
{
    "email" : "jgnault@uqac.ca",
    "information_livraison" : {
        "country" : "Canada",
        "address" : "201, rue Président-Kennedy",
        "postal_code" : "G7X 3Y7",
        "city" : "Chicoutimi",
        "province" : "QC"
    }
}

PUT http://127.0.0.1:5000/order/1 envoi du JSON suivant : 
{
    "credit_card" : {
        "name" : "John Doe",
        "number" : "4242 4242 4242 4242",
        "expiration_year" : 2024,
        "cvv" : "123",
        "expiration_month" : 9
    },
    "amount_charged": 10148 
}


## Technologies utilisées

- Python
- Flask
- Peewee
