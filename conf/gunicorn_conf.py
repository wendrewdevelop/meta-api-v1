workers = 3  # Adjust the number of workers based on your server's resources
bind = "api.metasolucoesambientais.com.br"
chdir = "/root/meta-api-v1"  # Path to your Django project directory
module = "meta-api-v1.meta.wsgi:application"  # Adjust 'your_project' to match your Django project's name
