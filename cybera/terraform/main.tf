terraform {
  required_version = ">= 0.14.0"
    required_providers {
      openstack = {
        source  = "terraform-provider-openstack/openstack"
        version = "~> 1.53.0"
      }
    }
}

variable password {
  type      = string
  sensitive = true
}


# Configure the OpenStack Provider
provider "openstack" {
  user_name   = "villarre@ualberta.ca"
  tenant_name = "villarre@ualberta.ca"
  password    = var.password
  auth_url    = "https://keystone-yeg.cloud.cybera.ca:5000/v3"
  region      = "Edmonton"
}