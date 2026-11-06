# The tea shop's log folder: four logs of different sizes, one with a space in its name (like many real files).
mkdir -p logs && cd logs
head -c 912 /dev/urandom | base64 > app.log
head -c 7311 /dev/urandom | base64 > payments.log
head -c 48213 /dev/urandom | base64 > orders.log
head -c 130554 /dev/urandom | base64 > "green tea.log"
