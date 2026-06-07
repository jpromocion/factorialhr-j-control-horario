# AGENTS.md - Documentacion para Agentes IA

## Proposito

Este documento proporciona contexto y instrucciones para agentes de IA que trabajen en el proyecto `factorialhr-j-control-horario`.

## Descripcion del Proyecto

Herramienta CLI escrita en Python (3.12+) para interactuar con la API REST de Factorial HR (https://api.factorialhr.com/) para gestion de control horario.

## Estructura del Codigo

```
factorialhr_j/
├── cli.py                 # Punto de entrada CLI. Comandos: calendario, imputar, actualizar-imputacion, borrar-imputacion
├── config.py              # Carga configuracion desde YAML (config.yaml > config.base.yaml)
├── models/                # Modelos de datos inmutables (dataclasses)
│   ├── calendar_day.py    # Dia del calendario (date, day, is_laborable, is_leave)
│   ├── estimated_time.py  # Tiempo estimado por dia (date, minutes)
│   ├── worked_day.py      # Dia con imputaciones trabajadas (date, minutes, worked_time_blocks)
│   └── shift.py           # Shift/imputacion individual (id, employee_id, date, clock_in, clock_out, workable, minutes)
├── utils/                 # Utilidades de formateo y display
│   ├── formatters.py      # format_date, format_minutes, format_time, get_day_letter
│   └── output_standard.py # output_error, output_warning, output_completion, output_shifts_results, output_single_shift, output_calendar
├── validators.py          # Validacion de parametros (fecha, hora, rango)
├── factorialhr/
│   ├── api_client.py     # Cliente HTTP con autenticacion por cookie
│   └── service.py         # Fachada con metodos para cada operacion de API
tests/
├── conftest.py            # Fixtures: sample_shift, sample_calendar_day, mock_factorial_service
├── test_validators.py    # Tests de validacion de parametros
└── test_cli_commands.py   # Tests de comandos CLI
```

## Configuracion

- **Ubicacion**: `config/config.base.yaml` (plantilla) y `config/config.yaml` (usuario)
- **Prioridad**: `config/config.yaml` > `config/config.base.yaml`
- **Valores**:
  - `id_empleado`: ID del empleado en Factorial HR
  - `cookie_sesion`: Cookie de sesion para autenticacion

## API REST - Endpoints

### Endpoints de Consulta (GET)

1. **Calendario**: `GET /attendance/calendar?start_on=&end_on=&id=`
   - Params: start_on (YYYY-MM-DD), end_on (YYYY-MM-DD), id (empleado)
   - Response: Array de dias con is_laborable, is_leave

2. **Tiempos Estimados**: `GET /api/2026-04-01/resources/attendance/estimated_times?employee_ids[]=&start_on=&end_on=`
   - Params: employee_ids[], start_on, end_on
   - Response: { data: [{ date, minutes }], meta: {...} }

3. **Dias con Imputaciones**: `GET /api/2026-04-01/resources/attendance/worked_times?employee_ids[]=&start_on=&end_on=&include_time_range_category=true&include_non_attendable_employees=true`
   - Params: employee_ids[], start_on, end_on
   - Response: { data: [{ date, minutes, worked_time_blocks }], meta: {...} }

4. **Shifts/Imputaciones**: `GET /api/2026-04-01/resources/attendance/shifts?employee_ids[]=&start_on=&end_on=`
   - Params: employee_ids[], start_on, end_on
   - Response: { data: [{ id, date, clock_in, clock_out, workable, minutes }], meta: {...} }

### Endpoints de Modificacion

5. **CreateShift**: `POST /api/2026-04-01/resources/attendance/shifts`
   - Body: { employee_id, date (YYYY-MM-DD), clock_in (YYYY-MM-DDTHH:MM:SS), clock_out (YYYY-MM-DDTHH:MM:SS) }
   - Response: Shift creado completo

6. **UpdateShift**: `PUT /api/2026-04-01/resources/attendance/shifts/{id}`
   - Body: { id, clock_in, clock_out }
   - Response: Shift actualizado

7. **DeleteShift**: `DELETE /api/2026-04-01/resources/attendance/shifts/{id}`
   - Response: Shift eliminado

## Comandos CLI

| Comando | Descripcion |
|---------|-------------|
| `factorialhr-j calendario --fechainicio DD/MM/YYYY --fechafin DD/MM/YYYY` | Muestra resumen con laborables, festivos y horas |
| `factorialhr-j imputar --fecha DD/MM/YYYY --inicio HH:MM --fin HH:MM` | Crea nueva imputacion |
| `factorialhr-j actualizar-imputacion --idshift ID --inicio HH:MM --fin HH:MM` | Modifica imputacion existente |
| `factorialhr-j borrar-imputacion --idshift ID` | Elimina imputacion |

## Dependencias

- `click` (>=8.1.0) - Framework CLI
- `pyyaml` (>=6.0) - Lectura de archivos YAML
- `requests` (>=2.31.0) - Cliente HTTP
- `pytest` (>=9.0.0) - Testing

## Convenciones de Codigo

- Usar dataclasses para modelos de datos
- Metodos estaticos `from_api()` para construccion desde JSON de API
- Tipado estatico con type hints
- Formato de fechas: API usa YYYY-MM-DD, CLI usa DD/MM/YYYY
- Formato de horas: HH:MM sin segundos en CLI, YYYY-MM-DDTHH:MM:SS en API
- Solo considerar shifts con `workable: True` para calculos de tiempo
- Separar logica de negocio (cli.py) de display (utils/output_standard.py)

## Notas de Implementacion

- La cookie de sesion se obtiene del navegador manualmente (no hay login programatico)
- El archivo `config/config.yaml` debe estar en `.gitignore`
- Se usa fallback: primero busca config.yaml, si no existe usa config.base.yaml
- Los errores de API se propagan con `response.raise_for_status()`

## Testing

### Ejecutar tests
```bash
pytest tests/ -v
```

### Reglas importantes
- Los tests NUNCA deben llamar a la API real - siempre usar mocks de `FactorialService`
- Usar `unittest.mock.patch` o fixtures de `conftest.py` para mockear servicios
- Usar `click.testing.CliRunner` para probar comandos CLI
- Tras cada cambio que afecte a validators o CLI, ejecutar `pytest tests/ -v` para verificar que todos los tests pasan