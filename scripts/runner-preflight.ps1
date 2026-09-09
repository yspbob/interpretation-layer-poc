# Inventories prerequisites without installing software or changing machine settings.
# The local report is not containment evidence and must not be committed publicly.
[CmdletBinding()]
param([ValidateSet('laptop', 'home', 'unassigned')][string]$MachineAlias = 'unassigned')

$ErrorActionPreference = 'Stop'
$observations = [ordered]@{}
$unknown = [System.Collections.Generic.List[string]]::new()
foreach ($item in @(
    @{ Name = 'os'; Class = 'Win32_OperatingSystem' },
    @{ Name = 'system'; Class = 'Win32_ComputerSystem' },
    @{ Name = 'cpu'; Class = 'Win32_Processor' }
)) {
    try { $observations[$item.Name] = @(Get-CimInstance -ClassName $item.Class) }
    catch { $observations[$item.Name] = @(); $unknown.Add($item.Name + ': query unavailable') }
}
$os = $observations.os | Select-Object -First 1
$system = $observations.system | Select-Object -First 1
$processors = @($observations.cpu)
$vboxVersion = $null
$vboxPath = $null
$vboxCommand = Get-Command VBoxManage.exe -ErrorAction SilentlyContinue
if ($vboxCommand) { $vboxPath = $vboxCommand.Source }
elseif ($env:ProgramFiles) {
    $candidate = Join-Path $env:ProgramFiles 'Oracle\VirtualBox\VBoxManage.exe'
    if (Test-Path -LiteralPath $candidate -PathType Leaf) { $vboxPath = $candidate }
}
if ($vboxPath) {
    try {
        $versionOutput = & $vboxPath --version 2>&1
        if ($LASTEXITCODE -ne 0) { throw 'Version query failed' }
        $vboxVersion = ($versionOutput | Out-String).Trim()
    } catch { $unknown.Add('VirtualBox: version query unavailable') }
}
$freeDiskGiB = $null
try {
    $projectDrive = (Get-Item -LiteralPath $PSScriptRoot).PSDrive
    if ($null -ne $projectDrive.Free) { $freeDiskGiB = [math]::Round($projectDrive.Free / 1GB, 1) }
} catch { $unknown.Add('project disk: free space unavailable') }
$report = [ordered]@{
    schemaVersion = 1
    observedAtUtc = [DateTime]::UtcNow.ToString('o')
    machineAlias = $MachineAlias
    purpose = 'Prerequisite inventory only; not containment qualification'
    os = if ($os) { @{ caption = $os.Caption; version = $os.Version; architecture = $os.OSArchitecture } } else { $null }
    totalMemoryGiB = if ($system) { [math]::Round($system.TotalPhysicalMemory / 1GB, 1) } else { $null }
    availableMemoryGiB = if ($os) { [math]::Round($os.FreePhysicalMemory / 1MB, 1) } else { $null }
    hypervisorPresent = if ($system) { $system.HypervisorPresent } else { $null }
    processors = @($processors | ForEach-Object { @{
        architectureCode = $_.Architecture
        logicalProcessors = $_.NumberOfLogicalProcessors
        virtualizationFirmwareEnabled = $_.VirtualizationFirmwareEnabled
    } })
    projectDiskFreeGiB = $freeDiskGiB
    virtualBoxVersion = $vboxVersion
    unknownObservations = @($unknown.ToArray())
    readyForModelRuns = $false
    requiredNextChecks = @(
        'Confirm supported x86-64 host and VirtualBox backend without disabling Windows security features',
        'Install and lock the proposed guest/container stack if prerequisites permit',
        'Measure smoke-test resources; free memory and disk must be rechecked at launch',
        'Implement and pass controller, transport, container and VM boundary probes on this host',
        'Configure and verify separate private record storage and handoff',
        'Satisfy working-plan qualification and authorised-budget gates'
    )
}
$reportDirectory = Join-Path (Split-Path -Parent $PSScriptRoot) 'local-runs'
if (-not (Test-Path -LiteralPath $reportDirectory)) { New-Item -ItemType Directory -Path $reportDirectory | Out-Null }
$reportPath = Join-Path $reportDirectory ('runner-preflight-' + $MachineAlias + '.json')
$report | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $reportPath -Encoding UTF8
Write-Output ('Local prerequisite report: ' + $reportPath)
Write-Output ('Memory (GiB): ' + $report.totalMemoryGiB + '; VirtualBox: ' + $(if ($vboxVersion) { $vboxVersion } else { 'not detected or unverified' }))
Write-Output ('Unavailable observations: ' + $unknown.Count + '; ready for model runs: false')
