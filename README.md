## Once off install

### Setup Flask

cp .env.example .env.local
awk -v key="$(openssl rand -base64 42)" '/^SECRET_KEY=/ {sub(/=.*/, "=" key)} 1' .env > temp_env && mv temp_env .env


poetry env use 3.12
poetry lock --no-update
poetry install

poetry shell
flask db upgrade

flask run --host 0.0.0.0 --port=5001 --debug


### Start Middleware - redis, postgres, plugins
cp middleware.env.example middleware.env
docker compose -f docker-compose.middleware.yaml up -d


### Start Web

cd web
pnpm i
pnpm run dev





## alternative to docker middleware path

### Start redis
brew services stop redis
redis-server --requirepass difyai123456


### Run Celery
poetry shell
celery -A app.celery worker -P gevent -c 1 --loglevel INFO -Q dataset,generation,mail,ops_trace


### Create local DB

docker create \
  --name postgres15 \
  --env POSTGRES_PASSWORD=Peter12q \
  --env POSTGRES_USER=genaitooladmin \
  --env POSTGRES_DB=genaitool \
  --env PGDATA=/var/lib/postgresql/data/pgdata \
  --volume postgres15_data:/var/lib/postgresql/data \
  --publish 5432:5432 \
  postgres:15

### Setup Database
flask db-upgrade





## Usefull COmmands

### Delete Data
cd api
poetry shell
python scripts/reset_db


### S3 Seeding environment

for var in \
  "STORAGE_TYPE=s3" \
  "S3_ENDPOINT=https://YOUR-S3-BUCKET.s3.ap-southeast-2.amazonaws.com" \
  "S3_REGION=ap-southeast-2" \
  "S3_BUCKET_NAME=your-bucket-name" \
  "S3_ACCESS_KEY=YOUR_AWS_ACCESS_KEY_ID" \
  "S3_SECRET_KEY=YOUR_AWS_SECRET_ACCESS_KEY" \
  "NGINX_HTTPS_ENABLED=true" \
  "NGINX_SERVER_NAME=your-domain.example.org" \
  "NGINX_CLIENT_MAX_BODY_SIZE=100m" \
  "UPLOAD_FILE_BATCH_LIMIT=10" \
  "UPLOAD_FILE_SIZE_LIMIT=60" \
  "NGINX_SSL_CERT_FILENAME=your-cert.crt" \
  "NGINX_SSL_CERT_KEY_FILENAME=your-key.key" \
  "CERTBOT_EMAIL=your-email@example.com" \
  "CERTBOT_DOMAIN=your-domain.example.org" \
  "CERTBOT_OPTIONS=--non-interactive --agree-tos"
do
  key=$(echo "$var" | cut -d= -f1)
  value=$(echo "$var" | cut -d= -f2-)
  if grep -q "^$key=" .env; then
    sed -i.bak -E "s|^$key=.*|$var|" .env
  else
    echo "$var" >> .env
  fi
done


### Azure Seeding environment


for var in \
  "STORAGE_TYPE=azure-blob" \
  "AZURE_BLOB_ACCOUNT_NAME=your-storage-account-name" \
  "AZURE_BLOB_ACCOUNT_KEY=YOUR_AZURE_STORAGE_ACCOUNT_KEY" \
  "AZURE_BLOB_CONTAINER_NAME=your-container-name" \
  "AZURE_BLOB_ACCOUNT_URL=https://your-account.blob.core.windows.net" \
  "NGINX_HTTPS_ENABLED=false" \
  "NGINX_SERVER_NAME=your-domain.example.com" \
  "NGINX_CLIENT_MAX_BODY_SIZE=100m" \
  "UPLOAD_FILE_BATCH_LIMIT=10" \
  "UPLOAD_FILE_SIZE_LIMIT=60" \
  "NGINX_SSL_CERT_FILENAME=your-cert.crt" \
  "NGINX_SSL_CERT_KEY_FILENAME=your-key.key" \
  "CERTBOT_EMAIL=your-email@example.com" \
  "CERTBOT_DOMAIN=your-domain.example.com" \
  "CERTBOT_OPTIONS=--non-interactive --agree-tos"
do
  key=$(echo "$var" | cut -d= -f1)
  value=$(echo "$var" | cut -d= -f2-)
  if grep -q "^$key=" .env; then
    # Mac-compatible version of sed in-place edit
    sed -i '' -E "s|^$key=.*|$var|" .env
  else
    echo "$var" >> .env
  fi
done




### Add SSH Key
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
cat ~/.ssh/id_rsa.pub
-- Add this to github
git clone git@github.com:SeanPreusse/ArgentiGenAI.git






## Packages
https://docs.dify.ai/plugins/publish-plugins/package-plugin-file-and-publish
https://github.com/langgenius/dify-plugin-daemon
https://docs.dify.ai/plugins/quick-start/develop-plugins/initialize-development-tools


## Docker Hub
make build-web
or
make push-web
or
make build-push-all
