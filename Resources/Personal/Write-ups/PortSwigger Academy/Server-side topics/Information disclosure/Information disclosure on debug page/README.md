# Information disclosure on debug page

```
❓

This lab contains a debug page that discloses sensitive information about the application.
To solve the lab, obtain and submit the `SECRET_KEY` environment variable.

```

In the screenshot, we see that while inspecting the home page’s source code, a commented-out anchor tag was discovered pointing to:

```php
<a href="/cgi-bin/phpinfo.php">
```

This snippet references a publicly accessible `phpinfo.php` script under `/cgi-bin/`. Once navigated to, the page displays output from the `phpinfo()` function. By searching within the rendered `phpinfo()` results for certain keywords like `SECRET_KEY`, the attacker (or tester) can find sensitive data that **should not** be exposed publicly.

![image.png](Information%20disclosure%20on%20debug%20page/image.png)

![image.png](Information%20disclosure%20on%20debug%20page/image%201.png)

After checking out that file, we can do a page search for “SECRET_KEY”, which we can use to submit for the solution.

![image.png](Information%20disclosure%20on%20debug%20page/image%202.png)

### **Why It’s Vulnerable**

1. **Sensitive Information Disclosure**
    
    The `phpinfo()` function dumps a large amount of detail about the server’s PHP configuration, environment variables, software versions, and loaded modules. If an attacker can access `phpinfo()` unauthenticated:
    
    - They may find sensitive keys, like the `SECRET_KEY` shown in your screenshot.
    - They might see internal file paths, database connection details, or other system environment variables.
    - They gain insights into the system that facilitate further attacks (e.g., identifying specific PHP/Apache versions with known exploits).
2. **Commented-Out Code Is Still in Source**
    
    Even though the link to `/cgi-bin/phpinfo.php` was commented out in the HTML, it’s still discoverable by **simply viewing page source**. This underscores a common misconception: “commented out” does **not** mean “removed.” Attackers routinely inspect source code or run automated scanners to look for leftover references to files or endpoints.
    
3. **Publicly Accessible `cgi-bin`**
    
    Direct access to the `cgi-bin/` directory is a classic misconfiguration, especially if it contains scripts or leftover files. This can expose old or dangerous functionality and is often a common target in penetration tests or vulnerability scans.
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
