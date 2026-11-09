# Ana's file server for the lab: two local users, a "Shop Staff" group, and two shares.
# Run in an elevated Windows PowerShell on a Windows Server (or Windows 10/11 Pro) test machine.
#   shop    share: Shop Staff may change files; folder: Shop Staff may modify
#   orders  share: Everyone full control; folder: only Administrators and SYSTEM (the forgotten folder lock)
param([Parameter(Mandatory)][securestring]$Password)
foreach ($u in 'ana', 'ben') {
    if (-not (Get-LocalUser $u -ErrorAction SilentlyContinue)) {
        New-LocalUser $u -Password $Password -PasswordNeverExpires -AccountNeverExpires | Out-Null
    }
}
if (-not (Get-LocalGroup 'Shop Staff' -ErrorAction SilentlyContinue)) {
    New-LocalGroup 'Shop Staff' | Out-Null
    Add-LocalGroupMember 'Shop Staff' -Member ana, ben
}
New-Item -ItemType Directory -Force C:\ShopData\shop, C:\ShopData\orders | Out-Null
'12 teas in stock' | Set-Content C:\ShopData\shop\stock.txt
'Order 1041: 2 x green tea' | Set-Content C:\ShopData\orders\orders.txt
icacls C:\ShopData\shop /grant 'Shop Staff:(OI)(CI)M' | Out-Null
icacls C:\ShopData\orders /inheritance:r /grant 'Administrators:(OI)(CI)F' 'SYSTEM:(OI)(CI)F' | Out-Null
New-SmbShare -Name shop -Path C:\ShopData\shop -ChangeAccess 'Shop Staff' | Out-Null
New-SmbShare -Name orders -Path C:\ShopData\orders -FullAccess 'Everyone' | Out-Null
