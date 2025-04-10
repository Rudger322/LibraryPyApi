# Указываем провайдера (в данном случае AWS)
provider "aws" {
  region = "us-east-1"  # Регион, где будет сервер*
}

# Создаём виртуальную машину (EC2 instance)
resource "aws_instance" "my_server" {
  ami           = "ami-0c55b159cbfafe1f0"  # ID образа операционной системы (например, Ubuntu)*
  instance_type = "t2.micro"               # Тип сервера (маленький и дешёвый)*
  tags = {
    Name = "MyFirstServer"                 # Имя для удобства*
  }
}