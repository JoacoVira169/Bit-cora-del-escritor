# Diario Personal con Reconocimiento de Voz

Este es un proyecto de diario personal basado en la web que permite a los usuarios registrarse, iniciar sesión y administrar sus notas o "tarjetas". Una característica clave es la capacidad de agregar texto a las notas mediante el reconocimiento de voz.

## Comenzando 🚀

Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.

### Pre-requisitos 📋

Necesitarás tener instalado `pipenv` para manejar las dependencias del proyecto. Si no lo tienes, puedes instalarlo con pip:

```
pip install pipenv
```

### Instalación 🔧

1.  Clona este repositorio en tu máquina local.
2.  Abre una terminal en el directorio del proyecto.
3.  Instala las dependencias usando `pipenv`:

    ```
    pipenv install
    ```
4.  Activa el entorno virtual de `pipenv`:

    ```
    pipenv shell
    ```
5.  Ejecuta la aplicación:
    ```
    python main.py
    ```
La aplicación estará disponible en `http://127.0.0.1:5000`.

## Ejecutando las pruebas ⚙️

Este proyecto no incluye un conjunto de pruebas automatizadas en este momento.

## Construido con 🛠️

*   [Flask](https://flask.palletsprojects.com/) - El framework web usado.
*   [SQLAlchemy](https://www.sqlalchemy.org/) - El kit de herramientas SQL de Python y mapeador relacional de objetos.
*   [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - Extensión de Flask para el soporte de SQLAlchemy.
*   [speech](https://pypi.org/project/speech/) - Biblioteca para el reconocimiento de voz.

## Autores ✒️

*   **Joaquín** - *Trabajo Inicial*

## Agradecimiento

Muchas gracias al profesor Beker Martínez por la ayuda y la formación que me ha proporcionado para que el proyecto sea posible y a la academia de Kodland.
