# AWS--Packer-Terraform-Python--Sample-Project
A Sample Project on AWS That utilized Packer, Terraform, Ansible and Python

## Task:
The attached code does the following:

1. Creates an AMI image with Packer
2. Builds an infrastructure with Terraform (VPC, EC2, ALB, ASG, etc...)
3. Deployes a sample app with Ansible & Docker-compose

---

## Usage

```bash
chmod +x build.py

# You can place the credentials in "aws credentials file"
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_DEFAULT_REGION="us-east-1" # Changing the Region might require changing the ami that Packer uses

./build.py
```

---


## Example

![image](https://user-images.githubusercontent.com/33789516/135709021-9567628a-5e52-4d21-a0b1-8dfc362cffe8.png)


---

Thank you

[Eslam Gomaa](https://www.linkedin.com/in/eslam-gomaa/)
