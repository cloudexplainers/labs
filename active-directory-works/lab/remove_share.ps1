# Undo setup_share.ps1 and remove Ben's Windows profile from this computer.
Remove-SmbShare shop -Force -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force C:\TeaShop -ErrorAction SilentlyContinue
Get-CimInstance Win32_UserProfile | Where-Object { $_.LocalPath -like '*\ben' -or $_.LocalPath -like '*\probeben' } | Remove-CimInstance
'srv clean'
