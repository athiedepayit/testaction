module "mitest-is_maintenance" {
  domain      = "s3licensing.net"
  source      = "../../module/worker"
  script_path = "maintenance.js"
  email       = "noreply@payitgov.com"
  # to add more sites to maintenance mode, just add them here
  patterns = [
    "ebci-agentlicensing.s3licensing.com/*",
    "ebci-events.s3licensing.com/*",
    "ebci-licensing.s3licensing.com/*",
    "ebci-controlcenter.s3licensing.com/*",
  ]
  enabled       = true
  whitelist_ips = local.worker_ip_whitelist
}
