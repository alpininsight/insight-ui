# Code-Block-Komponente (Version 0.1.0)

Diese Komponente bietet die Möglichkeit, Quellcode mit Syntax-Highlighting darzustellen. Darüber hinaus gibt es Möglichkeit, den dargestellten Quellcode, über einen Button in den Zwischenspeicher zu kopieren. Das Syntax-Highlighting umfasst so ziemlich alle gängigen und auch die meisten nicht sehr geläufigen Programmiersprachen.

## Abhängigkeiten

- **[prims.js](https://github.com/PrismJS/prism)**: Wird für das Syntax-Highlighting verwendet.
- **[clipboard.js](https://github.com/zenorocha/clipboard.js)**: Wird für das kopieren in den Zwischenspeicher verwendet.

## Verwendung

Diese Komponente wird ohne ein Template einzubinden, verwendet. Es muss lediglich ein HTML-Tag vorzugsweise ein `<div>` eingefügt werden. Dieses braucht eine Eindeutige `id`, diese ist für das Kopieren wichtig. Zum anderen muss das Tag den _data-Attribute_ ` data-insight-code-block` besitzen. Der Wert des _data-Attributes_ ist die gewünschte Programmiersprache. Innerhalb des Tags befindet sich dann ausschließlich der darzustellende Quellcode.

```django
<div id="code" data-insight-code-block="javascript">
    function greet(name) {
        return `Hello, ${name}!`;
    }
</div>
```

**_Info_**: Beim klick auf den **Copy** Button wird der Quellcode hervorgehoben und gleichzeitig in den Zwischenspeicher kopiert. Ein erneutes kopieren ist nicht notwendig.

## Verwandte Themen

- n.A.
