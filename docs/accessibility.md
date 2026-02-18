# Barrierefreiheit

Insight UI soll unter der Beachtung der Barrierefreiheit entwickelt werden. Alle Komponenten müssen den WCAG 2.1 AA-Richtlinien entsprechen und sollen eine optimale Benutzererfahrung für alle Benutzer, unabhängig von ihren Fähigkeiten oder der verwendeten Technologie, bieten.

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

### Automatisierte Tests

- _Kommen vielleicht irgendwann._

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
