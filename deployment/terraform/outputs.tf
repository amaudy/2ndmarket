output "droplet_ip" {
  value = digitalocean_droplet.market2hand.ipv4_address
}

output "droplet_name" {
  value = digitalocean_droplet.market2hand.name
} 