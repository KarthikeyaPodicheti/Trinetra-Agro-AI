param(
  [switch]$CheckOnly,
  [switch]$StartGateway
)

$argsList = @("production_runner.py")
if ($CheckOnly) { $argsList += "--check-only" }
if ($StartGateway) { $argsList += "--start-gateway" }

python $argsList
