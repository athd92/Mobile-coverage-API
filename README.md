# Mobile coverage API (test)

This project is an API service coded with the Python framework Django 3. It allows you to send an address by a GET method and gives you back some coverages informations relatives at the places mentionned.

  - Request example:
 
```sh
'http://127.0.0.1:8000/?q=8+rue+boetie+paris+75008'
```
- Will return:
```
{"SFR": {"2G": true, "3G": true, "4G": false}, "Bouygue": {"2G": true, "3G": true, "4G": true}, "Orange": {"2G": true, "3G": true, "4G": false}}
```


# Installation:

  - Git clone the project:
  ```
  $ git clone https://github.com/athd92/Mobile-coverage-API.git
  ```
  - Install requirements:
  ```
  $ pip install -r requirements.txt
  ```
  - Run django app:
  ```
  $ python3 manage.py runserver
  ```


# Complement informations:

### Datas:
Results are based on open source datas (CSV file) witch contains lambert93 positions, operator references and there type of coverages by zones.

- https://www.data.gouv.fr/s/resources/monreseaumobile/20180228-174515/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv 

### Custom django command:

Ive created a django specific command to dump datas from CSV file and insert them in a database. The command is:
  
  ```
  $ python3 manage.py dump_datas
  ```

Before insert each values in the SQLITE3 database, this custom command :
- Converts lambert93 coordonates to GPS
- Converts operators codes to  specifics names 
- Convert string coverage status to boolean 

