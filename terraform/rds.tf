resource "aws_security_group" "mysql_sg" {
  name        = "mysql_security_group"
  description = "Allow MySQL access"

  ingress {
    from_port   = 3306
    to_port     = 3306
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

resource "aws_security_group" "eb_sg" {
  name        = "elastic_beanstalk_sg"
  description = "Allow EB access to RDS"

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.mysql_sg.id] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_db_instance" "mysql_db" {
  allocated_storage                   = 20
  storage_type                        = "gp2"
  engine                              = "mysql"
  engine_version                      = "8.0.36"  
  instance_class                      = "db.t3.micro"  
  db_name                             = "mydb"
  username                            = "admin"
  password                            = "Secure0987Subh"  
  publicly_accessible                 = false
  vpc_security_group_ids              = [aws_security_group.mysql_sg.id, aws_security_group.eb_sg.id]
  multi_az                            = false
  backup_retention_period             = 7
  skip_final_snapshot                 = true
}

# Create an IAM Policy for RDS IAM Authentication
resource "aws_iam_policy" "rds_iam_auth" {
  name        = "RDSIAMAuthPolicy"
  description = "Allows IAM authentication for RDS MySQL"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = "rds-db:connect",
      Resource = "arn:aws:rds-db:${var.aws_region}:${var.aws_account_id}:dbuser/${aws_db_instance.mysql_db.resource_id}/admin"
    }]
  })
}

resource "aws_iam_role" "app_role" {
  name               = "rds-app-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

# Attach Policy to an IAM Role (for EC2, Lambda, or any other AWS service needing access)
resource "aws_iam_role_policy_attachment" "rds_iam_auth_attach" {
  role       = aws_iam_role.app_role.name  
  policy_arn = aws_iam_policy.rds_iam_auth.arn
}

# Create an Elastic Beanstalk Application
resource "aws_elastic_beanstalk_application" "fastapi_app" {
  name        = "fastapi-app"
  description = "FastAPI application deployed on AWS Elastic Beanstalk"
}

# Create an Elastic Beanstalk Environment
resource "aws_elastic_beanstalk_environment" "fastapi_env" {
  name                = "fastapi-env"
  application         = aws_elastic_beanstalk_application.fastapi_app.name
  solution_stack_name = "64bit Amazon Linux 2 v3.7.8 running Python 3.8"

# IAM Role for EC2 Instances
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "aws-elasticbeanstalk-ec2-profile"
  }

  # Database Connection String
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DATABASE_URL"
    value     = "mysql://admin:${aws_db_instance.mysql_db.endpoint}/mydb"
  }

  # Optional: Store DB Password Securely
#   setting {
#     namespace = "aws:elasticbeanstalk:application:environment"
#     name      = "DB_PASSWORD"
#     value     = var.db_password
#   }
  }
