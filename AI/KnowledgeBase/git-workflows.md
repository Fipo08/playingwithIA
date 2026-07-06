# Git Workflows

## Conventional Commits
```
feat: nueva funcionalidad
fix: corrección de bug
refactor: cambio sin corrección ni feature
docs: solo documentación
chore: tareas internas (build, CI)
test: agregar/modificar tests
```

## Merge vs Rebase
```bash
# Merge (preserva historia)
git checkout main && git merge feature

# Rebase (historia lineal)
git checkout feature && git rebase main
git checkout main && git merge feature
```

## Undo
```bash
git restore archivo               # descartar cambios sin commit
git restore --staged archivo      # unstaged
git reset --soft HEAD~1           # deshacer último commit (cambios staged)
git reset --hard HEAD~1           # deshacer último commit (perder cambios)
```

## Worktrees (ramas paralelas)
```bash
git worktree add ../project-feature feature-branch
git worktree list
git worktree remove ../project-feature
```

## Hooks (pre-commit)
```powershell
# .git/hooks/pre-commit
# Revisar archivos modificados antes de commit
```

## Stash
```bash
git stash push -m "WIP: mensaje"
git stash list
git stash pop
git stash drop stash@{0}
```
