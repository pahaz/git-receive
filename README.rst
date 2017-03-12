**Author**: `Pahaz Blinov`_

**Repo**: https://github.com/pahaz/git-receive/

`git-receive` is a UNIX command-line tool for wrapping `git push`/`git pull`
command on a server side.

**requirements**: Python3

**HOW-TO CREATE OWN STATIC SITE SAAS ?**

You need a SAAS? Just create it! 
Lets start with bootstraping::

    ./bootstrap.sh

What does the command do?
 * install requirements: python3-pip, sshcommand, nginx, gitreceive
 * setup special user: `static`
 * setup sshcommand
 * setup nginx

Then you need to add your named ssh-key::

    sshcommand acl-add static <USERNAME> <KEY_FILE>

or::

    curl https://github.com/<GITHUB-USERNAME>.keys | sshcommand acl-add static <GITHUB-USERNAME>


Deploy your first site
======================

Just clone one:

.. code-block:: bash

    $ git clone https://github.com/pahaz/dokku-static-site.git test1.8iq.ru
    Cloning into 'test1.8iq.ru'...
    remote: Counting objects: 75, done.
    remote: Compressing objects: 100% (50/50), done.
    remote: Total 75 (delta 23), reused 73 (delta 21), pack-reused 0
    Unpacking objects: 100% (75/75), done.

    $ cd test1.8iq.ru

Then deploy it:

.. code-block:: bash

    $ git push static@8iq.ru:test1.8iq.ru master
    Counting objects: 75, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (71/71), done.
    Writing objects: 100% (75/75), 152.88 KiB | 0 bytes/s, done.
    Total 75 (delta 23), reused 0 (delta 0)
    To 8iq.ru:test1.8iq.ru
     * [new branch]      master -> master

If you want to change templates and the `push` it to your github repository just change an origin:

.. code-block:: bash

    $ git remote set-url origin https://github.com/USERNAME/OTHERREPOSITORY.git

Create your first extension
===========================

TODO: write it!

.. _Pahaz Blinov: https://github.com/pahaz/
