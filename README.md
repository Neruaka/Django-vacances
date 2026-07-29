# Wanderlist — Carnet de destinations de voyage

Application Django + Django REST Framework permettant de consulter un
catalogue public de destinations et de gérer sa propre liste personnelle
d'envies de voyage, avec authentification JWT.

## 1. Fonctionnalités

- Consulter la liste des destinations (publique, sans compte).
- Créer/modifier/supprimer une destination (utilisateur authentifié).
- Ajouter une destination à ses envies personnelles, avec priorité,
  période souhaitée et notes.
- Un utilisateur ne voit et ne peut modifier que **ses propres** envies.
- Impossible d'ajouter deux fois la même destination à ses envies.
- Marquer une envie comme visitée via une action dédiée.
- Page HTML publique listant les destinations.

## 2. Installation

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
```

## 3. Lancement

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Le serveur écoute sur `http://127.0.0.1:8000/`.

## 4. Endpoints principaux

| Méthode | URL | Auth requise | Description |
|---|---|---|---|
| GET | `/destinations/` | non | Page HTML publique |
| GET | `/api/destinations/` | non | Liste des destinations (JSON) |
| POST | `/api/destinations/` | oui | Créer une destination |
| GET/PUT/PATCH/DELETE | `/api/destinations/<id>/` | non (GET) / oui (écriture) | Détail d'une destination |
| GET | `/api/wishes/` | oui | Liste de **mes** envies uniquement |
| POST | `/api/wishes/` | oui | Ajouter une envie |
| PATCH/DELETE | `/api/wishes/<id>/` | oui (et propriétaire) | Modifier/supprimer une envie |
| POST | `/api/wishes/<id>/mark-visited/` | oui (et propriétaire) | Marquer comme visitée |
| POST | `/api/token/` | non | Obtenir un jeton JWT (`username`, `password`) |
| POST | `/api/token/refresh/` | non | Renouveler un access token |

## 5. Exemple de scénario testable (curl)

```bash
# 1. Obtenir un jeton
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","password":"motdepasse"}'
# -> {"access": "...", "refresh": "..."}

# 2. Créer une destination (authentifié)
curl -X POST http://127.0.0.1:8000/api/destinations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"city":"Tokyo","country":"Japon","continent":"asia"}'

# 3. Ajouter cette destination à ses envies
curl -X POST http://127.0.0.1:8000/api/wishes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"destination":1,"priority":"high","desired_period":"printemps"}'
```

## 6. Architecture des données

```
User (fourni par Django)
  │
  │ possède plusieurs
  ▼
TravelWish  ──────────► concerne une ──────────►  Destination
```

- `Destination` : donnée publique (ville, pays, continent, budget moyen...).
- `TravelWish` : relie un utilisateur précis à une destination précise,
  avec ses informations personnelles (priorité, période, notes, statut
  visité). Une contrainte d'unicité (`user` + `destination`) empêche les
  doublons.

## 7. Choix de conception notables

- **Un modèle intermédiaire (`TravelWish`) plutôt qu'un `ManyToManyField`** :
  un simple M2M ne pourrait stocker que "Bob aime Tokyo", pas la priorité,
  la période souhaitée ou les notes propres à cette envie précise.
- **Double protection contre les doublons** : une `UniqueConstraint` en
  base de données (protection ultime) et une validation dans le
  sérialiseur (message d'erreur clair pour le client).
- **Isolation stricte par utilisateur** : `get_queryset()` filtre toujours
  sur `request.user`, y compris pour les routes de détail — accéder à
  l'envie d'un autre utilisateur renvoie `404`, jamais `403` (l'objet
  "n'existe pas" du point de vue de cet utilisateur).
- **`user` jamais modifiable par le client** : le champ est en lecture
  seule dans le sérialiseur, `perform_create()` l'attribue depuis le jeton
  JWT décodé côté serveur.

## 8. Utilisateurs de test (à créer localement)

```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
User.objects.create_user(username="bob", password="motdepasse")
User.objects.create_user(username="alice", password="motdepasse")
```
