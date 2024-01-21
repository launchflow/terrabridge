variable "gcp_project_id" {
    type = string
    description = "The GCP project to deploy resources into."
}

variable "bucket_name" {
    type = string
    description = "Name of the bucket."
}


provider "google" {
    project = var.gcp_project_id
    region  = "us-central1"
    zone    = "us-central1-a"
}

resource "google_storage_bucket" "bucket" {
    name = var.bucket_name
    location = "US"
}
