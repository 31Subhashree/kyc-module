provider "aws" {
  region = var.region
}

resource "aws_db_instance" "kyc_db" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "15.2"
  instance_class       = "db.t3.micro"
  db_name              = "kyc"
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.postgres15"
  skip_final_snapshot  = true
}

resource "aws_instance" "backend" {
  ami           = var.ami_id
  instance_type = "t2.micro"
  key_name      = var.key_name
  security_groups = [aws_security_group.backend_sg.name]

  tags = {
    Name = "KYC-Backend"
  }
}

resource "aws_security_group" "backend_sg" {
  name_prefix = "backend-sg-"
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
