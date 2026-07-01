# Template: Nuevo Proyecto

## Nombre del proyecto
[Nombre]

## Descripción
[Breve descripción de 2-3 líneas]

## Stack tecnológico
- Lenguaje(s):
- Framework(s):
- Base de datos:
- Herramientas:
- IA: [Ollama / OpenAI / etc.]

## Estructura inicial
```
/[nombre-proyecto]
├── src/
│   ├── components/
│   ├── services/
│   └── utils/
├── tests/
├── docs/
├── .env.example
├── .gitignore
├── README.md
└── package.json / requirements.txt
```

## Pasos iniciales
1. Crear estructura de carpetas
2. Inicializar git (`git init`)
3. Configurar .gitignore y .env.example
4. Instalar dependencias base
5. Primer commit: `chore: initial setup`
6. Crear rama develop: `git checkout -b develop`
7. Empezar primera feature: `git checkout -b feature/[nombre] develop`

## Integración con OpenCode Ultimate
- Registrar en `AI/Memory/proyectos.md`
- Seguir workflow `Crear Proyecto`
- Usar templates de commit y PR

## Ejemplo
```
Proyecto: MiAPI
Stack: Node.js, Express, PostgreSQL
```
