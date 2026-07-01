# Git Cheatsheet

## Comandos básicos
```
git init                          # Inicializar repo
git add .                         # Staging todo
git commit -m "mensaje"           # Commit
git push origin [rama]            # Subir cambios
git pull                          # Traer cambios
git status                        # Ver estado
git log --oneline                 # Historial resumido
```

## Ramas
```
git branch                        # Listar ramas
git checkout -b [nombre]          # Crear y cambiar a rama
git merge [rama]                  # Mergear rama a la actual
git branch -d [nombre]            # Eliminar rama local
git push origin --delete [nombre] # Eliminar rama remota
```

## Stash
```
git stash                         # Guardar cambios temporales
git stash pop                     # Recuperar cambios guardados
git stash list                    # Listar stashes
```

## Deshacer
```
git reset HEAD [archivo]          # Unstage archivo
git checkout -- [archivo]         # Descartar cambios en archivo
git reset --soft HEAD~1           # Deshacer último commit (sin perder cambios)
git revert HEAD                   # Revertir último commit (seguro)
```

## Tags
```
git tag -a v1.0 -m "v1.0"        # Crear tag anotado
git push origin --tags            # Subir tags
```
