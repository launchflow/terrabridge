variable "gcp_project_id" {
    type = string
    description = "The GCP project to deploy resources into."
}

resource "google_secret_manager_secret" "secret" {
  secret_id = "secret"

  replication {
    user_managed {
      replicas {
        location = "us-central1"
      }
    }
  }
}
