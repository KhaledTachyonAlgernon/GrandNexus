# GrandNexus Gem Audit

Compétence Manus pour auditer les snapshots GrandNexus structurés (`grandnexus/`, `tools/`, `tests_lab/`) avec des projets open source éprouvés.

## Utilisation

```bash
python skills/grandnexus-gem-audit/scripts/audit_grandnexus.py \
  /chemin/vers/GrandNexus --report /tmp/grandnexus-audit.json
```

La compétence couvre notamment :

- la comparaison différentielle de Nexus Logic avec [clingo](https://github.com/potassco/clingo) ;
- les tests génératifs du parseur avec [Hypothesis](https://github.com/HypothesisWorks/hypothesis) ;
- la projection sémantique et les requêtes SPARQL avec [RDFLib](https://github.com/RDFLib/rdflib) ;
- l’analyse de graphes locaux avec [NetworkX](https://github.com/networkx/networkx).

Le script est en lecture seule vis-à-vis du projet audité et ne télécharge ni n’installe de dépendances.
