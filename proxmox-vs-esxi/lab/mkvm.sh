# usage (on host via ssh): sh mkvm.sh NAME MEM_MB NIC_TYPE ISO DISK_GB GUESTOS FIRMWARE
set -e
N=$1; MEM=$2; NIC=$3; ISO=$4; DG=$5; GOS=$6; FW=${7:-efi}
D=/vmfs/volumes/SSD2/$N
mkdir -p $D
[ -f $D/$N.vmdk ] || vmkfstools -c ${DG}G -d thin $D/$N.vmdk >/dev/null
cat > $D/$N.vmx <<X
.encoding = "UTF-8"
config.version = "8"
virtualHW.version = "20"
displayName = "$N"
guestOS = "$GOS"
memSize = "$MEM"
numvcpus = "2"
vhv.enable = "TRUE"
firmware = "$FW"
uefi.secureBoot.enabled = "FALSE"
annotation = "Cloud Explainers P122 lab (nested). Delete after the video."
scsi0.present = "TRUE"
scsi0.virtualDev = "pvscsi"
scsi0:0.present = "TRUE"
scsi0:0.fileName = "$N.vmdk"
sata0.present = "TRUE"
sata0:0.present = "TRUE"
sata0:0.deviceType = "cdrom-image"
sata0:0.fileName = "$ISO"
sata0:0.startConnected = "TRUE"
ethernet0.present = "TRUE"
ethernet0.virtualDev = "$NIC"
ethernet0.networkName = "VM Network"
ethernet0.addressType = "generated"
ethernet0.startConnected = "TRUE"
tools.syncTime = "FALSE"
pciBridge0.present = "TRUE"
pciBridge4.present = "TRUE"
pciBridge4.virtualDev = "pcieRootPort"
pciBridge4.functions = "8"
pciBridge5.present = "TRUE"
pciBridge5.virtualDev = "pcieRootPort"
pciBridge5.functions = "8"
pciBridge6.present = "TRUE"
pciBridge6.virtualDev = "pcieRootPort"
pciBridge6.functions = "8"
pciBridge7.present = "TRUE"
pciBridge7.virtualDev = "pcieRootPort"
pciBridge7.functions = "8"
X
ID=$(vim-cmd vmsvc/getallvms | awk -v n="$N" '$2==n{print $1}')
[ -n "$ID" ] && vim-cmd vmsvc/reload $ID >/dev/null && echo $ID || vim-cmd solo/registervm $D/$N.vmx
