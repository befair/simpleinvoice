Istruzioni per installare Simpleinvoice (8 settembre 2014)
----------------------------------------------------------


0/6

	E' consigliato installare Simpleinvoice in un virtual environment 

	$ mkvirtualenv "name"  --> creare ambiente di lavoro

	I prossimi passi dell'installazione avranno come ambiente il virtual 
	environment creato. 
	



1/6 Scaricare il codice del progetto SIMPLEINVOICE dal repository pubblico:

	$ git clone https://github.com/befair/simpleinvoice.git


2/6 Installare i requisiti del progetto:

	simpleinvoice$ pip install -r requirements.txt
	

3/6 Configurare Simpleinvoice:

	1. Copiare il contenuto del file "settings_dist.py" nel 
       file "settings.py":
	
	/simpleinvoice$ cd simpleinvoice
	/simpleinvoice/simpleinvoice$ cp settings_dist.py settings.py
	
	2.	aprire il file "settings.py": 
	
	quindi inserire i settaggi relativi a "DATABASES" e ai vari valori "COMPANY_*".



4/6 Sincronizzare il database:

	1.	Creazione delle tabelle:

		In caso di utilizzo di postgreSQL è necessario disporre di un database già 
        creato ed associato ad un utente.
		Il nome del database, insieme all'username e alla password dell'utente a cui 
		è associato, vanno inseriti nei campi corrispondenti della struttura 
		DATABASES nel file "settings.py" in simpleinvoice/simpleinvoice/.
        In caso il database sia sqlite, sarà sufficiente settare il nome del database
        nello stesso file di cui sopra.

        Inizializzare il database eseguendo:
	
		    * simpleinvoice$ python manage.py migrate --noinput

        NOTA: Nel caso sia necessario settare username, password, ed email dell'utente 
              amministratore, eseguire:

            * simpleinvoice$ python manage.py createsuperuser
                
        Se durante la creazione viene visualizzato il messaggio:
            
            * " Your models have changes that are not yet reflected in a migration, and so won't be applied."

        Eseguire i comandi:

            * simpleinvoice$ python manage.py makemigrations
            * simpleinvoice$ python manage.py migrate

5/6	(punto facoltativo) Caricare dei dati di prova:

	* /simpleinvoice/simpleinvoice$ python manage.py loaddata initial_data.json

6/6 Far partire il server:

	* /simpleinvoice/simpleinvoice$ python manage.py runserver

	In seguito, sarà possibile accedere ai seguenti link tramite browser:
	
	* http://127.0.0.1:8000/




NOTE DI CONFIGURAZIONE
=====================

Visualizzare le email ed abilitarne l'invio

	Simpleinvoice di default imposta un indirizzo fittizio come indirizzo di default per l'utente amministratore, e un backend basato sulla creazione di file. Nel caso si voglia abilitare l'invio delle mail tramite SMTP, sarà necessario:

	* copiare la variabile EMAIL_BACKEND  presente nel file default_settings.py nel file settings.py e valorizzarlo con:
        
        * "django.core.mail.backends.smtp.EmailBackend"

	Inoltre, nel caso si voglia modificare il template di default per le mail, sarà necessario 
    
    * copiare  la variabile EMAIL_TEMPLATES presente nel file default_settings.py nel file default_settings.py e indicare il nome del template utilizzato nella chiave INSOLUTE, sostituendone il valore con il nome del fie template desiderato:

       * EMAIL_TEMPLATES = {
            'INSOLUTE' : 'template_name'
        }
    
   
    Informazioni aggiuntive e si possono trovare sul sito di documentazione di Django al link: https://docs.djangoproject.com/en/1.7/topics/email/#topic-email-backends
