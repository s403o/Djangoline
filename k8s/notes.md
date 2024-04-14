# OpenTelemetry Helm Chart Installation
```bash
kubectl create namespace monitoring
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm install otel-collector open-telemetry/opentelemetry-collector --set mode=deployment --set resources.requests.cpu=100m --set resources.requests.memory=100Mi --set resources.limits.cpu=200m --set resources.limits.memory=200Mi -n monitoring
helm install otel-operator open-telemetry/opentelemetry-operator -n monitoring
```
# Create the namespace for cert-manager
```bash 
kubectl create namespace cert-manager

# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io

# Update your local Helm chart repository cache
helm repo update

# Install the cert-manager Helm chart
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.6.1 \
  --set installCRDs=true
```

# ArgoCD Helm Chart Installation
```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm install argo-cd argo/argo-cd
```