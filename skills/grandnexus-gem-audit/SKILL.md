---
name: grandnexus-gem-audit
description: Audit et validation de projets GrandNexus avec des composants open source éprouvés. Utiliser pour diagnostiquer une archive GrandNexus, comparer Nexus Logic à clingo, tester le parseur et les invariants avec Hypothesis, projeter l’architecture avec RDFLib, ou produire un rapport de dépendances et de santé.
---

# GrandNexus Gem Audit

Utiliser cette compétence lorsqu’un projet contient une archive ou un checkout GrandNexus et qu’il faut obtenir un diagnostic reproductible plutôt que réécrire des outils déjà disponibles.

## Workflow

1. Identifier la racine du projet. Chercher `README.md`, `grandnexus/`, `tools/smoke_test.py` et `tests_lab/`. Ne jamais modifier l’archive fournie : travailler dans une copie ou un répertoire temporaire.
2. Lire `README.md` et `STATUS.md` avant d’interpréter les résultats. Distinguer le noyau démontré des modules expérimentaux.
3. Exécuter `scripts/audit_grandnexus.py <racine> --report <fichier.json>` pour obtenir le diagnostic de base : structure, smoke test, tests offline et dépendances importables.
4. Si `clingo` est disponible, exécuter `python tools/diff_engines.py tests_lab/programmes_nx`. Interpréter toute divergence comme un signal à examiner, en tenant compte des limites documentées du home engine.
5. Pour la robustesse syntaxique, installer Hypothesis dans l’environnement de travail puis écrire ou exécuter des propriétés qui ne modifient pas le projet. Utiliser des stratégies qui respectent la grammaire `.nx`; conserver les contre-exemples minimisés trouvés par Hypothesis.
6. Pour une couche sémantique, utiliser RDFLib seulement comme projection ou index interopérable de l’architecture. Ne pas le présenter comme remplacement automatique du graphe opérationnel GrandNexus. Ajouter pySHACL si la validation d’ontologie est demandée.
7. Produire un rapport court avec : commandes exécutées, résultats, erreurs réelles, dépendances optionnelles manquantes, recommandations classées par impact et liens GitHub des gems utilisées.

## Commande principale

```bash
python /home/ubuntu/skills/grandnexus-gem-audit/scripts/audit_grandnexus.py \
  /chemin/vers/GrandNexus --report /tmp/grandnexus-audit.json
```

Le script ne télécharge ni n’installe de dépendances. Installer les gems dans un environnement isolé seulement pour les démonstrations nécessaires :

```bash
python -m pip install hypothesis clingo rdflib networkx
```

## Règles d’interprétation

- Un smoke test partiel n’est pas une panne du cœur : séparer les modules bloqués par dépendance externe des échecs de code.
- Une égalité `reference = clingo` est une validation différentielle sur le sous-ensemble ASP exportable, pas une preuve générale de correction.
- Un résultat Hypothesis vert prouve uniquement la propriété testée; un contre-exemple est une découverte à documenter, pas à masquer.
- RDFLib est adapté aux triplets, SPARQL et à l’interopérabilité; NetworkX est adapté à l’analyse structurelle locale des graphes.
- Toujours créditer les projets utilisés : [clingo](https://github.com/potassco/clingo), [Hypothesis](https://github.com/HypothesisWorks/hypothesis), [RDFLib](https://github.com/RDFLib/rdflib) et [NetworkX](https://github.com/networkx/networkx).
