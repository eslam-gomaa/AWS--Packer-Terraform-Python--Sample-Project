
resource "aws_instance" "Bastion_Host" {
  ami             = var.ami
  key_name        = var.key_pair_name
  instance_type   = "t2.micro" #var.instance_type
  subnet_id       = element(aws_subnet.public.*.id, 0)
  security_groups = [aws_security_group.Public_Security_Group.id]
  tags = {
    Name = "Public Host - Testing"
  }
}

//data "aws_lb" "elb" {
//  arn  = aws_elb.terraform-elb.arn
//}
//
//resource "aws_instance" "Private_Host" {
//  ami             = var.ami
//  key_name        = var.key_pair_name
//  instance_type   = var.instance_type
//  subnet_id       = element(aws_subnet.private.*.id, 0)
//  security_groups = [aws_security_group.Private_Security_Group.id]
//  depends_on = [aws_elb.terraform-elb]
//  tags = {
//    Name = "Private Host - Testing"
//  }
//  user_data = <<EOF
//#!/bin/bash -x
//cd /home/ec2-user
//# Changing the LB URL
//sudo python3 docker-compose-replace-url.py ${data.aws_lb.elb.dns_name}
//
//chmod +x /etc/rc.local
//cat << EOD >> /etc/rc.local
//cd /home/ec2-user && sudo docker-compose up
//EOD
//
//sudo docker-compose up
//EOF
//}
