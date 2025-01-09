# Information disclosure in version control history

<aside>
❓ This lab discloses sensitive information via its version control history. To solve the lab, obtain the password for the `administrator` user then log in and delete the user `carlos`.
</aside>

To begin, I start off by doing a directory scan of the lab to see what we can find.

![Untitled](Information%20disclosure%20in%20version%20control%20history/1.png)

Not too long after, we get a few hits for `.git` directories.

![Untitled](Information%20disclosure%20in%20version%20control%20history/2.png)

Heading over to the `/.git` , I am greeted with a few files and directories, browsing around I come across the config file which contains information that maybe important later, I make sure to take note of this.

![git dir.gif](Information%20disclosure%20in%20version%20control%20history/3.gif)

Next I use wget to download the .git repository to view the version history logged by git. (At this point you will want to download Git if you have not done so already [Git (git-scm.com)](https://git-scm.com/)) 

`wget -r [LAB_URL]/.git` (you will have to brew install wget if you are on MacOS)

After navigating to the git directory, I use the command `git log` to check the log history of the git repository. Right off the bat, some useful information can be seen regarding the admin account.

![Screenshot 2024-06-29 at 6.49.40 PM.png](Information%20disclosure%20in%20version%20control%20history/4.png)

Lastly, I use `git show` to show information on the commit history. Doing so reveals the admin account password.

![Screenshot 2024-06-29 at 6.53.33 PM.png](Information%20disclosure%20in%20version%20control%20history/5.png)

# The Vulnerability

- The web application has its `.git` directory exposed publicly, which should never be accessible on a production server. The `.git` directory contains the complete version control history of the codebase.
- The developers appear to have committed sensitive credentials directly into the source code repository and later tried to remove them with subsequent commits. However, due to Git's design, the credentials remain in the commit history.
