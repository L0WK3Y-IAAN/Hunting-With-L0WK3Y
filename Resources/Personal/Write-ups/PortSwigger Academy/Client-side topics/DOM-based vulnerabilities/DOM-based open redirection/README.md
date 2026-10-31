---
title: "PortSwigger Academy — DOM-based open redirection (Web) Walkthrough"
---
# DOM-based open redirection

```
❓

<p>
This lab contains a DOM-based open-redirection vulnerability. To solve this lab, exploit this vulnerability and redirect the victim to the exploit server. 
</p>
```

Starting off with testing the store pages functionality, we make our way to one of the product pages, right clicking on the `< Back to Blog` button and inspecting it’s element, we see this code embedded in it’s anchor tag.

```javascript
<a href="#" onclick="returnUrl = /url=(https?:\/\/.+)/.exec(location); location.href = returnUrl ? returnUrl[1] : &quot;/&quot;">Back to Blog</a>
```

### **What the Code Does**

1. **Anchor Tag (****`<a>`****)**:
   - The `href="#"` makes the link do nothing by default when clicked.
2. **Inline JavaScript (****`onclick`****)**:
   - When the user clicks the link, the inline `onclick` JavaScript is executed.
3. **Regular Expression to Parse the URL**:
   - The following line tries to extract a URL from the `location` (current page URL):
     ```javascript
     returnUrl = /url=(https?:\/\/.+)/.exec(location);

     ```
   - It uses a **regular expression** `/url=(https?:\/\/.+)/` to match and extract a URL from a query string parameter named `url`.
     - `https?`: Matches `http` or `https`.
     - `:\/\/`: Matches the `://` portion of a URL.
     - `.+`: Matches the rest of the URL.
4. **Redirect Logic**:
   - If the regular expression matches (`returnUrl` is not null), the user is redirected to the captured URL (`returnUrl[1]`).
   - If no match is found, the user is redirected to `/` (the website's homepage):
     ```javascript
     location.href = returnUrl ? returnUrl[1] : "/";

     ```

---

### **How This Code is Vulnerable**

1. **Insufficient Validation**:
   - The code does not validate the extracted `url` parameter. It blindly redirects to any external URL found in the `url` query parameter.
2. **Attacker Control**:
   - An attacker can manipulate the `url` parameter in the URL of the page containing this code to craft malicious links.
3. **Exploit Scenario**:
   - Suppose this code is hosted on `https://example.com`.
   - If the user visits the following crafted URL:
     ```txt
     https://example.com/page?url=https://malicious-site.com

     ```

     ```txt
     https://example.com/page?key1=value1&url=https://malicious-site.com
     ```
   - When the user clicks the "Back to Blog" link, the regular expression extracts `https://malicious-site.com` and redirects the user there.
4. **Phishing Risk**:
   - Attackers can craft a trusted-looking link (`example.com`) to deceive users into clicking it, but the link ultimately redirects to a malicious website.

---

### **Attack Scenario**

1. **Crafted URL**:
   ```txt
   https://example.com/page?url=https://phishing-site.com

   ```

   ```txt
   https://example.com/page?key1=value1&url=https://phishing-site.com
   ```
2. **Steps**:
   - The user lands on the `example.com` page.
   - The "Back to Blog" link contains the vulnerable code.
   - When clicked, the JavaScript extracts `https://phishing-site.com` from the `url` query parameter and redirects the user there.
3. **Impact**:
   - The user unknowingly lands on the attacker's malicious site, where they may be tricked into entering sensitive information (e.g., credentials, payment details).

---

Now that we have an understand of how the code works, we can exploit it by redirecting the victim to the exploit server with the following URL, thus completing the lab.

```txt
https://0ad4009b0402d90c806f031800a00040.web-security-academy.net/post?postId=2&url=https://exploit-0ab9001f0414d99b8086027101da0025.exploit-server.net/
```
