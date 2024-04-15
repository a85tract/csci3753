$VIServer = "cs-vsphere.int.colorado.edu"
$GuestUsername = "<user>"
$GuestPassword = "<password>"
#This is the grouper group populated with enrollments from the sis
$ADGroup = "CS-SG-VDI CSCI OS"
#This will be used as part of vm name construction 
$Course = "csci3753"
$VMSeries = "vm1"
$answer = "hello_init"
#Save contents of the group into an object
$ADGroupObject = Get-ADGroupMember -Identity $ADGroup

$csvFilePath = "./PA1.csv"
$data = Import-Csv $csvFilePath
$answer = "hello_init"
$line = "="*80
Connect-VIServer $VIServer
for ($i = 0; $i -lt $ADGroupObject.Length; $i++) {
    $sis_login_id = $ADGroupObject[$i].Name
    $VMName = $Course+"-" + $VMSeries+ "-" + $sis_login_id
    $vm = Get-VM -Name $vmName
    Write-Output $vmName
    $commandList = @("echo `"<password>`" | sudo -S rmmod helloModule.ko","echo `"<password>`" | sudo -S insmod /home/kernel/modules/helloModule.ko",
                     "rm -r /tmp/test.c", "rm -r /tmp/pa1_test",
                     "wget http://ip:port/test.c -O /tmp/test.c", "gcc /tmp/test.c -o /tmp/pa1_test", "chmod +x /tmp/pa1_test", 
                     "echo `"<password>`" | sudo -S dmesg -c",
                     "/tmp/pa1_test",
                     "echo `"<password>`" | sudo -S dmesg",
                     "rm -r /tmp/test.c", "rm -r /tmp/pa1_test")

    foreach ($command in $commandList) {
        $exec_result = Invoke-VMScript -VM $VMName -GuestUser $GuestUsername -GuestPassword $GuestPassword -ScriptType Bash -ScriptText $command
        if ($command -eq $commandList[-3]) {
            Write-Output $exec_result.ScriptOutput
            $lines = $exec_result.ScriptOutput -split '\r?\n'
            $lineCount = $lines.Count
            Write-Output "Number of lines: $lineCount"
            $data | Where-Object { $_."SIS Login ID" -eq $sis_login_id } | ForEach-Object {
                if (-not $_) {
                    Write-Output "No student found with SIS Login ID: $sis_login_id"
                }
                else {
                    Write-Output "SIS Login ID: $($_."SIS Login ID")"
                    if ($lineCount -ge 3) {
                        Write-Output "PASS"
                        $_."PA1 - Syscalls & LKMs (1886853)" = "50.00"
                    } else {
                        Write-Output "FAILED"
                        $_."PA1 - Syscalls & LKMs (1886853)" = "0.00"
                    }
                }
            }
            Write-Output $line
        }
    }
}

$data | Export-Csv -Path "./PA1_out.csv" -NoTypeInformation 
Write-Output "Done."