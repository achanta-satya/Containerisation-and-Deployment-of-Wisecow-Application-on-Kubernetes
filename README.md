## Dockerization:
    
#### 1. Clone the repository git clone https://github.com/nyrahul/wisecow

#### 2.Write Dockerfile:
    
    # Use an official Python runtime as a parent image
    FROM python:3.9-slim

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    COPY . .

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Expose port 80 to the world outside the container
    EXPOSE 80

    # Define environment variable
    ENV NAME=Wisecow

    # Run app.py when the container launches
    CMD ["python", "app.py"]


#### 3. Build the Docker image:

    docker build -t wisecow-app .

#### 4. Test the Docker image locally:

    docker run -p 8080:80 wisecow-app
    Kubernetes Deployment
    Create Deployment YAML (deployment.yaml):
    apiVersion: apps/v1
    kind: Deployment
    metadata:
        name: wisecow-deployment
    labels:
        app: wisecow
    spec:
        replicas: 1
    selector:
        matchLabels:
        app: wisecow
    template:
        metadata:
        labels:
            app: wisecow
        spec:
            containers:
            - name: wisecow
            image: <your-container-registry>/wisecow-app:latest
            ports:
            - containerPort: 80

## Kubernetes Deployment

#### Create Service YAML (service.yaml):

    apiVersion: v1
    kind: Service
    metadata:
        name: wisecow-service
    spec:
        selector:
        app: wisecow
        ports:
        - protocol: TCP
        port: 80
        targetPort: 80
        type: LoadBalancer

#### Apply the manifest files:
    
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml

## TLS Configuration (ingress.yaml): (Challenge Goal)
        

    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: wisecow-ingress
      annotations:
         nginx.ingress.kubernetes.io/rewrite-target: /
      namespace: default
    spec:
      tls:
      - hosts:
        - your-domain.com
        secretName: wisecow-tls-secret
      rules:
      - host: your-domain.com
        http:
          paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: wisecow-service
                port:
                number: 80

#### Create a TLS secret:
    kubectl create secret tls wisecow-tls-secret --cert=cert.pem --key=key.pem


## CI/CD Pipeline
### GitHub Actions Workflow

Create a file at .github/workflows/ci-cd.yaml

    name: CI/CD Pipeline

    on:
      push:
        branches:
          - main

    jobs:
      build-and-deploy:
      runs-on: ubuntu-latest
      steps:
      - name: Checkout code
      uses: actions/checkout@v2

    - name: Login to Container Registry
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}

    - name: Build Docker image
      run: docker build -t <your-container-registry>/wisecow-app:latest .

    - name: Push Docker image
      run: docker push <your-container-registry>/wisecow-app:latest

    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f deployment.yaml
        kubectl apply -f service.yaml
        kubectl apply -f ingress.yaml
      env:
        KUBECONFIG: ${{ secrets.KUBE_CONFIG_DATA }}
