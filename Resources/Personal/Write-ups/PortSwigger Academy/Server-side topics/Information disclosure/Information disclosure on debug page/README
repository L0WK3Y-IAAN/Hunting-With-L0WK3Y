# Information disclosure on debug page

```
❓

This lab contains a debug page that discloses sensitive information about the application.
To solve the lab, obtain and submit the `SECRET_KEY` environment variable.

```

In the screenshot, we see that while inspecting the home page’s source code, a commented-out anchor tag was discovered pointing to:

```php
<a href="/cgi-bin/phpinfo.php">
```

This snippet references a publicly accessible `phpinfo.php` script under `/cgi-bin/`. Once navigated to, the page displays output from the `phpinfo()` function. By searching within the rendered `phpinfo()` results for certain keywords like `SECRET_KEY`, the attacker (or tester) can find sensitive data that **should not** be exposed publicly.

![image.png](Information%20disclosure%20on%20debug%20page/image.png)

![image.png](Information%20disclosure%20on%20debug%20page/image%201.png)

After checking out that file, we can do a page search for “SECRET_KEY”, which we can use to submit for the solution.

![image.png](Information%20disclosure%20on%20debug%20page/image%202.png)

### **Why It’s Vulnerable**

1. **Sensitive Information Disclosure**
    
    The `phpinfo()` function dumps a large amount of detail about the server’s PHP configuration, environment variables, software versions, and loaded modules. If an attacker can access `phpinfo()` unauthenticated:
    
    - They may find sensitive keys, like the `SECRET_KEY` shown in your screenshot.
    - They might see internal file paths, database connection details, or other system environment variables.
    - They gain insights into the system that facilitate further attacks (e.g., identifying specific PHP/Apache versions with known exploits).
2. **Commented-Out Code Is Still in Source**
    
    Even though the link to `/cgi-bin/phpinfo.php` was commented out in the HTML, it’s still discoverable by **simply viewing page source**. This underscores a common misconception: “commented out” does **not** mean “removed.” Attackers routinely inspect source code or run automated scanners to look for leftover references to files or endpoints.
    
3. **Publicly Accessible `cgi-bin`**
    
    Direct access to the `cgi-bin/` directory is a classic misconfiguration, especially if it contains scripts or leftover files. This can expose old or dangerous functionality and is often a common target in penetration tests or vulnerability scans.
