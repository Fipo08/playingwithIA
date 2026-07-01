# Workflow: Deploy

## Pasos

### 1. Pre-deploy
- Verificar que main está actualizada
- Ejecutar tests
- Revisar CHANGELOG
- Actualizar versión si aplica

### 2. Build
- Ejecutar script de build
- Verificar que build es exitoso
- Comprobar artefactos generados

### 3. Deploy
- Elegir entorno: dev / staging / production
- Ejecutar script de deploy correspondiente
- Verificar health check post-deploy

### 4. Post-deploy
- Monitorear logs por errores
- Confirmar que la app responde
- Notificar al equipo si aplica

## Rollback
Si algo sale mal:
1. Identificar última versión estable
2. `git revert HEAD` o checkout de tag anterior
3. Redeployar versión estable
4. Crear bug ticket para la incidencia
