terraform {
  backend "gcs" {
    bucket  = var.bucket_name
    prefix  = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. The Network
resource "google_compute_network" "vpc_network" {
  name                    = "mlops-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "gke_subnet" {
  name          = "gke-subnet"
  ip_cidr_range = "10.0.0.0/24"
  network       = google_compute_network.vpc_network.id
}

# 2. The GKE Cluster (Control Plane only)
resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = "${var.region}-a"

  remove_default_node_pool = true
  initial_node_count       = 1
  network                  = google_compute_network.vpc_network.name
  subnetwork               = google_compute_subnetwork.gke_subnet.name
  
  # Prevents accidental deletion of the cluster in production
  deletion_protection = false 
}

# 3. The Separately Managed Node Pool (Spot VMs)
resource "google_container_node_pool" "primary_nodes" {
  name       = "spot-node-pool"
  location   = "${var.region}-a"
  cluster    = google_container_cluster.primary.name
  node_count = 2

  node_config {
    machine_type = var.machine_type
    
    # Enables Spot VMs for cost optimization
    spot = true

    # Best practice: label nodes for targeted pod scheduling
    labels = {
      workload = "ml-inference"
      env      = "dev"
    }

    service_account = "default"
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}

/*
resource "google_artifact_registry_repository" "my_app_repo" {
  location      = var.region
  repository_id = "eviction-microservices-repo"
  description   = "Docker repository for ML microservices"
  format        = "DOCKER"
}
*/

# Create a Cloud Router (required for NAT)
resource "google_compute_router" "router" {
  name    = "gke-router"
  region  = var.region
  network = google_compute_network.vpc_network.name
}

# Create the NAT Gateway
resource "google_compute_router_nat" "nat" {
  name                               = "gke-nat"
  router                             = google_compute_router.router.name
  region                             = google_compute_router.router.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

resource "google_compute_firewall" "allow_http" {
  name    = "allow-http-ingress"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["80", "8080"]
  }

  source_ranges = ["0.0.0.0/0"]
}