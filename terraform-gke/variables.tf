variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "cluster_name" {
  description = "Name of the GKE cluster"
  type        = string
  default     = "ml-inference-cluster"
}

variable "machine_type" {
  description = "Node pool machine type"
  type        = string
  default     = "e2-medium"
}