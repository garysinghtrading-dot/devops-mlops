terraform {
  required_version = ">= 1.0"

  # Move your backend here to keep it centralized
  backend "gcs" {
    bucket = "tf-state-machine-learning-416604"
    prefix = "terraform/state"
  }

  required_providers {
    grafana = {
      source  = "grafana/grafana"
      version = ">= 3.0.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.0.0"
    }
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
}

# 1. Google Provider Configuration
provider "google" {
  project = var.project_id
  region  = var.region
}

# 2. Data source to get the Auth Token for the Helm provider
data "google_client_config" "default" {}

# 3. Helm Provider (Connects to your GKE Cluster)
provider "helm" {
  kubernetes = {
    host                   = "https://${google_container_cluster.primary.endpoint}"
    token                  = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
  }
}

# 4. Grafana Provider (Connects to the Grafana API)
provider "grafana" {
  url  = "http://localhost:3000" 
  auth = var.grafana_api_key
}