---
name: contacts
description: "Contacts & Leads verwalten. Warm Scores, ICP Matching, Hot Leads, Follow-ups, Dormant Connections, Network Health. Absorbiert /network als Sub-Command."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
---

# /contacts — Kontakte verwalten

Verwaltet LinkedIn-Kontakte und Leads mit Warm Score, ICP Match und Follow-up Tracking.

**WICHTIG: Delegiere die Arbeit an den `contact-scanner` Agent. Mach NICHTS selbst — starte den Agent mit dem `Agent`-Tool und übergib den Sub-Command (scan, hot, follow-up, stats, etc.).**

## Verwendung

```
/contacts scan          # Neue Engagers scannen (via contact-scanner)
/contacts hot           # Hot Contacts anzeigen (Warm Score >= 60)
/contacts warm          # Warm Contacts (Score 25-59)
/contacts follow-up     # Fällige Follow-ups
/contacts dormant       # Dormant Connections (>90 Tage inaktiv)
/contacts <name>        # Bestimmten Kontakt suchen/anzeigen
/contacts stats         # Network Health + Statistiken (absorbiert /network)
```

## Ablauf

### scan
1. **`contact-scanner` Agent** starten
2. Neue und aktualisierte Contacts zeigen
3. Warm Scores und ICP Matching

### hot
Contacts mit Score "Hot" aus Datenspeicher:
```
Hot Contacts (5):

  1. Anna Schmidt | CTO @ TechAG
     Warm Score: 85 | ICP: High | 4 Interactions
     Letztes: Kommentar vor 2 Tagen
     Status: Engaged → Ready for outreach

  2. Peter Mueller | VP Sales @ SaaS Inc
     Warm Score: 72 | ICP: High | 3 Interactions
     Letztes: Reaction vor 5 Tagen
     Status: New → Research + Connect
```

### follow-up
Contacts mit Follow-up Date <= heute:
```
Fällige Follow-ups (2):

  1. Max Muster | Developer @ StartupCo
     Status: Contacted | Outreach: Connection Request vor 8 Tagen
     Response: No Response → Re-follow-up oder abhaken?

  2. Lisa Weber | Head of Product @ BigCorp
     Status: Dormant → Reactivated
     → Reaktivieren mit personalisierter Nachricht
```

### dormant
Connected Contacts mit Last Interaction > dormant_days (default 90 Tage)

### <name>
Contact suchen und alle Details zeigen:
- Profil-Daten, Warm Score, ICP Match
- Interaction History
- Outreach History
- Optional: Profil via CLI auffrischen

### stats (absorbiert /network)
Network Health + Kontakt-Statistiken:
```
Contact-Statistiken:

Total: 245 | Hot: 5 | Warm: 89 | Cold: 122 | Dormant: 29
Neue (diese Woche): 12
ICP Match: 34 High, 67 Medium, 144 Low/None
Follow-ups fällig: 3
Avg Warm Score: 28

Network Health:
  Rollen: 75% Developer, 15% Manager, 5% C-Level, 5% Other
  → Gap bei Entscheidern (ICP sagt CTO/VP)
  Branchen: 80% Software, 10% Finance, 10% Other
  → Zu einseitig für Lead-Gen Ziel
  Connection Degree: 60% 1st, 30% 2nd, 10% 3rd
  Audience vs. ICP: 60% Developer statt CTO → Content anpassen
```

## Regeln

- **Privacy** — nur öffentliche LinkedIn-Daten
- **Kein Spam** — Outreach nur mit User-Bestätigung
- **Qualität > Quantität** — lieber 10 Hot als 100 Cold
- **Warm Score Decay** — Scores veralten, wird bei /auto automatisch angewendet
