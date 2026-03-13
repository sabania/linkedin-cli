---
name: data-schema
description: Komplettes Daten-Schema für LinkedIn-Tracking. 10 Sheets mit allen Spalten, Typen, erlaubten Werten. Agents lesen diesen Skill bevor sie Daten lesen/schreiben.
user-invocable: false
---

# Data Schema Reference

Der Datenspeicher (Format wird beim `/setup` festgelegt — Default: Excel `.xlsx`) trackt alle LinkedIn-Marketing-Daten. Das Schema unten ist das **Default-Template** — Users können es beim Onboarding anpassen.

**Vor jeder Daten-Operation:**
1. Lies `config.json` → `tracking` für Format, Datei, aktive Sheets, Runtime
2. Lies diesen Skill für die Spaltenstruktur
3. Passe dein Script an `tracking.runtime` an (python/node/etc.)

---

## Sheet: Posts (33 Spalten)

Trackt den gesamten Content-Lifecycle von Idee bis analysiert. Jede Eigenschaft die Performance beeinflussen kann ist eine Spalte.

| Spalte | Typ | Quelle | Beschreibung | Erlaubte Werte |
|--------|-----|--------|--------------|----------------|
| Title | text | Agent/User | Hook/erste Zeile (~80 Zeichen) | |
| Status | select | System/User | Content-Pipeline-Status | Idea, Approved, Draft, In Review, Ready, Scheduled, Published, Analyzed, Evolved, Rejected |
| Lifecycle | select | Berechnet | Mess-Phase (orthogonal zu Status) | Active, Cooling, Archived |
| Pillar | select | Agent/User | Content-Säule | *Aus config.json → content.pillars* |
| Hook Type | select | Agent | Stil der ersten Zeile | Statistics, Personal Story, Question, Surprising Fact, Contrarian, How-To, List, Problem-Solution, Behind-Scenes |
| Format | select | Agent/CLI | Content-Format | Text, Image, Video, Document, Carousel, Poll |
| Content Type | select | Agent | Inhaltliche Kategorie | Educational, Case-Study, Opinion, Behind-Scenes, How-To, News-Commentary, Inspirational, Controversial |
| Language | select | Agent | Sprache | DE, EN, *andere* |
| Length Category | select | Berechnet | Längen-Kategorie | Short (<500 chars), Medium (500-1500), Long (>1500) |
| Char Count | number | Berechnet | Exakte Zeichenzahl | |
| CTA Type | select | Agent | Call-to-Action am Ende | Question, Statement, Link, None |
| Hashtag Count | number | Berechnet | Anzahl Hashtags | |
| Hashtags | text | Berechnet | Komma-separiert | |
| Emoji Count | number | Berechnet | Anzahl Emojis | |
| Has Personal Reference | boolean | Agent | Bezug auf eigenes Projekt/Erfahrung | true, false |
| Is Timely | boolean | Agent | Aktuelles Event vs. Evergreen | true, false |
| LinkedIn URL | text | User | Post-URL nach Publishing | |
| URN | text | CLI | LinkedIn Activity URN | `urn:li:activity:...` |
| Published Date | date | User/CLI | Veröffentlichungsdatum | ISO 8601 |
| Published Day | select | Berechnet | Wochentag | Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday |
| Published Hour | number | Berechnet | Uhrzeit (0-23) | |
| Reactions | number | CLI | Aktuelle Reactions | |
| Comments | number | CLI | Aktuelle Comments | |
| Shares | number | CLI | Aktuelle Shares | |
| Impressions | number | CLI | Aus Analytics | |
| Members Reached | number | CLI | Unique Viewer (Analytics) | |
| Engagement Rate | number | Berechnet | (Reactions+Comments+Shares)/Impressions*100 | |
| Followers Gained | number | CLI | Neue Follower durch diesen Post | |
| Profile Views From Post | number | CLI | Profil-Besuche durch diesen Post | |
| Top Demographics | text | CLI | JSON: Top Job-Titel, Industries, Seniority aus Analytics | |
| Last Snapshot | number | System | Welche Messung (1-3) | 1, 2, 3 |
| Snapshot Date | date | System | Letzte Messung | ISO 8601 |
| Experiment | text | Agent | Experiment-Zugehörigkeit | |
| Idea Source | text | Agent | Woher kam die Idee | Feed Trend, Competitor Gap, Repurpose, Pattern, News, Experiment, Audience Request, Manual |
| Draft Path | text | System | Pfad zur .md Draft-Datei | Relativ zum CWD |

### Status Flow
```
Idea → Approved → Draft → [In Review →] Ready → [Scheduled →] Published → Analyzed → Evolved
                                                                                ↓
Any status can → Rejected
```

### Snapshot Timing
- Snapshot 1: Tag 3 nach Veröffentlichung
- Snapshot 2: Tag 7
- Snapshot 3: Tag 14 → Status wechselt zu "Analyzed"

### Post Lifecycle (Mess-Phase)

Orthogonal zum Status (Content-Pipeline). Ein Post kann `Published + Active` sein, dann `Published + Cooling`, dann `Analyzed + Archived`.

| Phase | Tage seit Published | Was passiert | API-Last |
|-------|---------------------|-------------|----------|
| **Active** | 0-7 | Jede Session: Metriken aus Notifications updaten | Analytics bei Morning Check |
| **Cooling** | 7-14 | Letzter Snapshot bei Tag 14 | 1x Analytics-Call |
| **Archived** | 14+ | Finale Metriken. Nie wieder angefasst. | Null |

**Automatische Übergänge (bei Session-Start, lokal):**
```python
for post in posts.where(status="Published"):
    days = (today - post.published_date).days
    if days >= 14 and post.lifecycle != "Archived":
        post.lifecycle = "Archived"
        post.status = "Analyzed"  # wenn Snapshot 3 da
    elif days >= 7 and post.lifecycle == "Active":
        post.lifecycle = "Cooling"
    elif post.lifecycle is None:
        post.lifecycle = "Active"
```

---

## Sheet: Contacts (23 Spalten)

Trackt LinkedIn-Kontakte, Leads und Engagement-Beziehungen. Zentrales Sheet für Audience Intelligence.

| Spalte | Typ | Quelle | Beschreibung | Erlaubte Werte |
|--------|-----|--------|--------------|----------------|
| Name | text | CLI | Voller Name | |
| LinkedIn URL | text | Berechnet | Profil-URL | |
| Public ID | text | CLI | LinkedIn Username/Slug | |
| Headline | text | CLI | Job-Titel/Headline | |
| Company | text | CLI | Aktuelle Firma | |
| Industry | text | CLI | Branche (aus Profil) | |
| Location | text | CLI | Standort | |
| Connection Degree | select | CLI | Verbindungsgrad | 1st, 2nd, 3rd |
| Source | select | System | Wie entdeckt | Post Reaction, Comment, Profile View, Invitation, Search, Competitor Engager, Feed, Manual |
| Source Detail | text | System | Details (z.B. Post-URN, Suchbegriff) | |
| Interaction Types | text | System | Komma-separiert | like, comment, share, view, reply, praise, interest, empathy, entertainment |
| Score | select | Berechnet | Lead-Temperatur (aus Warm Score) | Hot, Warm, Cold |
| Warm Score | number | Berechnet | Numerischer Score 0-100 | |
| ICP Match | select | System | Passt zum Ideal Customer Profile | High, Medium, Low, None |
| Status | select | User/System | Beziehungsstatus | New, Researched, Engaged, Contacted, Replied, Connected, Dormant |
| First Seen | date | System | Erster Kontakt | ISO 8601 |
| Last Interaction | date | System | Letzte Interaktion | ISO 8601 |
| Interaction Count | number | System | Gesamtzahl Interaktionen | |
| Follow-up Date | date | System | Nächstes Follow-up | ISO 8601 |
| Last Outreach | date | User | Wann letzte Nachricht gesendet | ISO 8601 |
| Outreach Type | select | User | Art der letzten Kontaktaufnahme | Connection Request, Message, InMail, Comment Reply |
| Response Status | select | User | Antwort auf letzte Outreach | Pending, Accepted, Replied, No Response |
| Notes | text | User/Agent | Freitext | |

### Warm Score Berechnung
```
+10  pro Reaction auf eigenen Post
+25  pro Kommentar auf eigenen Post
+15  für Profil-View
+5   pro Nachricht (gesendet oder empfangen)
+20  bei ICP Match (High)
+10  bei ICP Match (Medium)
-5   pro Woche ohne Interaktion (Decay)
Cap: 100
```

### Score-Ableitung aus Warm Score
- **Hot**: Warm Score >= 60
- **Warm**: Warm Score 25-59
- **Cold**: Warm Score < 25

### Dormant-Erkennung
Contact mit Status "Connected" und Last Interaction > 90 Tage → Status wird "Dormant"

---

## Sheet: Patterns (14 Spalten)

Erkannte Content-Patterns mit Confidence-Level. Basis für datengetriebene Strategie.

| Spalte | Typ | Quelle | Beschreibung | Erlaubte Werte |
|--------|-----|--------|--------------|----------------|
| Name | text | Agent | Pattern-Name | z.B. "Question hooks boost comments" |
| Type | select | Agent | Pattern-Kategorie | Hook, Format, Topic, Timing, Length, CTA, Content-Type, Combination |
| Dimension | text | Agent | Getesteter Wert | z.B. "Question", "Video", "Tuesday" |
| Dimension 2 | text | Agent | Für Kombinations-Patterns | z.B. "Carousel" bei "Question + Carousel" |
| Avg Reactions | number | Berechnet | Durchschnittliche Reactions | |
| Avg Comments | number | Berechnet | Durchschnittliche Comments | |
| Avg Engagement Rate | number | Berechnet | Durchschnittliche Engagement Rate | |
| Avg Impressions | number | Berechnet | Durchschnittliche Impressions | |
| Sample Size | number | Berechnet | Anzahl Posts | |
| Success Rate | number | Berechnet | % über Baseline | |
| Confidence | select | Berechnet | Statistische Sicherheit | Low (<5 Posts), Medium (5-15), High (>15) |
| Status | select | Agent | Pattern-Status | Active, Testing, Deprecated, Disproven |
| Discovery Date | date | System | Wann erstmals erkannt | ISO 8601 |
| Notes | text | Agent | Hypothese, Konfounds | |

### Pattern-Dimensionen für Analyse

| Dimension | Werte | Beispiel |
|-----------|-------|---------|
| Hook Type | 9 Typen | "Question-Hooks: 2x Comments" |
| Format | 6 Typen | "Carousels: 3x Impressions" |
| Content Type | 8 Typen | "Case Studies > Opinions" |
| Published Day | Mo-So | "Dienstag = bester Tag" |
| Published Hour | 0-23 | "8:00 schlägt 17:00" |
| Length Category | 3 Kategorien | "Medium = Sweet Spot" |
| CTA Type | 4 Typen | "Question CTAs: 2x Comments" |
| Pillar | User-definiert | "AI Praxis = stärkstes Pillar" |
| Has Personal Ref | boolean | "Personal: +40% Engagement" |
| Is Timely | boolean | "Timely = Reach, Evergreen = Engagement" |
| **Kombinationen** | Paare | "Question + Carousel + Dienstag" |

---

## Sheet: Strategy (5 Spalten — unverändert)

Versionierte Content-Strategie. Nur eine Row mit Status=Active.

| Spalte | Typ | Beschreibung | Erlaubte Werte |
|--------|-----|--------------|----------------|
| Version | text | Versions-Kennung | z.B. "v1.0", "v2.1" |
| Status | select | Ob aktiv | Active, Archived |
| Valid From | date | Gültig ab | ISO 8601 |
| Changes | text | Was sich geändert hat | |
| Content | text | Vollständiger Strategie-Text | Markdown |

---

## Sheet: Reports (16 Spalten)

Wöchentliche Performance-Reports mit KPIs und Trends.

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Week | text | z.B. "KW 11 2026" |
| Period Start | date | Start der Periode |
| Period End | date | Ende der Periode |
| Posts Count | number | Publizierte Posts |
| Total Reactions | number | Summe Reactions |
| Total Comments | number | Summe Comments |
| Total Impressions | number | Summe Impressions |
| Avg Reactions | number | Durchschnitt pro Post |
| Avg Comments | number | Durchschnitt pro Post |
| Avg Engagement Rate | number | Durchschnittliche Engagement Rate |
| Followers | number | Aktueller Stand |
| Follower Change | number | +/- seit letztem Report |
| Top Post URN | text | Bester Post der Woche |
| Pillar Distribution | text | JSON: Verteilung der Pillars |
| Competitor Comparison | text | Kurzer Vergleichstext |
| Insights | text | Key Learnings |

---

## Sheet: Competitors (18 Spalten)

Wettbewerber-Tracking und Benchmarking.

| Spalte | Typ | Quelle | Beschreibung |
|--------|-----|--------|--------------|
| Name | text | User | Name |
| Public ID | text | User/CLI | LinkedIn Username |
| LinkedIn URL | text | Berechnet | Profil-URL |
| Headline | text | CLI | Deren Headline |
| Followers | number | CLI | Follower-Zahl |
| Follower Change | number | Berechnet | Delta seit letzter Analyse |
| Posting Frequency | text | Agent | Posts pro Woche |
| Avg Reactions | number | Berechnet | Durchschnitt pro Post |
| Avg Comments | number | Berechnet | Durchschnitt pro Post |
| Avg Engagement Rate | number | Berechnet | Engagement Rate |
| Top Format | select | Agent | Bestes Content-Format |
| Top Hook Type | select | Agent | Häufigster Hook-Stil |
| Content Pillars | text | Agent | Deren Themen-Mix |
| Shared Engagers | number | Agent | Personen die bei beiden engagen |
| Content Gaps | text | Agent | Themen die sie haben, wir nicht |
| Last Analyzed | date | System | Letzte Analyse |
| Analysis Count | number | System | Wie oft analysiert |
| Notes | text | Agent | Key Learnings |

---

## Sheet: Signals (11 Spalten) — NEU

Trigger-Events die Aktionen auslösen. Signal-Inbox für tägliches Arbeiten.

| Spalte | Typ | Quelle | Beschreibung | Erlaubte Werte |
|--------|-----|--------|--------------|----------------|
| Date | date | System | Wann erkannt | ISO 8601 |
| Type | select | System | Signal-Typ | profile_view, engagement_hot, repeat_engagement, job_change, keyword_mention, competitor_post, new_follower_icp, dormant_reactivation, comment_opportunity, funding_signal |
| Contact Name | text | System | Betroffene Person | |
| Contact Public ID | text | System | Für Linking | |
| Headline | text | System | Kontext | |
| Priority | select | Berechnet | Dringlichkeit | High, Medium, Low |
| Action | select | System | Empfohlene Aktion | follow_up, connect, comment, outreach, research, monitor |
| Action Detail | text | Agent | Konkrete Empfehlung | |
| Status | select | User/System | Bearbeitungsstatus | New, Acknowledged, Acted, Dismissed, Expired |
| Source | text | System | Was hat ausgelöst (URN, Suche, etc.) | |
| Notes | text | Agent | Zusätzlicher Kontext | |

### Signal-Typen und Default-Priority

| Type | Priority | Trigger | Empfohlene Action |
|------|----------|---------|-------------------|
| engagement_hot | High | Warm Score überschreitet Threshold | outreach |
| repeat_engagement | High | 3+ Interactions in 30 Tagen | follow_up |
| job_change | High | Headline hat sich geändert | outreach |
| new_follower_icp | High | Neuer Follower matcht ICP | connect |
| profile_view | Medium | Jemand hat Profil angesehen | research |
| keyword_mention | Medium | Keyword in neuer Post | comment |
| dormant_reactivation | Medium | Stiller Contact engagiert wieder | follow_up |
| comment_opportunity | Medium | High-Momentum Post im Feed | comment |
| competitor_post | Low | Neuer Post von Competitor | monitor |
| funding_signal | Medium | Firma postet viele Jobs / Wachstum | research |

### Signal-Lifecycle
```
Detected → New → Acknowledged → Acted / Dismissed
                                    ↓
New → Expired (nach 7 Tagen ohne Aktion)
```

---

## Sheet: Feed Insights (14 Spalten) — NEU

Analysierte Feed-Posts für Trend-Detection und Comment Intelligence.

| Spalte | Typ | Quelle | Beschreibung |
|--------|-----|--------|--------------|
| URN | text | CLI | Post-URN |
| Author | text | CLI | Wer hat gepostet |
| Author Public ID | text | CLI | Für Linking |
| Text Preview | text | CLI | Erste 200 Zeichen |
| Topic | text | Agent | Erkanntes Thema (AI-klassifiziert, mappt auf eigene Pillars + "Other") |
| Reactions | number | CLI | Reaction Count |
| Comments | number | CLI | Comment Count |
| Posted At | date | CLI | Veröffentlichungszeitpunkt |
| Momentum Score | number | Berechnet | `(reactions + comments*2) / max(stunden_seit_post, 1)` |
| Is Competitor | boolean | System | Ist ein getrackter Competitor |
| Comment Opportunity | boolean | Agent | Lohnt sich ein Kommentar |
| Comment Priority | select | Agent | Priorisierung | High, Medium, Low |
| Trend Tag | text | Agent | Trending-Topic Tag |
| Scanned Date | date | System | Wann gescannt |

### Momentum Score
Misst wie schnell ein Post Engagement sammelt:
```
momentum = (reactions + comments * 2) / max(hours_since_posted, 1)
```
Hoher Score + relevantes Topic + junger Post = Comment-Opportunity.

### Trend Detection
Topic-Tags werden über 7 Tage aggregiert. Themen mit 3+ Erscheinungen und überdurchschnittlichem Engagement = Trend → fliesst in `/ideas`.

---

## Sheet: ICP Profile (7 Spalten) — NEU

Ideal Customer Profile — wird über Zeit aus Engagement-Daten geschärft.

| Spalte | Typ | Quelle | Beschreibung | Erlaubte Werte |
|--------|-----|--------|--------------|----------------|
| Dimension | select | System | Profil-Dimension | Job Title, Industry, Seniority, Company Size, Location, Function |
| Value | text | Agent | Konkreter Wert | z.B. "CTO", "Software", "DACH" |
| Engagement Count | number | Berechnet | Wie viele Engager matchen | |
| Conversion Rate | number | Berechnet | % die Hot Contact wurden | |
| Source | text | System | Woher die Daten | Post Demographics, Engager Profiles, Manual |
| Confidence | select | Berechnet | Datensicherheit | Low, Medium, High |
| Last Updated | date | System | Letzte Aktualisierung | ISO 8601 |

### ICP-Schärfung
1. Initial: User definiert Ziel-ICP beim Setup
2. Post-Demographics (aus `posts analytics --json`) zeigen wer wirklich engaged
3. Engager-Profile zeigen welche Titel/Branchen interagieren
4. Delta zwischen Soll-ICP und Ist-ICP → Strategie-Anpassung
5. Conversion Rate zeigt welche Dimensionen tatsächlich zu Hot Contacts führen

---

## Sheet: Comment Tracking (9 Spalten) — NEU

Trackt strategische Kommentare auf fremden Posts.

| Spalte | Typ | Quelle | Beschreibung |
|--------|-----|--------|--------------|
| Target Post URN | text | User/Agent | Wo kommentiert |
| Target Author | text | Agent | Wessen Post |
| Target Author Public ID | text | Agent | Für Linking |
| Comment Text | text | User | Was kommentiert |
| Comment Date | date | User | Wann |
| Target Post Reactions | number | CLI | Wie gross war der Ziel-Post |
| Visibility Gained | select | Agent | Geschätzte Sichtbarkeit (High/Medium/Low) |
| New Connections From | number | User | Resultierende neue Connections |
| Notes | text | User | Freitext |

---

## config.json Session & Lifecycle Block

Zusätzlich zu den bestehenden config-Feldern (`linkedin`, `goals`, `icp`, `content`, `competitors`, `signals`, `tracking`, `environment`) enthält die config:

```json
{
  "session": {
    "last_session_date": "2026-03-13T08:00:00Z",
    "last_report_date": "2026-03-09",
    "last_evolve_date": "2026-03-09",
    "last_competitor_check": "2026-03-01",
    "setup_completed": true,
    "posts_baseline_count": 23
  },
  "lifecycle": {
    "active_days": 7,
    "cooling_days": 14
  }
}
```

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `session.last_session_date` | ISO 8601 | Wann der Agent zuletzt gelaufen ist (für Delta-Berechnung) |
| `session.last_report_date` | ISO 8601 | Letzter Wochen-Report |
| `session.last_evolve_date` | ISO 8601 | Letzte Strategie-Evolution |
| `session.last_competitor_check` | ISO 8601 | Letzter Competitor-Check |
| `session.setup_completed` | boolean | Setup abgeschlossen? |
| `session.posts_baseline_count` | number | Anzahl Posts bei Initial-Analyse |
| `lifecycle.active_days` | number | Tage bis Active → Cooling (Default: 7) |
| `lifecycle.cooling_days` | number | Tage bis Cooling → Archived (Default: 14) |

**Delta-Berechnung bei Session-Start:**
```python
from datetime import datetime
last = datetime.fromisoformat(config["session"]["last_session_date"])
delta = datetime.now() - last
# → Nur Daten seit last_session_date holen
# → Warm Score Decay: -5 * (delta.days / 7)
# → Lifecycle-Übergänge für alle Published Posts berechnen
```

---

## Data Access Patterns

### Reading Excel (Python)
```python
import openpyxl

wb = openpyxl.load_workbook("linkedin-data.xlsx")
ws = wb["Posts"]
headers = [cell.value for cell in ws[1]]
records = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if all(v is None for v in row):
        continue
    records.append(dict(zip(headers, row)))
```

### Writing/Updating Excel (Python)
```python
import openpyxl

wb = openpyxl.load_workbook("linkedin-data.xlsx")
ws = wb["Posts"]
headers = [cell.value for cell in ws[1]]

# Append new row
ws.append(["My Post Title", "Idea", "AI Praxis", ...])

# Update existing row (find by URN)
urn_col = headers.index("URN") + 1
for row in ws.iter_rows(min_row=2):
    if row[urn_col - 1].value == target_urn:
        row[headers.index("Reactions")].value = new_reactions
        break

wb.save("linkedin-data.xlsx")
```

### Creating Excel with all Sheets (Python)
```python
import openpyxl

SCHEMA = {
    "Posts": ["Title", "Status", "Lifecycle", "Pillar", ...],  # 33 columns
    "Contacts": ["Name", "LinkedIn URL", ...],     # 23 columns
    "Patterns": ["Name", "Type", ...],             # 14 columns
    "Strategy": ["Version", "Status", ...],        # 5 columns
    "Reports": ["Week", "Period Start", ...],      # 16 columns
    "Competitors": ["Name", "Public ID", ...],     # 18 columns
    "Signals": ["Date", "Type", ...],              # 11 columns
    "Feed Insights": ["URN", "Author", ...],       # 14 columns
    "ICP Profile": ["Dimension", "Value", ...],    # 7 columns
    "Comment Tracking": ["Target Post URN", ...],  # 9 columns
}

wb = openpyxl.Workbook()
wb.remove(wb.active)
for sheet_name, headers in SCHEMA.items():
    ws = wb.create_sheet(sheet_name)
    ws.append(headers)
wb.save("linkedin-data.xlsx")
```

### Querying (Python)
```python
# Published posts sorted by engagement rate
published = sorted(
    [r for r in posts if r["Status"] == "Published"],
    key=lambda r: r.get("Engagement Rate") or 0,
    reverse=True
)

# Hot contacts with pending follow-up
from datetime import date
hot_followups = [
    r for r in contacts
    if r.get("Score") == "Hot"
    and r.get("Follow-up Date")
    and r["Follow-up Date"] <= date.today()
]

# New signals
new_signals = [s for s in signals if s.get("Status") == "New"]
high_priority = [s for s in new_signals if s.get("Priority") == "High"]

# Trending topics from feed
from collections import Counter
topics = Counter(f.get("Topic") for f in feed_insights if f.get("Topic"))
trending = [t for t, count in topics.most_common(5) if count >= 3]

# Active patterns with high confidence
proven = [p for p in patterns if p["Status"] == "Active" and p["Confidence"] == "High"]
```
