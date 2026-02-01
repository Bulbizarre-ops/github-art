import os
import subprocess
from datetime import datetime, timedelta

# --- VOTRE CHAINE DE DONNEES (7x52) ---
DATA_STRING = (
    "0000011100100010000000000001000101110111101111011110000020000020020000000000000200020020020020200002000200003000003030000000000000030003003003003030000300030000044400440000444440000004000400400444404444044440000000003030300000000000000300030030030030300003030000000000202002000000000000002020002002002020000200200000111100100010000000000000010001110111101111010001"
)

COMMIT_MESSAGE = "chore: refresh github art"
COMMITS_PER_INTENSITY = 15


def _validate_data_string(data: str) -> None:
    if len(data) != 7 * 52:
        raise ValueError("DATA_STRING doit faire 364 caracteres (7x52).")
    if any(c not in "01234" for c in data):
        raise ValueError("DATA_STRING doit contenir uniquement des chiffres 0-4.")


def update_existing_repo_with_art() -> None:
    # 1. Verification de securite
    if not os.path.exists(".git"):
        print("❌ Erreur : Ce dossier n'est pas un depot Git. Lancez ce script a la racine du depot.")
        return

    _validate_data_string(DATA_STRING)

    # 2. Calcul du Dimanche de depart (il y a 52 semaines)
    today = datetime.now()
    start_date = today - timedelta(weeks=52)
    while start_date.weekday() != 6:  # recule jusqu'au dimanche
        start_date -= timedelta(days=1)

    rows = [DATA_STRING[i : i + 52] for i in range(0, 364, 52)]

    print("🚀 Injection du motif dans l'historique...")
    print(f"📅 Date de debut : {start_date.strftime('%Y-%m-%d')}")

    total_commits = 0
    for col in range(52):
        for row in range(7):
            intensity = int(rows[row][col])
            if intensity <= 0:
                continue

            commit_date = start_date + timedelta(weeks=col, days=row)
            date_str = commit_date.strftime("%Y-%m-%dT12:05:00")
            num_commits = intensity * COMMITS_PER_INTENSITY

            for _ in range(num_commits):
                env = os.environ.copy()
                env["GIT_AUTHOR_DATE"] = date_str
                env["GIT_COMMITTER_DATE"] = date_str

                subprocess.run(
                    [
                        "git",
                        "commit",
                        "--allow-empty",
                        "-m",
                        COMMIT_MESSAGE,
                        "--quiet",
                    ],
                    check=False,
                    env=env,
                )
                total_commits += 1

        print(f"Semaine {col + 1}/52 traitee...", end="\r")

    print(f"\n\n✅ Termine ! {total_commits} commits ajoutes a votre historique.")
    print("👉 Il ne vous reste plus qu'a faire : git push")


if __name__ == "__main__":
    update_existing_repo_with_art()
