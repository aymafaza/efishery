# Task Odoo Engineer Efishery

## Live Demo
In case you have problems during the installation process, you can my live server demo.
URL: http://103.183.74.21:8069/
username: tester
password: tester

## Requirements
- Latest version of docker https://www.docker.com/
## Installation
- Build container using docker compose. ```docker-compose up -d```
- Update/Create (if not exist) odoo.conf file in /odoo-config/odoo.conf
```
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons/external_module,/mnt/extra-addons/efishery
```
Add addons_path ```/mnt/extra-addons/external_module,/mnt/extra-addons/efishery```
```
server_wide_modules = base,web,queue_job
workers = 0

[queue_job]
channels = root:1
```
Add job queue configuration server_wide_modules,workers, and channels.

- Access & setup odoo using localhost. ```http://localhost:8069/```
## Usage
- Install required modules ```efishery_auth, efishery_user, efishery_fetch, efishery_marketplace
![Module](/img/1.png)
### User Module
- To create new user by using import. Access Setting module ```Setting=>User & Companies=>Users```
- Clik Button ```Favorites=>Import``` Records
![Module](/img/2.png)
- Import your files, and make sure check ```Import in the background``` option.
![Module](/img/3.png)
- User can check the progress by accessing ```Job Queue``` Module
![Module](/img/4.png)
- Once the import process is complete, the user will receive a notification via live chat and email.
![Module](/img/5.png)

### Auth Module
- To generate token user can access Odoo JSON API by using ```/auth/login``` endpoints.
- User must include the required parameters in the request Body. Mandatory parameters are the ```username``` and ```password```, while the db parameter is optional. (if empty the system will use currently active db)
![Module](/img/6.png)

### Fetch Module
- To fetch resources user can access Odoo JSON API by using ```/fetch``` endpoints.
- User must include the jwt token when requesting by using ```Bearer token``` method.
![Module](/img/7.png)

### Marketplace Module
- To create and get sale order data, user can access Odoo JSON API by using ```/sale-order``` endpoints.
- User must include the jwt token when requesting by using ```Bearer token``` method.
![Module](/img/8.png)
![Module](/img/9.png)

### Notes
All sample API requests have been listed via the Postman Collection, the files can be accessed on the github repo.
