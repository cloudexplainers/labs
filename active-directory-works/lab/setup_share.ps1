# The tea shop's file share on a domain-joined Windows Server: only the domain group "Tea Shop Staff" may use it.
# Run in an elevated Windows PowerShell on a member server of a test domain, after the group exists.
# The group is given by its SID: a computer caches name lookups, so a group deleted and made again under the
# same name could otherwise resolve to the old SID.
param([Parameter(Mandatory)][string]$GroupSid)
New-Item -ItemType Directory -Force C:\TeaShop\shop | Out-Null
'12 teas in stock' | Set-Content C:\TeaShop\shop\stock.txt
icacls C:\TeaShop\shop /inheritance:r /grant 'Administrators:(OI)(CI)F' 'SYSTEM:(OI)(CI)F' "*$($GroupSid):(OI)(CI)M" | Out-Null
New-SmbShare -Name shop -Path C:\TeaShop\shop -FullAccess 'Everyone' | Out-Null
(icacls C:\TeaShop\shop) -join "`n"
