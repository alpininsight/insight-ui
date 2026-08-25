# CLA — Prüfauftrag

Arbeitsdokument für die anwaltliche Prüfung von [`CLA.md`](../CLA.md). Es hält
fest, was bereits entschieden ist, damit die Prüfung sich auf die offenen
Punkte beschränken kann.

## Auftrag in einem Satz

Trägt die vorliegende Contributor-Vereinbarung nach deutschem Recht die
Doppellizenzierung von Insight UI — und was ist zu ändern, damit sie es tut?

Es geht ausdrücklich nicht um eine allgemeine Durchsicht. Der Text ist ein
etablierter internationaler Standard; der Auftrag ist die Anpassung an
deutsches Recht.

## Ausgangslage

Alpin Insight Solutions veröffentlicht Insight UI, ein Komponenten-Framework
für Django, unter zwei Lizenzen:

- **AGPL-3.0** für alle
- eine **kommerzielle Enterprise-Lizenz** für Organisationen, die die
  Netzwerk-Copyleft-Pflicht aus §13 AGPL nicht erfüllen können

Das setzt voraus, dass wir für jeden Teil des Codes die Rechte halten, ihn
unter beiden Lizenzen zu vergeben. Beiträge Dritter, die nur unter AGPL
hereinkommen, könnten nie in eine Enterprise-Auslieferung und ließen sich
später kaum herauslösen.

## Was bereits entschieden ist

| | |
|---|---|
| Vorlage | Harmony Agreements v1.0 (04.07.2011), HA-CLA-I und HA-CLA-E, CC BY 3.0 |
| Variante | **CLA**, nicht CAA — keine Vollabtretung, Contributor behält sein Copyright |
| Outbound-Lizenz | **§2.3 Option Five** der Vorlage |
| Anwendbares Recht | Deutschland (§6.1) |
| Gerichtsstand | Berlin, als Vorschlag in §6.6 ergänzt |
| Vertragspartei | Alpin Insight Solutions GmbH & Co. KG, Friedrichstraße 171, 10117 Berlin |
| Vertragsschluss | Kommentar des Contributors im ersten Pull Request, protokolliert durch einen Bot |

Option Five bedeutet: wir dürfen einen Beitrag unter beliebiger Lizenz
verwerten, auch proprietär, sind aber gebunden, ihn weiterhin unter der
Open-Source-Lizenz auszuliefern, die am Einreichungstag galt. Ein Beitrag kann
nicht nachträglich closed-source-only werden.

## Offene Punkte

### 1. Vollständigkeit der Vertragspartei

Der Signaturblock nennt die KG mit Anschrift. Offen sind HRA-Nummer der KG,
Firma und HRB-Nummer der Komplementär-GmbH sowie die Geschäftsführung. Bitte um
Bestätigung, dass die Vertretungskette KG → Komplementärin → Geschäftsführer im
Dokument korrekt abgebildet ist.

Zusätzlich: Soll die KG selbst Rechteinhaberin sein, oder eine andere Einheit
der Gruppe? Die Vereinbarung soll die gesamte `insight-ui*`-Familie abdecken,
nicht nur ein Repository — §1 der Vorlage sieht das vor.

### 2. §2.4 — Verzicht auf Urheberpersönlichkeitsrechte

Die Vorlage lässt den Contributor auf die Geltendmachung von
Urheberpersönlichkeitsrechten verzichten, „to the maximum extent permitted by
law". Vor dem Hintergrund von § 29 UrhG: was bleibt davon nach deutschem Recht
wirksam, und genügt die Öffnungsklausel?

### 3. §2.1(b) — unbefristete, unwiderrufliche Lizenz an künftigen Werken

Die Vereinbarung erfasst auch künftige Beiträge. Wie verhält sich das zu
§ 40 UrhG (Kündbarkeit nach fünf Jahren) und § 41 UrhG (Rückrufsrecht wegen
Nichtausübung)? Falls die Bindung insoweit nicht trägt: welche praktische
Folge hat das für bereits ausgelieferte Enterprise-Versionen?

### 4. §§ 4, 5 — Gewährleistung und Haftung als AGB

Die Vereinbarung wird gegenüber allen Contributorn unverändert verwendet und
ist damit AGB. Halten der Gewährleistungsausschluss (§4) und die
Haftungsbegrenzung (§5) der Inhaltskontrolle nach §§ 305–310 BGB stand,
insbesondere § 309 Nr. 7 BGB?

### 5. Vertragsschluss per Kommentar

Der Contributor antwortet im Pull Request mit einem festen Satz; ein Bot
protokolliert Zeitpunkt, GitHub-Benutzernamen und die Zustimmung in einer
Datei. Genügt das für einen wirksamen Vertragsschluss, und taugt das
Protokoll als Nachweis der Rechteeinräumung?

### 6. Contributor als Verbraucher

Beiträge kommen weltweit und überwiegend unentgeltlich von Privatpersonen.
Soweit diese Verbraucher sind: welche Folgen hat Art. 6 Rom-I für die
Rechtswahl, und ist die Gerichtsstandsklausel in §6.6 in der vorgeschlagenen
eingeschränkten Fassung sinnvoll oder besser zu streichen?

### 7. Arbeitnehmer und Minderjährige

§3(c) verlangt bei Angestellten die Zustimmung des Arbeitgebers und bei unter
Achtzehnjährigen die der Eltern. Sollte für Beiträge im Rahmen eines
Arbeitsverhältnisses zwingend Teil B (Entity) gezeichnet werden — auch mit
Blick auf § 43 UrhG? Und ist die Elternzustimmung per Kommentar praktikabel,
oder soll die Vereinbarung Minderjährige ausschließen?

### 8. Englische Sprachfassung

Der Text ist englisch, auch gegenüber deutschsprachigen Contributorn.
Bestehen Bedenken, oder empfiehlt sich eine deutsche Fassung als
verbindliche oder nachrichtliche Version?

### 9. Signaturverzeichnis

Name und GitHub-Benutzername der Zeichnenden stehen öffentlich im Repository.
Das ist bei diesem Verfahren üblich und für den Nachweis erforderlich. Bitte um
eine kurze Einordnung, ob daraus über die Vertragsdokumentation hinaus etwas
zu veranlassen ist.

## Was wir als Ergebnis brauchen

1. Bestätigung oder Änderungsvorschläge zu den neun Punkten
2. Freigabe des Textes zur Verwendung gegenüber Contributorn
3. Die fehlenden Registerangaben für den Signaturblock

## Beigefügte Unterlagen

| | |
|---|---|
| `CLA.md` | der zu prüfende Text |
| `COMMERCIAL_LICENSE.md` | beide Lizenzen und der Enterprise-Umfang |
| `LICENSE` | AGPL-3.0 im Wortlaut |
| `CONTRIBUTING.md` | wie die Vereinbarung Contributorn begegnet |
| `ha-cla-i-v1.pdf`, `ha-cla-e-v1.pdf` | die Harmony-Originale zum Abgleich |
