#!/bin/bash

set -e

echo "Introducing incorrect backend Service selector..."

kubectl patch service backend \
  -p '{"spec":{"selector":{"app":"backend-broken"}}}'

echo ""
echo "Checking backend Pod..."
kubectl get pods -l app=backend

echo ""
echo "Checking backend Service..."
kubectl describe service backend

echo ""
echo "Checking backend EndpointSlices..."
kubectl get endpointslices \
  -l kubernetes.io/service-name=backend

echo ""
echo "Failure simulation completed."
echo "Expected: Backend Service has no ready endpoints."
