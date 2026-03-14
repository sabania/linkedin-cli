---
name: draft
description: "Neuen LinkedIn-Post oder strategischen Kommentar erstellen. Nutzt Brand Voice, Strategie und Patterns. +Comment-Draft-Modus."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
---

# /draft — Post oder Kommentar erstellen

Erstellt LinkedIn-Post-Entwürfe oder strategische Kommentare.

**WICHTIG: Delegiere die Arbeit an den `content-writer` Agent. Mach NICHTS selbst — starte den Agent mit dem `Agent`-Tool und übergib Thema + Modus (Post oder Comment).**

## Verwendung

```
/draft <thema>              # Post zu einem Thema
/draft                      # Nächste Approved Idea aus Pipeline nehmen
/draft comment <urn>        # Kommentar-Draft für einen Post (absorbiert /comment)
```

## Ablauf

### Post-Draft

1. **Thema bestimmen:**
   - Argument übergeben? → Dieses Thema verwenden
   - Kein Argument? → Älteste Idea mit Status "Approved" aus Datenspeicher
   - Keine Approved Idea? → User fragen oder `/ideas` vorschlagen

2. **`content-writer` Agent** starten mit dem Thema

3. **Draft präsentieren** — den geschriebenen Post dem User zeigen

4. **Feedback-Loop:**
   - User kann Änderungen vorschlagen
   - Post iterativ verbessern
   - Wenn zufrieden: Status auf "Draft" setzen, .md Datei gespeichert

### Comment-Draft (/draft comment <urn>)

1. **Ziel-Post laden** (aus Feed Insights oder via URN)
2. **`content-writer` Agent** im Comment-Modus starten:
   - Bezug zum Post-Inhalt (nicht generisch)
   - Eigene Expertise einbringen
   - Max 300-500 Zeichen
   - Frage am Ende (fördert Thread)
3. **Dem User zeigen** — nie automatisch posten

## Regeln

- **Immer den Draft zeigen** bevor er gespeichert wird
- **User hat das letzte Wort** — nie eigenständig finalisieren
- **Ein Draft pro Aufruf** — nicht mehrere auf einmal
- **NIE automatisch posten** — User kopiert und postet manuell
