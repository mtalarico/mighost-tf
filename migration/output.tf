output "ec2_ips" {
  value = [
    for each in aws_instance.mighost : each.public_ip
  ]
}
