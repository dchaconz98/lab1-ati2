# Lab 1 ATI-2

## Setup ambiente de desarrollo
Estas son las dependencias que tienen que tener instaladas en su sistema operativo para levantar el ambiente de desarrollo
1. docker
2. docker-compose

En la carpeta del repositorio, correr los siguientes comandos

Descargar las imágenes de docker

```bash
docker-compose -f local.yml pull postgres
DOCKER_BUILDKIT=1 docker-compose -f local.yml build django
```

Si estas utilizando Linux poner esto en tu `.bashrc` o `.zhsrc`, se necesita para los permisos de archivos

```bash
export UID=$(id -u)
export GID=$(id -g)
```

Activar servicio de base de datos
```bash
docker-compose -f local.yml up -d postgres
```

Crear entorno virtual de python y descargar dependencias, al final te pedirá credenciales, estas son para el usuario administrador

Pon las siguiente

- Username: admin
- Email: dev@dev
- Password: dev123456

```bash
docker-compose -f local.yml run -w /app --entrypoint bash --rm django setup_dev.sh
```

Iniciar servicios de docker

```bash
docker-compose -f local.yml up -d
```
Visitar `127.0.0.1:8000`

El ultimo comando es el comando que tienes que ejecutar para levantar el ambiente de desarrollo.

## Comandos basicos para el desarrollo

Ver los logs de django
```bash
docker-compose -f local.yml logs --no-log-prefix -f django
```

Iniciar una terminal interactiva en el contenedor de docker
```bash
docker-compose run --rm --no-deps -w /app --entrypoint "bash -c 'source .venv/bin/activate && bash'" django
```
Lo anterior sirve para correr cualquier comando que utilice las dependencias del entorno virtual como por ejemplo

```bash
python manage.py makemigrations
```
### Creación de usuarios

Cuando creas un usuario en http://127.0.0.1:8000/accounts/signup/, mandara un email de confirmación de cuenta, el email lo encontraras en los logs de django

```bash
docker-compose -f local.yml logs -f django
```
### Comandos handy y aliases
Estos comandos ubicados en `dev.sh` son de bastante utilidad, solo sirve si utilizas Linux o el subsistema de Linux de Windows

Para activarlos

```bash
source dev.sh
```

Por ejemplo, para activar el server de django

```bash
runserver
```

Para hacer cosas que necesiten del entorno virtual en una terminal interactiva

```bash
dockerpy bash
```

## Base de datos

### Borrar base de datos
Si necesitas borrar la base de datos o hacerle un reset, ejectuar los comandos en `commands/resetdb.sh`

```bash
bash commands/resetdb.sh
```
## Traducciones

Las traducciones se guardan en el directorio `locale/es/LC_MESSAGES/django.po`

Para que puedas ver las traducciones, hay que compilar el archivo `.po`

En una terminal interactiva en el contenedor de docker ejecutar

```bash
django-admin compilemessages
```

Para obtener los strings nuevos que marcaste como traducibles

```bash
django-admin makemessages -l en
```

El último Generara el message file o archivo `.po`

Para mayor documentación sobre las traducciones de django, visitar

https://docs.djangoproject.com/en/4.0/topics/i18n/translation/

## Documentacion adicional
Este repositorio esta basado en [django-cookie-cutter](https://cookiecutter-django.readthedocs.io/en/latest/)
