# Cloudflare Tunnel -- Dev-Umgebung

## Zweck

`mcp-dev.alpininsight.ai` wird ueber einen Cloudflare Named Tunnel
an den Dev-Cluster oder ein lokales Notebook angebunden. Der Tunnel
ersetzt die Notwendigkeit einer oeffentlichen IP oder eines LoadBalancers
fuer die Dev-Umgebung.

## Architektur

```
MCP-Client
    |
    v
mcp-dev.alpininsight.ai  (Cloudflare DNS, proxied)
    |
    v
Cloudflare Tunnel Netzwerk
    |
    v
cloudflared (im Dev-Cluster oder lokal)
    |
    v
Envoy AI Gateway (Dev-Instanz) oder direkt zum MCP-Server
```

## Setup

### 1. Tunnel erstellen

```bash
cloudflared tunnel create mcp-dev-tunnel
```

Output: Tunnel-ID und Credentials-Datei.

### 2. DNS-Eintrag anlegen

```bash
cloudflared tunnel route dns mcp-dev-tunnel mcp-dev.alpininsight.ai
```

Erstellt automatisch einen CNAME-Eintrag:
`mcp-dev.alpininsight.ai -> <tunnel-id>.cfargotunnel.com`

### 3. Tunnel-Konfiguration

```yaml
# ~/.cloudflared/config.yml
tunnel: <tunnel-id>
credentials-file: /root/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: mcp-dev.alpininsight.ai
    service: http://localhost:8080
    originRequest:
      noTLSVerify: true
  - service: http_status:404
```

### 4. Tunnel starten

```bash
# Lokal
cloudflared tunnel run mcp-dev-tunnel

# Als Kubernetes Deployment
kubectl apply -f cloudflared-deployment.yaml
```

### 5. Kubernetes Deployment (optional)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloudflared-dev
  namespace: mcp-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cloudflared-dev
  template:
    metadata:
      labels:
        app: cloudflared-dev
    spec:
      containers:
        - name: cloudflared
          image: cloudflare/cloudflared:latest
          args:
            - tunnel
            - --config
            - /etc/cloudflared/config.yml
            - run
          volumeMounts:
            - name: config
              mountPath: /etc/cloudflared
              readOnly: true
            - name: credentials
              mountPath: /etc/cloudflared/creds
              readOnly: true
      volumes:
        - name: config
          configMap:
            name: cloudflared-dev-config
        - name: credentials
          secret:
            secretName: cloudflared-dev-credentials
```

## Anwendungsfaelle

### Notebook-Zugriff

Entwickler startet lokales Notebook mit MCP-Server. Tunnel leitet
`mcp-dev.alpininsight.ai` direkt an `localhost:8080` weiter.
Claude/Codex koennen den Dev-MCP-Server erreichen.

### Test-Cluster

Tunnel laeuft als Pod im Test-Cluster und leitet an den internen
Envoy AI Gateway (Dev-Instanz) weiter. Gleiche MCP-Route-Konfiguration
wie Produktion, aber mit separater Audience.

## Sicherheit

- Tunnel-Credentials als Kubernetes Secret speichern
- `noTLSVerify` nur wenn Backend kein gueltiges Zertifikat hat
- Cloudflare Access kann **optional** vor dem Dev-Tunnel stehen
  (akzeptabel, da Dev-Nutzer den Browser-Login-Flow durchlaufen koennen)
- Access-Policy: Nur `@alpininsight.ai` Domain
