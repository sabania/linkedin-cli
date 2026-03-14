---
name: ideas
description: Content-Ideen aus 8 Quellen generieren. Feed Trends, Competitor Gaps, Repurposing, Patterns, News, Experiments, Audience Requests, User Input.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
  - WebSearch
---

# /ideas — Ideen generieren

Generiert Content-Ideen aus 8 verschiedenen Quellen für maximale Vielfalt und Relevanz.

**WICHTIG: Delegiere die Arbeit an den `content-writer` Agent. Mach NICHTS selbst — starte den Agent mit dem `Agent`-Tool und übergib Anzahl + optionalen Pillar.**

## Verwendung

```
/ideas              # 5 Ideen aus allen Quellen (Default)
/ideas 10           # 10 Ideen
/ideas AI Praxis    # Ideen für spezifischen Pillar
```

## 8 Quellen

1. **Feed Trends** — Was ist gerade hot im Feed?
2. **Competitor Gaps** — Themen die Competitors bespielen, du nicht
3. **Repurposing** — Guter alter Content neu aufbereitet
4. **Pattern-Driven** — Ideas die bewährte Patterns nutzen
5. **News/WebSearch** — Aktuelle Events in deiner Nische
6. **Experiment-Driven** — Posts für laufende Experimente
7. **Audience Requests** — Was deine Audience in Kommentaren fragt
8. **User Input** — Dein Thema in verschiedene Angles

## Ablauf

1. **`content-writer` Agent** starten mit Anzahl und optionalem Pillar
2. **Ideen präsentieren:**

```
Content-Ideen (5):

1. 📈 "Die meisten AI-Projekte scheitern nicht an der Tech..."
   Pillar: AI Praxis | Hook: Surprising Fact | Format: Text
   Quelle: Feed Trend ("AI Agents" trending diese Woche)
   Warum: Trending Topic + dein stärkster Pillar

2. 🔄 "So habe ich in einem Wochenende einen CLI gebaut..."
   Pillar: Side Projects | Hook: Personal Story | Format: Carousel
   Quelle: Repurpose (Original: URN:123, 89 Reactions aber nur 1.2k Impressions)
   Warum: Guter Content verdient mehr Reach, Carousel = 3x Impressions (Pattern)

3. ❓ "Braucht ein 10-Personen-Team wirklich ein AI-Tool?"
   Pillar: AI Praxis | Hook: Question | Format: Text
   Quelle: Experiment (hook-type-v1: Question-Variante, braucht noch 2 Posts)
   Warum: Experiment läuft, Question-Hooks brauchen mehr Datenpunkte

4. 🏢 "Was Apostroph über AI-Übersetzung gelernt hat..."
   Pillar: Behind the Scenes | Hook: Behind-Scenes | Format: Document
   Quelle: Competitor Gap (@competitor-1 postet darüber, du nicht)
   Warum: Content Gap schliessen, Behind-Scenes ist unterrepräsentiert

5. 🌍 "OpenAI launched gerade... hier ist was das für KMUs bedeutet"
   Pillar: Industry News | Hook: News-Commentary | Format: Text
   Quelle: News (WebSearch: aktuelle AI-Announcements)
   Warum: Timely Content = hohe Reach
```

3. **User wählt:**
   - Gut → Status "Approved" im Datenspeicher
   - Nicht gut → Status "Rejected"
   - Ändern → Idee anpassen

## Regeln

- **Vielfalt** — min. 2 Pillars, 2 Hook Types, 2 Formate
- **Keine Duplikate** — gegen bestehende Posts/Ideas prüfen
- **Datenbasiert** — jede Idee hat eine Begründung
- **Pillar-Gewichtung** beachten (aus config)
- **Experiment-bewusst** — wenn ein Experiment läuft, mindestens 1 passende Idee
