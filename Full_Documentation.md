#  Complete Deployment Guide
## AI Anime Recommendation System - Production Deployment

This comprehensive guide walks you through deploying your AI Anime Recommendation System to Google Cloud Platform with Kubernetes orchestration and Grafana Cloud monitoring.

---

##  Table of Contents

1. [Initial Setup](#1-initial-setup)
2. [Configure VM Instance](#2-configure-vm-instance)
3. [Configure Minikube (Kubernetes)](#3-configure-minikube-inside-vm)
4. [GitHub Integration](#4-github-integration)
5. [Build and Deploy Application](#5-build-and-deploy-application)
6. [Grafana Cloud Monitoring](#6-grafana-cloud-monitoring)
7. [Verification & Testing](#7-verification--testing)
8. [Cleanup](#8-cleanup)

---

## 1.  Initial Setup

### Prerequisites Checklist

Before starting, ensure you have:

-  GitHub account with your project repository
-  Google Cloud Platform (GCP) account
-  Groq API Key
-  HuggingFace API Token
-  Grafana Cloud account (free tier available)

### Step 1.1: Prepare Your Code

**Push your project to GitHub:**

```bash
cd your-project-directory
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Meenatchisundari/AI-ANIME-RECOMMENATION-SYSTEM---LLMOPS.git
git push -u origin main
```

### Step 1.2: Create Dockerfile

Create a `Dockerfile` in your project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 1.3: Create Kubernetes Deployment File

Create `llmops-k8s.yaml` in your project root:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llmops-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: llmops
  template:
    metadata:
      labels:
        app: llmops
    spec:
      containers:
      - name: llmops-container
        image: llmops-app:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8501
        env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: llmops-secrets
              key: GROQ_API_KEY
        - name: HUGGINGFACEHUB_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: llmops-secrets
              key: HUGGINGFACEHUB_API_TOKEN
---
apiVersion: v1
kind: Service
metadata:
  name: llmops-service
spec:
  type: LoadBalancer
  selector:
    app: llmops
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8501
```

### Step 1.4: Create GCP VM Instance

1. **Navigate to Google Cloud Console**
   - Go to: **Compute Engine** → **VM Instances**
   - Click **"CREATE INSTANCE"**

2. **Configure Instance Settings:**

   | Setting | Value |
   |---------|-------|
   | **Name** | `anime-recommender-vm` |
   | **Region** | Choose nearest to you |
   | **Machine Type** | E2 Standard |
   | **Memory** | 16 GB RAM |
   | **Boot Disk** | Ubuntu 24.04 LTS |
   | **Boot Disk Size** | 256 GB |

3. **Networking Configuration:**
   -  Allow HTTP traffic
   -  Allow HTTPS traffic

4. **Create the Instance**
   - Click **"CREATE"**
   - Wait for the instance to start (green checkmark)

5. **Connect via SSH**
   - Click the **SSH** button next to your instance
   - Browser-based terminal will open

---

## 2.  Configure VM Instance

### Step 2.1: Clone Your Repository

```bash
# Clone your GitHub repository
git clone https://github.com/Meenatchisundari/AI-ANIME-RECOMMENATION-SYSTEM---LLMOPS.git

# Navigate to project directory
cd AI-ANIME-RECOMMENATION-SYSTEM---LLMOPS

# Verify files
ls -la
```

**Expected output:**
```
app.py
pipeline.py
vector_store.py
requirements.txt
Dockerfile
llmops-k8s.yaml
...
```

### Step 2.2: Install Docker

#### 2.2.1: Install Docker Engine

```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### 2.2.2: Test Docker Installation

```bash
# Test with hello-world container
sudo docker run hello-world
```

**Expected output:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

#### 2.2.3: Configure Docker to Run Without sudo

```bash
# Create docker group
sudo groupadd docker

# Add your user to docker group
sudo usermod -aG docker $USER

# Activate changes to groups
newgrp docker

# Test without sudo
docker run hello-world
```

#### 2.2.4: Enable Docker on Boot

```bash
# Enable Docker service
sudo systemctl enable docker.service
sudo systemctl enable containerd.service

# Start Docker service
sudo systemctl start docker
```

#### 2.2.5: Verify Docker Setup

```bash
# Check Docker status
systemctl status docker

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a
```

---

## 3.  Configure Minikube Inside VM

### Step 3.1: Install Minikube

```bash
# Download Minikube binary
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# Install Minikube
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify installation
minikube version
```

### Step 3.2: Start Minikube Cluster

```bash
# Start Minikube with Docker driver
minikube start --driver=docker

# This may take 2-5 minutes
```

**Expected output:**
```
😄  minikube v1.32.0 on Ubuntu 24.04
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔥  Creating docker container (CPUs=2, Memory=2200MB) ...
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster
```

### Step 3.3: Install kubectl

```bash
# Install kubectl via snap
sudo snap install kubectl --classic

# Verify installation
kubectl version --client
```

### Step 3.4: Verify Minikube Setup

```bash
# Check Minikube status
minikube status

# Expected output:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured

# Check Kubernetes nodes
kubectl get nodes

# Expected output:
# NAME       STATUS   ROLES           AGE   VERSION
# minikube   Ready    control-plane   5m    v1.28.3

# Get cluster info
kubectl cluster-info

# Verify Docker container
docker ps
```

---

## 4.  GitHub Integration

### Step 4.1: Configure Git

```bash
# Set your Git email (use your actual email)
git config --global user.email "meenatchisundarimuthirulappan@gmail.com"

# Set your Git username (use your GitHub username)
git config --global user.name "Meenatchisundari"

# Verify configuration
git config --list
```

### Step 4.2: Push Changes to GitHub

```bash
# Stage all changes
git add .

# Commit changes
git commit -m "Add Dockerfile and Kubernetes deployment"

# Push to main branch
git push origin main
```

**When prompted for credentials:**
- **Username**: Your GitHub username
- **Password**: Your GitHub Personal Access Token (not your password)

>  **Note**: The token won't be visible when you paste it - this is normal!

### Step 4.3: Create GitHub Personal Access Token

If you don't have a token:

1. Go to: **GitHub.com** → **Settings** → **Developer Settings**
2. Click **"Personal Access Tokens"** → **"Tokens (classic)"**
3. Click **"Generate new token (classic)"**
4. Give it a name: `GCP-VM-Access`
5. Select scopes: `repo`, `workflow`
6. Click **"Generate token"**
7. **Copy and save the token** (you won't see it again!)

---

## 5.  Build and Deploy Application

### Step 5.1: Point Docker to Minikube

```bash
# Configure shell to use Minikube's Docker daemon
eval $(minikube docker-env)

# Verify Docker is pointing to Minikube
docker ps
```

### Step 5.2: Build Docker Image

```bash
# Build the Docker image
docker build -t llmops-app:latest .

# Verify image was created
docker images | grep llmops-app
```

**Expected output:**
```
llmops-app    latest    abc123def456    2 minutes ago    1.2GB
```

### Step 5.3: Create Kubernetes Secrets

```bash
# Create secrets for API keys
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="your_actual_groq_api_key_here" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="your_actual_huggingface_token_here"

# Verify secret was created
kubectl get secrets
```

>  **Important**: Replace the placeholder values with your actual API keys!

### Step 5.4: Deploy to Kubernetes

```bash
# Apply Kubernetes configuration
kubectl apply -f llmops-k8s.yaml

# Expected output:
# deployment.apps/llmops-app created
# service/llmops-service created

# Watch pods starting up
kubectl get pods -w

# Wait until STATUS shows "Running"
# Press Ctrl+C to stop watching
```

### Step 5.5: Verify Deployment

```bash
# Check deployment status
kubectl get deployments

# Expected output:
# NAME         READY   UP-TO-DATE   AVAILABLE   AGE
# llmops-app   1/1     1            1           2m

# Check pods
kubectl get pods

# Check services
kubectl get svc llmops-service
```

### Step 5.6: Expose Application

**Open TWO separate SSH terminals to your VM**

**Terminal 1 - Start Minikube Tunnel:**
```bash
# This creates a network route from your host to Minikube
minikube tunnel

# Keep this running! Do NOT close this terminal
```

**Terminal 2 - Port Forward:**
```bash
# Forward traffic from external port 8501 to service
kubectl port-forward svc/llmops-service 8501:80 --address 0.0.0.0

# Keep this running! Do NOT close this terminal
```

### Step 5.7: Access Your Application

1. **Get External IP:**
   ```bash
   # In a third terminal
   kubectl get svc llmops-service
   ```

2. **Open in Browser:**
   ```
   http://EXTERNAL_IP:8501
   ```
   
   Or use the VM's external IP from GCP console:
   ```
   http://34.67.178.77:8501
   ```

3. **Test the Application:**
   - Enter a query: "soft romance anime with beautiful animation"
   - Click recommend
   - View results!

---

## 6.  Grafana Cloud Monitoring

### Step 6.1: Create Monitoring Namespace

**Open a NEW SSH terminal (Terminal 3):**

```bash
# Create monitoring namespace
kubectl create namespace monitoring

# Verify namespace
kubectl get namespaces

# Expected output includes:
# NAME              STATUS   AGE
# default           Active   30m
# monitoring        Active   5s
```

### Step 6.2: Set Up Grafana Cloud Account

1. **Go to**: [grafana.com/products/cloud](https://grafana.com/products/cloud)
2. **Sign up** for free account
3. **Navigate to**: 
   - Left Pane → **Observability** → **Kubernetes**
   - Click **"Start Sending Data"**

### Step 6.3: Install Helm

```bash
# Download and install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify installation
helm version

# Expected output:
# version.BuildInfo{Version:"v3.13.0", ...}
```

### Step 6.4: Configure Grafana Integration

**In Grafana Cloud Web UI:**

1. **Backend Installation** → Click **"Install"**
2. **Configuration:**
   - **Cluster Name**: `minikube`
   - **Namespace**: `monitoring`
   - **Platform**: Kubernetes
   - Keep other defaults

3. **Create Access Token:**
   - Click **"Create new access token"**
   - **Token Name**: `minikube-token`
   - Click **"Create"**
   - **Copy and save the token** immediately!

4. **Select Deployment Method:**
   - Choose **"Helm"**
   - You'll see auto-generated Helm chart deployment command

### Step 6.5: Create Helm Values File

**Copy the Helm command from Grafana Cloud.** It looks like:

```bash
helm repo add grafana https://grafana.github.io/helm-charts &&
  helm repo update &&
  helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
    --namespace "monitoring" --create-namespace --values - <<'EOF'
cluster:
  name: minikube
... (lots of configuration)
EOF
```

**Create the values file:**

```bash
# Create and edit values.yaml
vi values.yaml
```

**In the editor:**
1. Press `i` to enter insert mode
2. Paste ONLY the YAML content (everything between the initial command and `EOF`)
3. Remove the `EOF` line at the end
4. Press `Esc`
5. Type `:wq!` and press Enter

**Your values.yaml should look like:**

```yaml
cluster:
  name: minikube
externalServices:
  prometheus:
    host: https://prometheus-prod-XX-XXX.grafana.net
    basicAuth:
      username: "123456"
      password: "glc_..."
  loki:
    host: https://logs-prod-XXX.grafana.net
    basicAuth:
      username: "123456"
      password: "glc_..."
# ... rest of configuration
```

### Step 6.6: Deploy Grafana Monitoring

```bash
# Add Grafana Helm repository and install
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
  --namespace "monitoring" --create-namespace --values values.yaml
```

**Expected output:**
```
Release "grafana-k8s-monitoring" has been installed.
STATUS: deployed
REVISION: 1
```

**This may take 2-5 minutes to complete.**

### Step 6.7: Verify Monitoring Setup

```bash
# Check all monitoring pods
kubectl get pods -n monitoring

# Expected output (all should be "Running"):
# NAME                                           READY   STATUS    RESTARTS   AGE
# grafana-k8s-monitoring-grafana-agent-0         2/2     Running   0          2m
# grafana-k8s-monitoring-kube-state-metrics-0    1/1     Running   0          2m
# grafana-k8s-monitoring-prometheus-node-exp...  1/1     Running   0          2m
# grafana-k8s-monitoring-prometheus-opera...     2/2     Running   0          2m

# Check if all are running
kubectl get all -n monitoring
```

### Step 6.8: View Metrics in Grafana Cloud

1. **Return to Grafana Cloud** web interface
2. Click **"Go to Homepage"**
3. **Refresh the page**
4. **Navigate**: Home → **Observability** → **Kubernetes** → **Nodes**
5. **Explore Your Metrics:**
   - Node CPU usage
   - Memory utilization
   - Pod status
   - Network traffic
   - And much more!

 **Success!** Your cluster is now being monitored!

---

## 7.  Verification & Testing

### Application Health Check

```bash
# Check all resources
kubectl get all

# Check logs from your app
kubectl logs -l app=llmops

# Check pod details
kubectl describe pod -l app=llmops

# Test application endpoint
curl http://localhost:8501
```

### Monitoring Health Check

```bash
# Verify Grafana monitoring
kubectl get pods -n monitoring
kubectl logs -n monitoring -l app.kubernetes.io/name=grafana-agent

# Check Helm releases
helm list -n monitoring
```

### Full System Status

```bash
# Minikube status
minikube status

# Cluster info
kubectl cluster-info

# All namespaces
kubectl get all --all-namespaces

# Node status
kubectl top nodes

# Pod resource usage (requires metrics-server)
kubectl top pods
```

---

## 8.  Cleanup

### When You're Done Testing

**Stop the Application (keep cluster running):**

```bash
# Delete deployment and service
kubectl delete -f llmops-k8s.yaml

# Delete secrets
kubectl delete secret llmops-secrets

# Verify deletion
kubectl get all
```

**Stop Monitoring (optional):**

```bash
# Remove Grafana monitoring
helm uninstall grafana-k8s-monitoring -n monitoring

# Delete monitoring namespace
kubectl delete namespace monitoring
```

**Stop Minikube:**

```bash
# Stop Minikube cluster
minikube stop

# Verify it stopped
minikube status
```

**Delete Everything (if starting fresh):**

```bash
# Delete Minikube cluster
minikube delete

# Remove Docker images
docker rmi llmops-app:latest

# Verify cleanup
docker images
```

**Delete GCP VM Instance:**

1. Go to **GCP Console** → **Compute Engine** → **VM Instances**
2. Select your VM
3. Click **"DELETE"**
4. Confirm deletion

>  **Important**: Deleting the VM will permanently remove all data!

---

##  Quick Reference Commands

### Docker Commands

```bash
docker ps                          # List running containers
docker images                      # List images
docker logs <container-id>         # View logs
docker exec -it <container> bash   # Access container shell
docker system prune -a             # Clean up everything
```

### Kubernetes Commands

```bash
kubectl get pods                   # List pods
kubectl get svc                    # List services
kubectl get deployments            # List deployments
kubectl describe pod <pod-name>    # Pod details
kubectl logs <pod-name>            # View pod logs
kubectl delete pod <pod-name>      # Delete pod
kubectl apply -f <file.yaml>       # Apply configuration
```

### Minikube Commands

```bash
minikube start                     # Start cluster
minikube stop                      # Stop cluster
minikube delete                    # Delete cluster
minikube status                    # Check status
minikube dashboard                 # Open dashboard
minikube service list              # List services
```

### Git Commands

```bash
git status                         # Check status
git add .                          # Stage changes
git commit -m "message"            # Commit changes
git push origin main               # Push to GitHub
git pull origin main               # Pull from GitHub
```

---

##  Troubleshooting

### Issue: Pod Not Starting

```bash
# Check pod status
kubectl get pods

# View pod details
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Common fixes:
# 1. Check if image exists
docker images

# 2. Verify secrets
kubectl get secrets

# 3. Recreate deployment
kubectl delete -f llmops-k8s.yaml
kubectl apply -f llmops-k8s.yaml
```

### Issue: Cannot Access Application

```bash
# Verify service is running
kubectl get svc llmops-service

# Check if tunnel is running
# In Terminal 1: minikube tunnel (should be active)
# In Terminal 2: kubectl port-forward (should be active)

# Test locally on VM
curl http://localhost:8501

# Check GCP firewall rules
# Ensure port 8501 is open
```

### Issue: Grafana Not Showing Data

```bash
# Check monitoring pods
kubectl get pods -n monitoring

# View logs
kubectl logs -n monitoring -l app.kubernetes.io/name=grafana-agent

# Verify Helm installation
helm list -n monitoring

# Reinstall if needed
helm uninstall grafana-k8s-monitoring -n monitoring
# Then follow Step 6.6 again
```

---

##  Additional Resources

- **Kubernetes Documentation**: [kubernetes.io/docs](https://kubernetes.io/docs)
- **Minikube Documentation**: [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io)
- **Docker Documentation**: [docs.docker.com](https://docs.docker.com)
- **Helm Documentation**: [helm.sh/docs](https://helm.sh/docs)
- **Grafana Cloud**: [grafana.com/docs](https://grafana.com/docs)
- **GCP Documentation**: [cloud.google.com/docs](https://cloud.google.com/docs)

---

##  Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs: `kubectl logs <pod-name>`
3. Open an issue on GitHub
4. Contact: meenatchisundarimuthirulappan@gmail.com

---

**Congratulations! ** You've successfully deployed your AI Anime Recommendation System to production with monitoring!

**Happy Deploying! **
