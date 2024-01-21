variable "gcp_project_id" {
    type = string
    description = "The GCP project to deploy resources into."
}

provider "google" {
    project = var.gcp_project_id
    region  = "us-central1"
    zone    = "us-central1-a"
}

resource "google_sql_database_instance" "sql_server_sql_instance" {
    name = "terrabridge-testing-instance-sql-server"
    project = var.gcp_project_id
    database_version = "SQLSERVER_2019_STANDARD"
    region = "us-central1"
    root_password="root-password"
    settings {
        tier = "db-custom-1-3840"
    }
}

resource "google_sql_database" "sql_server_database" {
    name = "terrabridge-testing-database"
    project = var.gcp_project_id
    instance = google_sql_database_instance.sql_server_sql_instance.name
}

resource "google_sql_user" "sql_server_user" {
    name = "terrabridge-testing-user"
    project = var.gcp_project_id
    instance = google_sql_database_instance.sql_server_sql_instance.name
    password = "terrabridge-testing-password"
}