# MCP Gateway Reference Architecture -- alpininsight.ai

## Zielbild

```
Codex / Claude / andere MCP-Clients
        |
        v
mcp.alpininsight.ai
        |
        v
Cloudflare (DNS / TLS / WAF / Tunnel)
        |
        v
Envoy AI Gateway
  +-- MCPRoute: internal  ->  OpenAPI MCP, GitHub MCP, Context7 MCP
  +-- MCPRoute: partner   ->  Partner-spezifische MCPs
  +-- MCPRoute: dev       ->  Notebook / Dev MCPs
```

Das MCP Gateway aggregiert mehrere Backend-MCP-Server hinter einem einzigen,
oeffentlich erreichbaren Endpoint. MCP-Clients (Claude, Codex, eigene Agents)
verbinden sich ausschliesslich mit dem Gateway. Die Backend-Server bleiben privat.

-----

## Subdomain-Struktur

| Subdomain                     | Zweck                                                      |
|-------------------------------|------------------------------------------------------------|
| `mcp.alpininsight.ai`        | Internes Haupt-Gateway fuer Mitarbeiter und Standard-Agents |
| `mcp-partner.alpininsight.ai`| Separater MCP-Endpoint fuer externe Partner                 |
| `mcp-dev.alpininsight.ai`    | Dev/Test -- darf auf Notebook oder Test-Cluster zeigen      |
| `ops-mcp.alpininsight.ai`    | Admin/UI/Observability -- optional hinter Cloudflare Access |

**Wichtigste Designentscheidung:** Die MCP-Spec erlaubt zwar mehrere
`authorization_servers`, aber Envoy AI Gateway modelliert in `securityPolicy.oauth`
aktuell einen einzelnen Issuer pro MCPRoute. Deshalb ist ein Hostname/Endpoint
pro Trust-Zone bzw. pro OIDC-Issuer die sauberste Struktur.

Siehe [mcp-subdomains.md](mcp-subdomains.md) fuer Details.

-----

## Auth-Modell

### Nordseite -- Client -> Envoy MCP Gateway

- MCP-konformes OAuth am Gateway
- OIDC-Discovery oder OAuth Authorization Server Metadata vom IdP
- PKCE muss funktionieren
- `resource` in `protectedResourceMetadata` muss auf den kanonischen
  MCP-Endpoint zeigen, z.B. `https://mcp.alpininsight.ai/mcp`

### Suedseite -- Gateway -> Backend-MCPs

- **Kein** Token-Passthrough des Client-Tokens
- Eigene Upstream-Credentials via `backendRefs[].securityPolicy.apiKey`
- Ideal: private Backends (ClusterIP) oder API-Key zwischen Gateway und Backend

**Sicherheitshinweis:** Das ist keine Stilfrage, sondern MCP-Sicherheitsmodell.
Die Spec verlangt Audience-Bindung und verbietet Token-Passthrough.

Siehe [mcp-auth-model.md](mcp-auth-model.md) fuer die vollstaendige Beschreibung.

-----

## Envoy AI Gateway -- Architekturkomponenten

### GatewayClass + Gateway

Die GatewayClass registriert den Envoy AI Gateway Controller.
Die `Gateway`-Ressource stellt die Listener bereit -- pro Trust-Zone
ein dedizierter Listener mit eigenem Hostname.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: envoy-ai-gateway
spec:
  controllerName: gateway.envoyproxy.io/gatewayclass-controller
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: mcp-gateway
  namespace: mcp-system
spec:
  gatewayClassName: envoy-ai-gateway
  infrastructure:
    parametersRef:
      group: gateway.envoyproxy.io
      kind: EnvoyProxy
      name: mcp-envoy-proxy
  listeners:
    - name: https-mcp-internal
      protocol: HTTPS
      port: 443
      hostname: mcp.alpininsight.ai
```

### MCPRoute (aigateway.envoyproxy.io/v1alpha1)

Jede Trust-Zone erhaelt eine eigene `MCPRoute`. Diese definiert:
- Gateway-Bindung (`parentRefs` -- Array)
- MCP-Endpoint-Pfad (`path`, Default: `/mcp`)
- Client-Auth (`securityPolicy.oauth` -- eingebettet in MCPRoute)
- Autorisierung (`securityPolicy.authorization` -- Scope/Claim/CEL-basiert)
- Backend-Server (`backendRefs` -- mit `kind: Service` oder `kind: Backend`)
- Tool-Filter (`backendRefs[].toolSelector` -- include/exclude mit Regex)
- Backend-Auth (`backendRefs[].securityPolicy.apiKey`)

```yaml
apiVersion: aigateway.envoyproxy.io/v1alpha1
kind: MCPRoute
metadata:
  name: mcp-internal
  namespace: mcp-system
spec:
  parentRefs:
    - name: mcp-gateway
      kind: Gateway
      group: gateway.networking.k8s.io
  path: "/mcp"
  securityPolicy:
    oauth:
      issuer: "https://login.alpininsight.ai/realms/internal"
      audiences:
        - "https://mcp.alpininsight.ai/mcp"
      protectedResourceMetadata:
        resource: "https://mcp.alpininsight.ai/mcp"
        scopesSupported:
          - "openid"
          - "mcp:base"
          - "tools.github.read"
    authorization:
      defaultAction: Deny
      rules:
        - source:
            jwt:
              scopes:
                - "tools.github.read"
          target:
            tools:
              - backend: github-mcp
  backendRefs:
    - name: github-mcp
      kind: Service
      port: 8080
      path: "/mcp"
      toolSelector:
        includeRegex:
          - ".*issues?.*"
          - ".*pull_requests?.*"
      securityPolicy:
        apiKey:
          secretRef:
            name: github-mcp-api-key
```

### Tool-Naming und Filterung

Tool-Namen werden automatisch vom Gateway mit dem Backend-Namen prefixed:
- Backend `github-mcp` mit Tool `list_issues` -> `github-mcp__list_issues`
- Backend `context7-mcp` mit Tool `get_library_docs` -> `context7-mcp__get_library_docs`

Tool-Filter (`toolSelector`) unterstuetzt vier Modi:

| Feld            | Beschreibung                              | Hinweis                     |
|-----------------|-------------------------------------------|-----------------------------|
| `include`       | Exakte Tool-Namen (Whitelist)             | Exklusiv mit `includeRegex` |
| `includeRegex`  | RE2-Regex-Muster (Whitelist)              | Exklusiv mit `include`      |
| `exclude`       | Exakte Tool-Namen (Blacklist)             | Exklusiv mit `excludeRegex` |
| `excludeRegex`  | RE2-Regex-Muster (Blacklist)              | Exklusiv mit `exclude`      |

Exclude hat Vorrang vor Include.

### Autorisierung (CEL-Expressions)

MCPRoutes unterstuetzen CEL-basierte Autorisierungsregeln:

```yaml
authorization:
  rules:
    - source:
        jwt:
          scopes:
            - "tools.github.read"
          claims:
            - name: tenant
              valueType: String
              values:
                - acme
      target:
        tools:
          - backend: github-mcp
            tool: list_issues
      cel: 'request.mcp.params.arguments.repo.matches("^alpininsight/.*")'
```

Verfuegbare CEL-Variablen:

| Variable                       | Typ                  | Beschreibung                    |
|--------------------------------|----------------------|---------------------------------|
| `request.method`               | string               | HTTP-Methode                    |
| `request.headers`              | map[string]string    | HTTP-Header (lowercase)         |
| `request.path`                 | string               | Request-Pfad                    |
| `request.auth.jwt.claims`      | map[string]any       | JWT-Claims                      |
| `request.auth.jwt.scopes`      | []string             | JWT-Scopes                      |
| `request.mcp.method`           | string               | MCP-Methode (tools/list, etc.)  |
| `request.mcp.backend`          | string               | Upstream-Backend-Name           |
| `request.mcp.tool`             | string               | Tool-Name (ohne Prefix)         |
| `request.mcp.params`           | object               | JSON-RPC-Parameter              |

### Backend-Services

Jeder MCP-Backend-Server laeuft als Kubernetes Service im Cluster.
Die Services sind **nicht** oeffentlich erreichbar -- nur das Gateway
kann sie ueber ClusterIP ansprechen (NetworkPolicy erzwungen).

Fuer externe MCP-Server (z.B. GitHub Copilot MCP) wird ein
`Backend`-Objekt mit `BackendTLSPolicy` verwendet:

```yaml
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: Backend
metadata:
  name: github-copilot
spec:
  endpoints:
    - fqdn:
        hostname: api.githubcopilot.com
        port: 443
---
apiVersion: gateway.networking.k8s.io/v1alpha3
kind: BackendTLSPolicy
metadata:
  name: github-copilot-tls
spec:
  targetRefs:
    - group: gateway.envoyproxy.io
      kind: Backend
      name: github-copilot
  validation:
    wellKnownCACertificates: "System"
    hostname: api.githubcopilot.com
```

-----

## Technische Grenzen in Envoy AI Gateway (Stand v0.5)

| Aspekt                          | Status                                                |
|---------------------------------|-------------------------------------------------------|
| MCPRoute Backend-Aggregation    | Unterstuetzt -- mehrere Backends pro Route             |
| Backend-Namen                   | Muessen eindeutig sein (automatisches Tool-Prefixing)  |
| `toolSelector`                  | include/includeRegex/exclude/excludeRegex (RE2)        |
| `securityPolicy.oauth`          | Ein Issuer pro MCPRoute (eingebettet, kein separates CRD) |
| `securityPolicy.authorization`  | Scope/Claim/CEL-basiert, defaultAction: Allow oder Deny |
| `securityPolicy.apiKeyAuth`     | Alternative zu OAuth fuer einfache Szenarien           |
| `securityPolicy.extAuth`        | gRPC-basierte externe Autorisierung                    |
| Backend `securityPolicy.apiKey` | API-Key-Injection via Header oder Query-Param          |
| Backend OIDC upstream           | Kein empfohlener Standardpfad                          |
| `spec.path`                     | Default `/mcp`, konfigurierbar pro Route               |
| Header-basiertes Routing        | Unterstuetzt via `spec.headers` (Multi-Tenant)         |

**Praktische Konsequenz:** Gateway macht nordseitig OAuth, Backends bleiben
privat oder bekommen API-Key/interne Auth. SecurityPolicy ist Teil der
MCPRoute, kein separates CRD.

-----

## Rollout-Empfehlung

1. Start mit einem produktiven Endpoint: **`mcp.alpininsight.ai`**
2. Einen OIDC-Issuer fuer intern verwenden
3. Zuerst 2-3 private MCP-Backends dahinter haengen (OpenAPI, GitHub, Context7)
4. `partner` und `dev` erst danach ueber eigene Hostnames trennen
5. `mcp-dev.alpininsight.ai` fuer den Notebook-/Tunnel-Fall nutzen --
   **nicht** `mcp.alpininsight.ai`

-----

## Quellen

- [Envoy AI Gateway -- GitHub](https://github.com/envoyproxy/ai-gateway)
- [Envoy AI Gateway API Reference](https://gateway.envoyproxy.io/docs/api)
- [Envoy AI Gateway MCP Examples](https://github.com/envoyproxy/ai-gateway/tree/main/examples/mcp)
- [MCP Authorization Spec 2025-11-05](https://spec.modelcontextprotocol.io/specification/2025-11-05/basic/authorization/)
- [Cloudflare Tunnel Routing](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/routing/)
- [Cloudflare Access Generic OIDC](https://developers.cloudflare.com/cloudflare-one/identity/idp-integration/generic-oidc/)
