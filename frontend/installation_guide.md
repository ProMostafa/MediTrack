
## Dockerize App and Test Locally
### Installing docker & docker compose
Please refer to this [link](https://support.netfoundry.io/hc/en-us/articles/360057865692-Installing-Docker-and-docker-compose-for-Ubuntu-20-04) to install docker and docker compose

### Clone meditrack repository
```bash
 git ..
 cd frontend
```

### Build the Docker Image for React
for build image
```bash
docker build -t meditrack-frontend .
```
Run the React Container
```bash
docker run -d -p 3000:3000 --name meditrack-frontend meditrack-frontend
```

### Access the React Application
Once the containers are running, you can access the React application at http://localhost:3000.