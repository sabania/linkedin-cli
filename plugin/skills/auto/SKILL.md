---
name: auto
description: "Morning Check / Session Entry Point. Delta-Pipeline: Stage 1 COLLECT → Stage 2 ENRICH → Stage 3 DETECT (+ Feed parallel). Vereinigt bisheriges /daily + /auto."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - Grep
---

# /auto — Morning Check (Session Entry Point)

Der zentrale Entry Point für jede automatische Session. Führt die 3-Stage-Pipeline aus und gibt dem User eine priorisierte Zusammenfassung.

**Ersetzt das bisherige `/daily` und `/auto`.** Wird vom Cron-Job (täglich ~08:00) oder manuell aufgerufen.

## Verwendung

```
/auto              # Voller Morning Check (3-Stage Pipeline)
/auto quick        # Nur Stage 1 (Daten sammeln, kein Feed)
```

## 3-Stage Pipeline

```
Stage 1: COLLECT          Stage 2: ENRICH         Stage 3: DETECT
data-collector  ────────► contact-scanner  ──────► signal-detector
(Data Analyst)            (Community Manager)      (Intelligence Officer)
                                           parallel:
                                                    feed-analyst
                                                    (Social Media Scout)
```

### Stage 1: COLLECT (data-collector Agent)

**Was passiert:**
1. Lokale Berechnungen (KEIN API-Call):
   - Post-Lifecycle-Übergänge (Active → Cooling → Archived)
   - Warm Score Decay (-5 pro Woche seit letzter Session)
   - Signal-Expiry (New > 7 Tage → Expired)
2. Notifications holen (1 API-Call = 80% der Deltas)
3. Analytics für aktive Posts (nur Lifecycle=Active/Cooling)
4. Snapshot-Checks (Tag 3/7/14)

**Output → Stage 2:** Neue/aktualisierte Contacts mit Interaction-Typ und Post-URN.

### Stage 2: ENRICH (contact-scanner Agent)

**Input:** Output von Stage 1 (keine eigenen API-Calls).

**Was passiert:**
1. Contacts updaten (neu anlegen oder bestehende aktualisieren)
2. Warm Scores neu berechnen
3. ICP Matching für neue Contacts
4. Dormant Detection + Reactivation
5. Follow-ups identifizieren

**Output → Stage 3:** Angereicherte Contacts (Score-Änderungen, neue Hot Contacts, Reactivations).

### Stage 3: DETECT (parallel)

**3a: signal-detector Agent**
- Input: Angereicherte Contacts von Stage 2
- Signals erkennen aus Pipeline-Input (kein API nötig für meiste)
- Optional: Keyword-Search (1 API-Call pro Keyword)
- Output: Priorisierte Signal-Liste

**3b: feed-analyst Agent (parallel)**
- Unabhängig von Stage 1-2 (eigener Feed-Call)
- Feed holen (1 API-Call)
- Trends erkennen, Comment-Opportunities finden
- Output: Trending Topics + Comment-Opportunities

## Zusammenfassung an User

```
Morning Check abgeschlossen (seit letzter Session: 18h)

📊 DATEN:
  [n] Notifications verarbeitet
  [n] Post-Metriken aktualisiert
  [n] Lifecycle-Übergänge (Active→Cooling: 1, Cooling→Archived: 0)

👥 CONTACTS:
  [n] neue Contacts | [n] aktualisiert
  [n] neue Hot Contacts: [Namen]
  [n] Follow-ups fällig

🚨 SIGNALS ([n] neu):
  🔴 engagement_hot — Anna Schmidt (Score: 72)
  🔴 job_change — Max Müller (→ VP Engineering @ NewCo)
  🟡 keyword_mention — "AI Agents" in Post von @tech-leader

📈 FEED:
  Trending: "AI Agents" (7x, 2.3x avg), "Remote Work" (4x)
  💬 Comment-Opportunities:
    1. [HIGH] @sarah-k: "The future of..." (89 Rx in 3h)
    2. [MEDIUM] @tech-leader: "Why we switched..." (45 Rx in 5h)

⚠️ BRAUCHT DEINE ENTSCHEIDUNG:
  - 2 Follow-ups fällig → /contacts follow-up
  - Letzter Post vor 5 Tagen → /draft für neuen Post?
  - Neue Patterns erkannt → /evolve für Strategy-Update?
  - 2 Comment-Opportunities → Draft schreiben?

✅ ALLES OK:
  Content-Pipeline: 5 Ideas, 2 Drafts
  Competitors: aktuell (vor 8 Tagen)
  Strategy: v1.2
```

## Optionale Checks (am Ende)

Nach der Pipeline — nur Hinweise, keine Aktionen:
- Content-Pipeline dünn (< 3 Ideas)? → "/ideas um nachzufüllen"
- Published Post ohne Analyse? → "/analyze <urn>"
- Competitor-Daten > 2 Wochen? → "Beim nächsten /report wird Competitor-Update gemacht"
- Wöchentlicher Report fällig? → "/report erstellen"

## Regeln

- **Session updaten** — nach Abschluss `session.last_session_date` setzen
- **Delta-basiert** — nur Daten seit letzter Session
- **Pipeline-Reihenfolge** — Stage 1 → 2 → 3 (Feed parallel zu 3)
- **Daten sammeln: ja. Aktionen nach aussen: nur mit Bestätigung.**
- **Nie eigenständig posten, senden, kommentieren**
- **Kurz und actionable** — keine langen Erklärungen
- **Agents parallel** wo möglich (Stage 3a + 3b)
- **Priorität** — Signals und Follow-ups vor Content
