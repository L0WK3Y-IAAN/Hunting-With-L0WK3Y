# IP Halloween 2025 - Spirit Halloween! Walkthrough

<aside>

**Difficulty:** Hard 🔴

**Category:** Web Pentesting/Reverse Engineering

**Description**: We just launched the website for our new Halloween store. This used to be a CVS but now its the premiere place to buy costumes online, we invite you to test out Spirit Halloween!

**Author**: L0WK3Y

**Notes**: Use the command **!ctfchallenge** and you will be sent instructions for starting the challenge.

</aside>

### Initial Setup

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image.png)

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%201.png)

---

### Phase 1: Web Pentest

After navigating to the IP and landing on the front page, you will come across your first clue. The release of the new “`*Spirit of Shopping*`” **app.**

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%202.png)

> *At this point, the player will have done enough recon to know that directory discovery is the next move to make*
> 

During directory discovery, you will come across the directory `dev`.

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%203.png)

In this directory resides the application `Spirit of Shopping` you will just have to figure out the extension.

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%204.png)

---

### Phase 2. Reverse Engineering

Once you have downloaded the APK, proceed with opening it in the decompiler of your choice, for this walkthrough I will be using [JADX](https://github.com/skylot/jadx). Head over to the `AndroidManifest.xml`. 

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%205.png)

Inside of the manifest you will find the `MainActivity` but the main activity will not contain any information on the flag itself, you will need to head to the location where the MainActivity class is located `com.halloween.party`.

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%206.png)

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%207.png)

After reaching the location of the MainActivity class, you will see another class called `Paranormal`, immediately after the Paranormal class is initialized, you will spot a native library being loaded called `spookytime`. You will need to export this library, you can do so by navigating to `Resources/lib/<ARCH_OF_YOUR_CHOOSING>/libspookytime.so` > Export.

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%208.png)

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%209.png)

Once you’ve downloaded the library, you can open it in the decompiler of your choosing (Ghidra, Cutter, IDA Pro, etc…). 

After loading the library in the decompiler, head to the functions and scroll until you reach the function `sym.Java_com_halloween_party_paranormal_Paranormal_validateAndRevealNative` 

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%2010.png)

Once, there scroll down until you see a massive encoded string:

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%2011.png)

```
3ZqjnJxy4PSKcZD8jnCgTymBK8SQHYuhuwmnshPBkDT3ZbK2j9XLESrKELxaU4gb2dULbkEmZ7CDEj9JJB3RxGT7QDDTENFXjRUw6wg9udAuPjoxju6o42XBUQc7bwQaugZoKhToaedKQkkZA6RP897F5S9zrhpGzynxLWJgrUqby9umb3vWKKxDtpHp4PnEaesTw81dvhSbPrajj2AQYLhFdZw
```

From here you can use Cyberchef to decode the string and get the flag.

![image.png](IP%20Halloween%202025%20-%20Spirit%20Halloween!%20Walkthrough/image%2012.png)

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
