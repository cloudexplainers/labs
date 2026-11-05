# Linux Package Managers: apt vs Snap vs Flatpak

Video: https://youtu.be/LuUzbFeknns  
Written version: https://cloudexplainers.com/linux-package-managers-apt-vs-snap-vs-flatpak/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### Three ways to install

```sh
# ana@ubuntu:~$
gimp --version
snap run gimp --version
flatpak run org.gimp.GIMP --version
```

### apt: Ubuntu's own packages

```sh
# ana@ubuntu:~$
sudo apt update
apt policy gimp
sudo apt install -y gimp
gimp --version
```

### Snap: one bundle per app

```sh
# ana@ubuntu:~$
sudo snap install gimp
du -h /var/lib/snapd/snaps/*.snap
which -a gimp
snap run gimp --version
```

### Flatpak: apps on a shared runtime

```sh
# ana@ubuntu:~$
sudo apt install -y flatpak
sudo flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
sudo flatpak install -y flathub org.gimp.GIMP
flatpak run org.gimp.GIMP --version
flatpak list --columns=application,version,size
```

### Round 2: Disk space

```sh
# ana@ubuntu:~$
sudo apt install -y gnome-calculator
sudo snap install gnome-calculator
sudo flatpak install -y flathub org.gnome.Calculator
```

### Round 3: The sandbox

```sh
# ana@ubuntu:~$
ls ~/Pictures; head -1 ~/.bashrc
snap run --shell gimp -c 'ls ~/Pictures; head -1 ~/.bashrc'
snap connections gimp
flatpak info --show-permissions org.gimp.GIMP
flatpak run --command=head org.gimp.GIMP -1 ~/.bashrc
flatpak override --user --nofilesystem=host org.gimp.GIMP
flatpak run --command=head org.gimp.GIMP -1 ~/.bashrc
```

### Round 4: Updates

```sh
# ana@ubuntu:~$
cat /etc/apt/apt.conf.d/20auto-upgrades
snap refresh --time
sudo flatpak update
```

### Which one to use

```sh
# ana@ubuntu:~$
apt show firefox
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
