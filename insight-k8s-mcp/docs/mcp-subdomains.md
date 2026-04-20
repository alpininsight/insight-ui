# MCP Subdomain-Strategie -- alpininsight.ai

## Ueberblick

Jede Trust-Zone erhaelt einen eigenen Hostname. Das ist die sauberste
Struktur, weil Envoy AI Gateway in `MCPRouteOAuth` aktuell einen einzelnen
Issuer pro Route modelliert.

```
                    alpininsight.ai
                          |
         +----------------+------------------+------------------+
         |                |                  |                  |
   mcp.            mcp-partner.        mcp-dev.          ops-mcp.
   alpininsight.ai alpininsight.ai    alpininsight.ai   alpininsight.ai
```

-----

## Subdomain-Details

### mcp.alpininsight.ai

| Eigenschaft     | Wert                                                   |
|-----------------|--------------------------------------------------------|
| Zweck           | Internes Haupt-Gateway fuer Mitarbeiter und Agents     |
| Trust-Zone      | Internal                                               |
| OIDC-Issuer     | `https://login.alpininsight.ai/realms/internal`        |
| Audience        | `https://mcp.alpininsight.ai/mcp`                      |
| Scopes          | `mcp:base`, `tools.openapi.*`, `tools.github.*`, `tools.context7.*` |
| Backends        | OpenAPI MCP, GitHub MCP, Context7 MCP                  |
| Cloudflare      | DNS + TLS + WAF + Rate Limiting                        |
| Zugang          | Authentifizierte Mitarbeiter und autorisierte Agents   |

### mcp-partner.alpininsight.ai

| Eigenschaft     | Wert                                                   |
|-----------------|--------------------------------------------------------|
| Zweck           | Separater Endpoint fuer externe Partner                |
| Trust-Zone      | Partner                                                |
| OIDC-Issuer     | Separater Issuer oder Client-Set im IdP                |
| Audience        | `https://mcp-partner.alpininsight.ai/mcp`              |
| Scopes          | `mcp:base`, `tools.partner.*`                          |
| Backends        | Partner-spezifische MCP-Server                         |
| Cloudflare      | DNS + TLS + WAF + strengeres Rate Limiting             |
| Zugang          | Nur autorisierte Partner-Clients                       |

### mcp-dev.alpininsight.ai

| Eigenschaft     | Wert                                                   |
|-----------------|--------------------------------------------------------|
| Zweck           | Dev/Test-Umgebung, Notebook-Zugang                     |
| Trust-Zone      | Dev                                                    |
| OIDC-Issuer     | Dev-Issuer oder gleiches IdP mit separater Audience    |
| Audience        | `https://mcp-dev.alpininsight.ai/mcp`                  |
| Scopes          | `mcp:base`, `tools.*`                                  |
| Backends        | Dev/Test MCP-Server, Notebooks                         |
| Cloudflare      | Optional Named Tunnel zum Notebook/Dev-Cluster         |
| Zugang          | Entwickler mit Dev-Berechtigung                        |

### ops-mcp.alpininsight.ai

| Eigenschaft     | Wert                                                   |
|-----------------|--------------------------------------------------------|
| Zweck           | Admin-UI, Observability, Gateway-Management            |
| Trust-Zone      | Ops                                                    |
| Auth            | Cloudflare Access (OIDC-basiert)                       |
| Backends        | Envoy Admin, Prometheus, Grafana                       |
| Cloudflare      | DNS + TLS + **Cloudflare Access**                      |
| Zugang          | Nur Ops/Admin-Team                                     |

-----

## Warum ein Hostname pro Trust-Zone?

### Technischer Grund

`MCPRouteOAuth` in Envoy AI Gateway unterstuetzt aktuell **einen Issuer pro Route**.
Mehrere Trust-Zones auf einem Hostname wuerden erfordern, dass der Gateway
anhand des Tokens entscheidet, welche Route gilt -- das ist fragil und
nicht im aktuellen API-Design vorgesehen.

### Sicherheitsgrund

Getrennte Hostnames erzwingen:
- Eigene TLS-Zertifikate pro Zone
- Eigene Audience-Bindung pro Zone
- Eigene Rate-Limiting-Regeln pro Zone
- Klare Trennung in Logs und Monitoring

### Operativer Grund

- DNS-basiertes Failover/Routing pro Zone moeglich
- Cloudflare-Regeln (WAF, Access) pro Subdomain konfigurierbar
- Unabhaengiges Deployment und Rollback pro Zone

-----

## DNS-Konfiguration

Alle Subdomains zeigen auf den gleichen Kubernetes-Ingress/LoadBalancer.
Die Routing-Entscheidung trifft der Envoy AI Gateway anhand des
`Host`-Headers.

```
mcp.alpininsight.ai          -> CNAME -> k8s-lb.alpininsight.ai
mcp-partner.alpininsight.ai  -> CNAME -> k8s-lb.alpininsight.ai
mcp-dev.alpininsight.ai      -> CNAME -> tunnel-dev.cfargotunnel.com  (oder k8s-lb)
ops-mcp.alpininsight.ai      -> CNAME -> k8s-lb.alpininsight.ai
```

Siehe [../infra/cloudflare/dns-plan.md](../infra/cloudflare/dns-plan.md) fuer
die vollstaendige DNS-Konfiguration.
