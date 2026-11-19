#!/bin/bash

set -e

echo "Deploying backend..."
kubectl apply -f manifests/backend.yaml

echo "Deploying frontend..."
kubectl apply -f manifests/frontend.yaml

echo "Deploying client..."
kubectl apply -f manifests/client.yaml

echo "Waiting for deployments..."

kubectl rollout status deployment/backend
kubectl rollout status deployment/frontend
kubectl rollout status deployment/client

echo "All deployments completed successfully!"

echo "Checking Pods..."
kubectl get pods -o wide

echo "Checking Services..."
kubectl get svc

echo "Checking EndpointSlices..."
kubectl get endpointslices
