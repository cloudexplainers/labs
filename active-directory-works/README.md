# How Active Directory Works

Video: https://youtu.be/LEO35h3DJAw  
Written version: https://cloudexplainers.com/how-active-directory-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/remove_share.ps1`](lab/remove_share.ps1)
- [`lab/setup_share.ps1`](lab/setup_share.ps1)

## Commands, in the order the video runs them

### One password, every door

```sh
# ben@ben-laptop:~$
ssh ben@lab.internal@srv01
PS C:\Users\ben> whoami
PS C:\Users\ben> hostname
```

### The directory

```sh
PS C:\TeaShop> New-ADOrganizationalUnit -Name TeaShop -Path 'DC=lab,DC=internal'
PS C:\TeaShop> New-ADGroup 'Tea Shop Staff' -GroupScope Global -Path 'OU=TeaShop,DC=lab,DC=internal'
PS C:\TeaShop> New-ADUser ben -GivenName Ben -Path 'OU=TeaShop,DC=lab,DC=internal' -AccountPassword (Read-Host -AsSecureString 'Password') -Enabled $true
PS C:\TeaShop> Get-ADUser ben
```

### Signing in with tickets

```sh
PS C:\Users\ben> klist
```

### Groups open the doors

```sh
PS C:\Users\ben> dir \\srv01\shop
PS C:\TeaShop> Add-ADGroupMember 'Tea Shop Staff' -Members ben
PS C:\TeaShop> Get-ADGroupMember 'Tea Shop Staff' | Format-Table Name, ObjectClass
PS C:\Users\ben> dir \\srv01\shop
PS C:\Users\ben> whoami /groups | Select-String 'Tea Shop'
PS C:\Users\ben> exit
# ben@ben-laptop:~$
ssh ben@lab.internal@srv01
PS C:\Users\ben> whoami /groups | Select-String 'Tea Shop'
PS C:\Users\ben> dir \\srv01\shop
```

### Rules in one place

```sh
PS C:\TeaShop> Get-ADDefaultDomainPasswordPolicy | Format-List MinPasswordLength, ComplexityEnabled, MaxPasswordAge
PS C:\TeaShop> Set-ADAccountPassword ben -Reset -NewPassword (ConvertTo-SecureString 'tea1' -AsPlainText -Force)
PS C:\Users\ben> dir \\dc01\sysvol\lab.internal\Policies
PS C:\Users\ben> klist | Select-String 'Server:'
```

### When someone leaves

```sh
PS C:\TeaShop> Disable-ADAccount ben
PS C:\TeaShop> Get-ADUser ben | Format-List Name, Enabled
# ben@ben-laptop:~$
ssh ben@lab.internal@srv01
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
