# Information disclosure in error messages

<aside>
❓ This lab's verbose error messages reveal that it is using a vulnerable version of a third-party framework. To solve the lab, obtain and submit the version number of this framework.

</aside>

# Lab

In this lab, I start things off by scanning for directories like normal although nothing of interest was found. 

![Screenshot 2024-06-29 at 8.33.17 PM.png](Information%20disclosure%20in%20error%20messages/Screenshot_2024-06-29_at_8.33.17_PM.png)

I then proceed to click on one of the product “View details” buttons and spot a query added to the URL.

![Screenshot 2024-07-05 at 1.27.50 PM.png](Information%20disclosure%20in%20error%20messages/Screenshot_2024-07-05_at_1.27.50_PM.png)

![Untitled](Information%20disclosure%20in%20error%20messages/Untitled.png)

*Image by codecademy.com*

Here's a breakdown of the components of the URL in the image:

1. **https://**: This indicates that the URL is using the HTTPS protocol, which is a secure version of HTTP.
2. [**0aba008d0441c60a8ae1056600f00075.web-security-academy.net**](http://0aba008d0441c60a8ae1056600f00075.web-security-academy.net/):
    - **0aba008d0441c60a8ae1056600f00075**: This is likely a subdomain or a unique identifier for a specific user, session, or resource.
    - [**web-security-academy.net**](http://web-security-academy.net/): This is the main domain name. It indicates that the site belongs to the Web Security Academy, which is likely related to cybersecurity training or education.
3. **/product**: This is the path of the URL, indicating that the resource being accessed is related to products.
4. **?productId=1**: This is a query parameter.
    - **?**: Indicates the start of the query string.
    - **productId=1**: This key-value pair specifies that the query parameter `productId` is set to `1`. This parameter is likely used by the server to identify and return information about a specific product.

If you were to change the query parameter to `productId=2` it would take you to the product webpage for that query. What if I were to change the product ID to something that isn’t listed, such the letter “A” or a large integer. First I tried “99999” to see what would happen. All I got was a `“Not Found”` message. So I added more 9’s until I got the error below:

```java
Internal Server Error: java.lang.NumberFormatException: For input string: "9999999999"
	at java.base/java.lang.NumberFormatException.forInputString(NumberFormatException.java:67)
	at java.base/java.lang.Integer.parseInt(Integer.java:665)
	at java.base/java.lang.Integer.parseInt(Integer.java:777)
	at lab.e.b.g.e.E(Unknown Source)
	at lab.q.je.k.z.O(Unknown Source)
	at lab.q.je.d.h.c.Y(Unknown Source)
	at lab.q.je.d.p.lambda$handleSubRequest$0(Unknown Source)
	at d.o.k.o.lambda$null$3(Unknown Source)
	at d.o.k.o.b(Unknown Source)
	at d.o.k.o.lambda$uncheckedFunction$4(Unknown Source)
	at java.base/java.util.Optional.map(Optional.java:260)
	at lab.q.je.d.p.n(Unknown Source)
	at lab.server.k.p.y.L(Unknown Source)
	at lab.q.je.a.J(Unknown Source)
	at lab.q.je.a.L(Unknown Source)
	at lab.server.k.p.b.x.j(Unknown Source)
	at lab.server.k.p.b.q.lambda$handle$0(Unknown Source)
	at lab.e.a.n.q.S(Unknown Source)
	at lab.server.k.p.b.q.V(Unknown Source)
	at lab.server.k.p.a.E(Unknown Source)
	at d.o.k.o.lambda$null$3(Unknown Source)
	at d.o.k.o.b(Unknown Source)
	at d.o.k.o.lambda$uncheckedFunction$4(Unknown Source)
	at lab.server.gv.D(Unknown Source)
	at lab.server.k.p.a.N(Unknown Source)
	at lab.server.k.s.f.L(Unknown Source)
	at lab.server.k.r.C(Unknown Source)
	at lab.server.k.x.C(Unknown Source)
	at lab.server.gy.b(Unknown Source)
	at lab.server.gy.t(Unknown Source)
	at lab.x.l.lambda$consume$0(Unknown Source)
	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1144)
	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:642)
	at java.base/java.lang.Thread.run(Thread.java:1583)

Apache Struts 2 2.3.31
```

## The Vulnerability

After doing some research I found that the error I’m encountering is due to the way the Java application handling the request processes the `productId` parameter. Specifically, the `java.lang.NumberFormatException: For input string: "9999999999"` indicates that the application is attempting to parse the `productId` parameter as an integer, but the value "9999999999" exceeds the range that can be represented by a 32-bit signed integer.

In Java, the `Integer.parseInt()` method is used to convert a string into an integer. However, Java's `int` type has a maximum value of \(2,147,483,647\) (which is \(2^{31} - 1\)). When the `productId` is "9999999999", it exceeds this limit, leading to a `NumberFormatException`.

When you use a 9-digit number (e.g., "999999999"), it falls within the acceptable range for an integer, so the application can parse it without any issues.

To summarize, the site crashes with a 10-digit `productId` because:

1. The application tries to convert the `productId` to an integer using `Integer.parseInt()`.
2. A 10-digit number like "9999999999" exceeds the maximum value that a 32-bit integer can hold.
3. This causes a `NumberFormatException`, resulting in an internal server error.

The solution would involve modifying the application to handle larger numbers, possibly by using a `long` type (which has a much larger range) or by handling the `productId` as a string if appropriate for the application's logic.

## Solution

The flag can be seen at the bottom of the error message “`Apache Struts 2 2.3.31`”.
