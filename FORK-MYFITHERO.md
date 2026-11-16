# Fork MyFitHero

Ce dépôt est la copie (fork) de `Jakeschincariol/founder-skill` utilisée par le
projet MyFitHero. L'original n'a pas bougé depuis sa v1.0 (dernière vérification :
16/11/2026). Ce fork y ajoute ce que les analyses MyFitHero ont appris depuis le
22/10/2026.

## Ce qui diffère de l'original

| Où | Changement | Pourquoi |
|---|---|---|
| `skills/founder-subscription/` (nouveau) | CFO pour app à abonnement : commissions Apple/Google/web, remboursements, LTV, CAC, 3 scénarios de stress, `--hold` (installations à trouver chaque mois pour tenir N payants), `--budget` (payants qu'un budget pub permet de tenir) | Le CFO d'origine est taillé pour un café (prix unitaire, ventes par jour, loyer). Outil né le 22/10/2026, enrichi des calculs du business plan du 15/11/2026 |
| Toutes les entrées marché | Source publique datée, lue pour l'analyse en cours. Les anciens chiffres de `founder/` et du dépôt sont obsolètes par défaut | Décision de Christophe, 15/11/2026 |
| `founder-consumer` | Panel hostile : objections d'abord, le taux d'achat simulé n'est jamais présenté comme une demande ni utilisé comme conversion | Les acheteurs simulés penchent vers l'accord (limite que l'original écrit lui-même) : leur taux d'achat est un plafond, pas une mesure |
| `founder-pricing` | Van Westendorp = fourchette de prix seulement sur de vraies réponses ; sur le panel simulé, ce sont des candidats à tester | L'audit du 03/11 avait tiré une fourchette 4-15 $ d'un panel simulé |
| `founder-launch` | Étape 0 : pré-mortem et critères d'arrêt chiffrés, écrits avant de dépenser | Repris de `launch-test.md` (22/10/2026) |
| `founder-cfo`, `founder-plan` | Renvoient vers `founder-subscription` pour une app ; le taux d'achat simulé ne nourrit plus la rampe ni le verdict | Même raison que le panel |
| `skills/founder-killtest/` (nouveau, 16/11/2026) | Test de mise à mort avant une dépense : dossier figé, échelle de preuves (payé > action coûteuse > intention déclarée > attention > analogie), quatre relecteurs aveugles, verdict KILL / HOLD / VALIDATE / ADVANCE, trois tests réels les moins chers avec seuil écrit d'avance, registre en ajout seul | Adapté de SensaiXo/kill-it-first (MIT, licence copiée dans le dossier). Utile avant de payer les micro-influenceurs |
| `founder-launch` (16/11/2026) | Les 30 premiers jours deviennent 90 jours en trois blocs (mesurer, convertir, décider), chacun fermé par une décision écrite d'avance | Une app ne lit son revenu par installation qu'autour du 60e jour. Rédaction propre au fork |
| `founder-subscription` (16/11/2026) | Chaque URL citée est ouverte et vérifiée avant le calcul | Idée reprise de alinaqi/ideavalidator (MIT) |
| Correctifs de fiabilité | Repris de la proposition #7 de l'original (non fusionnée là-bas) : `--quick`, nettoyage des réponses au ré-init, virgule décimale, verdict sans coûts = Incomplete | Bugs réels de l'original |

## Se resynchroniser avec l'original

```bash
git remote add upstream https://github.com/Jakeschincariol/founder-skill
git fetch upstream
git merge upstream/main   # sur une branche, jamais sur main directement
```

Les changements du fork sont rangés dans des sections marquées « MyFitHero fork »
pour que les conflits restent lisibles.

## Dépôts examinés le 16/11/2026 et non repris

| Dépôt | Licence | Pourquoi pas |
|---|---|---|
| CaptainCPO/startup-viability-check | CC BY-NC 4.0 (usage commercial interdit sans accord écrit) | MyFitHero est commercial : rien copié. Le plan à 90 jours de `founder-launch` est écrit indépendamment, sans reprendre son texte |
| MaxKmet/idea-validation-agents | MIT | Valide une idée avant de la construire ; ses repères de CAC et de rétention ne sont pas sourcés ; la note sur 100 donne une fausse précision |
| alinaqi/ideavalidator | MIT | Pipeline lourde (clé Gemini ou compte Palgu), pensée pour une idée. Seule la vérification des citations est reprise |
| Nirikshan95/VettIQ | MIT | Application FastAPI + Streamlit avec un modèle hébergé : pas un skill, et ses avis sont générés par IA |
