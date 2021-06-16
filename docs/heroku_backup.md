# Heroku Backup

This tutorial assumes you have access to a remote always-running Linux x86\_64
machine, like, for example, from your CS Department.


## Authorizing Heroku

Little bit of clarification:
We have Heroku, the service which helps developers deploy their apps.

We also the `heroku` command line command, which is used to interface with the Heroku service.
This is the easiest way to access Heroku the service from a lab machine. Lab machines do not have web browsers
(they're all accessed with the command line). 

By authorizing Heroku, we mean giving accessibility of Heroku the service to a lab machine. We are allowing
access to a specific user in the Heroku service.

This is a little tricky, since you can't necessarily follow the simple step
of `heroku login`, since Heroku will detect the IP address mismatch and
prevent you from continuing.

Instead you need to create a new authorization through the Heroku website
("Account Settings" > "Applications" > "Create authorization")

Then you need to copy the Authorization token and put it in
[`~/.netrc`](https://devcenter.heroku.com/articles/authentication):
```
machine api.heroku.com
	login YOUR@EMAIL
	password AUTHORIZATION_TOKEN
```
You'll want to protect this file with `chmod 600 ~/.netrc` to ensure
no one else can read it (this assumes you trust your system administrators,
of course).

An equivalent command `chmod go-rwx`. Let's break this down:
* `chmod` = change 
* `g` = group 
* `o` = other (anyone else who is not that in that group; e.g. at W&M, small group of people, such as professors and administrators, though certain administrators can bypass all, so be aware of that)
* `-` = delete
* `r` = read access
* `w` = write access
* `x` = execute access

## Backup Script

Next, put the following in `~/hackerforce-backup.sh`:

```bash
# When you try and run a text file (which is this script), this tells Linux to interpret this file as a shell executable
# and execute it upon command. Instead of running the text file directly (which doesn't make sense), it runs the shell
# with this script as its first argument. 

# Right below is called a shebang/hasbang/etc. (https://en.wikipedia.org/wiki/Shebang_%28Unix%29) along with a 
# path to run a certain command. 

#!/bin/sh
# Script for installing the Heroku CLI and backing up hackerforce
set -e

# Replace with whatever your hackerforce instance is
# e.g. myhackerforce.herokuapp.com would be myhackerforce
HACKERFORCE=MYHACKERFORCE

cd "$HOME"

# Checks for a directory named "heroku"
# if it does not exist
if [ ! -d heroku ]
then
    # get the heroku .tar.gz file from the internet 
    HEROKUTAR=heroku-linux-x64.tar.gz
    wget "https://cli-assets.heroku.com/$HEROKUTAR"
    # extract it
    tar xzvf "$HEROKUTAR"
    # remove the .tar.gz file (we've extracted it; we don't need it anymore)
    rm "$HEROKUTAR"
fi


# if it does exist, then we dont' need to re-install everything. 
# we have a heroku folder that has everything we need to run


# this is the location of the  heroku command 
# this is making it so that the shell knows where to look for the `heroku` command
export PATH="$PATH:$HOME/heroku/bin"

heroku update

# if a hackerforce backups directory does exist, create one
if [ ! -d hackerforce-backups ]
then
    mkdir hackerforce-backups
    # 1 (execute) + 2 (write) + 4 (read) = 7
    # You can set up any combination of the above ^^ (e.g. just execute and read = 1 + 4 = 5; in this case we want all permissions) 
    # See below section on chmod octal format to understand how things like chmod 600 and chmod 700 work
    chmod 700 hackerforce-backups
fi

# move to the folder we just created/already created from right above
cd hackerforce-backups

# The heroku command so that on our speicfic application, that is our HackerForce instance, we run Django's manage.py and dump our data
# to a file in JSON format, and that file's name format is the current date and time.

heroku run -a "$HACKERFORCE" -- python manage.py dumpdata > "$(date --iso-8601=seconds).json"
```

```
Here's how chmod octal format works:

You have three digits: 
_                           _                            _
^                           ^                            ^
permissions for owner.     permissions for group        permissions for others

And for each digit, you can set specific permissions according to a number.
1 = execute access
2 = write access
4 = read access

0 = none of the above

Anytime you want a combination of these types of access, you add up the corresponding numbers.

for example, if you want the owner to have both execute and read access, 
you set the leftmost digit to 1 (execute) + 4 (read) = 5. 

If you want to do the equivalent for group and others, you just place 5 
in the middle and rightmost digit, respectively.

In chmod 600 ..., this means giving the owner write and read access, but no execute access. 
So, in chmod 700 ..., this means giving the owner execute, write, and read acess and no permissions to nayone else.
```

After that make sure to mark it executable (`chmod u+x hackerforce_backup.sh`) and run it, to make sure it actually works. If it functions correctly, you should have two new folders: `heroku`
and `hackerforce-backups`, and `hackerforce-backups` should contain a JSON file
with your backups.

Additional notes on `chmod u+x hackerforce_backup.sh`
```
"u" is for user and "+x" for giving executable access. 
So, in conversion to octal format, `u+x` just changes the leftmost digit, 
and does not change the middle digit and the rightmost digits (keeps them the same).
```

## Cron Job ([How Cron Works](http://crontab.guru))

For this to be useful, it has to be run regularly.
This is precisely what cron allows you to do.

Run `crontab -e` and add the following lines:
```
MAILTO=YOUR@EMAIL
7	4	*	*	*	./hackerforce-backup.sh
```
(Note that this technically only works on Debian/Ubuntu-based machines,
because only their version of cron respects environment variables set in
crontabs)

This will backup at 4:07 AM every morning.

Assuming your machine has a working email setup, this will email you once
a day about your backups so you can keep an eye on them.

If you don't care whether you get confirmation emails, use this instead, without the MAILTO:
```
7	4	*	*	*	./hackerforce-backup.sh > /dev/null 2>&1
```
If you don't add the `/dev/null` bit, Cron will still attempt to send emails,
probably to your local account, which is usually pointless and just takes up
space.

## Restoring
To restore a backup `mybackup.json`, use the heroku CLI again:
```
heroku run --no-tty -a myhackerforce -- python manage.py loaddata -e contenttypes --format=json - < mybackup.json
```
If your backup file begins with the line "Downloading the sponsorship packet to: {} /app/website/static/sponsorship.pdf"
you'll need to remove this line in order for the data to load successfully.
