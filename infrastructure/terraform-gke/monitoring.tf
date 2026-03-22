# 1. THE INSTALLER
resource "helm_release" "kube_prometheus_stack" {
  name             = "monitoring-stack"
  repository       = "https://prometheus-community.github.io/helm-charts"
  chart            = "kube-prometheus-stack"
  namespace        = "monitoring"
  create_namespace = true

  set = [
    {
      name  = "grafana.enabled"
      value = "true"
    }
  ]
}

# 2. THE CONFIGURATOR
resource "grafana_dashboard" "app_metrics" {
  config_json = file("${path.module}/dashboards/main-metrics.json")
  
  depends_on = [helm_release.kube_prometheus_stack]
}