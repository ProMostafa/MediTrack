## Deployment Guide to AWS Using AWS Copilot

This guide will walk you through the steps to deploy both the Django backend and React frontend applications to AWS using AWS Copilot, and configure a PostgreSQL RDS instance for the Django application.

### Prerequisites
- An AWS account
- AWS CLI installed and configured
- AWS Copilot CLI installed (You can find installation instructions [here](https://aws.github.io/copilot-cli/docs/getting-started/installation/))
- Docker installed

### Step 1: Set Up AWS Copilot
1. **Initialize Copilot**  
   In the root directory of your project, run the following command to initialize your application:

   ```bash
   copilot init
   ```
### Follow the prompts to:
1. Name your application (e.g., meditrack).
2. Choose a service type (select "Load Balanced Web Service" for Django).
3. Provide the Dockerfile path (usually ./backend/Dockerfile).
4. Set the port (default is 8000).
5. Choose a deployment environment (e.g., test or prod).


### Deploy the Backend
After initialization, deploy your Django application:
```bash
   copilot deploy
   ```

### copilot deploy
This command will build the Docker image, create the necessary infrastructure, and deploy your Django service.

### Step 2: Set Up PostgreSQL RDS
1. Create the Database
2. Create a PostgreSQL database using the AWS Management Console or by running the 

### following command with AWS Copilot:
1. copilot storage init
2. Select "PostgreSQL" as the database type and provide the required details (e.g., database name, username, and password). This will create the RDS instance and store the connection details.

### Update Django Settings
After the RDS instance is created, update your Django settings to connect to the PostgreSQL database. In your settings.py,
***Ensure you add requireing roles to enable access database.***

***Ensure that you have the environment variables DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, and DB_PORT set correctly in your Copilot environment.***

### Step 3: Deploy the React App
Initialize and Deploy the Frontend
Navigate to your React app directory (usually frontend) and run:
```bash
   copilot init
   ```
Select "Frontend" as the service type and follow the prompts to complete the setup.
Deploy the Frontend Service

### After initialization, deploy your React application:
```bash
   copilot deploy
   ```

### Step 4: Access Your Applications
Once the deployments are complete, AWS Copilot will provide URLs for both the backend and frontend services. You can access them in your terminal output.

### Additional Configuration
Environment Variables: Ensure that all necessary environment variables for the Django application are set in the Copilot environment. You can do this using:


### Redepoy after changes
```bash
   copilot svc deploy
   ```

### show logs
```bash
   copilot svc logs
   ```

### show status
```bash
   copilot svc status
   ```

### Be Cautious
1. **Permissions**  
   Ensure your user has the necessary permissions to use AWS Copilot for managing your projects. This may include permissions for services like ECS, RDS, and IAM.

2. **Database Connection Rules**  
   Configure security rules for your PostgreSQL RDS instance to allow connections from your backend service. This typically involves setting up security group rules to allow inbound traffic on the database port (default is 5432) from the backend service.

3. **Backend Configuration**  
   Configure your Django backend to accept requests from the frontend application. This may involve updating CORS settings or adjusting allowed hosts in your `settings.py` to include the frontend's URL.
