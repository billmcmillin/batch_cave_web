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
