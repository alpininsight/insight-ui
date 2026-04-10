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
  +-- MCPRoute: internal  ->  OpenAPI MCP, GitHub MCP, Jira MCP
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
`authorization_servers`, aber Envoy AI Gateway modelliert in `MCPRouteOAuth`
aktuell einen einzelnen Issuer pro Route. Deshalb ist ein Hostname/Endpoint
pro Trust-Zone bzw. pro OIDC-Issuer die sauberste Struktur.

Siehe [mcp-subdomains.md](mcp-subdomains.md) fuer Details.

-----

## Auth-Modell

### Nordseite -- Client -> Envoy MCP Gateway

- MCP-konformes OAuth am Gateway
- OIDC-Discovery oder OAuth Authorization Server Metadata vom IdP
- PKCE muss funktionieren
- `resource` muss auf den kanonischen MCP-Endpoint zeigen,
  z.B. `https://mcp.alpininsight.ai/mcp`

### Suedseite -- Gateway -> Backend-MCPs

- **Kein** Token-Passthrough des Client-Tokens
- Eigene Upstream-Credentials verwenden
- Ideal: private Backends oder API-Key/mTLS zwischen Gateway und Backend

**Sicherheitshinweis:** Das ist keine Stilfrage, sondern MCP-Sicherheitsmodell.
Die Spec verlangt Audience-Bindung und verbietet Token-Passthrough.

Siehe [mcp-auth-model.md](mcp-auth-model.md) fuer die vollstaendige Beschreibung.

-----

## Envoy AI Gateway -- Architekturkomponenten

### Gateway

Die zentrale `Gateway`-Ressource (Gateway API) stellt den Listener bereit.
Fuer MCP wird ein HTTPS-Listener auf Port 443 konfiguriert, der ueber
Cloudflare terminiertes TLS oder eigene Zertifikate arbeitet.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: mcp-gateway
  namespace: mcp-system
spec:
  gatewayClassName: envoy-ai-gateway
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
```

### MCPRoute

Jede Trust-Zone erhaelt eine eigene `MCPRoute`. Diese definiert:
- Welcher Gateway-Listener angesprochen wird (`parentRef`)
- Welche Hostnames akzeptiert werden
- Welche Backend-MCP-Server aggregiert werden (`backendRefs`)
- Optionale Tool-Filter (`toolSelector`)
- OAuth-Konfiguration (`oauth`)

```yaml
apiVersion: aigateway.envoyproxy.io/v1alpha1
kind: MCPRoute
metadata:
  name: mcp-internal
  namespace: mcp-system
spec:
  parentRef:
    name: mcp-gateway
  hostnames:
    - mcp.alpininsight.ai
  oauth:
    issuer: https://login.alpininsight.ai/realms/internal
    audience: https://mcp.alpininsight.ai/mcp
  backendRefs:
    - name: openapi-mcp
      toolSelector:
        prefix: "openapi__"
    - name: github-mcp
      toolSelector:
        prefix: "github__"
```

### SecurityPolicy

Security Policies definieren OAuth/OIDC-Parameter, erlaubte Scopes und
Zugriffsregeln. Sie werden per `targetRef` an eine `MCPRoute` oder
ein `Gateway` gebunden.

### Backend-Services

Jeder MCP-Backend-Server laeuft als Kubernetes Service im Cluster.
Die Services sind **nicht** oeffentlich erreichbar -- nur das Gateway
kann sie ueber ClusterIP ansprechen.

-----

## Technische Grenzen in Envoy AI Gateway (Stand v0.5)

| Aspekt                          | Status                                              |
|---------------------------------|-----------------------------------------------------|
| MCPRoute Backend-Aggregation    | Unterstuetzt -- mehrere Backends pro Route           |
| Backend-Namen                   | Muessen eindeutig sein (sonst Tool-Kollisionen)      |
| `toolSelector`                  | Verfuegbar -- Prefix/Regex-basierte Filterung        |
| `MCPRouteOAuth`                 | Ein Issuer pro Route                                 |
| Backend `securityPolicy`        | Aktuell auf API-Key fokussiert                       |
| Backend OIDC upstream           | Kein empfohlener Standardpfad                        |

**Praktische Konsequenz:** Gateway macht nordseitig OAuth, Backends bleiben
privat oder bekommen API-Key/interne Auth.

-----

## Rollout-Empfehlung

1. Start mit einem produktiven Endpoint: **`mcp.alpininsight.ai`**
2. Einen OIDC-Issuer fuer intern verwenden
3. Zuerst 2-3 private MCP-Backends dahinter haengen
4. `partner` und `dev` erst danach ueber eigene Hostnames trennen
5. `mcp-dev.alpininsight.ai` fuer den Notebook-/Tunnel-Fall nutzen --
   **nicht** `mcp.alpininsight.ai`

-----

## Quellen

- [Envoy AI Gateway Capabilities](https://gateway.envoyproxy.io/docs/capabilities)
- [Envoy AI Gateway API Reference](https://gateway.envoyproxy.io/docs/api)
- [Envoy AI Gateway v0.5 Release Notes](https://gateway.envoyproxy.io/docs/releases/v0.5)
- [MCP Authorization Spec 2025-11-05](https://spec.modelcontextprotocol.io/specification/2025-11-05/basic/authorization/)
- [Cloudflare Tunnel Routing](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/routing/)
- [Cloudflare Access Generic OIDC](https://developers.cloudflare.com/cloudflare-one/identity/idp-integration/generic-oidc/)
