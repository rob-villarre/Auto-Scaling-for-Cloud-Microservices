resource "openstack_compute_instance_v2" "client_vm" {
  name = "Client_VM"
  image_name = "Ubuntu 20.04"
  flavor_name = "m1.small"

  key_pair = openstack_compute_keypair_v2.keypair.name

  security_groups = [ openstack_compute_secgroup_v2.default.name ]

  # provisioner "local-exec" {
  #   command = <<-EOT
  #     sudo apt -y install python-pip
  #     pip install requests
  #   EOT
  # }

  connection {
    type = "ssh"
    user = "ubuntu"
    host = self.access_ip_v6
    private_key = openstack_compute_keypair_v2.keypair.private_key
    agent = false
  }

  provisioner "remote-exec" {
    inline = [ 
      "sudo apt -y install python-pip",
      "pip install requests"
     ]
  }

  depends_on = [ openstack_compute_keypair_v2.keypair ]
}

output "client_vm_instance_ip_addr" {
  value = openstack_compute_instance_v2.client_vm.access_ip_v6
}

resource "openstack_compute_keypair_v2" "keypair" {
  name = "instance-keypair"
}