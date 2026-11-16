"""
Générateur du jeu de données synthétique « Fréquence ».

Produit cinq fichiers CSV : utilisateurs.csv, titres.csv, abonnements.csv,
ecoutes.csv (le socle, chapitre P1C3) et playlists.csv (activité du chapitre P1C3).
Toutes les données sont fictives. Le générateur est déterministe : avec la même
graine, il produit exactement les fichiers du dépôt.

Usage :
  python generate_frequence.py --out ../../donnees                    # horodatages ISO (2026-03-15 18:42:07)
  python generate_frequence.py --out /tmp/frequence --horodatage fr  # horodatages 15/03/2026 18:42:07
"""
import argparse
import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--horodatage", choices=["iso", "fr"], default="iso")
parser.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
parser.add_argument("--seed", type=int, default=2026)
args = parser.parse_args()

rng = np.random.default_rng(args.seed)
os.makedirs(args.out, exist_ok=True)

# ----------------------------------------------------------------------------
# Paramètres
# ----------------------------------------------------------------------------
PERIOD_START = date(2025, 10, 1)
PERIOD_END = date(2026, 10, 1)            # exclu : dernière écoute le 30/09/2026
N_DAYS = (PERIOD_END - PERIOD_START).days
DAYS = np.array([PERIOD_START + timedelta(days=i) for i in range(N_DAYS)])
N_USERS = 3000
N_TITRES = 1200
N_ARTISTES = 260
TARGET_ECOUTES = 500_000
FIRST_USER_ID = 10001

GENRES = {  # genre : (poids global, durée min s, durée max s)
    "Pop": (0.19, 150, 240), "Rap FR": (0.18, 140, 230), "Électro": (0.12, 180, 360),
    "Rock": (0.13, 170, 300), "R&B": (0.07, 160, 250), "Variété française": (0.08, 160, 260),
    "Afro": (0.06, 160, 240), "Latino": (0.05, 160, 240), "Jazz": (0.035, 200, 420),
    "Classique": (0.03, 240, 720), "Metal": (0.025, 200, 380), "Lo-fi": (0.025, 110, 190),
}
GENRE_NAMES = list(GENRES)
G_W = np.array([GENRES[g][0] for g in GENRE_NAMES]); G_W /= G_W.sum()
GI = {g: i for i, g in enumerate(GENRE_NAMES)}

REGIONS = {  # région : poids (≈ population)
    "Île-de-France": 0.185, "Auvergne-Rhône-Alpes": 0.12, "Hauts-de-France": 0.09,
    "Nouvelle-Aquitaine": 0.09, "Occitanie": 0.09, "Grand Est": 0.08,
    "Provence-Alpes-Côte d'Azur": 0.077, "Pays de la Loire": 0.057, "Normandie": 0.05,
    "Bretagne": 0.05, "Bourgogne-Franche-Comté": 0.042, "Centre-Val de Loire": 0.038, "Corse": 0.005,
}
AGES = {"18-24": 0.25, "25-34": 0.30, "35-44": 0.20, "45-54": 0.13, "55-64": 0.08, "65+": 0.04}
# affinité genre selon l'âge (multiplicateurs)
AGE_AFFINITY = {
    "18-24": {"Rap FR": 1.8, "Afro": 1.6, "Latino": 1.3, "Lo-fi": 1.5, "Rock": 0.6, "Variété française": 0.5, "Jazz": 0.5, "Classique": 0.4},
    "25-34": {"Rap FR": 1.3, "Électro": 1.3, "Afro": 1.2, "R&B": 1.2},
    "35-44": {"Rock": 1.3, "Pop": 1.1, "Électro": 1.1},
    "45-54": {"Rock": 1.6, "Variété française": 1.5, "Jazz": 1.3, "Rap FR": 0.5},
    "55-64": {"Variété française": 2.0, "Rock": 1.5, "Jazz": 1.6, "Classique": 1.8, "Rap FR": 0.3, "Afro": 0.5},
    "65+": {"Variété française": 2.4, "Classique": 2.5, "Jazz": 1.8, "Rap FR": 0.2, "Électro": 0.4, "Afro": 0.4},
}

# ----------------------------------------------------------------------------
# Titres et artistes (noms fictifs)
# ----------------------------------------------------------------------------
PRENOMS = ["Lou", "Nina", "Sacha", "Elio", "Maé", "Noé", "Iris", "Malo", "Zoé", "Rayan", "Ines", "Timéo",
           "Lina", "Nael", "Jade", "Soline", "Yanis", "Alma", "Marius", "Céleste", "Kenza", "Oscar", "Rose", "Aya"]
SUFFIXES = ["Nova", "Lune", "Kairo", "Vega", "Orsay", "Blanc", "Sorel", "Mistral", "Azur", "Delta", "Ferro",
            "Lys", "Corail", "Onyx", "Saphir", "Rivière", "Prisme", "Echo", "Arcade", "Sable", "Volta", "Néon"]
GROUPES = ["Les", "The", "Collectif", "Duo", "Trio", "Orchestre", "Quartet", "Club"]
MOTS = ["Nuit", "Été", "Rivage", "Lumière", "Métro", "Horizon", "Silence", "Vertige", "Boulevard", "Néon", "Orage",
        "Comète", "Marée", "Saison", "Écho", "Asphalte", "Velours", "Miroir", "Sirène", "Tempête", "Pluie",
        "Cendre", "Aurore", "Minuit", "Ivresse", "Distance", "Satellite", "Mirage", "Voyage", "Carrousel"]
ADJS = ["bleue", "lente", "électrique", "perdue", "dorée", "infinie", "fragile", "sauvage", "douce", "brûlante",
        "secrète", "lointaine", "nouvelle", "parfaite", "immobile", "solaire", "rêveuse", "nocturne"]

artist_genre = rng.choice(len(GENRE_NAMES), size=N_ARTISTES, p=G_W)
artist_names, seen = [], set()
while len(artist_names) < N_ARTISTES:
    if rng.random() < 0.25:
        n = f"{rng.choice(GROUPES)} {rng.choice(SUFFIXES)}s"
    else:
        n = f"{rng.choice(PRENOMS)} {rng.choice(SUFFIXES)}"
    if n not in seen:
        seen.add(n); artist_names.append(n)

# chaque titre appartient à un artiste ; le genre du titre est celui de l'artiste
# (on garantit au moins 40 titres par genre)
titre_artist = []
for gi in range(len(GENRE_NAMES)):
    arts = np.where(artist_genre == gi)[0]
    if len(arts) == 0:
        arts = np.array([rng.integers(N_ARTISTES)]); artist_genre[arts[0]] = gi
    n = max(40, int(round(G_W[gi] * N_TITRES)))
    titre_artist += list(rng.choice(arts, size=n))
titre_artist = np.array(titre_artist)
N_TITRES = len(titre_artist)
titre_genre = artist_genre[titre_artist]
titles, seen = [], set()
for k in range(N_TITRES):
    while True:
        r = rng.random()
        if r < 0.45:
            t = f"{rng.choice(MOTS)} {rng.choice(ADJS)}"
        elif r < 0.75:
            t = f"{rng.choice(MOTS)} de {rng.choice(MOTS).lower()}"
        else:
            t = f"{rng.choice(MOTS)} {rng.integers(1, 99)}"
        if t not in seen:
            seen.add(t); break
    titles.append(t)
titre_duree = np.array([rng.integers(GENRES[GENRE_NAMES[g]][1], GENRES[GENRE_NAMES[g]][2] + 1) for g in titre_genre])
titre_annee = rng.choice(np.arange(1965, 2027), size=N_TITRES,
                         p=(lambda w: w / w.sum())(np.exp(np.linspace(-4, 0, 2027 - 1965))))
# popularité intra-genre (loi de Zipf)
titre_pop = np.zeros(N_TITRES)
genre_titres = {}
for gi in range(len(GENRE_NAMES)):
    idx = np.where(titre_genre == gi)[0]
    rng.shuffle(idx)
    w = 1.0 / np.arange(1, len(idx) + 1) ** 0.9
    titre_pop[idx] = w / w.sum()
    genre_titres[gi] = (idx, w / w.sum())
TITRE_ID0 = 1
titres = pd.DataFrame({
    "id_titre": np.arange(TITRE_ID0, TITRE_ID0 + N_TITRES),
    "titre": titles,
    "artiste": [artist_names[a] for a in titre_artist],
    "genre": [GENRE_NAMES[g] for g in titre_genre],
    "duree_secondes": titre_duree,
    "annee_sortie": titre_annee,
})

# ----------------------------------------------------------------------------
# Utilisateurs
# ----------------------------------------------------------------------------
uid = np.arange(FIRST_USER_ID, FIRST_USER_ID + N_USERS)
ages = rng.choice(list(AGES), size=N_USERS, p=np.array(list(AGES.values())) / sum(AGES.values()))
regions = rng.choice(list(REGIONS), size=N_USERS, p=np.array(list(REGIONS.values())) / sum(REGIONS.values()))
early = rng.random(N_USERS) < 0.76
d_early = [date(2022, 1, 3) + timedelta(days=int(x)) for x in rng.integers(0, (PERIOD_START - date(2022, 1, 3)).days, N_USERS)]
d_late = [PERIOD_START + timedelta(days=int(x)) for x in rng.integers(0, N_DAYS - 20, N_USERS)]
inscription = [a if e else b for a, b, e in zip(d_early, d_late, early)]
utilisateurs = pd.DataFrame({"id_utilisateur": uid, "tranche_age": ages, "region": regions,
                             "date_inscription": inscription})

# ----------------------------------------------------------------------------
# Abonnements (périodes contiguës, sans chevauchement ; date_fin exclue)
# ----------------------------------------------------------------------------
def rand_date(a, b):
    """date uniforme dans [a, b)"""
    if b <= a:
        return a
    return a + timedelta(days=int(rng.integers(0, (b - a).days)))

abon_rows = []          # (id_utilisateur, offre, debut, fin, statut)
user_segments = {}      # uid -> liste (offre, debut, fin) des périodes actives (pour les écoutes)
user_churn = {}
for k in range(N_USERS):
    u = int(uid[k]); I = inscription[k]
    offre = "premium" if rng.random() < 0.34 else "gratuit"
    lines = []
    start = I
    # historique avant la période : un ancien abonnement d'une autre offre (25 % des anciens)
    if I < PERIOD_START - timedelta(days=60) and rng.random() < 0.25:
        sw = rand_date(I + timedelta(days=30), PERIOD_START - timedelta(days=15))
        lines.append([("gratuit" if offre == "premium" else "premium"), I, sw, "termine"])
        start = sw
    lo = max(start, PERIOD_START) + timedelta(days=7)
    hi = PERIOD_END - timedelta(days=2)
    events = []
    p_switch = 0.17 if offre == "gratuit" else 0.07
    if rng.random() < p_switch and lo < hi:
        events.append(("switch", rand_date(lo, hi)))
    if rng.random() < 0.09 and lo < hi:
        c = rand_date(lo, hi)
        if events and c <= events[0][1]:
            c = rand_date(events[0][1] + timedelta(days=5), PERIOD_END) if events[0][1] + timedelta(days=5) < PERIOD_END else None
        if c and c < PERIOD_END:
            events.append(("churn", c))
    cur_off, cur_start = offre, start
    for kind, d in sorted(events, key=lambda e: e[1]):
        if kind == "switch":
            lines.append([cur_off, cur_start, d, "termine"])
            cur_off = "premium" if cur_off == "gratuit" else "gratuit"
            cur_start = d
        else:
            # export pas encore à jour : résiliation dans les 14 derniers jours encore « actif »
            st = "actif" if d >= PERIOD_END - timedelta(days=14) else "resilie"
            lines.append([cur_off, cur_start, d, st])
            user_churn[u] = d
            cur_off = None
    if cur_off is not None:
        lines.append([cur_off, cur_start, None, "actif"])
    for off, a, b, st in lines:
        abon_rows.append((u, off, a, b, st))
    segs = []
    for off, a, b, st in lines:
        a2 = max(a, PERIOD_START, I)
        b2 = min(b or PERIOD_END, PERIOD_END)
        if a2 < b2:
            segs.append((off, a2, b2))
    user_segments[u] = segs

abonnements = pd.DataFrame(abon_rows, columns=["id_utilisateur", "offre", "date_debut", "date_fin", "statut"])
abonnements.insert(0, "id_abonnement", np.arange(1, len(abonnements) + 1))

# ----------------------------------------------------------------------------
# Profils d'écoute
# ----------------------------------------------------------------------------
base = rng.lognormal(mean=0.0, sigma=0.9, size=N_USERS)
dormant = rng.random(N_USERS) < 0.02            # comptes quasi inactifs
base[dormant] *= 0.01
pref = np.zeros((N_USERS, len(GENRE_NAMES)))
for k in range(N_USERS):
    aff = np.array([AGE_AFFINITY[ages[k]].get(g, 1.0) for g in GENRE_NAMES])
    pref[k] = rng.dirichlet(G_W * aff / (G_W * aff).sum() * 6.0) * 0.7 + (G_W * aff / (G_W * aff).sum()) * 0.3

# décrochage : abonnés premium actifs à la fin de la période
last_day = PERIOD_END - timedelta(days=1)
decl_factor = {}
for k in range(N_USERS):
    u = int(uid[k]); segs = user_segments[u]
    if segs and segs[-1][0] == "premium" and segs[-1][2] == PERIOD_END and not dormant[k]:
        r = rng.random()
        if r < 0.07:   decl_factor[u] = 0.0       # silencieux depuis 30 jours
        elif r < 0.11: decl_factor[u] = 0.15
        elif r < 0.15: decl_factor[u] = 0.35
        elif r < 0.20: decl_factor[u] = 0.6

def season(d):
    m = d.month
    return {12: 1.15, 1: 1.05, 7: 0.86, 8: 0.82, 9: 0.97}.get(m, 1.0)

day_season = np.array([season(d) for d in DAYS])
DAY_WE = np.array([d.weekday() >= 5 for d in DAYS])
DAY_MONTH = np.array([d.year * 12 + d.month - 1 for d in DAYS])
DAY64 = np.array([np.datetime64(d) for d in DAYS]).astype('datetime64[s]')
day_weekend = np.array([1.12 if d.weekday() >= 5 else 1.0 for d in DAYS])
Q3_START, Q2_START = date(2026, 7, 1), date(2026, 4, 1)

def genre_factor(d):
    f = np.ones(len(GENRE_NAMES))
    if d >= Q3_START:                         # le Rock décroche au 3e trimestre 2026
        f[GI["Rock"]] = 0.58
    if d.month in (7, 8):                     # tubes de l'été
        f[GI["Latino"]] *= 1.5; f[GI["Afro"]] *= 1.35
    if d.month == 12:
        f[GI["Classique"]] *= 1.35
    return f

HOURS_WEEK = np.array([1.0, .6, .4, .3, .3, .6, 2.0, 4.5, 5.5, 4.0, 3.5, 3.8, 4.8, 4.6, 3.6, 3.6, 4.2, 5.2, 6.2, 6.8, 7.2, 7.0, 5.5, 3.0])
HOURS_WEND = np.array([1.8, 1.2, .8, .5, .3, .3, .5, 1.0, 2.0, 3.2, 4.2, 4.8, 5.0, 4.8, 4.6, 4.6, 4.8, 5.2, 5.8, 6.4, 7.0, 7.2, 6.2, 4.0])
HOURS_WEEK /= HOURS_WEEK.sum(); HOURS_WEND /= HOURS_WEND.sum()
TERM = {"gratuit": (["mobile", "web", "desktop"], [0.72, 0.18, 0.10]),
        "premium": (["mobile", "desktop", "enceinte", "tv", "web"], [0.55, 0.17, 0.14, 0.06, 0.08])}

# calibrage : nombre attendu d'écoutes -> facteur d'échelle
def user_day_rates(k):
    u = int(uid[k]); rates = np.zeros(N_DAYS); offers = np.empty(N_DAYS, dtype=object)
    for off, a, b in user_segments[u]:
        i0, i1 = (a - PERIOD_START).days, (b - PERIOD_START).days
        rates[i0:i1] = base[k] * (2.3 if off == "premium" else 1.0)
        offers[i0:i1] = off
    rates *= day_season * day_weekend
    if u in user_churn:                       # moins d'écoutes avant une résiliation
        c = (user_churn[u] - PERIOD_START).days
        rates[max(0, c - 30):c] *= 0.5
    if u in decl_factor:
        rates[N_DAYS - 30:] *= decl_factor[u]
    return rates, offers

expected = sum(user_day_rates(k)[0].sum() for k in range(N_USERS))
SCALE = TARGET_ECOUTES / expected

rows_u, rows_t, rows_ts, rows_d, rows_term = [], [], [], [], []
for k in range(N_USERS):
    u = int(uid[k])
    rates, offers = user_day_rates(k)
    counts = rng.poisson(rates * SCALE)
    if counts.sum() == 0:
        continue
    day_idx = np.repeat(np.arange(N_DAYS), counts)
    n = len(day_idx)
    # heure
    is_we = DAY_WE[day_idx]
    hours = np.where(is_we, rng.choice(24, size=n, p=HOURS_WEND), rng.choice(24, size=n, p=HOURS_WEEK))
    secs = hours * 3600 + rng.integers(0, 3600, size=n)
    # genre puis titre (préférences x saisonnalité des genres)
    gsel = np.empty(n, dtype=int)
    months = DAY_MONTH[day_idx]
    for mo in np.unique(months):
        mask = months == mo
        p = pref[k] * genre_factor(date(int(mo) // 12, int(mo) % 12 + 1, 1)); p /= p.sum()
        gsel[mask] = rng.choice(len(GENRE_NAMES), size=mask.sum(), p=p)
    tsel = np.empty(n, dtype=int)
    for gi in np.unique(gsel):
        m = gsel == gi
        idx, w = genre_titres[gi]
        tsel[m] = rng.choice(idx, size=m.sum(), p=w)
    # terminal et durée selon l'offre du jour
    offs = offers[day_idx]
    term = np.empty(n, dtype=object)
    dur = np.empty(n, dtype=int)
    for off in ("gratuit", "premium"):
        m = offs == off
        if not m.any():
            continue
        labels, p = TERM[off]
        term[m] = rng.choice(labels, size=m.sum(), p=p)
        full = titre_duree[tsel[m]]
        r = rng.random(m.sum())
        skip_p = 0.26 if off == "gratuit" else 0.14
        d_skip = rng.integers(5, 30, size=m.sum())
        d_part = (rng.uniform(0.15, 0.9, size=m.sum()) * full).astype(int).clip(30)
        d_full = full - rng.integers(0, 4, size=m.sum())
        dur[m] = np.where(r < skip_p, d_skip, np.where(r < skip_p + 0.22, d_part, d_full))
    rows_u.append(np.full(n, u)); rows_t.append(tsel + TITRE_ID0)
    rows_ts.append(DAY64[day_idx] + secs.astype("timedelta64[s]"))
    rows_d.append(dur); rows_term.append(term)

ecoutes = pd.DataFrame({
    "id_utilisateur": np.concatenate(rows_u),
    "id_titre": np.concatenate(rows_t),
    "horodatage": np.concatenate(rows_ts),
    "duree_ecoutee": np.concatenate(rows_d),
    "terminal": np.concatenate(rows_term),
}).sort_values(["horodatage", "id_utilisateur"]).reset_index(drop=True)
ecoutes.insert(0, "id_ecoute", np.arange(1, len(ecoutes) + 1))

# ----------------------------------------------------------------------------
# Playlists (activité P1C3) — date_ajout au format jj/mm/aaaa : piège volontaire
# ----------------------------------------------------------------------------
NOMS_PL = ["Road trip", "Focus", "Running", "Soirée", "Dimanche matin", "Chill", "Apéro", "Workout", "Pluie",
           "Découvertes", "Nostalgie", "Cuisine", "Trajet", "Été", "Concentration", "Fête", "Réveil", "Sieste"]
pl_rows = []
pl_id = 1
owners = rng.choice(uid, size=2400, replace=True,
                    p=(lambda w: w / w.sum())(np.where(abonnements.groupby("id_utilisateur")["offre"].apply(lambda s: (s == "premium").any()).reindex(uid).fillna(False).values, 3.0, 1.0)))
for u in owners:
    k = int(u - FIRST_USER_ID)
    nom = f"{rng.choice(NOMS_PL)}" + ("" if rng.random() < 0.6 else f" {rng.integers(2, 9)}")
    n = int(rng.integers(4, 26))
    created = rand_date(max(inscription[k], PERIOD_START - timedelta(days=120)), PERIOD_END - timedelta(days=1))
    g = rng.choice(len(GENRE_NAMES), size=n, p=pref[k])
    chosen = set()
    for gi in g:
        idx, w = genre_titres[gi]
        t = int(rng.choice(idx, p=w))
        if t in chosen:
            continue
        chosen.add(t)
        da = rand_date(created, PERIOD_END)
        pl_rows.append((pl_id, nom, int(u), t + TITRE_ID0, da))
    pl_id += 1
playlists = pd.DataFrame(pl_rows, columns=["id_playlist", "nom_playlist", "id_utilisateur", "id_titre", "date_ajout"])
# quelques titres ajoutés deux fois à la même playlist (surprise réaliste)
dup = playlists.sample(n=37, random_state=args.seed).copy()
dup["date_ajout"] = [d + timedelta(days=int(rng.integers(1, 40))) if d + timedelta(days=40) < PERIOD_END else d for d in dup["date_ajout"]]
playlists = pd.concat([playlists, dup]).sort_values(["id_playlist", "date_ajout"]).reset_index(drop=True)

# ----------------------------------------------------------------------------
# Écriture
# ----------------------------------------------------------------------------
def fmt_date(d):
    return "" if d is None or (isinstance(d, float) and np.isnan(d)) or pd.isna(d) else d.strftime("%Y-%m-%d")

utilisateurs.assign(date_inscription=utilisateurs.date_inscription.map(fmt_date)) \
    .to_csv(os.path.join(args.out, "utilisateurs.csv"), index=False)
titres.to_csv(os.path.join(args.out, "titres.csv"), index=False)
abonnements.assign(date_debut=abonnements.date_debut.map(fmt_date), date_fin=abonnements.date_fin.map(fmt_date)) \
    .to_csv(os.path.join(args.out, "abonnements.csv"), index=False)
ts_fmt = "%Y-%m-%d %H:%M:%S" if args.horodatage == "iso" else "%d/%m/%Y %H:%M:%S"
ecoutes.assign(horodatage=pd.to_datetime(ecoutes.horodatage).dt.strftime(ts_fmt)) \
    .to_csv(os.path.join(args.out, "ecoutes.csv"), index=False)
playlists.assign(date_ajout=playlists.date_ajout.map(lambda d: d.strftime("%d/%m/%Y"))) \
    .to_csv(os.path.join(args.out, "playlists.csv"), index=False)

for name, df in [("utilisateurs", utilisateurs), ("titres", titres), ("abonnements", abonnements),
                 ("ecoutes", ecoutes), ("playlists", playlists)]:
    print(f"{name:13s} {len(df):>8,d} lignes")
