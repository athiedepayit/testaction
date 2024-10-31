module "mitest-is_maintenance" {
  domain        = "s3licensing.net"
  source        = "../../module/worker"
  script_path   = "maintenance.js"
  email         = "noreply@payitgov.com"
  enabled       = true
  whitelist_ips = local.worker_ip_whitelist
  # to add more sites to maintenance mode, just add them here
  patterns = [
    "asite-test.s3licensing.net/*",
    "s3lt-controlcenter.s3licensing.net/*",
  ]
}
