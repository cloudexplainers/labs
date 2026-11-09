# Undo setup_server.ps1 (and turn the SMB-In firewall rule back on if the lab left it off).
Remove-SmbShare shop -Force -ErrorAction SilentlyContinue
Remove-SmbShare orders -Force -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force C:\ShopData -ErrorAction SilentlyContinue
Get-LocalUser ana, ben -ErrorAction SilentlyContinue | Remove-LocalUser
Remove-LocalGroup 'Shop Staff' -ErrorAction SilentlyContinue
Enable-NetFirewallRule -DisplayName 'File and Printer Sharing (SMB-In)'
