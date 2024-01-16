resource "openstack_compute_secgroup_v2" "default" {
  name = "default"
  description = "Default security group"

  lifecycle {
    prevent_destroy = true
  }
}

resource "openstack_networking_secgroup_rule_v2" "secgroup_rule" {
  direction         = "ingress"
  ethertype         = "IPv4"
  port_range_min    = 0
  port_range_max    = 0
  security_group_id = openstack_compute_secgroup_v2.default.id
}

resource "openstack_networking_secgroup_rule_v2" "ssh_ipv4" {
  direction         = "ingress"
  ethertype         = "IPv4"
  port_range_min    = 22
  port_range_max    = 22
  protocol          = "tcp"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_compute_secgroup_v2.default.id
}

resource "openstack_networking_secgroup_rule_v2" "ssh_ipv6" {
  direction         = "ingress"
  ethertype         = "IPv6"
  port_range_min    = 22
  port_range_max    = 22
  protocol          = "tcp"
  remote_ip_prefix  = "::/0"
  security_group_id = openstack_compute_secgroup_v2.default.id
}

resource "openstack_networking_secgroup_rule_v2" "icmp_ipv4" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "icmp"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_compute_secgroup_v2.default.id
}

resource "openstack_networking_secgroup_rule_v2" "icmp_ipv6" {
  direction         = "ingress"
  ethertype         = "IPv6"
  protocol          = "icmp"
  remote_ip_prefix  = "::/0"
  security_group_id = openstack_compute_secgroup_v2.default.id
}

resource "openstack_networking_secgroup_rule_v2" "swarm_one" {
  direction         = "ingress"
  ethertype         = "IPv4"
  port_range_min    = 2376
  port_range_max    = 2376
  protocol          = "tcp"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_compute_secgroup_v2.default.id
}

resource "openstack_networking_secgroup_rule_v2" "swarm_two" {
  direction         = "ingress"
  ethertype         = "IPv4"
  port_range_min    = 2377
  port_range_max    = 2377
  protocol          = "tcp"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_compute_secgroup_v2.default.id
}

resource "openstack_networking_secgroup_rule_v2" "visualization" {
  direction         = "ingress"
  ethertype         = "IPv4"
  port_range_min    = 5000
  port_range_max    = 5000
  protocol          = "tcp"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_compute_secgroup_v2.default.id
}

resource "openstack_networking_secgroup_rule_v2" "webapp" {
  direction         = "ingress"
  ethertype         = "IPv4"
  port_range_min    = 8000
  port_range_max    = 8000
  protocol          = "tcp"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_compute_secgroup_v2.default.id
}

resource "openstack_networking_secgroup_rule_v2" "redis" {
  direction         = "ingress"
  ethertype         = "IPv4"
  port_range_min    = 6379
  port_range_max    = 6379
  protocol          = "tcp"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_compute_secgroup_v2.default.id
}