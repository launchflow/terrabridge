variable "gcp_project_id" {
    type = string
    description = "The GCP project to deploy resources into."
}

provider "google" {
    project = var.gcp_project_id
    region  = "us-central1"
    zone    = "us-central1-a"
}

resource "google_sql_database_instance" "postgres_sql_instance" {
    name = "terrabridge-testing-instance-mysql"
    project = var.gcp_project_id
    database_version = "POSTGRES_15"
    region = "us-central1"
    settings {
        tier = "db-custom-1-3840"
    }
}

resource "google_sql_database" "postgres_database" {
    name = "terrabridge-testing-database"
    project = var.gcp_project_id
    instance = google_sql_database_instance.postgres_sql_instance.name
}

resource "google_sql_user" "postgres_user" {
    name = "terrabridge-testing-user"
    project = var.gcp_project_id
    instance = google_sql_database_instance.postgres_sql_instance.name
    password = "terrabridge-testing-password"
}
