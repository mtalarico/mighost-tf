variable "local_ips" {
  type = list(string)
}

variable "aws" {
  type = object({
    sg_name       = string
    subnet_id     = string
    key_name      = string
    region        = string
    instance_type = string
    tags = object({
      owner       = string
      expire      = string
      description = string
    })
  })
}

variable "mongosync_config" {
  type = object({
    source_conn_string = string
    target_conn_string = string
    version            = string
    features           = string
  })
}

variable "source_shard_ids" {
  type        = set(string)
  description = "source shards to launch a mongosync process against, name **must** be id (sh.status() or config.shards)"
  default     = [""] # will only launch 1 mongosync with no --id if no shard map is provided
}

variable "atlas" {
  type = object({
    public_key  = string
    private_key = string
    project_id  = string
  })
}
