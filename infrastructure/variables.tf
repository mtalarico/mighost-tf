variable "local_ips" {
  type = list(string)
}

variable "aws" {
  type = object({
    sg_name   = string
    subnet_id = string
    region    = string
    tags = object({
      owner       = string
      expire      = string
      description = string
    })
  })
}

variable "atlas" {
  type = object({
    public_key  = string
    private_key = string
    project_id  = string
  })
}
