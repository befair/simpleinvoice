��    k      t  �   �       	  �   !	  �   
  D  �
          (  .   /  '   ^  3   �     �     �     �  %   �     �       �    
   �  $   �  "   !     D     K     X     n  .   �  (   �     �  ;   �  3        M     U     j     �     �     �  :   �     �       3   %     Y     f     s  
   w  9   �     �      �     �     	        9   &  .   `     �     �     �     �     �     �  
   �     �     �     �     �  	   �               *     3     S  	   Y     c     g  1   p  #   �     �     �     �     �     �                    !     &     ,     /     5     >     F     O     V     o     �     �     �     �     �     �     �     �     �               /  
   <     G     K  	   X     b  k  j    �  �   �  h  �     "  	   ?      I     j  V   �     �     �     �  @   �     4     R  �  V  
     -   "  8   P     �     �  !   �     �  1   �  #        4  >   C  8   �     �     �  &   �  &        ,     F  O   N     �     �  6   �     �                    >   '      f   <   y      �      �      �   1   �   4   $!     Y!  	   g!     q!     w!     �!     �!  	   �!     �!     �!     �!     �!     �!     �!     "     "  %   #"     I"     P"     b"     f"  ?   "  '   �"     �"     �"     #     #     /#  	   7#     A#     Y#     ^#     c#     h#     k#     q#  	   �#     �#     �#  &   �#     �#     �#     �#     �#     $     $     1$     @$     F$     W$     h$     x$     �$     �$     �$     �$     �$     �$     >       g                     :          5              e   X   %   T   	   J   F         \   7      C   1   ?   6       a   M   .          G   Z       (   f       K   )      !   _   <      8          /      S       Q   +   b                  2       0   4   A   E             c                   #       H       U       "   R          *   V       d   @       L   ,   -   =           j       ^          $       ]   
           B      h   I   9   '   k             ;   3          Y   D      W   i   O                      `   P      N       &       [                

Hi %(customer)s, 

we inform you that you should pay %(pretty_amount)s euro  
for the subscription to service

"%(service)s"

from date %(initial)s to date %(end)s.

Thanks for your attention and your choice.

We wish you best days!

beFair team
 
          <option value="money transfer">money transfer<option>
          <option value="cash">cash<option>
          <option value="credit card">credit card<option>
          
    <p>Hi %(customer)s,</p>

    <p>we inform you that you should pay %(pretty_amount)s &euro;,  
    for the subscription to service</p>

    <p>%(service)s</p>

    <p>from date %(initial)s to date %(end)s.</p>

    <p>Thanks for your attention and your choice</p>

    <p>We wish you best days!</p>

    beFair team
     %s reminder mails sents Amount Cancel selected service subscription payments  Cancel selected service subscription/s  Customer %s should pay, but is has no email address Days Description Discount Discount has to be a percentage value Display selected invoices Hours Indicator to modify the periodic payment deadline. This value has to be greater than -(period), and represents the relative number of period units (for instance, months) that should be considered to determine the final service payment deadline. So, if the period is of 12 months, and the modifier is set to -2, then the actual service payment deadline is computed as (12 + (-2) = 10) months. In the same way, a modifier of 2 chenges the deadline to (12 + 2 = 14) month.  Invoice n. Make selected invoices as paid today Money transfer can be done on IBAN Months More info... Next invoice id is %s Payment due for %s Payment of %(customer)s to service %(service)s Restore selected service subscription/s  SSN SSN number must be inserted if customer is a natural person Send a reminder mail about unsolved subcscpriptions Service Service subscription Service subscription payment Service subscription payments Service subscriptions Services Set this value only if you need a specific invoice number. Simple invoice Social Security Number Subscription of %(customer)s to service %(service)s Total amount Total to pay VAT VAT number VAT number must be inserted if customer is a legal person VAT percentage Vat has to be a percentage value What date has he paid until? When has it been paid? Years You can invalidate this invoice by unchecking this field. You should write social security or vat number abbreviation address amount cash city cost created on credit card customer customer contact customer contacts customers default vat percentage description discount display measure unit for period email emit date fax how many how many period lasts before creating an invoice? indicator of a period by raw units. invoice invoice entries invoice entry invoice number invoices is valid money transfer name note notes of other paid for paid on pay with period period deadline modifier period measure of unit period unit source phone raw unit service service details social security number state subscribed from (datetime) subscribed from (value) subscribed on subscribed until subscription updated on vat when deleted when paid zipcode Project-Id-Version: PACKAGE VERSION
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2014-10-14 11:12+0200
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language-Team: LANGUAGE <LL@li.org>
Language: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
 

Buongiorno %(customer)s, 

ti ricordiamo che devi pagare %(pretty_amount)s euro  
per la tua sottoscrizione al servizio

"%(service)s"

dal %(initial)s al %(end)s.

Grazie per l'attenzione e la tua scelta.

Ti auguriamo di trascorrere i giorni migliori della tua vita!

il team beFair
 
          <option value="money transfer">trasferimento monetario<option>
          <option value="cash">contanti<option>
          <option value="credit card">carta di credito<option>
          
    <p>Buongiorno %(customer)s,</p>

    <p>ti ricordiamo che devi pagare %(pretty_amount)s euro 
    par la tua sottoscrizione al servizio</p>

    <p>%(service)s</p>

    <p>dal %(initial)s al %(end)s.</p>

    <p>Grazie per l'attenzione e la tua scelta.</p>

    <p>Ti auguriamo di trascorrere i giorni migliori della tua vita!</p>

    il team beFair
     %s mail di sollecito inviate Quantità Cancella i pagamenti selezionati Cancella sottoscrizioni Il cliente %s dovrebbe pagare, ma non ha un indirizzo email cui spedirgli il sollecito Giorni Descrizione Sconto Lo sconto deve essere un valore percentuale (compreso tra 0 e 1) Mostra le fatture selezionate Ore Indicatore per la modifica della scadenza del periodo. Questo valore deve essere maggiore di -(periodo) e rappresenta il numero di unità di periodo (ad esempio mesi) che vanno a modificare la vera scadenza per il pagamento del servizio. Così se il periodo è di 12 mesi e il modificatore è -2, la vera scadenza del pagamento sarà dopo (12 + (-2) = 10) mesi. Allo stesso modo, un modificatore settato a 2 cambia la scadenza a (12 + 2) = 14 mesi. Fattura n. Segna le fatture selezionate come pagate oggi Il trasferimento di denaro puo essere fatto tramite IBAN Mesi Altre informazioni... L'id della prossima fattura è %s Promemoria pagamento %s Pagamento di %(customer)s al servizio %(service)s Riabilita sottoscrizioni cancellate Codice Fiscale Inserire il Codice Fiscale se il cliente è una persona fisica Invia email di sollecito per il pagamento degli insoluti Servizio Sottoscrizione a servizio Pagamento di sottoscrizione a servizio Pagamenti di sottoscrizione a servizio Sottoscrizioni a servizio Servizi Inserisci questo valore solo se si necessita di uno specifico numero di fattura Fattura semplice Codice Fiscale Sottoscrizione di %(customer)s al servizio %(service)s Quantità totale Totale da pagare IVA partita IVA Inserire la Partita IVA se il cliente è una persona giuridica IVA in percentuale L'Iva deve essere un valore percentuale (compreso tra 0 e 1) Fino a quando è stato pagato? Quando è stato pagato? Anni Invalida la fattura deselezionando questa casella Dovresti scrivere il codice fiscale o la partita IVA abbreviazione indirizzo Costo contanti città costo creata il carta di credito cliente contatto del cliente contatti del cliente clienti IVA predefinita in percentuale descrizione sconto in percentuale mostra l'unità di misura del periodo e-mail data di emissione fax Numero di sottoscrizioni periodi che devono passare prima della creazione di una fattura indicatore del periodo in unità grezze fattura annotazioni di fattura annotazione di fattura numero di fattura fatture Validità trasferimento monetario nome note note di altro pagato fino al pagato il paga con periodo modificatore per la scadenza periodica unità di misura del periodo fonte unità di misura telefono unità grezza Servizio Dettagli di sottoscrizione Codice Fiscale stato sottoscritta dal sottoscritta dal sottoscritta il sottoscritta fino a sottoscrizione aggiornato il Partita IVA data di cancellazione data di pagamento CAP 