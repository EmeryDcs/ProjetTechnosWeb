V={};

V.formatTemplate = function( data, tplSelector ){
    let template = document.querySelector(tplSelector);
    let html = template.innerHTML;

    for (const prop in data){
      html = html.replaceAll("~~"+prop+"~~", data[prop]);
    }
    return html;
}
  


V.render = function(data, tplSelector, target){
    let html = '';
    let div = document.querySelector(target);

    for(let o of data){
        html += V.formatTemplate(o, tplSelector);
    }

    div.innerHTML += html;
        
    return html;
}


document.addEventListener('DOMContentLoaded', function() {
    let storedArticles = JSON.parse(localStorage.getItem('articles'));
    V.render(storedArticles, '#order-template', '#orderList');
    let AllOrderItemQuantity = document.querySelectorAll("#orderItemQuantity")
    console.log(AllOrderItemQuantity)
    for (const o of AllOrderItemQuantity) {
        o.addEventListener("input", (event)=>{
            if (o.value == 0) {
                var confirmation = window.confirm("Vous allez retirer cet article du panier. Êtes-vous sûr ?");
                if (confirmation) {
                    let article = o.parentNode.parentNode
                    article.remove()
                } else {
                   o.value = 1
                }
            }
        })
    }
});

