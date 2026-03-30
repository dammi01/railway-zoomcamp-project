terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  # Replace this with your actual Project ID from the GCP Console
  project = "eng-district-485200-n2"
  region  = "europe-west4"
}

# Data Lake (GCS Bucket)
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "railway-data-lake-dammi-2026" # Must be globally unique
  location      = "EU"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# Data Warehouse (BigQuery Dataset)
resource "google_bigquery_dataset" "dataset" {
  dataset_id = "railway_data"
  project    = "eng-district-485200-n2"
  location   = "EU"
}
