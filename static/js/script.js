V = {};
let total = 0;

V.formatTemplate = function (data, tplSelector) {
    let template = document.querySelector(tplSelector);
    let html = template.innerHTML;
    html = html.replace("~~id~~", data.id);
    html = html.replace("~~nom~~", data.nom);
    html = html.replace("~~prix~~", data.prix);

    return html;
}



V.render = function (data, tplSelector, target) {
    let html = '';
    let div = document.querySelector(target);

    html += V.formatTemplate(data, tplSelector);

    div.innerHTML += html;

    return html;
}


let togglePanier = function () {
    let panier = document.querySelector("#panier");
    panier.classList.toggle("hidden");
    let body = document.querySelector("body")
    body.classList.toggle("no-scroll")
}

window.addEventListener("load", (event) => {
    let listProduit = document.querySelector("#produits")
    listProduit.addEventListener("click", (e) => {
        let item;
        if (e.target.tagName != "LI") {
            item = e.target.parentNode
            if (item.tagName != "LI") {
                item = e.target.parentNode.parentNode
                if (item.tagName != "LI") {
                    item = e.target.parentNode.parentNode.parentNode
                    if (item.tagName != "LI") {
                        item = e.target.parentNode.parentNode.parentNode.parentNode
                    }
                }
            }
        }

        let article = {};
        article.id = item.id
        article.nom = item.querySelector("#produitNom").innerHTML
        article.prix = parseInt(item.querySelector("#produitPrix").innerHTML.match(/\d+/)[0])
        let panierList = document.querySelector("#panierList")
        let allArticles = panierList.querySelectorAll("li")
        let articleExist;
        for (const o of allArticles) {
            if (o.id == article.id) {
                articleExist = o
            }
        }

        if (!articleExist) {
            // Si l'article n'est pas encore dans le panier, l'ajouter
            V.render(article, '#panier-template', '#panierList');
            quantity = 1

        } else {
            // Si l'article est déjà dans le panier, augmenter la quantité
            let articleQuantity = articleExist.querySelector("#articleQuantity")
            let quantity = parseInt(articleQuantity.innerHTML.match(/\d+/)[0])
            quantity += 1
            articleQuantity.innerHTML = quantity
        }
        panierInit(article, quantity)

    })


});

let panierInit = function (article = null, quantity = 1) {
    let nbArticles = document.querySelector("#nbArticles")
    let totalPrice = document.querySelector("#totalPrice")
    let panierList = document.querySelector("#panierList")
    if (panierList) {
        let totalQuantity = panierList.querySelectorAll("#articleQuantity")
        var nb = 0;
        for (let number of totalQuantity) {
            nb += parseInt(number.innerHTML);
        }

        if (nb < 2) {
            nbArticles.innerHTML = nb + " article"
        }
        else {
            nbArticles.innerHTML = nb + " articles"
        }
        if (article) {
            total += article.prix * quantity
            totalPrice.innerHTML = total + "$CAD"
        }
    }
}

let goToOrder = function () {
    let panierList = document.querySelector("#panierList")
    let allArticles = panierList.querySelectorAll("li")
    if (allArticles.length > 0) {
        let articlesData = [];

        for (const o of allArticles) {
            let articleId = o.id;
            let articleNom = o.querySelector(".article__name").innerHTML;
            let articleQuantity = parseInt(o.querySelector("#articleQuantity").innerHTML);
            articlesData.push({ id: articleId, nom: articleNom, quantity: articleQuantity });
        }
        // Stocker les données des articles dans localStorage avant de rediriger
        localStorage.setItem('articles', JSON.stringify(articlesData));
        window.location.href = "/order";
    } else {
        alert("Vous devez sélectionner au moins un article pour passer commande.")
    }

}
// panierInit()
