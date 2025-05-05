import networkx as nx

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


