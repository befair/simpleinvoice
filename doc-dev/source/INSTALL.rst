Istruzioni per installare simpleinvoice (8 settembre 2014)
==========================================================

Si suggerisce di operare in un virtual environment python (v. :ref:`suggerimento`).

1/6 Download
------------

Scaricare il codice del progetto SIMPLEINVOICE dal repository pubblico:

$ git clone https://github.com/befair/simpleinvoice.git

2/6 Requisiti
-------------

Installare i requisiti del progetto:

$ cd simpleinvoice
$ pip install -r requirements.txt

In caso di consultare :ref:`faq-1`

3/6 Configurazione di base
--------------------------

1. Copiare il contenuto del file "settings_dist.py" nel 
   file "settings.py". Su sistemi GNU/Linux o Unix-like:

   simpleinvoice$ cp simpleinvoice/settings_dist.py simpleinvoice/settings.py

2. aprire il file "settings.py" e modificare i settaggi relativi a:
   - "COMPANY_*" con le impostazioni della propria azienda
   - "SECRET_KEY" con il valore riportato dal comando TODO ???django-admin.py startproject???

4/6 Inizializzazione
--------------------

La configurazione di default prevede l'uso di `sqlite <http://sqlite.org>`__.

Inizializzare il database eseguendo:

1. simpleinvoice$ python manage.py migrate --noinput
2. simpleinvoice$ python manage.py createsuperuser
            
5/6 Avviare il servizio
-----------------------

* simpleinvoice$ python manage.py runserver

6/6 Fatto!
----------

Accedere a `simpleinvoice` puntando il browser all'indirizzo:
	
* http://127.0.0.1:8000/


[PER TESTARE] Caricare i dati di prova
--------------------------------------

* simpleinvoice$ python manage.py loaddata initial_data.json

.. _suggerimento:

[SUGGERIMENTO] Operare in un virtual environment
------------------------------------------------

È consigliato installare simpleinvoice in un `virtual environment python <https://virtualenv.pypa.io/en/latest/>`__ . Per fare ciò si consiglia di installare gli script `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/en/latest/>`__ ed eseguire

$ mkvirtualenv <name> per creare ambiente di lavoro ed entrarci

Per uscire digitare

(<name>)$ deactivate

Per entrare nuovamente

$ workon <name>



REFERENCE DI CONFIGURAZIONE
===========================

Premessa
--------

Simpleinvoice dispone di vari parametri configurabili. Essi sono nei file:

* `simpleinvoice/settings_dist.py`: i più comuni da verificare ed adattare ad ogni installazione;
* `simpleinvoice/default_settings.py`: quelli di sviluppo di simpleinvoice
* tutti quelli previsti dalla `configurazione di Django 1.7 <https://docs.djangoproject.com/en/1.7/topics/settings/>` __

Per adattare un parametro di configurazione alla propria installazione 
basta copiarlo nel file `simpleinvoice/settings.py` e modificarne il valore.

Si riportano le impostazioni specifiche di simpleinvoice e le più comuni
che possono richiedere adattamento. Per ulteriori dettagli su parametri meno comuni
si rimanda all'ottima `documentazione di Django <https://docs.djangoproject.com/en/1.7/ref/settings/>`__

DATABASE SETTINGS
-----------------

Per configurare il database, è necessario impostarne i valori nel file `simpleinvoice/settings.py`, nel setting `DATABASES`. Qui è possibile impostare il database di `default`.

Per database di tipo SQLite, è sufficiente impostare:

* `ENGINE`: 'django.db.backends.sqlite3'
* `NAME`: il nome del database

Per altri tipi di database supportati ( `Django <https://docs.djangoproject.com/en/1.7/ref/databases/>`__ ), impostare:

* `ENGINE`: relativo al database (vedere referenza sopra)
* `NAME`: il nome del database
* `USER`: l'utente del database
* `PASSWORD`: la password del database
* `HOST`: facoltativo. Indica l'host da usare per la connessione al database. Se non impostato, viene usato il localhost
* `PORT`:  facoltativo. Indica la porta da usare per la connessione al database. Se non impostato, viene usato il valore di default 

Per ulteriori dettagli sulle configurazioni al database consultare la `documentazione di Django 1.7 <https://docs.djangoproject.com/en/1.7/ref/settings/#databases>`__

EMAIL SETTINGS
--------------

* `EMAIL_TEMPLATES` (default: { 'INSOLUTE' : 'base_mail.html' })

* `EMAIL_BACKEND` (default: "django.core.mail.backends.smtp.EmailBackend")
* `EMAIL_HOST` (default: localhost) l'host da usare per l'invio delle mail 
* `EMAIL_SENDER` (default: "webmaster@localhost") 

Per ulteriori dettagli sulle configurazioni email consultare 
https://docs.djangoproject.com/en/1.7/topics/email/#topic-email-backends


FAQ
===

.. _faq-1:

1. **Q**: nell'installazione dei requisiti di sistema ho questo errore (TODO incollare un permission denied)
1. **A**: potrebbero essere necessari i permessi di root 
(se non si opera in un virtual environment - v. :ref:`suggerimento`). 
Eventualmente eseguire

$ sudo pip install -r requirements.txt
	
.. _faq-2:

2. **Q**: non riesco ad avviare il server
2. **A**: installa il driver python per lo specifico database:
    * SQLite: pysqlite
    * MySQL: MySQL-python
    * postgreSQL: psycopg2

.. _faq-3:

3. **Q**: sono supportati database differenti da sqlite (PostgreSQL/MySQL ad esempio)?
3. **A**: sì, tutti quelli supportati da `Django <http://www.djangoproject.com>`__

.. _faq-4:

4. **Q**: io utilizzo PostgreSQL/MySQL come posso inizializzare il database?
4. **A**: è necessario impostare i dati per la connessione al database con il parametro "DATABASES" in settings.py. Per maggiori info http://link_alla_pagina_dei_settings_del_database. Inoltre è necessario disporre di un database già 
    creato ed associato ad un utente.
    Il nome del database, insieme all'username e alla password dell'utente a cui 
    è associato, vanno inseriti nei campi corrispondenti della struttura 
    DATABASES nel file "settings.py" in simpleinvoice/simpleinvoice/.

.. _faq-5:

5. **Q**: Vorrei avere una previsione delle mail che invio prima di inviarle effettivamente, come posso fare?
5. **A**: Modifica il parametro "EMAIL_*" in settings.py

[X MATTEO] Riprodurre il bug partendo da una clonazione pulita
--------------------------------------------------------------

    Se durante la creazione viene visualizzato il messaggio:
        
        * " Your models have changes that are not yet reflected in a migration, and so won't be applied."

    Eseguire i comandi:

        * simpleinvoice$ python manage.py makemigrations
        * simpleinvoice$ python manage.py migrate

