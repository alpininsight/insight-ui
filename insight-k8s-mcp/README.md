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
Envoy AI Gateway (aigateway.envoyproxy.io/v1alpha1)
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
        gateway.yaml           # GatewayClass + Gateway (Listener)
        gatewayconfig.yaml     # EnvoyProxy Konfiguration
      mcproutes/
        mcp-internal.yaml      # MCPRoute: intern (OAuth + Authorization + Backends)
        mcp-partner.yaml       # MCPRoute: Partner
        mcp-dev.yaml           # MCPRoute: Dev/Test
      backends/
        openapi-mcp.yaml       # Deployment + Service: OpenAPI MCP Server
        github-mcp.yaml        # Deployment + Service: GitHub MCP Server
        jira-mcp.yaml          # Deployment + Service: Jira MCP Server
      policies/
        oauth-internal.yaml    # Secret-Templates: API-Keys und Credentials
        oauth-partner.yaml     # Secret-Templates: Partner Credentials
        ext-auth.yaml          # NetworkPolicies: Backend-Isolation + Gateway-Ingress
  docs/
    mcp-reference-architecture.md   # Referenzarchitektur (Hauptdokument)
    mcp-auth-model.md               # Auth-Modell Nord/Sued
    mcp-subdomains.md               # Subdomain-Strategie
```

## Schnellstart

```bash
# Namespace anlegen
kubectl apply -f infra/k8s/namespaces/

# Gateway deployen (GatewayClass + Gateway + EnvoyProxy)
kubectl apply -f infra/k8s/gateway/

# Secrets erstellen (VORHER echte Werte einsetzen!)
kubectl apply -f infra/k8s/policies/

# Backends deployen (Deployments + Services)
kubectl apply -f infra/k8s/backends/

# MCPRoutes aktivieren (OAuth + Authorization + Backends)
kubectl apply -f infra/k8s/mcproutes/
```

## Voraussetzungen

- Kubernetes 1.30+
- Envoy AI Gateway v0.5+ (`aigateway.envoyproxy.io/v1alpha1`)
- Gateway API CRDs installiert (`gateway.networking.k8s.io/v1`)
- OIDC-Provider (Entra ID / Keycloak / Authentik)
- Cloudflare Account mit DNS-Verwaltung fuer `alpininsight.ai`

## API-Referenz

Alle MCPRoutes verwenden die Envoy AI Gateway API:

- **apiVersion:** `aigateway.envoyproxy.io/v1alpha1`
- **kind:** `MCPRoute`
- **SecurityPolicy** ist in der MCPRoute eingebettet (kein separates CRD)
- **Tool-Namen** werden automatisch mit dem Backend-Namen prefixed
- **toolSelector** nutzt `include`/`includeRegex`/`exclude`/`excludeRegex`

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
