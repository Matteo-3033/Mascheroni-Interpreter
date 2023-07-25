# Mascheroni language interpreter

Mascheroni language interpreter developed as a project for the course "Linguaggi e traduttori" at the Milan Statale University. The Mascheroni language is a toy-language specifically created for the project. However, it can represent all the geometric constructions that can be drawn using only a ruler and compass. A complete description of the language can be found [here](https://htmlpreview.github.io/?https://github.com/let-unimi/progetti/blob/master/03-Mascheroni/Testo.html) in Italian.

## Specifiche discusse col docente:

* Linguaggio: Python (con uso del modulo geometry.py)
* Parser: ANTLR (uso diretto, senza LibLeT)
* Mascheroni: completo (con costruzioni induttive, upto e if)

## Grammatica:

La grammatica, nella directory [Grammatica](Grammatica), permette la generazione di codice nel [linguaggio di Mascheroni](https://htmlpreview.github.io/?https://github.com/let-unimi/progetti/blob/master/03-Mascheroni/Testo.html).<br>
Rispetto al linguaggio originale si evidenziano le seguenti differenze:
- Per problemi di encoding per le operazioni di intersezione al posto del carattere `∩` viene utilizzato `^`; non è tuttavia necessario eseguire manualmente la sostituzione nel codice poiché se ne occupa direttamente l'interprete;
- Una variante del passo show, `showLabel`, permette la visualizzazione delle etichette dei punti;
- Precedere il primo construct definito con la parola `approximate` permette di approssimare i calcoli delle intersezioni per velocizzare l'esecuzione del codice.
- Si assume che tutti i construct accettino almeno un parametro poiché altrimenti non avrebbero enti da cui partire nella loro computazione;
- I construct induttivi possono restituire solamente enti induttivi che condividono lo stesso pedice.

## Esecuzione:

Per eseguire un programma scritto nel linguaggio di Mascheroni è necessario:
- Creare un oggetto della classe `Interpreter`;

    <code>
    from Interpreter import Interpreter

    interprete = Interpreter()
    </code>

- Passargli il codice tramite il suo metodo `source`.<br>
Nonostante la grammatica definisca l'operatore di intersezione come `^` non è tuttavia necessario sostituire `∩` nel codice poiché questa operazione è svolta direttamente dall'interprete;

    <code>
    source = "codice sorgente"

    interprete.source(source)
    </code>

- Se il metodo `source` restituisce `True` e non vengono sollevate eccezioni passare l'input tramite il metodo `eval` o l'operatore di call. Ogni punto deve essere passato come una tupla di due numeri, mentre ogni retta, semiretta, segmento e cerchio come una tupla di due tuple di due numeri.

    <code>
    interprete.eval(input)

    \# Alternativa: interprete(input)
    </code>

- Se l'esecuzione del codice non solleva nessun errore il risultato è visibile nel nuovo file creato `mascheroni.html`; è possibile modificare il file in cui salvare l'output tramite l'attributo `OUTPUT_FILE_NAME` della classe Interpreter. Se il codice contiene almeno un'istruzione di _show_ o _showLabel_ gli input verranno visualizzati in rosso, gli output in blu, mentre in nero gli altri enti generati.
- È possibile eseguire nuovamente lo stesso codice sorgente, eventualmente su nuovi input, senza passare per la fase di parsing semplicemente invocando il metodo _eval_ o l'operatore di call; si può invece modificare il codice sorgente invocando il metodo _source_.

Nel caso si volesse eseguire il codice su input casuali è possibile non passare all'interprete alcun argomento di input o passargliene solamente alcuni; i restanti argomenti mancanti vengono generati casualmente con i seguenti vincoli:
- Non vengono generati punti sovrapposti o allineati orizzontalmente o verticalmente, anche se potrebbero comunque essere particolarmente vicini;
- Le rette che passano per i due punti che definiscono rette, semirette, segmenti e cerchi non vengono generate parallele o perpendicolari;
- Tutti i punti generati hanno coordinate intere comprese nell'area individuata dagli attributi `MIN_X`, `MAX_X`, `MIN_Y` e `MAX_Y` della classe Interpreter; i valori base di questi attributi sono 0 per quelli minimi e 100 per quelli massimi. La modifica di questi attributi potrebbe impedire la corretta generazione dell'input e uno stallo dell'interprete nel caso nell'area individuata dagli attributi non sia possibile identificare abbastanza punti che soddisfino questi vincoli.

Il file [test.py](test.py) in ogni caso fornisce un modello per l'esecuzione di codice mascheroni, mentre i file nella directory [examples](examples) rappresentano degli esempi di esecuzione.


## Da fare:

- ~~Show~~:
    - ~~Modificare il colore dei simboli in output~~:
        - ~~Input: rosso~~;
        - ~~Output: blu~~;
        - ~~Altri enti: nero~~;
    - ~~Mostrare tutti gli output degli show invece di solamente quello dell'ultimo~~;
    - ~~Creare una variante che mostra anche le etic<hette dei punti~~;
    - ~~Considerare una possibile variante che mostra anche i construct intermedi~~.
- ~~Impedire il riassegnamento dei nomi degli enti~~;
- ~~Costruct induttivi~~:
    - ~~Attivare un nuovo record di attivazione per ogni chiamata induttiva~~;
    - ~~Cercare di migliorare le prestazioni, magari salvando i risultati parziali per evitare di ricalcolarli~~;
    - ~~Considerare di permettere anche più di un ente in output~~;
- ~~With~~:
    - ~~Creare un nuovo scope per ogni with, ma permettendo agli enti definiti all'interno di essere visibili anche fuori~~;
- ~~Input~~:
    - ~~Permettere al main di ricevere non solamente Point in input~~;
    - ~~Generare casualmente l'input mancante~~;
- ~~Output~~:
    - ~~Stampare anche i punti in input e in output~~;
    - ~~Visualizzare meglio il risultati dei passi di show~~;
- ~~Permettere di specificare l'indice di upto tramite espressioni intere~~;
- ~~Migliorare i messaggi d'errore~~;
- ~~Ricontrallare come sono definiti i nomi nella grammatica~~;
- ~~Considerare di controllare staticamente i tipi~~;
- ~~Indagare i problemi di encoding del carattere di intersezione~~.
