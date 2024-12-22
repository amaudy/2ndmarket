terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}

# Create a new Web Droplet
resource "digitalocean_droplet" "market2hand" {
  image     = "ubuntu-22-04-x64"
  name      = "market2hand-${var.environment}"
  region    = var.region
  size      = "s-1vcpu-1gb"
  ssh_keys  = [data.digitalocean_ssh_key.addskillsdev1.id]
}

# Get existing SSH key
data "digitalocean_ssh_key" "addskillsdev1" {
  name = "addskillsdev1"
}

# Create a firewall
resource "digitalocean_firewall" "market2hand" {
  name = "market2hand-${var.environment}"
  droplet_ids = [digitalocean_droplet.market2hand.id]

  # SSH
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # HTTP
  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Outbound: Allow all
  outbound_rule {
    protocol              = "tcp"
    port_range           = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

resource "local_file" "ansible_inventory" {
  content = templatefile("${path.module}/../ansible/inventory/hosts.yml.tpl", {
    droplet_ip = digitalocean_droplet.market2hand.ipv4_address
  })
  filename = "${path.module}/../ansible/inventory/hosts.yml"
}

resource "null_resource" "ansible_provisioner" {
  depends_on = [local_file.ansible_inventory]

  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../ansible/inventory/hosts.yml ../ansible/site.yml"
  }
} 