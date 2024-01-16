resource "openstack_compute_instance_v2" "client_vm" {
  name = "Client_VM"
  image_name = "Ubuntu 20.04"
  flavor_name = "m1.small"

  key_pair = openstack_compute_keypair_v2.keypair.name

  security_groups = [ data.openstack_networking_secgroup_v2.default.name ]

  depends_on = [ openstack_compute_keypair_v2.keypair ]
}

resource "null_resource" "client_vm_provision" {

  depends_on = [ openstack_compute_instance_v2.client_vm ]

  connection {
    type = "ssh"
    user = "ubuntu"
    host = openstack_compute_instance_v2.client_vm.access_ip_v6
    private_key = openstack_compute_keypair_v2.keypair.private_key
    agent = false
  }

  provisioner "remote-exec" {
    inline = [ 
      "sudo apt-get -y install software-properties-common",
      "sudo apt-add-repository universe",
      "sudo apt-get -y update",
      "sudo apt-get -y install python3-pip",
      "pip install requests",
      "wget https://raw.githubusercontent.com/zhijiewang22/ECE422-Proj2-StartKit/master/http_client.py",
      # "python3 http_client.py ${openstack_compute_instance_v2.swarm_manager_vm.access_ip_v4} 1 1 &"
     ]
  }
}

resource "openstack_compute_instance_v2" "swarm_manager_vm" {
  name = "Swarm_Manager_VM"
  image_name = "Ubuntu 20.04"
  flavor_name = "m1.small"

  key_pair = openstack_compute_keypair_v2.keypair.name

  security_groups = [ data.openstack_networking_secgroup_v2.default.name ]

  depends_on = [ openstack_compute_keypair_v2.keypair ]
}

resource "null_resource" "swarm_manager_vm_provision" {

  depends_on = [ openstack_compute_instance_v2.swarm_manager_vm ]

  connection {
    type = "ssh"
    user = "ubuntu"
    host = openstack_compute_instance_v2.swarm_manager_vm.access_ip_v6
    private_key = openstack_compute_keypair_v2.keypair.private_key
    agent = false
  }

  provisioner "remote-exec" {
    inline = [ 
      "sudo apt-get -y update",
      "curl -fsSL https://get.docker.com -o get-docker.sh",
      "sudo sh ./get-docker.sh",
      "sudo docker swarm init",
      "wget https://raw.githubusercontent.com/zhijiewang22/ECE422-Proj2-StartKit/master/docker-compose.yml",
      "sudo docker stack deploy --compose-file docker-compose.yml app_name"
    ]
  }
}

resource "openstack_compute_instance_v2" "swarm_node_vm" {
  name = "Swarm_Node_VM"
  image_name = "Ubuntu 20.04"
  flavor_name = "m1.small"

  key_pair = openstack_compute_keypair_v2.keypair.name

  security_groups = [ data.openstack_networking_secgroup_v2.default.name ]

  depends_on = [ openstack_compute_keypair_v2.keypair ]
}

resource "null_resource" "swarm_node_vm_provision" {

  depends_on = [ openstack_compute_instance_v2.swarm_node_vm ]

  connection {
    type = "ssh"
    user = "ubuntu"
    host = openstack_compute_instance_v2.swarm_node_vm.access_ip_v6
    private_key = openstack_compute_keypair_v2.keypair.private_key
    agent = false
  }

  provisioner "remote-exec" {
    inline = [ 
      "sudo apt-get -y update",
      "curl -fsSL https://get.docker.com -o get-docker.sh",
      "sudo sh ./get-docker.sh",
    ]
  }

}

resource "openstack_compute_keypair_v2" "keypair" {
  name = "instance-keypair"
}

variable "private_key_path" {
  type = string
}