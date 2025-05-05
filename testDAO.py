#uso questa classe per testare gli oggetti creati dal DAO, senza dover fare tutto il controller per verificare

from database.DAO import DAO
from model.model import Model

listObjects = DAO.getAllNodes() #creo lista in cui ci sono tutti gli oggetti perchè il metodo getAllNodes() restituisce una lista con tutti oggetti

print(len(listObjects))

#voglio testare il metodo che crea gli archi getAllArchi --> questo metodo però utilizza idMap che è nel model, quindi creo un OGGETTO Model su cui lavorare
mymodel=Model()
mymodel.buildGraph()
edges=DAO.getAllArchi(mymodel.getIdMap()) #passo la Mappa
print(len(edges))
