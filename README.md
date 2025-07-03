# 🛍️ Registro de Ventas Django

Sistema para registrar y gestionar ventas, desarrollado con Django y SQL.

---

## Funcionalidades principales

- Registro de ventas
- Registro de usuarios con diferenciación de vistas según permisos
- Perfil de cada usuario con posibilidad de modificación de datos
- Revisión de historial de ventas

---

## Capturas

![Vista principal](registro_ventas/media/captura.png)

---

## Estructura del proyecto

```text
registro_ventas/               # Carpeta raíz del proyecto
├── manage.py
├── requirements.txt
├── pages/                     # App para páginas generales
├── registro_ventas/          # Configuración principal del proyecto
├── static/                   # Archivos estáticos (CSS, JS, etc.)
├── usuarios/                 # App para gestión de usuarios
└── ventas/                   # App para lógica de ventas
```

---

## Inicio rápido

### 1. Clonar el repositorio  
```bash
git clone https://github.com/agustingomez1986/registro_ventas_django.git
cd registro_ventas_django
```

### 2. Crear entorno virtual e instalar dependencias  
```bash
python3 -m venv env
source env/bin/activate  # en Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar variables de entorno  
Crear un archivo `.env` (o copiar `.env.example`) y definir al menos:  
```
SECRET_KEY=tu_clave_secreta
DEBUG=True
DATABASE_URL=postgres://usuario:password@localhost:5432/tu_basededatos
```

### 4. Ejecutar migraciones  
```bash
python manage.py migrate
```

### 5. Crear usuario administrador  
```bash
python manage.py createsuperuser
```

### 6. Iniciar servidor  
```bash
python manage.py runserver
```

Por defecto estará accesible en `http://127.0.0.1:8000/`.

---

## Preguntas y contacto

Para sugerencias, dudas o reportes de errores, abre una *issue* en el repositorio o mándame un mensaje directo. ¡Feedback siempre bienvenido!