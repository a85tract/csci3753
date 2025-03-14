#Hossein: This script 
# Add this at the beginning of your script
if (-not (Get-Module -ListAvailable -Name ActiveDirectory)) {
    Write-Error "ActiveDirectory module not found. Please install RSAT tools."
    exit 1
}
Import-Module ActiveDirectory
# Add this before attempting to connect to vSphere
if (-not (Get-Module -ListAvailable -Name VMware.PowerCLI)) {
    Write-Error "VMware.PowerCLI module not found. Install using: Install-Module -Name VMware.PowerCLI -RequiredVersion 12.7.0.20091289"
    exit 1
}
Import-Module VMware.PowerCLI

# Set PowerCLI configuration to handle certificate issues
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false



$VIServer = "cs-vsphere.int.colorado.edu"
$GuestUsername = "instructor"
$GuestPassword = "3753InstructorS25"
#This is the grouper group populated with enrollments from the sis
$ADGroup = "CS-SG-VDI CSCI 2W9"
#This will be used as part of vm name construction 
$Course = "csci3753"
$VMSeries = "vm1"
#Save contents of the group into an object
$ADGroupObject = Get-ADGroupMember -Identity $ADGroup

$csvFilePath = "./2025-03-04T1133_Grades-CSCI_3753_pa0.csv"
$data = Import-Csv $csvFilePath
$answer = "6.6.11-rev1"

# Connect to vSphere
try {
    Connect-VIServer $VIServer
} catch {
    Write-Error "Failed to connect to vSphere server: $_"
    exit 1
}

for ($i = 0; $i -lt $ADGroupObject.Length; $i++) {
    $sis_login_id = $ADGroupObject[$i].Name
    $VMName = $Course+"-" + $VMSeries+ "-" + $sis_login_id
    
    try {
        $vm = Get-VM -Name $VMName -ErrorAction Stop
        
        # Check if VM is powered on
        if ($vm.PowerState -ne "PoweredOn") {
            Write-Warning "VM $VMName is not powered on. Current state: $($vm.PowerState)"
            $data | Where-Object { $_."SIS Login ID" -eq $sis_login_id } | ForEach-Object {
                $_."PA0 - Kernel (2200811)" = 0.00
            }
            continue
        }

        # Try to get kernel version with improved command
        try {
            $exec_result = Invoke-VMScript -VM $vm -GuestUser $GuestUsername -GuestPassword $GuestPassword -ScriptType Bash -ScriptText "printf $GuestPassword | sudo -S -u root ls /boot/ | grep rev1" -ErrorAction Stop
            Write-Output "VM: $($vm.Name), Found rev1 kernels: $($exec_result.ScriptOutput)"

            $data | Where-Object { $_."SIS Login ID" -eq $sis_login_id } | ForEach-Object {
                if ($exec_result.ScriptOutput.Trim() -ne "") {
                    Write-Output "PASS - Found rev1 kernel"
                    $_."PA0 - Kernel (2200811)" = 50.00
                } else {
                    Write-Output "FAILED - No rev1 kernel found"
                    $_."PA0 - Kernel (2200811)" = 0.00
                }
            }
        } catch {
            Write-Error "Failed to execute command on VM $VMName : $_"
            $data | Where-Object { $_."SIS Login ID" -eq $sis_login_id } | ForEach-Object {
                $_."PA0 - Kernel (2200811)" = 0.00
            }
        }
    } catch {
        Write-Error "Failed to process VM $VMName : $_"
        $data | Where-Object { $_."SIS Login ID" -eq $sis_login_id } | ForEach-Object {
            $_."PA0 - Kernel (2200811)" = 0.00
        }
    }

}

# Export results
$data | Export-Csv -Path "./PA0.csv" -NoTypeInformation
Write-Output "Done."

# Disconnect from vSphere
Disconnect-VIServer -Confirm:$false
Disconnect-VIServer -Confirm:$false
