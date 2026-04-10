# insight-k8s-mcp

MCP Gateway Infrastruktur auf Basis von Envoy AI Gateway, Cloudflare und Kubernetes
fuer [alpininsight.ai](https://alpininsight.ai).

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

## Struktur

```
insight-k8s-mcp/
  infra/
    cloudflare/
      dns-plan.md              # DNS-Eintraege und Subdomain-Planung
      tunnel-dev.md            # Cloudflare Tunnel Setup fuer Dev
    k8s/
      namespaces/
        mcp-system.yaml        # Namespace fuer Gateway-Komponenten
      gateway/
        gateway.yaml           # Envoy AI Gateway Instanz
        gatewayconfig.yaml     # Gateway-Konfiguration (Envoy Proxy)
      mcproutes/
        mcp-internal.yaml      # MCPRoute: internes Gateway
        mcp-partner.yaml       # MCPRoute: Partner-Endpoint
        mcp-dev.yaml           # MCPRoute: Dev/Test-Endpoint
      backends/
        openapi-mcp.yaml       # Backend: OpenAPI MCP Server
        github-mcp.yaml        # Backend: GitHub MCP Server
        jira-mcp.yaml          # Backend: Jira MCP Server
      policies/
        oauth-internal.yaml    # SecurityPolicy: internes OAuth/OIDC
        oauth-partner.yaml     # SecurityPolicy: Partner OAuth
        ext-auth.yaml          # SecurityPolicy: Ops/Admin (Cloudflare Access)
  docs/
    mcp-reference-architecture.md   # Referenzarchitektur (Hauptdokument)
    mcp-auth-model.md               # Auth-Modell Nord/Sued
    mcp-subdomains.md               # Subdomain-Strategie
```

## Schnellstart

```bash
# Namespace anlegen
kubectl apply -f infra/k8s/namespaces/

# Gateway deployen
kubectl apply -f infra/k8s/gateway/

# Policies anwenden
kubectl apply -f infra/k8s/policies/

# Backends deployen
kubectl apply -f infra/k8s/backends/

# MCPRoutes aktivieren
kubectl apply -f infra/k8s/mcproutes/
```

## Voraussetzungen

- Kubernetes 1.30+
- Envoy AI Gateway v0.5+
- Gateway API CRDs installiert (`gateway.networking.k8s.io/v1`)
- OIDC-Provider (Entra ID / Keycloak / Authentik)
- Cloudflare Account mit DNS-Verwaltung fuer `alpininsight.ai`

## Dokumentation

Siehe [docs/](docs/) fuer die vollstaendige Referenzarchitektur, das Auth-Modell
und die Subdomain-Strategie.

## Rollout-Reihenfolge

1. **Phase 1:** `mcp.alpininsight.ai` mit internem OIDC-Issuer
2. **Phase 2:** 2-3 private MCP-Backends anbinden (OpenAPI, GitHub, Jira)
3. **Phase 3:** `mcp-partner.alpininsight.ai` mit separatem Issuer/Scopes
4. **Phase 4:** `mcp-dev.alpininsight.ai` fuer Notebook/Tunnel-Szenarien

## Lizenz

Intern - alpininsight.ai
