##Batch-mobile
### The webified version of Batchcave

## The Environment
* Python 3.6
* Geckodriver 0.19.1 from https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
- put it in PATH ~/anaconda3/bin or /opt
* Managed with conda. 
```
conda env create -f environment.yml
source activate batchcave
```
* Batchcave environment was created with
```conda install django=1.11.3
conda install selenium=3.9.0```

### Environment Variables
* the .env file contains the variable 'DJANGOKEY' 
* run ```source .env``` from batchmobile root dir to add it to environment

## The structure
* The root-level directory, batchmobile, contains configuration files and odds and ends related to dev and testing
* batchcave is the folder for project-wide settings. No content lives here
* converter is the app that contains models, views, etc.
* why so many names? To avoid namespace issues when importing modules, avoid repeating names further up the directory structure

### Apps
* The admin app has been disabled
* converter is the app with most code and tests
* many settings are in batch_cave/settings.py

## Command Line
```
python3
import django
django.setup()
c = Conversion()
c.name = 'testing'
c.save()
saved_c = Conversion.objects.first()
```

## Functional/Acceptance Tests
Functional tests are in converter/functional_tests. Run with
```python3 manage.py test functional_tests```

Tests are isolated with the LiveServerTestCase class.


## Unit Tests
Run with
```python3 manage.py test converter```


## Static Files
All static files are currently in converter/static
If there are additional apps in the future, it will be best to collect them all in to one static directory for serving. This has been configured in settings.py as /static in the root dir of the project. Collect all static filles into this folder with
```python3 manage.py collectstatic```

## The database
Flush development db with
```python3 manage.py flush```

## Set up Staging Site on a new server
* install conda
``` curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
md5sum Miniconda....
``` 
Check against installer md5 at https://repo.continuum.io/miniconda/

```
sudo bash Miniconda...
```
Install in /usr/bin/miniconda3
append source to .bashrc
do for local user as well as root
sftp conda env file to server

```
conda env create -f conda_batch_cave_env.txt
source activate batchcave
cd /var/www/html/batch_cave_web
source .env
pip install pymarc
```

* Allow it through the firewall
```
sudo firewall-cmd --zone=public --add-port=8000/tcp
```

* Add host to ALLOWED_HOSTS in settings
 
* sftp the .env file to the server
* cd /var/www/html
* sudo git clone https://github.com/billmcmillin/batch_cave_web.git
* sudo mv ~/.env batch_cave_web
* ```python3 manage.py runserver 0.0.0.0:8000```

## Apache settings
```
ProxyPass / http://localhost:8000/
ProxyPassReverse / http://localhost:8000/ 
```

## Setting up a new Production Site
* RHEL and Apache
```cd /var/www/html
source activate batchcave
sudo yum install mod_wsgi
conda install gunicorn

sudo git clone https://github.com/billmcmillin/batch_cave_web.git

sudo su tricerashopper

cd /var/www/html/batch_cave_web
gunicorn batch_cave.wsgi:application
```

#### Enable static files to be served by Apache, not Gunicorn
```
python manage.py collectstatic --noinput
```

in /etc/httpd/conf/httpd.conf: 
ProxyPassMatch ^/static !
ProxyPass / http://localhost:8000/
ProxyPassReverse / http://localhost:8000/ 

Then
```
sudo systemctl restart httpd.service
```
restart gunicorn


#### set a unique key on each server
in python:
```
a - random.SysRandom()
>>> dk = ''
>>> for i in range(0,50):
...     dk += a.choice('abcdefghijklmnopqrstuvwxyz01234567890')
... 
>>> dk

```
