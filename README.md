# GitHub Art

Ce depot genere un "GitHub Art" via des commits dates sur les 52 dernieres semaines.

## Utilisation locale

1. Initialiser le depot puis ajouter un remote.
2. Lancer le script :
   ```bash
   python generate_art.py
   ```
3. Pousser :
   ```bash
   git push
   ```

## CI/CD

Un workflow GitHub Actions s'execute a chaque push sur `main` et chaque semaine (dimanche 03:00 UTC)
pour rafraichir le motif.
Vous pouvez aussi le lancer manuellement via **Actions > Refresh GitHub Art**.
Pour que les commits apparaissent sur votre graphique de contributions, configurez les secrets suivants :
`GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL` (optionnellement `GIT_COMMITTER_NAME`, `GIT_COMMITTER_EMAIL`).
Le workflow force-push sur `main` pour regenerer l'historique a chaque execution.
Apres chaque execution de la CI/CD, mettez a jour votre repo local avec :
```bash
git reset --hard origin/main
```

## Donnees

Le motif est defini par `DATA_STRING` dans `generate_art.py`.
Chaque caractere (0-4) represente l'intensite des commits pour une case de la grille 7x52.
