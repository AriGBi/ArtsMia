from database.DB_connect import DBConnect
from model.Arco import Arco
from model.artObject import ArtObject


class DAO():

    @staticmethod
    def getAllNodes():
        """ Prendo dal database tutte le opere d'arte, presenti nella tabella objects"""
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result=[]
        query=""" select * from objects o"""
        cursor.execute(query) #la query non ha parametri, non mi serve la tupla
        for row in cursor:
            result.append(ArtObject(**row)) #appendo alla lista oggetti ArtObject che creo ogni volta sul momento con il costruttore

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(v1,v2): #prende come argomento due nodi
        """N.B. questo metodo non va benissimo perchè dovremo farlo PER OGNI coppia di nodi, ne facciamo uno sotto migliore --> getAllArchi """
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ select eo.object_id, eo2.object_id, count(*) as peso
                    from exhibition_objects eo , exhibition_objects eo2 
                    where eo.exhibition_id=eo2.exhibition_id and eo.object_id < eo2.object_id and eo.object_id=%s and eo2.object_id =%s
                    group by eo.object_id, eo2.object_id """
        #prendo la tabella exhibition_object e cerco le righe in cui NELLA STESSA EXHIBITION sono stati esposti i due oggetti che ho passato come parametri.
        #metto eo.object_id < eo2.object_id così non mi prende le righe in cui c'è lo stesso oggetto con se stesso e mi prende solo le rige con opere A+B e non anche B+A
        #faccio la group by così conto le righe di exhibitions  che sono venute fuori --> 2 righe vuol dire due exhibitions e quindi il peso dell'arco sarà 2

        cursor.execute(query, (v1.object_id,v2.object_id))  #io passo come parametro tutto l'oggetto ma per fare la query prendo solo l'id
        for row in cursor:
            result.append(**row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArchi(idMap):  # prende come argomento due nodi
        """ """
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ select eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                    from exhibition_objects eo , exhibition_objects eo2 
                    where eo.exhibition_id=eo2.exhibition_id and eo.object_id < eo2.object_id 
                    group by eo.object_id, eo2.object_id 
                    order by peso desc """
        # prendo la tabella exhibition_object e cerco le righe in cui NELLA STESSA EXHIBITION sono stati esposti due opere d'artr.
        # metto eo.object_id < eo2.object_id così non mi prende le righe in cui c'è lo stesso oggetto con se stesso e mi prende solo le rige con opere A+B e non anche B+A
        # faccio la group by così conto le righe di exhibitions  che sono venute fuori --> 2 righe vuol dire due exhibitions e quindi il peso dell'arco sarà 2

        cursor.execute(query, ())
        for row in cursor:
            result.append(Arco(idMap[row["o1"]],idMap[row["o2"]],row["peso"]))  # appendo alla lista oggetti Arco che creo ogni volta sul momento con il costruttore
            #o1 e o2 sono due stringe con gli id_object presi dal database. Ma la classe Arco vuole l'oggetto vero e proprio.
            #Posso recuperare l'oggetto a partire dall'id_object da una MAPPA in cui salvo id_object=object.
            #la mappa gliela passo come PARAMETRO nel Model quando chiamo questo metodo

        cursor.close()
        conn.close()
        return result



