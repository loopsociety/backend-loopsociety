# LoopSociety API

API del foro colaborativo de la comunidad LoopSociety, desarrollada en FastAPI con SQLModel y MySQL. Este repositorio está diseñado para ser limpio, escalable y mantener prácticas profesionales de desarrollo colaborativo, incluyendo Alembic para migraciones, autenticación JWT, OAuth2 y código modular.

---

## ⚙️ Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [MySQL](https://www.mysql.com/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Docker](https://www.docker.com/)
- [JWT](https://jwt.io/)
- Python 3.10+

---

## 🚀 Estado del proyecto

> Este proyecto aún está en desarrollo. Se están construyendo los endpoints principales y las funcionalidades base para luego avanzar con las colaboraciones del equipo.

---

## 🧪 Cómo ejecutar localmente

1. Clona el repositorio:

```bash
git clone https://github.com/loopsociety/loopsociety-api.git
cd loopsociety-api
```

## 🐳 Uso de Docker Compose y Devcontainer

Este proyecto soporta dos formas principales de desarrollo con Docker: usando **Docker Compose** directamente o usando el entorno de desarrollo remoto de **Devcontainer** en VS Code. Ambas opciones aíslan las dependencias y facilitan la colaboración.

---

### 🚀 Opción 1: Usar Docker Compose

1. **Copia el archivo `.env` y edítalo** con tus credenciales de base de datos y variables necesarias.  
   Un ejemplo de archivo `.env` para usar Docker Compose es:

   ```env
   DATABASE_URL=mysql+pymysql://user:password@db:3306/loopsociety
   SECRET_KEY=supersecret
   MYSQL_USER=user
   MYSQL_ROOT_PASSWORD=password
   MYSQL_PASSWORD=password
   MYSQL_DATABASE=loopsociety
   ```

   > **Nota:**  
   > Si solo quieres usar el servicio de base de datos (`db`) de Docker y correr FastAPI localmente (fuera de Docker), cambia `db` por `localhost` en la variable `DATABASE_URL`:
   > ```
   > DATABASE_URL=mysql+pymysql://user:password@localhost:3306/loopsociety
   > ```

2. **Levanta los servicios** (FastAPI y MySQL):

   ```bash
   docker-compose up --build
   ```

   Esto construirá la imagen, instalará dependencias y levantará la base de datos y la app.

3. **Accede a la API** en [http://localhost:8000](http://localhost:8000).

4. **Detén los servicios** con:

   ```bash
   docker-compose down
   ```

---

### 💻 Opción 2: Usar Devcontainer en VS Code

El devcontainer te permite desarrollar dentro de un contenedor con todas las herramientas y extensiones configuradas automáticamente.

1. **Abre el proyecto en VS Code**.

2. Si tienes la extensión [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) instalada, haz clic en la esquina inferior izquierda (><) y selecciona:

   ```
   Reopen in Container
   ```

   VS Code construirá el contenedor usando la configuración de `.devcontainer/`.

3. **¡Listo!**  
   El servidor FastAPI y las migraciones se ejecutan automáticamente al iniciar el contenedor.  
   Solo tienes que abrir [http://localhost:8000](http://localhost:8000) en tu navegador para acceder a la API.

   > **Tip:**  
   > El servidor FastAPI se ejecuta con la opción `--reload`, lo que significa que cualquier cambio en el código fuente se reflejará automáticamente sin necesidad de reiniciar el contenedor.

---

## 🐳 Debuguear FastAPI dentro del Devcontainer

1. **Abre el proyecto en VS Code** y selecciona "Reopen in Container" si se te solicita.
2. **Asegúrate de que el contenedor esté corriendo** (puedes usar `docker-compose up` o el botón de VS Code).
3. **Abre la pestaña "Run and Debug"** (Ctrl+Shift+D).
4. **Selecciona la configuración** `"Debugger: FastAPI in container (Port 5678)"`.
5. **Haz clic en "Run" (F5)** o presiona F5 para iniciar la depuración.
6. **Coloca breakpoints** en tu código Python y navega a [http://localhost:5678/docs](http://localhost:5678/docs) para probar tu API en modo debug.

> **Nota:**  
> Si el contenedor ya está ejecutando Uvicorn por defecto (por el `CMD` del Dockerfile), detén ese proceso antes de lanzar el debugger desde VS Code para evitar conflictos de puertos.  
> El puerto 5678 está expuesto en `docker-compose.yml` para permitir la depuración remota.

---

## 🛠️ ¿Cómo colaborar?
1. Crea una rama nueva:

```bash
git checkout -b feature/mi-nueva-funcion
```

2. Haz tus cambios siguiendo las reglas:

**✅ Reglas para Pull Requests**
- Usa convenciones de commits (feat:, fix:, refactor:, docs:).
- Sigue la estructura de carpetas.
- Escribe PRs claros con propósito, descripción y capturas si aplica.

3. Añade tus cambios:

```bash
git add .
git commit -m "feat: added login endpoint"
```
4. Actualiza tu fork con el último estado del proyecto:

```bash
git pull origin main --rebase
```

5. Envía tu PR:

```bash
git push origin feature/mi-nueva-funcion
```

---

## ✨ Convenciones de commits

Utilizamos [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):
```vbnet
feat: agrega una nueva funcionalidad
fix: corrección de error
docs: cambios de documentación
style: cambios de formato (no funcionales)
refactor: reestructuración sin afectar comportamiento
test: agregar o mejorar tests
chore: cambios de configuración o dependencias
```

---

## 🤝 Código de Conducta
- Respeta las ideas y opiniones.
- Sé claro al comunicar cambios.
- Apoya a quienes están aprendiendo.