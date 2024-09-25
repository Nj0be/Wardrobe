Ingegneria del Software

APP: accounts

1. Sign up
2. Log in
3. customer profile

APP: products

come approcciare il problema della ricorsione delle categorie?

all'inizio al template search vengono passate tutte le categorie poste e False, incluso quelle master (quelle con parent_id=0)
nonostante ciò, faranno già parte del template, in quanto ci penserà javascript a renderle visibili man mano che l'utente
le clicca.

per ogni click ci sono tre opzioni:

Dopo il click sulla categoria scelta, l'utente sceglie "visualizza tutto" -> viene passata come True la categoria scelta
Dopo il click sulla categoria scelta, l'utente seleziona una sottocategoria:
    Se è una sottocategoria foglia allora viene passata come True la sottocategoria scelta
    Se è una sottocategoria padre allora js apre un altro pop up per visualizzare le sue sub figlie
