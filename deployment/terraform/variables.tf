variable "do_token" {
  description = "DigitalOcean API Token"
  sensitive   = true
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  default     = "dev"
}

variable "region" {
  description = "DigitalOcean region"
  default     = "sgp1"
}

variable "django_secret_key" {
  description = "Django Secret Key"
  sensitive   = true
} 