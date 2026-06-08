# FactorialHR - Control Horario

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-green.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-orange)
[![Donar PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/donate/?hosted_button_id=S2CX67ZD5C97C)

Herramienta CLI para interactuar con la API REST de Factorial HR para control horario.

> [!WARNING]
> Proyecto con fines lúdicos. El autor no se hace responsable del uso indebido que cada usuario haga.


## ☕ Acho tio... pagate un café!

Si te gusta... pagate algo, ¿no?:
[![Donar PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/donate/?hosted_button_id=S2CX67ZD5C97C)

## 📋 Caracteristicas

- **Calendario**: Consulta el calendario laboral con dias laborables, festivos y horas imputadas
- **Imputar**: Crea nuevas imputaciones de tiempo. Imputación masiva.
- **Actualizar imputacion**: Modifica imputaciones existentes
- **Borrar imputacion**: Elimina imputaciones existentes
- **Configuracion simple**: Archivo YAML para credenciales y configuracion

## 🚀 Inicio Rapido

### 1. Instalacion

```bash
# A) Instalar dependencias, pero no instalarse como paquete
pip install -r requirements.txt
# B) Instalar como paquete con las dependencias. RECOMENDADO
pip install -e .
```

#### NOTA: Sobre ejecución de los comandos

En Ubuntu, el comando es python3 en vez de python.

La mejor forma de trabajar con VS Code:
- Crear un entorno con el plugin de Python y luego usar "Create Terminal" con ese entorno.
- En Windows, VS Code tiene un panel lateral de Python para abrir la terminal conectada a ese entorno Python
- En Ubuntu, ejecutas el comando desde el grupo de Python.
- Luego, en esa terminal, carga el entorno de Python antes de la ruta y puedes ejecutarlo con normalidad.
```bash
(.venv) aaaaa:../factorialhr-j-control-horario$

# Activarlo desde PowerShell
& C:/.../factorialhr-j-control-horario/.venv/Scripts/Activate.ps

# Activarlo desde cmd
C:\...\factorialhr-j-control-horario\.venv\Scripts\activate.bat
```

También puedes forzarlo a ejecutarse en una consola normal de Ubuntu:
```bash
# Crear y activar un entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Al terminar, desactiva el entorno:
deactivate
```

Ejecutar comandos tras instalación solo por dependencias:
```bash
python -m factorialhr-j.cli ...
```

Ejecutar comandos tras instalación de paquete (RECOMENDADA):
```bash
factorialhr-j ...
```

### 2. Configuracion

1. Copia el archivo de configuracion base:
```bash
cp config/config.base.yaml config/config.yaml
```

2. Edita `config/config.yaml` y establece tus valores:
   - `id_empleado`: Tu ID de empleado en Factorial HR. Ver como se saca la cookie, y se ve facilmente cual es tu id interno.
   - `cookie_sesion`: La cookie de sesion (obtenida del navegador tras hacer login en la aplicacion web)
**Importante**: El archivo `config/config.yaml` esta en `.gitignore` y nunca debe subirse al repositorio.

#### Obtener los datos anteriores

1. Abre el navegador y entra en https://app.factorialhr.com
2. Inicia sesion con tus credenciales
3. Abre las herramientas de desarrollo (F12) y ve a la pestana de Red/Network
4. Realiza cualquier accion en la aplicacion que haga una peticion a la API
  - Entrar a "Mi control horario" y ver en Network la petición tipica de "https://api.factorialhr.com/attendance/calendar?..."
5. En la petición encontraras el Request header "Cookie" - copia su valor completo
6. En la petición encontraras el el parametro con tu id de empleado.
7. Ese valor es el que debes poner en `cookie_sesion` del archivo de configuracion

> [!NOTE]
> La cookie es la de sesión del navegador, expira a menudo: por lo que si da "401 - Unauthorized", ya sabes lo que toca.
> La [API en si](https://apidoc.factorialhr.com/docs/authentication) esta preparada para invocarse por 2 metodos:
> - Oauth token -> Me da que esto se tiene que activar a nivel de compañia... no veo como obtenerlo rapido, facil y limpico... vaya shit!! Igual dedicandole tiempo alguna "alma caritativa" obtenga mas info.
> - API Key -> solo desarrolladores de factorial. Pa' que decir más

> [!TIP]
> Otra alternativa sería ejecutar en background navegador, loguear automatizadamente, y leer cookie.... Pero vamos, esta protegido por "cloudfare"... de otros proyectos, se que es mejor "pegarse un tiro" antes que intentar automatizar algo con el puto cloudfare de por medio.

## 📁 Estructura del Proyecto

```
factorialhr-j-control-horario/
├── factorialhr_j/                  # Paquete principal
│   ├── cli.py                      # Interfaz CLI
│   ├── __init__.py                 # Inicializador del paquete
│   ├── config.py                   # Gestion de configuracion
│   ├── models/                     # Modelos de datos
│   │   ├── calendar_day.py
│   │   ├── estimated_time.py
│   │   ├── worked_day.py
│   │   └── shift.py
│   ├── utils/                     # Utilidades varias
│   │   ├── ...
│   └── factorialhr/                # Logica de integracion con la API
│       ├── api_client.py
│       └── service.py
├── config/                         # Archivos de configuracion YAML
│   ├── config.base.yaml            # Plantilla de configuracion
│   └── config.yaml                 # Configuracion local (no subir)
├── test/                           # Tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_validators.py
│   └── test_cli_commands.py
├── requirements.txt                # Dependencias Python
├── setup.py                        # Instalador del paquete
├── README.md                       # Documentacion
├── AGENTS.md                       # Documentacion para agentes IA
└── LICENSE                         # Licencia
```

## 🔧 Referencia de Comandos

### Comando `calendario`

Muestra un resumen del periodo especificado con dias laborables, festivos y horas imputadas, alertas...

```bash
factorialhr-j calendario --fechainicio "01/06/2026" --fechafin "05/06/2026"
```

**Salida de ejemplo:**
```
📅 Dias desde 01/06/2026 hasta 10/06/2026
──────────────────────────────────────────────────

📆 DIA: 01/06/2026
────────────────────────────────────────
   ✅ Laborable   ⚪ No festivo
   ⏱️ Tiempo estimado: 8 horas - 30 minutos
   ⏱️ Tiempo imputedo: 8 horas - 30 minutos
   📋 Desglose:
      🕑 08:00 - 15:00 -> 7 horas - 0 minutos  (Id shift: 123123)
      🕑 16:00 - 17:30 -> 1 horas - 30 minutos  (Id shift: 123213)
...

📆 DIA: 03/06/2026
────────────────────────────────────────
   ✅ Laborable   ⚪ No festivo
   ⏱️ Tiempo estimado: 8 horas - 30 minutos
   ⏱️ Tiempo imputedo: 0 horas - 0 minutos
   ⚠️ ALERTA: Dia sin imputar. Faltan 8 horas - 30 minutos
...
📆 DIA: 06/06/2026
   ❌ No laborable   ⚪ No festivo
   ⏱️ Tiempo estimado: 0 horas - 0 minutos
   ⏱️ Tiempo imputedo: 0 horas - 0 minutos

🎯 Proceso completado!
```

### Comando `imputar`

Crea una nueva imputacion de tiempo para un dia y horario especifico.

```bash
# 1 imputacion
factorialhr-j imputar --fecha "02/06/2026" --inicio "08:00" --fin "15:00"

# 2 imputaciones en mismo dia
factorialhr-j imputar --fecha "02/06/2026" --inicio "08:00,16:00" --fin "15:00,17:30"

# 3 imputaciones con rango dia / modelo. Escapado en matriz-modelo para ": todo parametro con simples '' y dentro escapar con \"
#   3.1 Ejemplo: Imputar semana en "horario oficina" estandar
factorialhr-j imputar --rango "01/06/2026-05/06/2026" --matriz-modelo '[{\"dia\": \"L\",\"imputaciones\": [{\"inicio\": \"08:00\",\"fin\": \"14:00\"},{\"inicio\": \"15:00\",\"fin\": \"17:30\"}]},{\"dia\": \"M\",\"imputaciones\": [{\"inicio\": \"08:00\",\"fin\": \"14:00\"},{\"inicio\": \"15:00\",\"fin\": \"17:30\"}]},{\"dia\": \"X\",\"imputaciones\": [{\"inicio\": \"08:00\",\"fin\": \"14:00\"},{\"inicio\": \"15:00\",\"fin\": \"17:30\"}]},{\"dia\": \"J\",\"imputaciones\": [{\"inicio\": \"08:00\",\"fin\": \"14:00\"},{\"inicio\": \"15:00\",\"fin\": \"17:30\"}]},{\"dia\": \"V\",\"imputaciones\": [{\"inicio\": \"08:00\",\"fin\": \"14:00\"}]}]'

#   3.2 Ejemplo: Imputar semana en horario reducido verano (con "descanso" intermedio)
factorialhr-j imputar --rango "06/07/2026-10/07/2026" --matriz-modelo '[{\"dia\": \"L\",\"imputaciones\": [{\"inicio\": \"08:00\",\"fin\": \"12:00\"},{\"inicio\": \"12:15\",\"fin\": \"15:15\"}]},{\"dia\": \"M\",\"imputaciones\": [{\"inicio\": \"08:00\",\"fin\": \"12:00\"},{\"inicio\": \"12:15\",\"fin\": \"15:15\"}]},{\"dia\": \"X\",\"imputaciones\": [{\"inicio\": \"08:00\",\"fin\": \"12:00\"},{\"inicio\": \"12:15\",\"fin\": \"15:15\"}]},{\"dia\": \"J\",\"imputaciones\": [{\"inicio\": \"08:00\",\"fin\": \"12:00\"},{\"inicio\": \"12:15\",\"fin\": \"15:15\"}]},{\"dia\": \"V\",\"imputaciones\": [{\"inicio\": \"08:00\",\"fin\": \"12:00\"},{\"inicio\": \"12:15\",\"fin\": \"15:15\"}]}]'
```
Parametros:
- **fecha**: Fecha del día en formato "DD/MM/YYY".
- **inicio**: Hora de inicio de la imputación en formato "HH24:MI". Admite pasar varias separadas por ",", como `"08:00,16:00"`, lo que realizará varias imputaciones en el mismo dia. Los parámetros `inicio` y `fin` deben contener el mismo número de elementos para hacer la correspondencia.
- **fin**: Hora de fin de la imputación en formato "HH24:MI". Admite pasar varias separadas por ",", como `"15:00,17:30"`, lo que realizará varias imputaciones en el mismo dia. Los parámetros `inicio` y `fin` deben contener el mismo número de elementos para hacer la correspondencia.
- **rango**: Tipo de imputación alternativa a "fecha". Se indica un rango de fecha, con fecha inicio y fin separadas por el "-" y con formato "DD/MM/YYY". Todos los días que sean laborables y no festivos y esten dentro de ese rango sos suceptibles de imputarse.
- **matriz-modelo**: Adicional al tipo de imputación con "rango". Se especifica el modelo de imputaciones que debe aplicarse por cada día concreto de la semana:
  - JSON ejemplo:
    ```json
    [
      {
        "dia": "L",
        "imputaciones": [
          {
            "inicio": "08:00",
            "fin": "15:00"
          },
          {
            "inicio": "16:00",
            "fin": "17:30"
          }
        ]
      },
      {
        "dia": "M",
        "imputaciones": [
          {
            "inicio": "08:00",
            "fin": "15:00"
          },
          {
            "inicio": "16:00",
            "fin": "17:30"
          }
        ]
      },
    ...
    ]
    ```
    - *dia*: Dia de la semana modelo:
      - *L*: Lunes
      - *M*: Martes
      - *X*: Miercoles
      - *J*: Jueves
      - *V*: Viernes
      - *S*: Sabado
      - *D*: Domingo
    - *imputaciones*: cada elemento es una imputacion que realizar. `inicio` indica la hora de inicio en formato "HH24:MI" y `fin` indica la hora de fin en formato "HH24:MI"


**Salida de ejemplo:**
```
  📆 DIA: 01/06/2026
  ──────────────────────────────────────
    1️⃣ 🕐 08:00 - 15:00
        ⏱️  7 horas - 0 minutos
        🆔 Id shift: 499202248
    2️⃣ 🕐 16:00 - 17:30
        ⏱️  1 horas - 30 minutos
        🆔 Id shift: 499202253

  📆 DIA: 02/06/2026
  ──────────────────────────────────────
    1️⃣ 🕐 08:00 - 15:00
        ⏱️  7 horas - 0 minutos
        🆔 Id shift: 499202255
    2️⃣ 🕐 16:00 - 17:30
        ⏱️  1 horas - 30 minutos
        🆔 Id shift: 499202256

✅ Imputaciones creadas: 4

🎯 Proceso completado!
```

**Salida de ejemplo error:**
```
  📆 DIA: 02/06/2026
  ──────────────────────────────────────
    ❌ Error 422: Error de validacion (422)
        Detalle: base: se solapa con el turno de 08:00 a 15:00 del 2026-06-02
    ❌ Error 422: Error de validacion (422)
        Detalle: base: se solapa con el turno de 16:00 a 17:30 del 2026-06-02
❌ Imputaciones fallidas: 2

🎯 Proceso completado!
```

### Comando `actualizar-imputacion`

Modifica una imputacion existente (solo permite cambiar el horario, no la fecha).

```bash
factorialhr-j actualizar-imputacion --idshift 498876197 --inicio "18:00" --fin "20:00"
```

**Salida de ejemplo:**
```
✅ Imputacion actualizada OK
   📆 Dia: 02/06/2026
   🆔 Id shift: 498876197
   🕐 Hora inicio: 18:00
   🕑 Hora fin: 20:00
   ⏱️ Tiempo: 2 horas - 0 minutos

🎯 Proceso completado!
```

### Comando `borrar-imputacion`

Elimina una imputacion existente.

```bash
# 1 Borrar por id del shift
factorialhr-j borrar-imputacion --idshift 498871544

# 2 Borrar todos los shift de un dia
factorialhr-j borrar-imputacion --fecha "02/06/2026"
```
Parametros:
- **idshift**: Id de la imputación concreta a eliminar. Es devuelto por comandos anteriores.
- **fecha**: Forma de invocar alternativa "idshift". Fecha del día en formato "DD/MM/YYY". Buscará las imputaciones (shifts) de ese día, y las eleminará.

**Salida de ejemplo:**
```
  📆 DIA: 02/06/2026
  ──────────────────────────────────────
    1️⃣ 🕐 08:00 - 15:00
        ⏱️  7 horas - 0 minutos
        🆔 Id shift: 499202255
    2️⃣ 🕐 16:00 - 17:30
        ⏱️  1 horas - 30 minutos
        🆔 Id shift: 499202256

✅ Imputaciones eliminadas: 2

🎯 Proceso completado!
```

## 🧪 Test
Se ejecutan con "pytest" (Instalado en dependencias de proyecto)

```bash
# Todos los tests
pytest tests/
# Solo un archivo
pytest tests/test_cli_commands.py -v
# Solo un test específico
pytest tests/test_validators.py::TestValidateDate::test_invalid_date_raises_bad_parameter -v
```

> [!IMPORTANT]
> Los tests usan mocks de FactorialService - nunca llaman a la API real.

## 📈 Mejoras Futuras

- [ ] Borrar por rango de fechas... Visto el lio de como imputar... a lo mejor
- [ ] Operacion "autofill": para que? sino esta activado. El servicio te dice "Forbidden by Attendance::ShiftPolicy::Autofill"
- [ ] Soporte para autenticacion mediante Oauth token: ¿sera posible? investigarcion... que pereza!
- [ ] NO Oauth token: Y hacer un script que te abra navegador de logueas, y te chupe el cookie el solito para actualizartelo en el config.yaml... Automatico seguro que no por el puto cloudfare
- [ ] Soporte para exportar datos a CSV/JSON de la salida de comandos: Mmmm... quiza, tampoco veo que aporte nada para estas salidas.

## 🤝 Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la licencia Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

**Resumen:**
- Eres libre de usar, copiar, modificar y distribuir este software para fines no comerciales, siempre que otorgues el crédito adecuado al autor original ("jpromocion").
- Para cualquier uso comercial de este software o de trabajos derivados, debes obtener el permiso expreso y por escrito de "jpromocion".
- El software se proporciona "tal cual", sin garantía de ningún tipo.

Para más detalles, consulta el archivo [LICENSE](./LICENSE) y la licencia oficial [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/legalcode).