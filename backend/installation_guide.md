
## Dockerize App and Test Locally
### Installing docker & docker compose
Please refer to this [link](https://support.netfoundry.io/hc/en-us/articles/360057865692-Installing-Docker-and-docker-compose-for-Ubuntu-20-04) to install docker and docker compose

### Clone meditrack repository
```bash
 git ..
 cd meditrack
```

### Build & run docker compose file 
for build image
```bash
docker-compose build
```
for run unit tests
```bash
docker-compose run test-runner
```
for run images
```bash
docker-compose up
```
for stop containers and remove it
```bash
docker-compose down
```
## Create Admin user
make sure you run docker-compose up
```bash
docker exec -it <container_id> sh python manage.py createsuperuser
```

### Access the React Application
Once the containers are running, you can access the React application at http://localhost:8000.