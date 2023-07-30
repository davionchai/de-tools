enable-addons:
	minikube addons enable metrics-server
	minikube addons enable ingress-dns

addons-list:
	minikube addons list

minikube_disk:
	minikube ssh "df -h"

minikube_start:
	minikube start --vm-driver none
	minikube addons enable metrics-server

dependency:
	helm dependency build

install:
	helm install spark ./ --namespace spark --create-namespace --values ./values.yaml

upgrade:
	helm upgrade spark ./ --namespace spark --values ./values.yaml

delete:
	helm uninstall spark --namespace spark

runwebserver:
	kubectl port-forward svc/spark-master-svc 8080:80 --namespace spark 

output:
	helm get values spark --namespace spark -a > output-values.yaml

context:
	kubectl config get-contexts
	kubectl config use-context minikube
