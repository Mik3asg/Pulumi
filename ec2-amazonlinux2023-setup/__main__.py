import pulumi
import pulumi_aws as aws

# Amazon Linux 2023 in region eu-west-2
ami_id = 'ami-0b31d93fb777b6ae6'

## Create a Security Group that allows HTTP and SSH access
#sec_group = aws.ec2.SecurityGroup('web-secgrp',
#    description="Allow HTTP and SSH",
#    ingress=[
#        {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]},
#        {"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]}
#    ],
#    egress=[
#        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}
#    ]
#)

# Use the existing security group ID
existing_sec_group_id = 'sg-0db88f78fb2f11b68'

# Create two EC2 instances using the default VPC and existing SSH key pair
instances = []
for i in range(2):
    instance = aws.ec2.Instance(f'web-instance-{i}',
        instance_type="t2.micro",
        ami=ami_id,
        key_name="ec2-london-ssh",  # Specify your existing key pair name
#        vpc_security_group_ids=[sec_group.id],  # Use the security group we just created
        vpc_security_group_ids=[existing_sec_group_id],  # Reference the existing security group
        tags={
            "Name": f"web-instance-{i}"
        }
    )
    instances.append(instance)

# Export the public IPs of the instances
pulumi.export("instance_ips", [instance.public_ip for instance in instances])
