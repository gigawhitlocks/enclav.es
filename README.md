#enclav.es
##A meta-community written in Python
###What is enclav.es?
enclav.es is an experimental community building platform. On the surface, it is a content aggregator similar to Reddit, the original Digg, or even 4chan. But what makes enclav.es different?

- enclav.es is and will remain invite-only. This means that bans have real consequence because it's non-trivial to enter the site again after a ban. Further, those who invite trolls and spammers may find themselves without invite privileges or banned themselves. This helps keep the community civil and keep out unwanted elements.

- enclav.es has identity management. This means that any user can have any number of identities that other users cannot tell are linked to the original user. This allows for unprecedented pseudonymity without the sacrifices of site-wide anonymity.

- enclav.es allows any user to form their own enclave. This is similar to Reddit's 'subreddit' feature but it is different in key ways. Enclaves may be democratically or authoritatively governed, and may be fully public, read-only with a membership whitelist maintained by the moderators, or fully private. These features will be baked into the software. Users who subscribe to an enclave will bind one of their identities to the enclave so that they continually post with the same username (unless the thread allows anonymity), maintaining a sense of community within the enclave. For public professional or informational enclaves, or private enclaves, users may even choose to post with their real names.

- Content filtering by content type on the frontpage will ensure that it is simple to easily filter between low and high energy content (ie via discussion posts and image macros).

###Want to help out?
1. Check out the repository.
3. Install [Vagrant](http://vagrantup.com) if you do not have it
4. ```vagrant up``` in the project directory 
5. ```vagrant ssh``` to log into the VM
6. ```sudo ./postinstall.sh``` and wait for it to complete (this will take awhile)
6. ```sudo -i``` to gain root.
6. ```sh /vagrant/provision.sh``` to run my custom scripts on the VM (this will take awhile)
6. ```exit``` to return to vagrant user and run ```python ~/enclaves/application.py``` to start the server, forwarded to http://localhost:8080 on host OS

If you need to start/stop neo4j, use the script located at ```/opt/neo4j-community-1.8.1/bin/neo4j```

Read [the TO DO](https://github.com/thewhitlockian/enclav.es/blob/master/TODO.markdown) to see what needs to be done.
