# DNS-Plan -- alpininsight.ai MCP Gateway

## DNS-Eintraege

Alle Eintraege werden ueber Cloudflare DNS verwaltet (Proxy-Modus: orange cloud).

| Record                          | Typ   | Ziel                                  | Proxy | Bemerkung                        |
|---------------------------------|-------|---------------------------------------|-------|----------------------------------|
| `mcp.alpininsight.ai`          | CNAME | `k8s-lb.alpininsight.ai`             | Ja    | Haupt-Gateway (intern)           |
| `mcp-partner.alpininsight.ai`  | CNAME | `k8s-lb.alpininsight.ai`             | Ja    | Partner-Gateway                  |
| `mcp-dev.alpininsight.ai`      | CNAME | `<tunnel-id>.cfargotunnel.com`       | Ja    | Dev via Cloudflare Tunnel        |
| `ops-mcp.alpininsight.ai`      | CNAME | `k8s-lb.alpininsight.ai`             | Ja    | Ops/Admin hinter CF Access       |
| `k8s-lb.alpininsight.ai`       | A     | `<LoadBalancer-IP>`                   | Nein  | Kubernetes Ingress LB            |

## Cloudflare-Einstellungen pro Subdomain

### mcp.alpininsight.ai

- **SSL/TLS:** Full (Strict) -- Zertifikat am Gateway erforderlich
- **WAF:** Managed Ruleset aktiviert
- **Rate Limiting:** 100 req/min pro Client-IP
- **Bot Management:** Deaktiviert (MCP-Clients sind programmatisch)
- **Browser Integrity Check:** Deaktiviert
- **Challenge Passage:** Deaktiviert

### mcp-partner.alpininsight.ai

- **SSL/TLS:** Full (Strict)
- **WAF:** Managed Ruleset + Custom Rules fuer Partner-IPs
- **Rate Limiting:** 50 req/min pro Client-IP (strenger)
- **IP Access Rules:** Optional Allowlist fuer Partner-IP-Ranges

### mcp-dev.alpininsight.ai

- **SSL/TLS:** Full -- Tunnel terminiert TLS
- **WAF:** Nur Basis-Regeln
- **Rate Limiting:** 200 req/min (Dev ist toleranter)
- **Cloudflare Tunnel:** Named Tunnel zum Dev-Cluster/Notebook

### ops-mcp.alpininsight.ai

- **SSL/TLS:** Full (Strict)
- **Cloudflare Access:** Aktiviert -- OIDC-Login erforderlich
- **Access Policy:** Nur `@alpininsight.ai` E-Mail-Domain
- **WAF:** Standard

## Wichtige Hinweise

1. **Kein Cloudflare Access vor `/mcp`-Endpoints** -- MCP-Clients erwarten
   die standardisierte OAuth-Discovery. CF Access wuerde den Flow brechen.

2. **Bot Management deaktivieren** fuer MCP-Subdomains -- Codex/Claude
   und andere Agents wuerden als Bots erkannt und blockiert.

3. **Browser Integrity Check deaktivieren** -- MCP-Clients senden keine
   Standard-Browser-Header.

4. **WebSocket-Support aktivieren** -- MCP kann SSE oder WebSocket
   als Transport nutzen.
