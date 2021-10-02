
variable "region" {
  type = string
  default = "us-east-2"
}

variable "vpcCidrBlock" {
  type = string
  default = "10.0.0.0/16"
}

variable "private_subnet" {
  type = list
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnet" {
  type = list
  default = ["10.0.4.0/24", "10.0.5.0/24"]
}

variable "ssh_ingress_cidrBlock" {
  type   = list
  default = ["0.0.0.0/0"]
}

variable "instance_type" {
  type    = string
  default = "t2.medium"  # t2.micro & t2.small are NOT enough for gitlab, 't2.medium' worked well.
}


variable "ami" {
    type    = string
  default = "ami-0e19bba4805a5e822"
}

variable "key_pair_name" {
    type    = string
    default = "testing1"
}