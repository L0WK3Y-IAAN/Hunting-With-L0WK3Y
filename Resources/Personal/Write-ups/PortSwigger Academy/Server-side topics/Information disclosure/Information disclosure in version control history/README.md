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
---

<style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

        * {
            font-weight: 400;
        }

        body {
            margin: 0;
            padding: 0;
            background-color: #101214;
            color: #fff;
            font-family: 'Montserrat', sans-serif;
        }

        .banner-container {
            display: flex;
            height: 50vh;
        }

        .left-panel, .right-panel {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 50px;
        }

        .left-panel {
            position: relative;
            border-radius: 50px;
            overflow: hidden;
        }

        .left-panel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url("https://i.imgur.com/xk7Q0EW.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: blur(3px);
            z-index: -1;
        }

        .card {
            position: relative;
            background-color: rgba(38, 38, 38, 0.7);
            padding: 25px;
            border-radius: 30px;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.5);
            text-align: center;
            max-width: 400px;
        }

        .card h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: #fff;
        }

        .social-links {
            margin-top: 20px;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }

        .social-links a {
            display: inline-block;
            text-decoration: none;
        }

        .social-links img {
            width: 150px;
            max-width: 150px;
            height: 40px;
            object-fit: cover;
        }

        /* Media query for mobile */
        @media (max-width: 768px) {
            .social-links {
                grid-template-columns: 1fr;
            }
        }

        .codex-button {
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #030e14;
            color: #ffffff;
            padding: 6px 12px;
            border-radius: 4px;
            font-family: 'Montserrat', sans-serif;
            font-size: 15px;
            font-weight: bold;
            height: 40px;
            text-decoration: none;
        }

        .codex-button img {
            height: 24px;
            width: auto;
            margin-right: 8px;
        }

        .right-panel {
            background-color: #111314;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .right-panel img {
            width: 300px;
            margin-bottom: 20px;
        }

        .right-panel h2 {
            font-size: 2.5rem;
            margin: 10px 0;
        }

        .right-panel p {
            font-size: 1.2rem;
            color: #ff8800;
        }

    </style>

<div class="banner-container">
        <div class="left-panel">
            <div class="card">
                <h2>Let's Connect!</h2>
                <div class="social-links">
                    <a href="https://github.com/L0WK3Y-IAAN" target="_blank">
                        <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
                    </a>
                    <a href="https://www.linkedin.com/in/iaansec/" target="_blank">
                        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
                    </a>
                </div>
            </div>
        </div>
    </div>
