Enclav.es
====
##A meta-community written in Python


###Want to help out?
1. Check out the repository.
3. Install [Vagrant](http://vagrantup.com) if you do not have it
4. ```vagrant up``` in the project directory 
5. ```vagrant ssh``` to log into the VM
6. ```sudo ./postinstall.sh``` and wait for it to complete (this will take awhile)
6. ```sudo -i``` to gain root.
6. ```sh /vagrant/provision.sh``` to run my custom scripts on the VM (this will take awhile)
6. ```exit``` to return to vagrant user and run ```python ~/cluster/cluster.py``` to start the server, forwarded to http://localhost:8080 on host OS

When you're done, run ```vagrant suspend``` to pause the VM, and ```vagrant resume``` to restart it.


Read [the TO DO](https://github.com/thewhitlockian/enclav.es/blob/master/TODO.markdown) to see what needs to be done.
