# Démo CKE (Kubernetes managé, bêta)

| Fichier | Quoi |
|---|---|
| `whoami.yaml` | Deployment (2 réplicas de `traefik/whoami:v1.11.0`) + Service ClusterIP |
| `whoami-lb.yaml` | Service `LoadBalancer` qui expose whoami publiquement (quota par défaut : un par organisation) |

## Le refaire chez vous

```bash
clever features enable k8s                        # une fois (bêta)
clever k8s create demo --watch                    # ajoutez --org <org> si besoin
mkdir -p ~/.kube
clever k8s get-kubeconfig demo > ~/.kube/cc-demo.yaml
export KUBECONFIG=~/.kube/cc-demo.yaml            # n'écrase pas votre ~/.kube/config
kubectl get nodes
kubectl create namespace demo
kubectl apply -n demo -f whoami.yaml
kubectl get pods -n demo -o wide
kubectl port-forward -n demo svc/whoami 8081:80   # puis curl http://localhost:8081/
```

⚠️ Le kubeconfig donne un accès complet au cluster : traitez-le comme un secret. Un cluster consomme des crédits : supprimez-le après (`clever k8s delete demo`).
