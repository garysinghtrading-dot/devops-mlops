#!/bin/bash
set -e

PROJECT_ID="machine-learning-416604"
REGION="us-central1"
REPO="eviction-microservices-repo"

SERVICES=("stock-data-service" "login-service" "eviction-service")

echo "=== Running Terraform Apply ==="
terraform -chdir=infrastructure apply -auto-approve

echo "=== Ensuring Artifact Registry Repository Exists ==="
if ! gcloud artifacts repositories describe $REPO --location=$REGION --project=$PROJECT_ID >/dev/null 2>&1; then
  echo "Creating repository $REPO..."
  gcloud artifacts repositories create $REPO \
    --repository-format=docker \
    --location=$REGION \
    --project=$PROJECT_ID
fi

echo "=== Configuring Docker Authentication ==="
gcloud auth configure-docker $REGION-docker.pkg.dev --quiet

echo "=== Building and Pushing Docker Images ==="
for SERVICE in "${SERVICES[@]}"; do
  echo "Building $SERVICE..."
  docker build -t $SERVICE ./services/$SERVICE

  echo "Tagging $SERVICE..."
  docker tag $SERVICE $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$SERVICE:latest

  echo "Pushing $SERVICE..."
  docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$SERVICE:latest
done

echo "=== Applying Kubernetes Manifests ==="
kubectl apply -f infrastructure/k8s/

echo "=== Deployment Complete ==="
