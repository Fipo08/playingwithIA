# Workflow: Git Flow

## Estrategia
- `main` — Rama de producción
- `develop` — Rama de integración
- `feature/*` — Nuevas funcionalidades
- `fix/*` — Correcciones
- `release/*` — Preparación de releases

## Pasos

### Iniciar feature
1. `git checkout -b feature/[nombre] develop`
2. Implementar cambios en commits atómicos
3. `git push origin feature/[nombre]`

### Terminar feature
1. `git checkout develop`
2. `git merge --no-ff feature/[nombre]`
3. `git branch -d feature/[nombre]`

### Hacer release
1. `git checkout -b release/[version] develop`
2. Ajustar versión y CHANGELOG
3. `git checkout main`
4. `git merge --no-ff release/[version]`
5. `git tag -a v[version] -m "v[version]"`
6. Volver a develop y mergear

### Hotfix
1. `git checkout -b fix/[nombre] main`
2. Corregir y commitear
3. Merge a main y develop
