##Fresh install on production
```
sudo su tricerashopper
cd ~
curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda....sh
source .bashrc
```

sftp conda_batchcave_dependencies.txt and .env to data server

move to tricerashopper home dir and chown 
```
sudo chown tricerashopper:tricerashopper conda_batchcave_dependencies.txt
sudo chown 1003:1003 /home/tricerashopper/.conda/pkgs/urls.txt 

sudo su tricerashopper
conda env create -f conda_batchcave_de..
source activate batchcave
exit

cd /var/www/html/
sudo git clone https://github.com/billmcmillin/batch_cave_web.git
sudo chown -R tricerashopper:tricerashopper batch_cave_web
sudo su tricerashopper
cd batch_cave_we
source .env
pip install pymarc
```

* Add host to ALLOWED_HOSTS in settings
 
* ```python3 manage.py runserver 0.0.0.0:8000```
test with
``` curl -XGET localhost```

## Apache settings
```
ProxyPass / http://localhost:8000/
ProxyPassReverse / http://localhost:8000/ 


```
echo "conda activate" >> ~/.bashrc
/etc/systemd/system/gunicorn.service
#### Enable Gunicorn to run as a service with Systemd
[Unit]
Description=Gunicorn server for BatchCave 

[Service]
Restart=on-failure  
User=tricerashopper
WorkingDirectory=/var/www/html/batch_cave_web
EnvironmentFile=/var/www/html/batch_cave_web/.env

ExecStart=/home/tricerashopper/.conda/envs/batchcave/bin/gunicorn batch_cave.wsgi:application

[Install]
WantedBy=multi-user.target 

--------------
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn


Run with ```sudo systemctl start gunicorn```
* note: export command must be removed from env file for this work

##Updating 
* Log in to tricerashopper
* sudo systemctl stop gunicorn
* sudo su tricerashoper
* cd /var/www/html/batch_cave_web
* git pull
* exit
* sudo systemctl start gunicorn
