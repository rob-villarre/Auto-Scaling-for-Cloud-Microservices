output "client_vm_instance_ip_addr" {
  value = openstack_compute_instance_v2.client_vm.access_ip_v4
}

output "swarm_manager_vm_instance_ip_addr" {
  value = openstack_compute_instance_v2.swarm_manager_vm.access_ip_v4
}

output "swarm_node_vm_instance_ip_addr" {
  value = openstack_compute_instance_v2.swarm_node_vm.access_ip_v4
}

output "private_key" {
  value = nonsensitive(openstack_compute_keypair_v2.keypair.private_key)
}