# How to Fix 'Windows Cannot Access' Network Share Errors (SMB)

Video: https://youtu.be/onf1rzyfieM  
Written version: https://cloudexplainers.com/how-to-fix-windows-cannot-access-network-share-errors-smb/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/remove_server.ps1`](lab/remove_server.ps1)
- [`lab/setup_server.ps1`](lab/setup_server.ps1)

## Commands, in the order the video runs them

### Windows cannot access the share

```sh
PS C:\Work> net use \\files\shop /user:files\ben
```

### The usual fix: is port 445 open?

```sh
PS C:\Work> Test-NetConnection files -Port 445
PS C:\> Get-NetFirewallRule -DisplayName 'File and Printer Sharing (SMB-In)', 'File Server Remote Management (SMB-In)' | Format-Table DisplayName, Profile, Enabled
PS C:\> Enable-NetFirewallRule -DisplayName 'File and Printer Sharing (SMB-In)'
PS C:\> Get-NetFirewallRule -DisplayName 'File and Printer Sharing (SMB-In)', 'File Server Remote Management (SMB-In)' | Format-Table DisplayName, Profile, Enabled
PS C:\Work> Test-NetConnection files -Port 445
PS C:\Work> net use \\files\shop /user:files\ben
PS C:\Work> net use \\files\shop /user:files\ben
PS C:\Work> dir \\files\shop
PS C:\Work> net use \\files\shop /delete
```

### Can it find the server?

```sh
PS C:\Work> Test-NetConnection fles -Port 445
PS C:\Work> net use \\fles\shop /user:files\ben
```

### Is the share name right?

```sh
PS C:\Work> net use \\files\shopp /user:files\ben
PS C:\Work> net view \\files
# ana@laptop:~$
nc -zv files 445
smbclient //files/shopp -U ben
smbclient //files/shop -U ben
```

### Two locks on every share

```sh
PS C:\Work> net use \\files\shop /user:files\ben
PS C:\Work> dir \\files\orders
PS C:\> Get-SmbShareAccess orders
PS C:\> icacls C:\ShopData\orders
PS C:\> icacls C:\ShopData\orders /grant 'Shop Staff:(OI)(CI)RX'
PS C:\Work> dir \\files\orders
```

### One account per server

```sh
PS C:\Work> net use \\files\orders /user:files\ana
PS C:\Work> net use
PS C:\Work> net use * /delete /y
PS C:\Work> net use \\files\orders /user:files\ana
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
