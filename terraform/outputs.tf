output "db_endpoint" {
  value = aws_db_instance.kyc_db.endpoint
}

output "instance_public_ip" {
  value = aws_instance.backend.public_ip
}
