data "aws_key_pair" "selected" {
  key_name = var.aws.key_name
}


data "aws_ami" "amazon_linux" {
  most_recent = true

  filter {
    name   = "image-id"
    values = ["ami-0e731c8a588258d0d"]
  }

  owners = ["amazon"]
}

data "cloudinit_config" "mongosync" {
  for_each      = var.source_shard_ids
  gzip          = false
  base64_encode = false
  part {
    filename     = "migration-host-cloud-init.yaml"
    content_type = "text/cloud-config"

    content = templatefile("./scripts/migration-host-cloud-init.yaml", { source_conn_string = var.mongosync_config.source_conn_string, target_conn_string = var.mongosync_config.target_conn_string, mongosync_version = var.mongosync_config.version, shard_id = each.key, features = var.mongosync_config.features })
  }
}

resource "aws_instance" "mighost" {
  for_each               = data.cloudinit_config.mongosync
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.aws.instance_type
  key_name               = data.aws_key_pair.selected.key_name
  subnet_id              = data.aws_subnet.selected.id
  vpc_security_group_ids = [data.aws_security_group.selected.id]
  tags                   = merge({ "Name" : "mighost-${each.key}" }, var.aws.tags)
  user_data              = each.value.rendered
}
