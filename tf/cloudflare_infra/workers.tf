module "mitest-is_maintenance" {
  domain      = "s3licensing.net"
  source      = "../../module/worker"
  script_path = "maintenance.js"
  email       = "noreply@payitgov.com"
  # to add more sites to maintenance mode, just add them here
  patterns = [
    "mo-scheduledjobs.s3licensing.com/*",
    "mo-webapi.s3licensing.com/*",
    "mo-agentlicensing.s3licensing.com/*",
    "mo-events.s3licensing.com/*",
    "mo-licensing.s3licensing.com/*",
    "mo-controlcenter.s3licensing.com/*",
  ]
  enabled       = true
  whitelist_ips = local.worker_ip_whitelist
}
