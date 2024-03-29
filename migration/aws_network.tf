

data "aws_vpc" "selected" {
  id = data.aws_security_group.selected.vpc_id
}

data "aws_subnet" "selected" {
  id = var.aws.subnet_id
}

data "aws_security_group" "selected" {
  name = var.aws.sg_name
}

resource "aws_vpc_security_group_ingress_rule" "local_ssh" {
  security_group_id = data.aws_security_group.selected.id

  for_each = toset(var.local_ips)

  cidr_ipv4   = each.key
  from_port   = 22
  to_port     = 22
  ip_protocol = "TCP"
}

resource "aws_vpc_security_group_ingress_rule" "local_mongosync_api" {
  security_group_id = data.aws_security_group.selected.id

  for_each = toset(var.local_ips)

  cidr_ipv4   = each.key
  from_port   = 27182
  to_port     = 27182
  ip_protocol = "TCP"
}
