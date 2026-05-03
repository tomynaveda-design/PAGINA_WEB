# 🚗 API Sistema Estacionamiento Autónomo

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)

## 📝 Descripción
Este proyecto consiste en una **API RESTful** robusta diseñada para la gestión integral de un estacionamiento inteligente. La solución permite el control automatizado de vehículos, la administración de espacios en tiempo real y un sistema de tarificación dinámica basado en el tiempo de permanencia.

Desarrollada bajo estándares modernos, la API asegura la integridad de los datos mediante un ORM y facilita la configuración segura a través de variables de entorno.

---

## 👥 Integrantes
*   **Claudio Pérez**
*   **Tomás Naveda**

---

## 🛠️ Tecnologías Utilizadas
*   **Lenguaje:** Python 3.13
*   **Framework:** Flask
*   **Base de Datos:** MySQL
*   **ORM:** SQLAlchemy
*   **Gestión de Entorno:** Python-dotenv (`.env`)

---

## 🚀 Características Principales
- ✅ **Gestión de Disponibilidad:** Listado de cocheras con actualización de estado automático (Libre/Ocupado).
- ⏱️ **Cálculo de Tarifas:** Sistema que determina el monto a pagar basándose en la diferencia entre la hora de ingreso y egreso.
- 🛡️ **Validaciones Inteligentes:** Bloqueo de doble ingreso para evitar que un mismo vehículo ocupe dos lugares simultáneamente.
- ⚙️ **Configuración Segura:** Uso de archivos `.env` para proteger las credenciales de acceso a la base de datos.

---

## 🛣️ Endpoints Implementados

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| **GET** | `/espacios` | Lista todas las cocheras y su disponibilidad actual. |
| **POST** | `/ingreso` | Registra la entrada de un vehículo y ocupa un espacio. |
| **POST** | `/egreso/<id>` | Registra la salida, libera el lugar y devuelve el total a pagar. |

---

## 💻 Cómo Ejecutar el Proyecto

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repo>

2. **Configurar el entorno:**

Crear un archivo .env en la raíz.
Definir DATABASE_URL, FLASK_PORT y TARIF_POR_HORA.

3. **Instalar Dependencias**

pip install flask flask-sqlalchemy pymysql python-dotenv

4. **Lanzar la API**

python app.py

🌟 Aporte Individual
Como parte de la modalidad colaborativa en Git, se trabajó en ramas independientes (feature/):

Desarrollo de Modelos: Diseño de la arquitectura de tablas y relaciones en la DB.

Lógica de Negocio: Implementación de validaciones de ingreso y algoritmos de cobro.

Infraestructura: Configuración de entorno y depuración de conexión MySQL.
