#  AI Anime Recommendation System - LLMOps

An intelligent anime recommender application that leverages LLMOps techniques with LangChain, ChromaDB, Grafana Cloud, HuggingFace, and Groq to deliver personalized anime recommendations through an interactive Streamlit web interface.

![Architecture](https://via.placeholder.com/1200x300/1a1a1a/ffffff?text=AI+Anime+Recommendation+System)

##  Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Monitoring with Grafana Cloud](#-monitoring-with-grafana-cloud)
- [Technologies Used](#-technologies-used)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

##  Features

- **Personalized Recommendations**: Get anime suggestions based on natural language queries (e.g., "soft romance anime with beautiful animation")
- **Semantic Search**: Uses ChromaDB and HuggingFace embeddings for contextual retrieval
- **LLM-Powered**: Leverages Groq's `llama-3.1-8b-instant` model for intelligent recommendations
- **Interactive UI**: Clean Streamlit interface for easy interaction
- **Production-Ready**: Containerized with Docker and deployable on Kubernetes
- **Cloud Monitoring**: Integrated with Grafana Cloud for observability
- **Modular Pipeline**: Easy to extend and experiment with different models

---

##  Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PROJECT SETUP                                │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────────┐                │
│  │ Groq API │  │ HuggingFace  │  │    Virtual      │                │
│  │          │  │     API      │  │  Environment    │                │
│  └──────────┘  └──────────────┘  └─────────────────┘                │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────────┐                │
│  │ Logging  │  │   Custom     │  │    Project      │                │
│  │          │  │  Exception   │  │   Structure     │                │
│  └──────────┘  └──────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         CORE CODE                                   │
│                                                                     │
│  Configuration → Data Loader → ChromaDB → Prompt → Recommender      │
│       ↓              ↓            ↓       Templates      ↓          │
│   config.py    data_loader.py  vector_   prompt_    recommender.py  │
│                                 store.py template.py                │
│                                                                     │
│                  ↓  Train & Recommend  ↓                            │
│                    (pipeline.py)                                    │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      STREAMLIT APP                                  │
│                        (app.py)                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        DEPLOYMENT                                   │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────┐                  │
│  │ Dockerfile │  │  K8s Deploy │  │    GitHub    │                  │
│  │            │  │             │  │  Versioning  │                  │
│  └────────────┘  └─────────────┘  └──────────────┘                  │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────┐                  │
│  │  GCP VM    │  │   K8s App   │  │   Grafana    │                  │
│  │            │  │             │  │    Cloud     │                  │
│  └────────────┘  └─────────────┘  └──────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

##  Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8+** installed
- **Git** for version control
- **API Keys**:
  - Groq API Key ([Get it here](https://console.groq.com))
  - HuggingFace API Token ([Get it here](https://huggingface.co/settings/tokens))
- **For Deployment** (optional):
  - Docker installed
  - Google Cloud Platform account
  - Kubernetes (Minikube for local, GKE for production)
  - Grafana Cloud account

---

##  Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Meenatchisundari/AI-ANIME-RECOMMENATION-SYSTEM---LLMOPS.git
cd AI-ANIME-RECOMMENATION-SYSTEM---LLMOPS
```

### Step 2: Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `langchain` - LLM orchestration framework
- `langchain-community` - Community integrations
- `langchain-groq` - Groq LLM integration
- `langchain-huggingface` - HuggingFace embeddings
- `chromadb` - Vector database for semantic search
- `streamlit` - Web interface framework
- `pandas` - Data manipulation
- `python-dotenv` - Environment variable management
- `sentence-transformers` - Embeddings

---

##  Configuration

### Step 1: Create Environment File

Create a `.env` file in the root directory:

```bash
# Copy the example file
cp .env.example .env
```

### Step 2: Add Your API Keys

Edit the `.env` file and add your credentials:

```env
# Required API Keys
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here

# Model Configuration (default settings)
MODEL_NAME=llama-3.1-8b-instant
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Step 3: Prepare Your Data

Place your anime CSV files in the `data/` folder:

```
data/
├── animewithsynopsis.csv
```

**Note**: Update the file paths in `data_loader.py` if your files have different names.

---

##  Usage

### Step 1: Build the Vector Store

Process and embed the anime dataset for semantic search:

```bash
python build_pipeline.py
```

This will:
- Load anime data from CSV files
- Clean and structure the data
- Generate embeddings using HuggingFace models
- Store vectors in ChromaDB for fast retrieval

### Step 2: Run the Streamlit Application

Launch the web interface:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Step 3: Get Recommendations

1. Enter your anime preferences in natural language
   - Example: *"soft romance anime with beautiful animation"*
   - Example: *"teenage story with action and drama"*
   - Example: *"psychological thriller with complex characters"*

2. Click the recommend button

3. View personalized recommendations with:
   - Anime titles
   - Plot summaries
   - Why it matches your preferences

---

##  Project Structure

```
AI-ANIME-RECOMMENATION-SYSTEM---LLMOPS/
│
├── data/                          # Anime datasets
│   ├── animewithsynopsis.csv
│   └── animeupdated.csv
│
├── chroma_db/                     # ChromaDB vector store (generated)
│
├── app.py                         # Streamlit web application
├── pipeline.py                    # Orchestrates retrieval and LLM
├── vector_store.py                # ChromaDB creation and management
├── prompt_template.py             # Recommendation prompt templates
├── recommender.py                 # Groq LLM integration
├── build_pipeline.py              # Data vectorization script
├── data_loader.py                 # CSV data cleaning and loading
├── config.py                      # Environment variables and config
│
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup configuration
├── .env                          # Environment variables (create this)
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
│
├── Dockerfile                     # Docker container configuration
├── llmops-k8s.yaml               # Kubernetes deployment file
│
├── README.md                      # This file
└── FULL_DOCUMENTATION.md         # Deployment documentation
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI - handles user input and displays recommendations |
| `pipeline.py` | Main orchestration - connects data retrieval with LLM |
| `vector_store.py` | Manages ChromaDB vector database operations |
| `prompt_template.py` | Defines the prompt structure for the LLM |
| `recommender.py` | Integrates Groq API for generating recommendations |
| `build_pipeline.py` | Processes and vectorizes anime dataset |
| `data_loader.py` | Cleans and structures CSV data |
| `config.py` | Loads environment variables and model settings |

---

##  Deployment

### Local Deployment with Docker

#### Step 1: Build Docker Image

```bash
docker build -t anime-recommender:latest .
```

#### Step 2: Run Container

```bash
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  -e HUGGINGFACEHUB_API_TOKEN=your_token \
  anime-recommender:latest
```

### Production Deployment on Google Cloud (GCP)

#### Step 1: Create GCP VM Instance

1. Go to **VM Instances** → **Create Instance**
2. Configure:
   - **Name**: `anime-recommender-vm`
   - **Machine Type**: E2 Standard (16 GB RAM)
   - **Boot Disk**: Ubuntu 24.04 LTS, 256 GB
   - **Networking**: Enable HTTP/HTTPS traffic

3. **SSH** into the VM

#### Step 2: Install Docker

```bash
# Update system
sudo apt-get update

# Install Docker (follow official Docker documentation)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Run Docker without sudo
sudo usermod -aG docker $USER
newgrp docker

# Enable Docker on boot
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

#### Step 3: Install Kubernetes (Minikube)

```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start Minikube
minikube start

# Install kubectl
sudo snap install kubectl --classic

# Verify installation
kubectl version --client
minikube status
```

#### Step 4: Deploy to Kubernetes

```bash
# Point Docker to Minikube
eval $(minikube docker-env)

# Build image
docker build -t llmops-app:latest .

# Create secrets for API keys
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="your_groq_key" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="your_hf_token"

# Deploy application
kubectl apply -f llmops-k8s.yaml

# Check pods
kubectl get pods

# Expose the service
minikube tunnel  # Run in one terminal

# In another terminal
kubectl port-forward svc/llmops-service 8501:80 --address 0.0.0.0
```

#### Step 5: Access Your Application

Get the external IP:
```bash
kubectl get svc llmops-service
```

Open in browser: `http://EXTERNAL_IP:8501`

---

##  Monitoring with Grafana Cloud

### Step 1: Set Up Monitoring Namespace

```bash
# Create monitoring namespace
kubectl create ns monitoring

# Verify
kubectl get ns
```

### Step 2: Install Helm

```bash
# Install Helm (package manager for Kubernetes)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify installation
helm version
```

### Step 3: Configure Grafana Cloud

1. **Sign up** at [Grafana Cloud](https://grafana.com/products/cloud/)
2. Navigate to: **Observability** → **Kubernetes** → **Start Sending Data**
3. Select **Backend Installation** → **Install**
4. Configure:
   - **Cluster Name**: `minikube`
   - **Namespace**: `monitoring`
   - **Platform**: Kubernetes
5. **Create Access Token**: Name it `minikube-token` and save it

### Step 4: Create Helm Values File

```bash
# Create values file
vi values.yaml
```

Paste the configuration from Grafana Cloud (remove the initial `helm` command and `EOF`):

```yaml
# Paste your Grafana configuration here
cluster:
  name: minikube
# ... rest of configuration
```

Save and exit (`:wq`)

### Step 5: Deploy Grafana Monitoring

```bash
# Add Grafana Helm repository and deploy
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
  --namespace "monitoring" --create-namespace --values values.yaml

# Verify deployment
kubectl get pods -n monitoring
```

### Step 6: View Metrics

1. Go back to Grafana Cloud
2. Click **Go to Homepage**
3. Navigate to: **Home** → **Observability** → **Kubernetes** → **Nodes**
4. Explore metrics for your cluster!

---

##  Technologies Used

### Core Technologies
- **Python 3.8+** - Programming language
- **LangChain** - LLM application framework
- **Groq** - Ultra-fast LLM inference (`llama-3.1-8b-instant`)
- **HuggingFace** - Embeddings and model hosting
- **ChromaDB** - Vector database for similarity search
- **Streamlit** - Web UI framework

### Data Processing
- **Pandas** - Data manipulation
- **Sentence Transformers** - Text embeddings

### MLOps & Deployment
- **Docker** - Containerization
- **Kubernetes** - Container orchestration
- **Minikube** - Local Kubernetes cluster
- **Helm** - Kubernetes package manager
- **Grafana Cloud** - Monitoring and observability

### Development Tools
- **Git** - Version control
- **GitHub** - Code repository
- **python-dotenv** - Environment management

---

##  Troubleshooting

### Issue: ModuleNotFoundError

```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: API Key Errors

```bash
# Solution: Check your .env file
cat .env

# Ensure keys are set correctly
echo $GROQ_API_KEY
```

### Issue: ChromaDB not found

```bash
# Solution: Rebuild the vector store
python build_pipeline.py
```

### Issue: Streamlit won't start

```bash
# Solution: Check if port 8501 is available
lsof -i :8501

# Kill any process using the port
kill -9 <PID>

# Restart Streamlit
streamlit run app.py
```

### Issue: Docker build fails

```bash
# Solution: Clean Docker cache
docker system prune -a

# Rebuild
docker build --no-cache -t anime-recommender:latest .
```

### Issue: Kubernetes pod not running

```bash
# Check pod status
kubectl get pods

# View logs
kubectl logs <pod-name>

# Describe pod for more details
kubectl describe pod <pod-name>
```

---

##  Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Write unit tests for new features
- Update documentation as needed
- Test locally before submitting PR

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

##  Contact

**Meenatchi Sundari**

-  Email: meenatchisundarimuthirulappan@gmail.com
-  GitHub: [@Meenatchisundari](https://github.com/Meenatchisundari)

---

##  Acknowledgments

- **Groq** for ultra-fast LLM inference
- **HuggingFace** for embeddings and transformers
- **LangChain** community for the excellent framework
- **ChromaDB** for efficient vector storage
- **Streamlit** for the intuitive UI framework
- MyAnimeList and anime dataset contributors

---

## 📈 Future Enhancements

- [ ] Add user authentication and profiles
- [ ] Implement rating system for recommendations
- [ ] Add anime watchlist functionality
- [ ] Support for multiple languages
- [ ] Integration with MyAnimeList API
- [ ] Advanced filtering (year, studio, episodes)
- [ ] Recommendation explanation feature
- [ ] A/B testing for different prompts
- [ ] Cost optimization for API calls

---

 **If you find this project helpful, please give it a star!**

**Happy Anime Watching! **
