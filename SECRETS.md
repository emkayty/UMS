# Secrets Management Guide

## Using Environment Variables

1. Create `.env` file from example:
```bash
cp .env.example .env
```

2. Update with production values:
- SECRET_KEY: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
- DATABASE_URL: Your PostgreSQL connection string
- JWT_SECRET_KEY: Generate new key
- EMAIL_HOST_PASSWORD: Use App Password for Gmail

## Using Kubernetes Secrets

```bash
# Create secrets
kubectl create secret generic ums-secrets \
  --from-literal=secret-key='YOUR-SECRET' \
  --from-literal=database-url='YOUR-DB-URL' \
  --namespace=ums
```

## Using AWS Secrets Manager

```bash
# Store secret
aws secretsmanager create-secret \
  --name ums/production \
  --secret-string '{"DATABASE_URL":"..."}'
```

## Using HashiCorp Vault

```bash
# Store secret
vault kv put ums/production secret-key=YOUR-KEY
```