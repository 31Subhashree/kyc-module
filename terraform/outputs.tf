output "rds_endpoint" {
  value = aws_db_instance.mysql_db.endpoint
  description = "RDS MySQL instance endpoint"
}
