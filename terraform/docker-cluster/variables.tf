variable "public_key_path" {
  description = <<EOF
Path to the SSH public key to be used for authentication.
Ensure this keypair is added to your local SSH agent so provisioners can
connect.
Example: ~/.ssh/terraform.pub
  EOF
}

variable "key_name" {
  description = "deploy-key"
}

variable "aws_region" {
  description = "AWS region to launch servers."
  default     = "us-east-1"
}

variable "aws_amis" {
  default = {
    us-east-1 = "ami-772aa961"
  }
}
