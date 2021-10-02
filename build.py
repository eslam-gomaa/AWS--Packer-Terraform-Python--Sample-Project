#!/usr/bin/python
import os
import re
import json
import time
import sys
from datetime import datetime


class bcolors:
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def runcommand(cmd):
    """
    function to execute shell commands and returns a dic of
    """
    import subprocess

    info = {}
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    # print(std_out.encode('utf-8').decode('cp1252'))
    info['cmd'] = cmd
    info['rc'] = proc.returncode
    info['stdout'] = std_out.rstrip()
    info['stderr'] = std_err.rstrip()
    ## Python's rstrip() method
    # strips all kinds of trailing whitespace by default, not just one newline
    return info



###################################################################
# Main Variables
###################################################################

packer_file = './packer.json'
packer_var_file = './variables.json'
check_aws_credential_file = True

###################################################################
# Set AK/SK Environment variables  [ Setting them here for testing ]
###################################################################

if check_aws_credential_file:
    aws_cred_file = '~/.aws/credentials'
    if os.path.isfile(os.path.expanduser(aws_cred_file)):
        cred_file = open(os.path.expanduser(aws_cred_file), "r")
        cred_read = cred_file.read()
        ak_sk = re.findall("aws_access_key_id =\s\D|aws_secret_access_key =\s\D|aws_default_region =\s\D", cred_read)
        if len(ak_sk) < 3:
            print(bcolors.OKGREEN + "[ INFO ] " + bcolors.ENDC + "Seems that aws credentials file is missing something.\n\t Available parameters: {}".format(ak_sk))
            print(bcolors.OKGREEN + "[ INFO ] " + bcolors.ENDC + "Checking the ENV ..")
missing_env = []
for env in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", 'AWS_DEFAULT_REGION']:
    if not env in os.environ:
        missing_env.append(env)
        if len(missing_env) > 1:
            print(
                bcolors.FAIL + "[ ERROR ] " + bcolors.ENDC + "The following ENV are/is missing:  >> {} <<".format(
                    missing_env))
            print("\t --> Make sure to set the following Environment variables:")
            print(
                "export AWS_ACCESS_KEY_ID=''\nexport AWS_SECRET_ACCESS_KEY=''\nexport AWS_DEFAULT_REGION=''")
            exit(1)


###

# Create dir for output
now = datetime.now()
output_dir = now.strftime("%d-%m-%Y_%H-%M-%S")
if not os.path.isdir('./output'):
    os.mkdir('./output')
os.mkdir("./output/{}".format(output_dir))

###################################################################
# Packer
###################################################################

print("")
print(bcolors.WARNING + "[ INFO ] " + bcolors.ENDC + "STAGE 1  **************** Packer ****************")
print("")

# packer validate
# check_packer_syntax = runcommand("./packer validate -var-file={} {}".format(packer_var_file, packer_file))
check_packer_syntax = runcommand("packer validate -var-file={} {}".format(packer_var_file, packer_file))
if check_packer_syntax['rc'] != 0:
    print(bcolors.FAIL + "[ ERROR ] " + bcolors.ENDC + "Invalid Packer Syntax \n \t--> {}".format(
        check_packer_syntax['stdout']))
    print("\t--> {}".format(check_packer_syntax['stderr']))
    exit(1)

# packer build
print(bcolors.OKGREEN + "[ INFO ] " + bcolors.ENDC + "Building the AMI with Packer, might take some time ...")
run_packer = runcommand("packer build -var-file={} {}".format(packer_var_file, packer_file))
packer_out_file = './output/{}/packer_output.txt'.format(output_dir)
packer_out = open(packer_out_file, 'w')
packer_out.write(run_packer['stdout'])
packer_out.close()

if run_packer['rc'] != 0:
    print(bcolors.FAIL + "[ ERROR ] " + bcolors.ENDC + "Failed to run 'Packer build ...")
    print("\t --> Full Packer Output: ({})".format(packer_out_file))
    exit(1)
print(bcolors.OKGREEN + "[ INFO ] " + bcolors.ENDC + bcolors.OKGREEN + "Packer build done successfully" + bcolors.ENDC)
print(bcolors.OKGREEN + "[ INFO ] " + bcolors.ENDC + "Packer output saved in: ({})".format(packer_out_file))

# Getting the AMI ID
ami_search = re.findall('ami.*', run_packer['stdout'])  # Saving the AMI_ID to a variable, to pass to next STAGE
if len(ami_search) < 1:
    print(bcolors.FAIL + "[ ERROR ] " + bcolors.ENDC + "Failed to get AMI_ID; Exiting")
    exit(1)
ami = ami_search[-1].rstrip()
print(
    bcolors.OKGREEN + "[ INFO ] " + bcolors.ENDC + "AMI Created successfully\n \t --> AMI ID: " + bcolors.OKBLUE + "{}".format(
        ami) + bcolors.ENDC)

save_ami = open('ami.txt','w')
save_ami.write(ami)
save_ami.close()


###################################################################
# Terraform
###################################################################

print("")
print(bcolors.WARNING + "[ INFO ] " + bcolors.ENDC + "STAGE 2  **************** Terraform ****************")
print("")

# Build with Terraform
print(bcolors.OKGREEN + "[ INFO ] " + bcolors.ENDC + "Building the Infrastructure with Terraform, might take some time ...")
run_terraform = runcommand("terraform apply -var='ami={}' -auto-approve".format(ami))
terraform_out_file = './output/{}/terraform_output.txt'.format(output_dir)
terraform_out = open(terraform_out_file, 'w')
terraform_out.write(run_terraform['stdout'])
terraform_out.close()

if run_terraform['rc'] != 0:
    print(bcolors.FAIL + "[ ERROR ] " + bcolors.ENDC + "Failed to run 'terraform apply ...")
    print("\t --> Full Terraform Output: ({})".format(terraform_out_file))
    exit(1)
print(bcolors.OKGREEN + "[ INFO ] " + bcolors.ENDC + bcolors.OKGREEN + "Terraform build done successfully" + bcolors.ENDC)
print(bcolors.OKGREEN + "[ INFO ] " + bcolors.ENDC + "Terraform output saved in: ({})".format(terraform_out_file))

print("")
print(bcolors.OKGREEN +  "\t\t\t********** Task Done **********" + bcolors.ENDC)
print("")
lb_dns_name = runcommand("terraform output elb_dns_name")
print("ELB URL: {}".format(lb_dns_name['stdout']))
print("")
print("\t\tTo Destroy:")
print("\t\t-----------")
print(bcolors.WARNING + "\t terraform destroy -var='ami=${cat ami.txt}' -auto-approve" + bcolors.ENDC)

aws_cli_version = runcommand("aws --version")
if aws_cli_version['rc'] == 0:
    desc_ami = runcommand("aws ec2 describe-images --image-id {}".format(ami))
    ami_snapshot_json = json.loads(desc_ami['stdout'])
    snap_id = None
    for i in ami_snapshot_json['Images']:
        if i['ImageId'] == ami:
            snap_id = i['BlockDeviceMappings'][0]['Ebs']['SnapshotId']

    print(bcolors.WARNING + "\t aws ec2 deregister-image --image-id {}".format(ami) + bcolors.ENDC)
    print(bcolors.WARNING + "\t aws ec2 delete-snapshot --snapshot-id {}".format(snap_id) + bcolors.ENDC)
else:
    print(bcolors.WARNING + "[ WARN ] aws-cli is NOT installed, Install if u want to print the image delete command" + bcolors.ENDC)
