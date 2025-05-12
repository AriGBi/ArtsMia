import copy

import networkx as nx
from networkx.classes import neighbors

from database.DAO import DAO


class Model:
    def __init__(self):
        #nel costruttore posso già dire al mio modello che avrà un grafo
        self._graph=nx.Graph() #con Graph() crea un grafo NON ORIENTATO
        self._nodes=DAO.getAllNodes()  #i nodi del grafo sono gli oggetti creati nel DAO, salvati in una lista res che viene returnata
        # posso creare nel costruttore l'elenco dei nodi perchè per come è svolto l'esercizio, il grafo dovrà avere comunque TUTTE le opere d'arte
        self._idMap={}
        for v in self._nodes:
            self._idMap[v.object_id]=v #riempio la mappa con object_id=object

        self._bestPath=[] #lista che salverà il percorso ottimo
        self._bestCost=0 #salvo il costo ottimo


    def buildGraph(self):
        """ metodo che crea il grafo, in realtà ho già un grafo vuoto creato nel costruttore, ma qui lo RIENMPIO """
        self._graph.add_nodes_from(self._nodes)
        self.addAllEdges()

    def addEdgesV1(self):
        """ Versione 1 per creare gli archi che non va bene perchè itera su ogni COPPIA di nodi --> lungo"""
        for u in self._nodes:
            for v in self._nodes:
                peso= DAO.getPeso(u,v) #prendo ogni coppia di nodi e verifico dal database se sono stati esposti nella stessa exhibition
                #il metodo del DAO getPeso() avrà due parametri che sono le 2 opere d'arte che voglio vedere se sono state esposte nelle stesse esposizioni
                if (peso != None):
                    self._graph.add_edge(u, v, weight=peso)

    def addAllEdges(self):
        allEdges= DAO.getAllArchi(self._idMap) #questo metodo del grafo ha bisogno che io gli passi la mappa con object_id=object
        for edge in allEdges:
            self._graph.add_edge(edge.o1, edge.o2, weight=edge.peso)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getIdMap(self):
        return self._idMap


    def getInfoConnessa(self, idInput):
        """ Identifica la componente connessa che contiene idInput (id di un vertice) e ne restituisce la dimensione"""
        #si usa il metodo di esplorazione depht first che è utile per trovare le componenti connesse!!!
        #ha un metodo che, partendo da un nodo, identifica tutti i nodi raggiungibili (che è proprio la componente connessa)
        if not self.hasNode(idInput): #controllo ridondante perchè l'ho gia fatto nel controller, ha senso farlo solo per il testModel
            return None

        source=self._nodes[idInput] #l'utente mi passa l'id, ma i nodi sono OGGETTI. Dalla mappa, partendo dall'id, prendo l'oggetto e lo salvo in source

        #Modo 1: conto i SUCCESSORI di source
        succ=nx.dfs_successors(self._graph, source) #succ è un dizionario con come valori tutti i nodi successori
        # N.B dfs scelgie a caso un successore e non da una soluzione OGGETTIVA nè ottima. Per avere effettivamente il numero di tutti i successori faccio cosi:
        res=[]
        for s in succ.values():
            res.extend(s) #se il valore è un oggetto, allora lo aggiunge. Se invece è una lista (più successori) allora ne aggiunge uno alla volta
        print("Size connessa con modo 1: ", len(res)+1) #devo fare +1 per agiungere il source

        #Modo 2: conto i PREDECESSORI di source
        pred = nx.dfs_predecessors(self._graph, source)
        print("Size connessa con modo 2: ", len(pred.values())+1) #devo fare +1 per agiungere il source

        #Modo 3: conto i nodi dell'albero di visita
        dfsTree=nx.dfs_tree(self._graph, source)
        print("Size connessa con modo 3: ", len(dfsTree.nodes())) #conta anche la source --> è giusto così!!

        #Modo 4: uso il metodo nodes_connected_components di networkx
        conn=nx.node_connected_component(self._graph, source)
        print("Size connessa con modo 4: ", len(conn))

        return len(conn)

    def getOptPath(self,source,lun):
        self._bestPath=[]
        self._bestCost=0
        parziale=[source] #so che inizierà da source, quindi posso già metterlo in parziale
        #provo ad aggiungere un nodo e poi chiamo la ricorsione

        #devo ciclare sui vicini di QUEL nodo
        for n in self._graph.neighbors(source):
            if source.classification==n.classification:
                parziale.append(n)
                self._ricorsione(parziale,lun)
                parziale.pop() #backtracking
        return self._bestPath,self._bestCost

    def _ricorsione(self,parziale,lun):
        #step1: controllare se parziale è una soluzione --> condizione terminale
        if len(parziale) == lun: #allora parziale ha la lunghezza desiderata, o è una soluzione migliore della attuale o non lo è --> ma comunque devo uscire
            #verifico se è soluzione migliore:
            if self.costo(parziale)>self._bestCost:
                self._bestCost=self.costo(parziale)
                self._bestPath=copy.deepcopy(parziale)
            return

        #se parziale può ancora ammettere altri nodi:
        for n in self._graph.neighbors(parziale[-1]): #cerco i vicini dell'ultimo nodo che ho aggiunto
                if parziale[-1].classification==n.classification and n not in parziale: #posso aggiungere solo nodi con la stessa classificiation!!!
                    parziale.append(n)
                    self._ricorsione(parziale,lun)
                    parziale.pop()

    def costo(self, listObjects):
        totCosto=0
        for i in range(0,len(listObjects)-1):
            totCosto+=self._graph[listObjects[i]][listObjects[i+1]]["weight"] #prendo il peso dell'arco che connette i e i+1
        return totCosto



    def hasNode(self, idInput):
        return idInput in self._idMap #verifico se l'idInput fa parte delle chiavi del dizionario che ho creato.
        #se fa parte della mappa, allora questo id esiste (c'è il rischio che l'utente inserisca un id che non esiste)


    def getObjectFromId(self, idInput):
        return self._idMap[idInput]




