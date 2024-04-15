$VIServer = "cs-vsphere.int.colorado.edu"
$GuestUsername = "<user>"
$GuestPassword = "<password>"
#This is the grouper group populated with enrollments from the sis
$ADGroup = "CS-SG-VDI CSCI OS"
#This will be used as part of vm name construction 
$Course = "csci3753"
$VMSeries = "vm1"
#Save contents of the group into an object
$ADGroupObject = Get-ADGroupMember -Identity $ADGroup

$csvFilePath = "./2024-02-12T1352_Grades-CSCI_3753.csv"
$data = Import-Csv $csvFilePath
$answer = "6.6.11-rev1"

Connect-VIServer $VIServer
for ($i = 0; $i -lt $ADGroupObject.Length; $i++) {
    $sis_login_id = $ADGroupObject[$i].Name
    $VMName = $Course+"-" + $VMSeries+ "-" + $sis_login_id
    $vm = Get-VM -Name $vmName
    try {
        $exec_result = Invoke-VMScript -VM $VMName -GuestUser $GuestUsername -GuestPassword $GuestPassword -ScriptType Bash -ScriptText "ls /boot"
    }
    catch {
        Write-Output "VM: $($vm.Name), Kernel Version: Failed to execute the script"
        $data | Where-Object { $_."SIS Login ID" -eq $sis_login_id } | ForEach-Object {
            Write-Output "SIS Login ID: $($_."SIS Login ID")"
            $_."PA0 - Kernel (1846998)" = 0.00
        }
        continue
    }
    Write-Output "VM: $($vm.Name), Kernel Version: $($exec_result.ScriptOutput)"

    $data | Where-Object { $_."SIS Login ID" -eq $sis_login_id } | ForEach-Object {
        if (-not $_) {
            Write-Output "No student found with SIS Login ID: $sis_login_id"
        }
        else {
            Write-Output "SIS Login ID: $($_."SIS Login ID")"
            if ($exec_result.ScriptOutput -match $answer) {
                Write-Output "PASS"
                $_."PA0 - Kernel (1846998)" = 50.00
            } else {
                Write-Output "FAILED"
                $_."PA0 - Kernel (1846998)" = 0.00
            }
        }
    }
}

$data | Export-Csv -Path "./PA0.csv" -NoTypeInformation 
Write-Output "Done."