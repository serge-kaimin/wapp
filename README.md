# wapp

Send messages and images using greenapi

## Prerequisites

* Ensure you have Docker and Docker Compose installed on your machine.
* Ensure you have make installed on your machine.

## Environment Variables

Ensure you have the necessary environment variables set up. You can create a .env or .envrc file in the root of your project with the following content:

file: .env
```shell
REACT_APP_API_URL=http://localhost:8000/api
DEBUG=false
```

## Build and Start the Application

1) Clone the repository:

```shell
https://github.com/serge-kaimin/wapp.git
cd wapp
```

2) Build the Docker image: Use the make command to build the Docker image.

```shell
make build
```

3) Start the application: Use the make command to start the application in detached mode.

```shell
source .env
make up
```

4) View logs: To view the logs of the running containers, use the following command:

```shell
make logs
```

5) Stop the application: To stop the application, use the following command:

```shell
make down
```




Access the Application
Once the application is running, you can access it in your web browser at:

```text
http://localhost:8000
```

Additional Information
* Ensure your index.html file is located in the /app/public directory.
* Ensure your Django settings are correctly configured to serve static files and templates.

By following these instructions, you should be able to build and start **wapp** application successfully.