# nas-pod

nas based on samba using podman rootless

config
- smb.conf : samba share config
- setusers : set samba users and password
- setpermall : set permission for shared mount directories
- makeshare : create shared mount directories
- addusers : add samba users to container (used on every run)
- run & runfirst: run shared mount

install
- ./build && ./install

start
- ./run

stop
- ./stop
