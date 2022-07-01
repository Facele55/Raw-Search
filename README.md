# Raw-Search
##### Front page
![Front Page](./static/screenshots/front_page.png)

##### Admin Page
![Front Page](./static/screenshots/admin_page.png)

# WARNING: DON'T USE FOR PRODUCTION.

## Raw Search it is my diploma project for the topic "Design and implementation of a web search engine."

### Built With

* [Django](https://www.djangoproject.com/)
* [Elasticsearch](https://www.elastic.co/)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [PostgreSQL](https://www.postgresql.org)
* [SQLite3](https://www.sqlite.org/index.html)



### How to run:
* Python Virtual Environment. 
Check out the [for more information](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
  - Create a virtual environment:
    + `python -m venv venv` for Windows;
    + `python3 -m venv venv` for *nix(Ubuntu, Linux, macOS)
  - Activate it:
    + `venv\Scripts\activate` for Windows
    + `. venv/bin/activate` for *nix(Ubuntu, Linux, macOS)
  - Install requirements:
    + `pip install -r requirements.txt` Windows
    + `pip3 install -r requirements.txt` *nix(Ubuntu, Linux, macOS)
  - Run server:
    + `python manage.py runserver` for Windows
    + `python3 manage.py runserver` for *nix(Ubuntu, Linux, macOS)
  - Open in browser:
    + [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Docker
  - Navigate to project folder:
    + provide command: `docker-compose up`
  - Open in browser:
    + [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Migrations:

Check out the [for more information](https://docs.djangoproject.com/en/4.0/topics/migrations/)

* makemigrations
  + `python manage.py makemigrations` for Windows
  + `python3 manage.py makemigrations` for *nix(Ubuntu, Linux, macOS)


* migrate for application and database:

  **Because there are multiple databases in this project, we must specify EVERY application where we need to migrate.**

  Check out the [for more information](https://docs.djangoproject.com/en/4.0/topics/db/multi-db/)


  + **Admin, sessions, admin_honeypot it's dependencies for "Users":** 
  
    *and must be done __before__ "users"*
  
  + Admin
    - `python manage.py migrate admin --database=users_db` for Windows
    - `python3 manage.py migrate admin --database=users_db` for *nix(Ubuntu, Linux, macOS)
    
  + Sessions
    - `python manage.py migrate sessions --database=users_db` for Windows
    - `python3 manage.py migrate sessions --database=users_db` for *nix(Ubuntu, Linux, macOS)
  
  + Admin honeypot
    - `python manage.py migrate admin_honeypot --database=users_db` for Windows
    - `python3 manage.py migrate admin_honeypot --database=users_db` for *nix(Ubuntu, Linux, macOS)
    
  + Users
    - `python manage.py migrate users --database=users_db` for Windows
    - `python3 manage.py migrate users --database=users_db` for *nix(Ubuntu, Linux, macOS)

  + Core (search)
    - `python manage.py migrate core --database=search_db` for Windows
    - `python3 manage.py migrate core --database=search_db` for *nix(Ubuntu, Linux, macOS)

  + Feedback
    - `python manage.py migrate feedback --database=feedback_db` for Windows
    - `python3 manage.py migrate feedback --database=feedback_db` for *nix(Ubuntu, Linux, macOS)
 
  + Crawler  
    - `python manage.py migrate crawler --database=crawler_db` for Windows
    - `python3 manage.py migrate crawler --database=crawler_db` for *nix(Ubuntu, Linux, macOS)
 
  + Analytics  
    - `python manage.py migrate analytics --database=analytics_db` for Windows
    - `python3 manage.py migrate analytics --database=analytics_db` for *nix(Ubuntu, Linux, macOS)

### Internationalization and localization
Check out the [for more information](https://docs.djangoproject.com/en/4.0/topics/i18n/translation/)

* Make messages for all languages without virtual env
  - `python manage.py makemessages -a  --ignore  venv` for Windows
  - `python3 manage.py makemessages -a  --ignore  venv` for *nix(Ubuntu, Linux, macOS)
  
* Compile messages
  - `django-admin compilemessages`


### Elasticsearch 
* Update/rebuild indexes
    - `python manage.py search_index --rebuild` for Windows
    - `python3 manage.py search_index --rebuild` for *nix(Ubuntu, Linux, macOS)
    
* Commands for Linux/Unix

  + Check status of service:
    - `sudo systemctl status elasticsearch.service`
  + Start service:
    - `sudo systemctl start elasticsearch.service`
  + Stop service:
    - `sudo systemctl stop elasticsearch.service`


### The Project's Future

    • Adding more data mining tools
    • Improved searching algorithms
    • Add more analytical and analysis tools
    • Improve video search
    • Give a more useful services
    • User interface improvements


## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

Andrii Buzov -   [an-b@ukr.net](mailto:an-b@ukr.net)

Project Link: [https://github.com/Facele55/Raw-Search](https://github.com/Facele55/Raw-Search)
