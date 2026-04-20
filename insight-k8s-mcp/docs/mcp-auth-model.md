# MCP Auth-Modell -- alpininsight.ai

## Ueberblick

Das Auth-Modell folgt dem MCP-Security-Standard und trennt strikt zwischen
Nordseite (Client -> Gateway) und Suedseite (Gateway -> Backend).

```
MCP-Client (Claude/Codex)
    |
    | OAuth 2.1 + PKCE
    | Bearer Token (audience-gebunden)
    |
    v
Envoy AI Gateway  (MCP Resource Server)
    |
    | Eigene Credentials (API-Key / mTLS / ServiceAccount)
    | KEIN Token-Passthrough
    |
    v
Backend MCP Server (privat)
```

-----

## Nordseite -- Client -> Gateway

### OAuth-Flow

1. Client entdeckt den MCP-Endpoint via `/.well-known/oauth-protected-resource`
2. Response enthaelt den `authorization_server` und die `resource`-URI
3. Client fuehrt OAuth Authorization Code Flow mit PKCE durch
4. IdP stellt Token mit korrekter Audience aus
5. Client sendet Bearer Token an den MCP-Endpoint

### Anforderungen

| Anforderung              | Detail                                                    |
|--------------------------|-----------------------------------------------------------|
| OAuth-Version            | OAuth 2.1 (Authorization Code + PKCE)                    |
| Discovery                | OIDC Discovery oder OAuth AS Metadata                    |
| PKCE                     | Pflicht -- MCP-Clients muessen PKCE unterstuetzen         |
| `resource`-Parameter     | Muss auf kanonischen Endpoint zeigen                      |
| Audience                 | Muss mit `resource` uebereinstimmen                       |
| Scopes                   | Pro Route/Trust-Zone definiert                            |

### MCP-Discovery Response

```json
{
  "resource": "https://mcp.alpininsight.ai/mcp",
  "authorization_servers": [
    "https://login.alpininsight.ai/realms/internal"
  ],
  "scopes_supported": [
    "mcp:base",
    "tools.openapi.read",
    "tools.github.read",
    "tools.context7.read"
  ]
}
```

### IdP-Konfiguration

Der OIDC-Provider (Entra ID / Keycloak / Authentik) muss:

- Authorization Code Flow mit PKCE unterstuetzen
- `resource`-Parameter akzeptieren und in Audience einbetten
- Scopes wie `mcp:base`, `tools.*` definierbar machen
- OIDC Discovery unter `/.well-known/openid-configuration` bereitstellen

-----

## Suedseite -- Gateway -> Backend

### Designprinzip: Kein Token-Passthrough

Die MCP-Spec verlangt Audience-Bindung. Ein Client-Token mit
`aud: mcp.alpininsight.ai` darf **nicht** an ein Backend weitergeleitet werden,
das eine andere Audience erwartet. Das ist kein optionaler Best Practice,
sondern ein Sicherheitsmodell der Spec.

### Empfohlene Backend-Auth-Methoden

| Methode          | Anwendungsfall                                          |
|------------------|---------------------------------------------------------|
| Kein Auth        | Backend ist nur via ClusterIP erreichbar (empfohlen)    |
| API-Key          | Backend erwartet statisches Token im Header             |
| mTLS             | Gegenseitige Zertifikat-Validierung                     |
| ServiceAccount   | Kubernetes-native Auth via TokenReview                  |

### Konfiguration in Envoy AI Gateway

```yaml
# Backend mit API-Key Auth
backendRefs:
  - name: github-mcp
    securityPolicy:
      apiKey:
        secretRef:
          name: github-mcp-api-key
          namespace: mcp-system
```

-----

## Scope-Zuschnitt je Endpoint

### mcp.alpininsight.ai/mcp (Internal)

| Scope                  | Berechtigung                               |
|------------------------|--------------------------------------------|
| `mcp:base`             | Basis-MCP-Zugang (tools/list, ping)        |
| `tools.openapi.read`   | OpenAPI-Tools lesen/ausfuehren             |
| `tools.openapi.write`  | OpenAPI-Tools mit Schreibzugriff           |
| `tools.github.read`    | GitHub-Tools (Issues, PRs, Repos lesen)    |
| `tools.github.write`   | GitHub-Tools (Issues erstellen, PRs mergen)|
| `tools.context7.read`  | Context7-Tools (Library-Docs lesen)        |

### mcp-partner.alpininsight.ai/mcp (Partner)

| Scope                  | Berechtigung                               |
|------------------------|--------------------------------------------|
| `mcp:base`             | Basis-MCP-Zugang                           |
| `tools.partner.*`      | Nur Partner-spezifische Tools              |

### mcp-dev.alpininsight.ai/mcp (Dev)

| Scope                  | Berechtigung                               |
|------------------------|--------------------------------------------|
| `mcp:base`             | Basis-MCP-Zugang                           |
| `tools.*`              | Alle Tools (Dev-Umgebung)                  |

-----

## Sicherheitshinweise

1. **Cloudflare Access nicht vor /mcp setzen**, wenn MCP-Clients darauf
   zugreifen. MCP-Clients erwarten die standardisierte OAuth/MCP-Discovery
   ueber `WWW-Authenticate` und `/.well-known/oauth-protected-resource`.
   Cloudflare Access ist ideal fuer `ops-mcp.alpininsight.ai`.

2. **Token-Lifetime kurz halten** -- MCP-Sessions koennen langlebig sein,
   Tokens sollten es nicht. Refresh-Tokens mit Rotation verwenden.

3. **Scopes minimal halten** -- Nur die tatsaechlich benoetigten Tool-Scopes
   zuweisen. `tools.*` nur in Dev-Umgebungen.

4. **Backend-Isolation sicherstellen** -- Backends sollten nur via ClusterIP
   erreichbar sein. NetworkPolicies einsetzen.
