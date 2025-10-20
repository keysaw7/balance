### Zeus — Vision fondatrice

> « Concevoir une intelligence collective, ouverte et digne de confiance, au service du bien commun. »

---

## 1. Mission

Zeus est un écosystème d’intelligence artificielle open source destiné à aider les sociétés humaines à concevoir, débattre et mettre en œuvre des politiques publiques, des projets et des stratégies alignés sur la durabilité, l’équité, l’efficacité et le bien-être collectif. 

- **Pourquoi**: outiller la décision publique et citoyenne face à des systèmes complexes (climat, santé, éducation, économie, mobilité) en rendant l’analyse transparente, traçable et explicable.
- **Pour qui**: citoyens, associations, collectivités, chercheurs, journalistes, décideurs publics, entreprises à mission.
- **Comment**: une interface citoyenne participative, un moteur d’IA central pour l’analyse et la simulation, un système de données sécurisé et auditable, et une gouvernance technique démocratique garantissant l’évolution du modèle sous contrôle public.

> Encadré — **Finalité sociale**
>
> - Servir le bien commun sans captation privée du contrôle.
> - Favoriser l’inclusion, la pluralité et la délibération informée.
> - Préserver les droits fondamentaux: vie privée, liberté d’expression, non-discrimination.

---

## 2. Principes fondateurs

- **Open source intégral**: code, documentation, décisions de gouvernance et journaux d’audit publiquement accessibles; reproductibilité par conception.
- **Transparence et traçabilité**: sources de données, hypothèses, modèles, critères d’optimisation, explications et limites sont documentés et consultables.
- **Démocratie technologique**: les évolutions du modèle sont validées par un référendum technique associant la communauté d’ingénierie et un vote citoyen consultatif.
- **Respect de la vie privée (privacy by design)**: consentement explicite, minimisation, anonymisation robuste, chiffrement bout-en-bout, contrôle utilisateur et droit à l’oubli.
- **Neutralité et pluralisme**: pluralité de perspectives, publication des alternatives sur la frontière de Pareto, explicitation des arbitrages de valeurs.
- **Responsabilité collective**: gouvernance ouverte, gestion des conflits d’intérêts, revues indépendantes, rapports d’impact.

> Encadré — **Principe de transparence**
>
> - Toute recommandation est accompagnée d’explications lisibles, d’analyses de sensibilité et de liens vers les données et hypothèses.
> - Les limites et incertitudes sont affichées en premier.

> Encadré — **Principe de vie privée**
>
> - Recueil de consentements granulaires, révocables à tout moment.
> - Anonymisation par défaut, pseudonymisation contrôlée, et options de confidentialité renforcée.

---

## 3. Architecture globale et piliers techniques

### 3.1 Interface citoyenne participative (web et mobile)

- **Fonctionnalités cœur**:
  - Expression d’idées, priorités, propositions; débats argumentés et délibération.
  - Consentement explicite et granulaire (données contextuelles, localisation, historiques).
  - Tableau de bord personnel: accès, téléchargement, correction et suppression des données.
  - Boucles de retour: visualisation des impacts des contributions sur analyses et recommandations.
- **Protection des données**:
  - Anonymisation locale quand possible; chiffrement en transit (TLS) et au repos (AES-256).
  - Stockage segmenté et politiques de rétention minimales; masquage par défaut.
- **Expérience et accessibilité**:
  - Design inclusif, multilingue, WCAG AA+, faible bande passante, mode hors-ligne.

> Encadré — **Consentement éclairé**
>
> - Résumés lisibles des usages et bénéfices; bandeau de consentement granulaire.
> - Journal des consentements exportable, horodaté, réversible.

### 3.2 Moteur d’analyse et de simulation Zeus (IA centrale)

- **Objectifs**: cartographier besoins/ressources, simuler scénarios, évaluer politiques selon des critères multi-objectifs (durabilité, équité, efficacité, bien-être).
- **Approche**:
  - Combinaison de modèles: LLM explicables, graphes socio-techniques, séries temporelles, optimisation multi-critères.
  - Explicabilité systématique: chaînes de raisonnement auditées, cartes d’influence, analyses de sensibilité, contre-factuels.
  - Équité et robustesse: détection de biais, contraintes d’équité, tests adversariaux, validation croisée.
- **Capacités de simulation**:
  - Scénarios (court/long terme), chocs exogènes, budgets et contraintes réelles.
  - Publication d’un ensemble de solutions pareto-optimales avec explications.

> Encadré — **Optimisation multi-critères**
>
> - Présentation de plusieurs solutions non dominées plutôt qu’un unique « optimum ».
> - Exposition des compromis explicites et des critères dominants.

### 3.3 Système de données (architecture, sécurité, anonymisation)

- **Architecture**:
  - Lakehouse avec zones (raw/clean/curated), catalogage, versionnage de données (data versioning).
  - Gouvernance de schémas et lignage (data lineage) traçable de bout en bout.
- **Sécurité**:
  - Chiffrement au repos et en transit; gestion de clés (KMS/HSM), rotation, double contrôle.
  - Contrôles d’accès RBAC/ABAC, cloisonnement par domaine, journaux d’accès immuables.
- **Confidentialité**:
  - Anonymisation: k-anonymity, l-diversity; confidentialité différentielle pour analyses agrégées.
  - Pseudonymisation avec clés séparées; suppression vérifiable (« effacement prouvé »).
- **Qualité et provenance**:
  - Scores de qualité, tests de données, fiches de jeux de données (datasheets).
  - Labels de provenance, licences et restrictions d’usage intégrées.

> Encadré — **Anonymisation responsable**
>
> - Préférence pour traitements sur agrégats; réduction systématique de granularité.
> - Tests d’attaques de ré-identification et seuils de publication.

### 3.4 Gouvernance technique démocratique (référendum, versioning, audit)

- **Processus**:
  1. Propositions publiques documentées (code, données non sensibles, architecture, pondérations).
  2. Revue ouverte, débats techniques, analyses d’impact et d’équité.
  3. Vote du conseil technique (pondéré par expertise) + vote citoyen consultatif.
  4. Seuils de validation, quorum et période de commentaires.
  5. Déploiement contrôlé; archivage et versioning des décisions (registre public).
- **Garantie d’intégrité**:
  - Registre append-only (horodatage, signatures, hachages); liens vers artefacts et tests.
  - Déclarations de conflits d’intérêts; audits indépendants réguliers.

> Encadré — **Référendum technique**
>
> - « Pas de déploiement sans validation collective ».
> - Chaque version documente: changements, jeux de données, métriques, risques, atténuations.

### 3.5 Mécanisme de décision multi-échelle (local → global)

- **Subsidiarité et cohérence**:
  - Décisions prises au niveau le plus proche des citoyens, avec contraintes de cohérence inter-échelles.
- **Agrégation**:
  - Pondérations par population, vulnérabilités, capacités locales; consolidation ascendante.
- **Cadre d’arbitrage**:
  - Frontière de Pareto, scores composites paramétrables, règles lexicographiques pour droits fondamentaux.
  - Publication des alternatives et justifications des arbitrages.

> Encadré — **Du quartier au monde**
>
> - Les scénarios locaux alimentent des projections régionales et nationales; retour d’expériences réinjecté.

---

## 4. Philosophie d’intelligence collective

- **Humains et IA comme co-créateurs**: l’IA éclaire et structure; les humains décident et orientent les valeurs.
- **Délibération augmentée**: synthèse d’arguments, mise en évidence des désaccords féconds, scénarios comparatifs.
- **Contrôle humain**: garde-fous explicites, possibilité de refuser, éditer, ou prioriser les recommandations.

> Encadré — **Explicabilité d’abord**
>
> - Chaque sortie est accompagnée d’explications, d’alternatives et d’effets attendus.

---

## 5. Étapes de développement

### 5.1 MVP (3–4 mois)
- Collecte citoyenne minimale (idées, priorités), consentement granulaire, tableau de bord données.
- Premières analyses descriptives et visualisations; prototypes d’explication.
- Gouvernance: registre public de décisions, premiers RFC, vote technique expérimental.

### 5.2 Prototype Alpha (6–8 mois)
- Simulations simples multi-critères; publication de 2–3 alternatives pareto-optimales.
- Pipeline de données versionné, anonymisation automatisée, audit d’accès.
- Tests citoyens en environnement contrôlé; rapports d’impact et d’équité.

### 5.3 Bêta publique (9–12 mois)
- Élargissement des domaines (climat, mobilité, santé publique selon données disponibles).
- Gouvernance formalisée (quorum, seuils); audits externes; bug bounties.
- Outillage pour collectivités pilotes; API publiques et SDKs.

### 5.4 Déploiement itératif
- Montée en charge; résilience; monitoring SLO/SLA.
- Programmes de médiation scientifique et formation.

> Encadré — **Critères de succès**
>
> - Inclusion (diversité des participants), amélioration de la qualité délibérative, utilité perçue.
> - Réduction des biais, conformité RGPD, zéro incident majeur de confidentialité.

---

## 6. Indicateurs et audit

- **Indicateurs sociaux**: participation, diversité, satisfaction, confiance.
- **Indicateurs techniques**: disponibilité, latence, robustesse, couverture de tests, dettes techniques.
- **Indicateurs d’équité**: disparités d’impact, fairness metrics, analyses de sous-groupes.
- **Confidentialité**: incidents, temps moyen de suppression, résultats d’attaques de ré-identification.
- **Traçabilité**: complétude des journaux, reproductibilité des résultats, taux d’explications acceptées.

---

## 7. Risques et atténuations

- **Biais et discrimination**: audits d’équité; contraintes d’équité en optimisation; diversité des données.
- **Captation de gouvernance**: pluralisme institutionnel, transparence financière, rotation des rôles.
- **Empoisonnement de données**: validation des sources, filtres anti-spam, détection d’anomalies.
- **Atteintes à la vie privée**: minimisation, chiffrement, tests d’attaques, confidentialité différentielle.
- **Sur-dépendance à l’IA**: formation et pédagogie, « humain en dernier ressort », publication d’alternatives.

---

## 8. Licences, éthique et cadre juridique

- **Licences proposées**: 
  - Code serveur: AGPL-3.0 (garantit la réciprocité pour services).
  - SDKs/clients: Apache-2.0 (favorise l’extension et l’adoption).
  - Données non sensibles: licences ouvertes compatibles (ODC-By, CC-BY), selon sources.
- **Conformité**: RGPD, ePrivacy, cadres nationaux; DPIA et registres de traitement.
- **Comité d’éthique**: veille, arbitrages, audits de valeurs et de risques.

---

## 9. Roadmap synthétique

- T0–T4 mois: MVP, collecte et transparence.
- T4–T12 mois: simulations, gouvernance formalisée, pilotes territoriaux.
- > T12 mois: échelle nationale/régionale, APIs, écosystème partenaires.

---

## 10. Glossaire (extrait)

- **Frontière de Pareto**: ensemble de solutions non dominées selon plusieurs critères.
- **Confidentialité différentielle**: technique garantissant la confidentialité statistique d’individus.
- **Lignage de données (lineage)**: traçabilité des transformations et usages d’un jeu de données.
- **Subsidiarité**: principe d’allocation des décisions au niveau le plus proche pertinent.

---

## 11. Périmètre et limites

Zeus n’impose pas de décisions: il propose, explique et éclaire. Les décisions appartiennent aux humains, dans des cadres démocratiques. Les limites de données, d’incertitude et de valeurs sont explicitées pour éviter l’illusion de certitude.

> Encadré — **Boussole du projet**
>
> - Ouverture, sobriété, explicabilité, justice, sécurité.
> - Toujours laisser une porte ouverte à la contestation informée et à l’alternative.
