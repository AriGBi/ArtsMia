#questa classe serve a testare il Model senza dover scrivere il controller
#Model è una CLASSE, quindi devo comunque creare un oggetto model per poterci lavorare sopra

from model.model import Model

myModel=Model() #oggetto della classe Model

myModel.buildGraph() #chiamo il metodo buildGraph() per riempire il grafo del mio oggetto Model

print(f"Il numero di nodi è: ", myModel.getNumNodes(), ". Il numero di archi è: ", myModel.getNumEdges())

myModel.getInfoConnessa(1234)


