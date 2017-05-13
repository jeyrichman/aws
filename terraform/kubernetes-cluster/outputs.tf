output "address" {
        value = "${aws_instance.k8s_master.public_dns}"
}
