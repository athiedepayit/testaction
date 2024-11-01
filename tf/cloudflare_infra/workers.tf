module "mitest-is_maintenance" {
  domain      = "s3licensing.net"
  source      = "../../module/worker"
  script_path = "maintenance.js"
  email       = "noreply@payitgov.com"
  # to add more sites to maintenance mode, just add them here
  patterns = [
    "test.s3gov.com/*",
  ]
  enabled       = true
  whitelist_ips = local.worker_ip_whitelist
}
