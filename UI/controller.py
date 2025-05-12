import flet as ft


class Controller:
    def __init__(self, view, model): #quando nel main creo l'oggetto controller, gli passo degli OGGETTI view e model come èarametri
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        """quando schiaccio il bottone, devo creare il grafo"""
        self._model.buildGraph()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato. Il grafo contiene {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi pesati"))
        self._view._btnCompConnessa.disabled = False
        self._view._txtIdOggetto.disabled = False
        self._view.update_page()


    def handleCompConnessa(self,e):
        txtInput=self._view._txtIdOggetto.value #prendo il valore del TextField scritto dall'utente
        if txtInput == "": #controllo dati inseriti da utente
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserite un id valido", color="red"))
            self._view.update_page()
            return
        try:
            idInput=int(txtInput) #anche se l'utente scrive un numero, comunque viene salvato come stringa e poi lo trasformo in intero.
            # Se l'utente però scrive delle lettere, l'operazione int() fallisce --> allora lo mettp in try catch

        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Il valore inserito non è un numero", color="red"))
            self._view.update_page()
            return
        if not self._model.hasNode(idInput): #utente può inerire un numero che però non corrisponde a nessun id. Lo verifico con questo metodo nel model, che controlla nella mappa dei nodi se c'è quello inserito dall'utente
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("L'id inserito non corrisponde a nessun nodo", color="red"))
            self._view.update_page()
            return
        #se tutti i controlli passano, cerco la componente connessa:

        sizeCompConnessa=self._model.getInfoConnessa(idInput) #dato il nodo PASSATO DALL'UTENTE, nel model calcolo il grafo connessa e ritorno un intero (numero di nodi connessi)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La dimensione della componente connessa che contiene il nodo {self._model.getObjectFromId(idInput)} è {sizeCompConnessa}" ))

        self._view._ddLUN.disabled = False
        self._view._btnCerca.disabled = False

        myValues=range(2,sizeCompConnessa)
        # for v in myValues:
        #     self._view._ddLUN.options.append(ft.dropdown.Option(v))

        myValuesDD=map(lambda x: ft.dropdown.Option(x),myValues) #metodo map applica una certa funzione per OGNI elemento della lista myValues che gli passo
        #in particolare, voglio che per ogni elemento di myValues mi crei un oggetto Option --> lo faccio con una funzione lambda function

        self._view._ddLUN.options=myValuesDD

        self._view.update_page()
        return

    def handleCerca(self,e):
        source=self._model.getObjectFromId(int(self._view._txtIdOggetto.value)) #quello che mi passa l'utente l'ho già controllato in handleCompConnessa
        lun =self._view._ddLUN.value
        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare un parametro lunghezza", color="red"))
            self._view.update_page()
            return
        lunInt=int(lun)
        path, pesoTot=self._model.getOptPath(source,lunInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino che parte da {source} trovato con peso totale {pesoTot}"))

        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()
        return


