# Barrierefreiheit

**_STOP_**: Der Inhalt ist momentan als Guide für Entwickler zu verstehen, da leider viele Komponenten noch bei weitem nicht komplett Barrierefrei sind.

Insight UI unter der Beachtung der Barrierefreiheit entwickelt. Alle Komponenten entsprechen den WCAG 2.1 AA-Richtlinien und bieten eine optimale Benutzererfahrung für alle Benutzer, unabhängig von ihren Fähigkeiten oder der verwendeten Technologie.

## Barrierefreiheitsfunktionen

### Tastaturnavigation

Alle interaktiven Elemente sind vollständig über die Tastatur zugänglich:

- Fokusreihenfolge folgt dem natürlichen Dokumentfluss
- Sichtbarer Fokusindikator für alle interaktiven Elemente
- Tastaturkürzel für häufig verwendete Aktionen
- Skip-Links zum Überspringen von Navigationsblöcken

### Screenreader-Unterstützung

Alle Komponenten sind für Screenreader optimiert:

- Semantisches HTML mit korrekten ARIA-Attributen
- Aussagekräftige Alt-Texte für Bilder
- ARIA-Live-Regionen für dynamische Inhalte
- Beschreibende Labels für Formularelemente

### Farbkontrast und Sichtbarkeit

- Alle Text- und UI-Elemente erfüllen die WCAG 2.1 AA-Kontrastanforderungen
- Hochkontrastmodus für Benutzer mit Sehbehinderungen
- Keine Informationsübermittlung ausschließlich durch Farbe
- Responsive Designs mit anpassbarer Textgröße

### Responsive Design

- Vollständig responsive Layouts für alle Bildschirmgrößen
- Unterstützung für Zoom bis zu 400% ohne Verlust von Funktionalität
- Anpassung an verschiedene Eingabemethoden (Maus, Tastatur, Touch)

## Barrierefreiheits-Checkliste

Hier ist eine Checkliste, die Sie verwenden können, um sicherzustellen, dass Ihre Anwendung barrierefrei bleibt:

- [ ] Alle Bilder haben aussagekräftige Alt-Texte
- [ ] Farbkontrast erfüllt WCAG 2.1 AA-Anforderungen (4.5:1 für normalen Text, 3:1 für großen Text)
- [ ] Alle Funktionen sind über die Tastatur zugänglich
- [ ] Fokusreihenfolge ist logisch und intuitiv
- [ ] Formularelemente haben beschreibende Labels
- [ ] Dynamische Inhalte verwenden ARIA-Live-Regionen
- [ ] Keine Informationsübermittlung ausschließlich durch Farbe
- [ ] Seite ist bei 200% Zoom noch benutzbar
- [ ] Semantisches HTML wird verwendet
- [ ] Skip-Links sind vorhanden

## Testen auf Barrierefreiheit

Django Insight UI enthält automatisierte Tests für Barrierefreiheit, aber wir empfehlen auch manuelle Tests:

### Automatisierte Tests

```bash
# Führen Sie die automatisierten Barrierefreiheitstests aus
uv run pytest tests/accessibility/
```

### Manuelle Tests

- Testen Sie mit einem Screenreader (z.B. NVDA, JAWS, VoiceOver)
- Navigieren Sie durch Ihre Anwendung nur mit der Tastatur
- Testen Sie mit verschiedenen Zoomstufen
- Überprüfen Sie den Farbkontrast mit Tools wie dem WAVE Browser Extension
- Testen Sie im Hochkontrastmodus

## Ressourcen

- [WCAG 2.1 Richtlinien](https://www.w3.org/TR/WCAG21/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [The A11Y Project](https://www.a11yproject.com/)
- [MDN Web Docs: Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
