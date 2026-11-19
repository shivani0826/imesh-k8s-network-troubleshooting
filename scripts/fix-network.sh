#!/bin/bash

set -e

echo "Restoring correct backend Service selector..."

kubectl patch service backend \
  -p '{"spec":{"selector":{"app":"backend"}}}'

echo ""
echo "Waiting for backend EndpointSlice..."

sleep 3

kubectl get endpointslices \
  -l kubernetes.io/service-name=backend

echo ""
echo "Testing application connectivity..."

kubectl exec deployment/client -- \
  python -c 'import urllib.request; print(urllib.request.urlopen("http://frontend:8080", timeout=5).read().decode())'

echo ""
echo "Network recovery successful!"
