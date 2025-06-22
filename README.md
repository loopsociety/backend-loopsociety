# LoopSociety API

API del foro colaborativo de la comunidad LoopSociety, desarrollada en FastAPI con SQLModel y MySQL. Este repositorio está diseñado para ser limpio, escalable y mantener prácticas profesionales de desarrollo colaborativo, incluyendo Alembic para migraciones, autenticación JWT, OAuth2 y código modular.

---

## ⚙️ Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [MySQL](https://www.mysql.com/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Docker (opcional)](https://www.docker.com/)
- [JWT](https://jwt.io/)
- Python 3.10+

---

## 🚀 Estado del proyecto

> Este proyecto aún está en desarrollo. Se están construyendo los endpoints principales y las funcionalidades base para luego avanzar con las colaboraciones del equipo.

---

## 📁 Estructura base del proyecto
```
app/
│
├── api/ # Routers
├── core/ # Configs, seguridad, dependencias
├── db/
│ ├── database.py # Engine de SQLModel
│ ├── models/ # Modelos (User, Thread, etc)
│ └── schemas/ # Pydantic schemas
├── services/ # Lógica de negocio
├── main.py
alembic/
.env
README.md
```

---

## 🧪 Cómo ejecutar localmente

1. Clona el repositorio:

```bash
git clone https://github.com/loopsociety/loopsociety-api.git
cd loopsociety-api
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env`:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/loopsociety
SECRET_KEY=supersecret
```

4. Aplica las migraciones:

```bash
alembic upgrade head
```

5. Ejecuta el servidor:

```bash
uvicorn app.main:app --reload
```

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