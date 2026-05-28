<p align="center">
  <img src="logo.svg" alt="healthToPerformanceDB logo" width="600">
</p>

# healthToPerformanceDB

API REST basada en **FastAPI + TinyDB** que implementa el modelo de datos **ICAR Animal Data Exchange (ADE) v1.5** para operaciones CRUD sobre recursos ganaderos: animales, eventos de peso, sanitarios, movimientos, reproducción, ordeño y agrupaciones.

## Stack

| Componente | Versión |
|-----------|---------|
| Python | 3.11+ |
| FastAPI | 0.111+ |
| Pydantic | 2.x |
| TinyDB | 4.8+ |
| Uvicorn | 0.30+ |

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
# Desarrollo con hot-reload
uvicorn app.main:app --reload

# O mediante script
python run.py
```

## Carga de semilla

```bash
python seed_data.py
```

Inserta datos de ejemplo coherentes: nacimiento de ternera → ficha animal → peso neonatal → tratamiento por diarrea → agrupación en lote de recría → pesada de grupo.

## Documentación interactiva

| Recurso | URL |
|---------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Healthcheck | http://localhost:8000/healthcheck |
| OpenAPI JSON | http://localhost:8000/openapi.json |

## Uso con curl

### Animales

```bash
# Crear animal
curl -X POST http://localhost:8000/animals \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
    "specie": "Cattle",
    "gender": "Female",
    "birthDate": "2026-03-15T08:00:00Z",
    "location": {"scheme": "es.rea", "id": "ES430000001"},
    "primaryBreed": {"scheme": "es.rae", "id": "LIM"},
    "managementTag": "T-001",
    "productionPurpose": "Milk"
  }'

# Listar animales
curl http://localhost:8000/animals

# Obtener animal por identificador
curl http://localhost:8000/animals/es.magrama.bovine/ES091234567890

# Actualizar animal
curl -X PUT http://localhost:8000/animals/es.magrama.bovine/ES091234567890 \
  -H "Content-Type: application/json" \
  -d '{"identifier": {"scheme": "es.magrama.bovine", "id": "ES091234567890"}, "specie": "Cattle", "gender": "Female", "name": "Luna"}'

# Actualización parcial
curl -X PATCH http://localhost:8000/animals/es.magrama.bovine/ES091234567890 \
  -H "Content-Type: application/json" \
  -d '{"healthStatus": "Healthy"}'

# Eliminar animal
curl -X DELETE http://localhost:8000/animals/es.magrama.bovine/ES091234567890

# Eventos de un animal
curl http://localhost:8000/animals/es.magrama.bovine/ES091234567890/events
```

### Eventos

```bash
# Crear evento (cualquier tipo)
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "icarMovementBirthEventResource",
    "animal": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
    "location": {"scheme": "es.rea", "id": "ES430000001"},
    "eventDateTime": "2026-03-15T08:00:00Z",
    "remark": "Parto eutócico, ternera viva"
  }'

# Peso
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "icarWeightEventResource",
    "animal": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
    "eventDateTime": "2026-03-15T08:30:00Z"
  }'

# Listar eventos
curl http://localhost:8000/events

# Eventos por animal
curl http://localhost:8000/events/by-animal/es.magrama.bovine/ES091234567890

# Eventos por ubicación
curl http://localhost:8000/events/by-location/es.rea/ES430000001

# Eventos por tipo
curl http://localhost:8000/events/by-type/icarWeightEventResource
```

### Sanidad

```bash
# Crear tratamiento
curl -X POST http://localhost:8000/health/treatments \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "icarTreatmentEventResource",
    "animal": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
    "eventDateTime": "2026-03-18T10:00:00Z",
    "remark": "Diarrea neonatal - electrolitos orales"
  }'

# Programas de tratamiento
curl -X POST http://localhost:8000/health/treatment-programs \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "icarTreatmentProgramEventResource",
    "eventDateTime": "2026-03-18T10:00:00Z",
    "remark": "Protocolo diarrea neonatal leve"
  }'

# Listar
curl http://localhost:8000/health/treatments
curl http://localhost:8000/health/treatment-programs
```

### Pesos

```bash
# Crear pesada individual
curl -X POST http://localhost:8000/weights \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "icarWeightEventResource",
    "animal": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
    "eventDateTime": "2026-04-01T09:00:00Z"
  }'

# Pesada de grupo
curl -X POST http://localhost:8000/weights \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "icarGroupWeightEventResource",
    "location": {"scheme": "es.rea", "id": "ES430000001"},
    "eventDateTime": "2026-04-01T09:00:00Z",
    "remark": "Pesada lote recría Q1-2026"
  }'

# Pesos por animal
curl http://localhost:8000/weights/by-animal/es.magrama.bovine/ES091234567890

# Pesos por ubicación
curl http://localhost:8000/weights/by-location/es.rea/ES430000001
```

### Recursos genéricos

```bash
# Crear recurso (debe incluir resourceType)
curl -X POST http://localhost:8000/resources \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "icarAnimalCoreResource",
    "identifier": {"scheme": "es.magrama.bovine", "id": "ES099999999999"},
    "specie": "Cattle",
    "gender": "Male"
  }'

# Listar (opcionalmente filtrar por resourceType)
curl "http://localhost:8000/resources?resourceType=icarWeightEventResource&limit=10&offset=0"

# Obtener por ID interno
curl "http://localhost:8000/resources/<internalId>?resourceType=icarWeightEventResource"

# Actualizar
curl -X PUT "http://localhost:8000/resources/<internalId>?resourceType=icarWeightEventResource" \
  -H "Content-Type: application/json" \
  -d '{"resourceType": "icarWeightEventResource", "animal": {"scheme": "es.magrama.bovine", "id": "ES091234567890"}}'

# Actualización parcial
curl -X PATCH "http://localhost:8000/resources/<internalId>?resourceType=icarWeightEventResource" \
  -H "Content-Type: application/json" \
  -d '{"remark": "Peso corregido"}'

# Eliminar
curl -X DELETE "http://localhost:8000/resources/<internalId>?resourceType=icarWeightEventResource"

# Tipos de recurso disponibles
curl http://localhost:8000/resources/resource-types
```

### Grupos

```bash
curl -X POST http://localhost:8000/groups \
  -H "Content-Type: application/json" \
  -d '{"name": "Lote recría Q1-2026"}'

curl http://localhost:8000/groups
```

### Dispositivos / Medicamentos / Ubicaciones

```bash
curl -X POST http://localhost:8000/devices \
  -H "Content-Type: application/json" \
  -d '{"deviceType": "Ear tag RFID", "serialNumber": "RF-9420"}'

curl -X POST http://localhost:8000/medicines \
  -H "Content-Type: application/json" \
  -d '{"name": "Electrolitos orales", "activeIngredient": "Sodio, potasio, glucosa"}'

curl -X POST http://localhost:8000/locations \
  -H "Content-Type: application/json" \
  -d '{"name": "Explotación La Vega"}'
```

## Tests

```bash
pytest tests/ -v
```

## Estructura del proyecto

```
healthToPerformanceDB/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada FastAPI
│   ├── config.py             # Constantes y configuración
│   ├── database.py           # Conexión TinyDB
│   ├── models/
│   │   ├── common.py         # IcarIdentifierType, IcarMetaDataType, IcarResource, clases base
│   │   ├── animals.py        # IcarAnimalCoreResource
│   │   ├── events.py         # Eventos de movimiento (birth, arrival, departure, death, set join/leave)
│   │   ├── health.py         # Treatment, TreatmentProgram, GroupTreatment
│   │   ├── weights.py        # WeightEvent, GroupWeightEvent
│   │   ├── reproduction.py   # ReproInseminationEvent
│   │   ├── milking.py        # MilkingVisitEvent
│   │   ├── groups.py         # AnimalSetResource
│   │   └── resources.py      # GenericIcarResource (fallback)
│   ├── routers/
│   │   ├── animals.py        # /animals
│   │   ├── events.py         # /events
│   │   ├── generic_resources.py  # /resources
│   │   ├── groups.py         # /groups
│   │   ├── devices.py        # /devices
│   │   ├── medicines.py      # /medicines
│   │   ├── locations.py      # /locations
│   │   ├── health.py         # /health
│   │   └── weights.py        # /weights
│   ├── services/
│   │   ├── crud_service.py       # Operaciones CRUD genéricas sobre TinyDB
│   │   ├── resource_registry.py  # Mapa resourceType ↔ modelo Pydantic
│   │   └── validation_service.py # Validación dinámica de payloads
│   ├── schemas/
│   │   └── validators.py    # Validación de estructura JSON
│   └── utils/
│       ├── ids.py            # Generación de UUIDs
│       ├── dates.py          # Timestamps ISO 8601
│       └── pagination.py     # Normalización limit/offset
├── data/
│   └── tinydb.json           # Base de datos (se crea automáticamente)
├── tests/
│   ├── test_animals.py
│   ├── test_events.py
│   └── test_generic_resources.py
├── requirements.txt
├── seed_data.py
├── run.py
└── README.md
```

## Tipos de recurso soportados (70 types)

Todos los tipos del catálogo [adewg/ICAR ADE v1.5](https://github.com/adewg/ICAR/tree/ADE-1/resources) tienen modelo Pydantic dedicado.

| Categoría | Tipos modelados | Endpoints |
|-----------|----------------|-----------|
| **Animal** | `icarAnimalCoreResource` | `/animals` |
| **Movimiento individual** | `icarMovementBirthEventResource`, `icarMovementArrivalEventResource`, `icarMovementDepartureEventResource`, `icarMovementDeathEventResource` | `/events` |
| **Movimiento grupal** | `icarGroupMovementBirthEventResource`, `icarGroupMovementArrivalEventResource`, `icarGroupMovementDepartureEventResource`, `icarGroupMovementDeathEventResource`, `icarGroupPositionObservationEventResource`, `icarPositionObservationEventResource` | `/group-movements`, `/events` |
| **Pesos** | `icarWeightEventResource`, `icarGroupWeightEventResource` | `/weights`, `/events` |
| **Sanidad** | `icarTreatmentEventResource`, `icarTreatmentProgramEventResource`, `icarGroupTreatmentEventResource`, `icarAttentionEventResource`, `icarDiagnosisEventResource`, `icarHealthStatusObservedEventResource`, `icarRemarkEventResource`, `icarWithdrawalEventResource` | `/health`, `/health-ext`, `/events` |
| **Reproducción** | `icarReproInseminationEventResource`, `icarReproAbortionEventResource`, `icarReproDoNotBreedEventResource`, `icarReproEmbryoFlushingEventResource`, `icarReproEmbryoResource`, `icarReproHeatEventResource`, `icarReproMatingRecommendationResource`, `icarReproParturitionEventResource`, `icarReproPregnancyCheckEventResource`, `icarReproSemenStrawResource`, `icarReproStatusObservedEventResource`, `icarGestationResource` | `/reproduction`, `/events` |
| **Ordeño / Lactación** | `icarMilkingVisitEventResource`, `icarMilkingDryOffEventResource`, `icarLactationResource`, `icarLactationStatusObservedEventResource`, `icarDailyMilkingAveragesResource`, `icarMilkPredictionResource`, `icarTestDayResource`, `icarTestDayResultEventResource` | `/lactation`, `/events` |
| **Alimentación** | `icarFeedResource`, `icarFeedStorageResource`, `icarFeedTransactionResource`, `icarFeedIntakeEventResource`, `icarFeedRecommendationResource`, `icarFeedReportResource`, `icarRationResource`, `icarGroupFeedingEventResource` | `/feeding`, `/events` |
| **Genética** | `icarBreedingValueResource`, `icarProgenyDetailsResource` | `/resources` |
| **Canal / Sacrificio** | `icarCarcassResource`, `icarCarcassObservationsEventResource` | `/resources` |
| **Conformación** | `icarConformationScoreEventResource`, `icarTypeClassificationEventResource` | `/resources` |
| **Dispositivos** | `icarDeviceResource` | `/devices` |
| **Medicamentos** | `icarMedicineResource`, `icarMedicineTransactionResource` | `/medicines` |
| **Ubicaciones** | `icarLocationResource`, `icarInventoryTransactionResource` | `/locations` |
| **Catálogo** | `icarSchemeTypeResource`, `icarSchemeValueResource`, `icarSortingSiteResource`, `icarAnimalSortingCommandResource` | `/resources` |
| **Estadísticas** | `icarStatisticsResource`, `icarObservationSummaryResource`, `icarProcessingLotResource` | `/resources` |
| **Grupos** | `icarAnimalSetResource` | `/groups` |
| *fallback* | `GenericIcarResource` (tolerante) | `/resources` |

## Inspeccionar TinyDB

```bash
# Ver datos directamente
type data\tinydb.json

# O desde Python
python -c "from tinydb import TinyDB; db = TinyDB('data/tinydb.json'); print(db.all())"
```

## Limitaciones conocidas

- **TinyDB** no está diseñado para producción con alto volumen (sin concurrencia, sin índices reales)
- Sin autenticación ni autorización
- Validación de esquema solo para tipos registrados en `resource_registry.py`
- Sin integridad referencial entre recursos
- Paginación por `offset`/`limit` (no cursor-based)
- Sin búsqueda de texto completo
- Los 70 resource types modelados cubren la totalidad del catálogo ICAR ADE v1.5

## Próximos pasos

- [ ] Soportar todos los resource types del catálogo ADE v1.5
- [ ] Implementar las enumeraciones ICAR (`AnimalSpecieType`, `AnimalGenderType`, etc.) como `enum` de Python
- [ ] Añadir validación mediante JSON Schema
- [ ] Soft delete mediante `meta.isDeleted`
- [ ] Endpoints de exportación (JSON, GeoJSON, Excel)
- [ ] Autenticación mediante API key
- [ ] Operaciones batch (creación/actualización masiva)
- [ ] Migrar a SQLite vía SQLAlchemy para producción real
