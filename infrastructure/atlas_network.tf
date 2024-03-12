data "aws_vpc" "selected" {
  id = data.aws_security_group.selected.vpc_id
}

data "aws_subnet" "selected" {
  id = var.aws.subnet_id
}

data "aws_security_group" "selected" {
  name = var.aws.sg_name
}

resource "mongodbatlas_privatelink_endpoint" "aws_app" {
  project_id    = var.atlas.project_id
  provider_name = "AWS"
  region        = var.aws.region
}

resource "mongodbatlas_privatelink_endpoint_service" "aws_app" {
  project_id          = mongodbatlas_privatelink_endpoint.aws_app.project_id
  private_link_id     = mongodbatlas_privatelink_endpoint.aws_app.id
  endpoint_service_id = aws_vpc_endpoint.atlas_interface.id
  provider_name       = "AWS"
}

resource "aws_vpc_endpoint" "atlas_interface" {
  vpc_id             = data.aws_vpc.selected.id
  service_name       = mongodbatlas_privatelink_endpoint.aws_app.endpoint_service_name
  vpc_endpoint_type  = "Interface"
  subnet_ids         = [data.aws_subnet.selected.id]
  security_group_ids = [data.aws_security_group.selected.id]
  tags               = var.aws.tags
}
