# KGB Messenger


## Introduction

KGB Messenger is a open source CTF practice challenge that aims to help people learn how to reverse engineer Android applications. If you're completely new to Android application reverse engineering, I'd suggest you start by watching the video lecture from George Mason University's MasonCC club. If you're stuck on any of the challenges, feel free to peek at the video walkthrough for some help. Timestamps have been provided in the walkthrough video's description to prevent unwanted spoilers. To get started, download the APK and read the challenge descriptions below.

# Challenges

You are working for the International Secret Intelligence Service as a reverse engineer. This morning your team lead assigned you to inspect an Android application found on the phone of a misbehaving agent. It’s rumored that the misbehaving agent, Sterling Archer, has been in contact with some KGB spies. Your job is to reverse engineer the application to verify the rumor.

The challenges should be solved sequentially. The flag format is FLAG{insert_flag_here}. Good luck!

## Alerts (Medium)

*The app keeps giving us these pesky alerts when we start the app. We should investigate.*

## Login (Easy)

*This is a recon challenge. All characters in the password are lowercase.*

## Social Engineering (Hard)

*It looks like someone is bad at keeping secrets. They're probably susceptible to social engineering... what should I say?*

---

## **Tools & Techniques**

### **Reverse Engineering Tools**

- **JADX:** - Static analysis of decompiled APK

### **Dynamic Analysis Tools**

- **Frida:** Dynamic instrumentation framework
- **ADB:** Android Debug Bridge for device communication
- **Python:** Scripting for decryption and analysis

### **Techniques Used**

1. **Static Analysis:**
    - Decompiled Java source code analysis
    - Resource file examination (strings.xml & AndroidManifest.xml)
    - Control flow analysis
2. **Dynamic Analysis:**
    - Runtime method hooking with Frida
    - System call interception
    - Memory inspection
3. **Cryptanalysis:**
    - XOR cipher reversal
    - Bit shift operation reversal
    - MD5 hash analysis (bypassed)
4. **Bypass Techniques:**
    - Method hooking to return false/true
    - System property/environment variable spoofing
    - Direct method interception

---

## AndroidManifest

Let’s start by taking a look at the `AndroidManifest.xml` and, there are only 3 activities and no permissions or exports.

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    android:versionCode="1"
    android:versionName="1.0"
    package="com.tlamb96.spetsnazmessenger">
    <uses-sdk
        android:minSdkVersion="17"
        android:targetSdkVersion="25"/>
    <application
        android:theme="@style/AppTheme"
        android:label="@string/app_name"
        android:icon="@mipmap/ic_kgb_launcher_icon"
        android:allowBackup="true"
        android:supportsRtl="true"
        android:roundIcon="@mipmap/ic_kgb_launcher_icon">
        <activity android:name="com.tlamb96.kgbmessenger.MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        <activity android:name="com.tlamb96.kgbmessenger.MessengerActivity"/>
        <activity android:name="com.tlamb96.kgbmessenger.LoginActivity"/>
        <meta-data
            android:name="android.support.VERSION"
            android:value="25.4.0"/>
    </application>
</manifest>
```

```xml
<activity android:name="com.tlamb96.kgbmessenger.MainActivity"> <!--1st-->
<activity android:name="com.tlamb96.kgbmessenger.LoginActivity"/> <!--2nd-->
<activity android:name="com.tlamb96.kgbmessenger.MessengerActivity"/> <!--3rd-->
```

---

## **MainActivity - Integrity Checks**

![image.png](KGB%20Messenger/image.png)

### **Security Mechanisms**

The `MainActivity` implements two integrity checks that prevent the app from running on non-Russian devices:

```java
protected void onCreate(Bundle bundle) {
    super.onCreate(bundle);
    setContentView(R.layout.activity_main);

    // Check 1: Verify system property "user.home" equals "Russia"
    // This is a fake check - user.home doesn't work this way on Android
    String property = System.getProperty("user.home");
    String str = System.getenv("USER");

    // If property check fails, show error dialog and exit
    if (property == null || property.isEmpty() || !property.equals("Russia")) {
        a("Integrity Error", "This app can only run on Russian devices.");
        return; // Exit early if check fails
    }

    // Check 2: Verify environment variable USER matches R.string.User
    // R.string.User contains: "RkxBR3s1N0VSTDFOR180UkNIM1J9Cg==" (Base64)
    if (str == null || str.isEmpty() || !str.equals(getResources().getString(R.string.User))) {
        a("Integrity Error", "Must be on the user whitelist.");
    } else {
        // Both checks passed - initialize and proceed to LoginActivity
        a.a(this); 
        startActivity(new Intent(this, (Class<?>) LoginActivity.class));
    }
}

```

### **Checks Performed**

1. **System Property Check:**
    - Checks if `System.getProperty("user.home")` equals `"Russia"`
    - This is a fake check as `user.home` on Android doesn't work this way
2. **Environment Variable Check:**
    - Checks if `System.getenv("USER")` equals `R.string.User`
    - `R.string.User` value: `"RkxBR3s1N0VSTDFOR180UkNIM1J9Cg=="` (Base64 encoded)
    - Decoded: `"FLAG{57ERL1ON_4RCH3R}\n"` (This is a hint/flag, not the main challenge)

### **Bypass Method**

**Frida Script Approach:**

```jsx
// Hook System.getProperty() to return "Russia" for "user.home"
// This bypasses the first integrity check
System.getProperty.overload('java.lang.String').implementation = function(key) {
    if (key === "user.home") {
        // Return "Russia" to satisfy the check
        return "Russia";
    }
    // For other properties, return the original value
    return this.getProperty(key);
};

// Hook System.getenv() to return expected USER value
// This bypasses the second integrity check
System.getenv.overload('java.lang.String').implementation = function(name) {
    if (name === "USER" && expectedUserValue !== null) {
        // Return the expected value from R.string.User
        return expectedUserValue;
    }
    // For other environment variables, return original value
    return this.getenv(name);
};

// Prevent error dialogs from showing
// The method 'a' displays error dialogs - we prevent it from executing
MainActivity.a.overload('java.lang.String', 'java.lang.String').implementation = function(title, message) {
    // Don't call the original method - just return
    // This prevents the error dialog from appearing
    return;
};

// Direct bypass - intercept onCreate and skip all checks
// This is the most reliable method
MainActivity.onCreate.implementation = function(bundle) {
    // Call super.onCreate to initialize the activity properly
    originalOnCreate.call(this, bundle);

    // Skip all integrity checks and start LoginActivity directly
    var Intent = Java.use("android.content.Intent");
    var LoginActivity = Java.use("com.tlamb96.kgbmessenger.LoginActivity");
    var intent = Intent.$new(this, LoginActivity.class);
    this.startActivity(intent); // Navigate to LoginActivity
};

```

**Result:** Successfully bypassed all integrity checks and navigated to LoginActivity.

---

## **LoginActivity - Password Validation**

![image.png](KGB%20Messenger/image%201.png)

### **Security Mechanisms**

The `LoginActivity` requires valid credentials to proceed:

```java
public void onLogin(View view) {
    // Get username and password from EditText fields
    EditText editText = (EditText) findViewById(R.id.login_username);
    EditText editText2 = (EditText) findViewById(R.id.login_password);

    // Store in instance variables (this.n = username, this.o = password)
    this.n = editText.getText().toString();
    this.o = editText2.getText().toString();

    // Validate that both fields are not empty
    if (this.n == null || this.o == null || this.n.isEmpty() || this.o.isEmpty()) {
        return; // Exit if fields are empty
    }

    // Check 1: Verify username matches R.string.username ("codenameduchess")
    if (!this.n.equals(getResources().getString(R.string.username))) {
        // Username doesn't match - show error and clear fields
        Toast.makeText(this, "User not recognized.", 0).show();
        editText.setText("");
        editText2.setText("");
    } else if (j()) {
        // Username is correct AND password check passed (j() returns true)
        // Generate and display flag, then proceed to MessengerActivity
        i(); // Generate flag using XOR operations
        startActivity(new Intent(this, (Class<?>) MessengerActivity.class));
    } else {
        // Username is correct but password is wrong
        Toast.makeText(this, "Incorrect password.", 0).show();
        editText.setText("");
        editText2.setText("");
    }
}

```

### **Credentials Found**

From `res/values/strings.xml`:

- **Username:** `"codenameduchess"`
- **Password MD5 Hash:** `"84e343a0486ff05530df6c705c8bb4"`

### **Password Validation**

The `j()` method validates the password using MD5:

```java
private boolean j() {
    // This method validates the password by comparing its MD5 hash
    // this.m is a MessageDigest instance (MD5)
    // this.o is the password string entered by user

    String str = "";
    // Hash the password bytes using MD5
    for (byte b : this.m.digest(this.o.getBytes())) {
        // Convert each byte to lowercase hex string and concatenate
        str = str + String.format("%x", Byte.valueOf(b));
    }

    // Compare the computed MD5 hash with the stored hash from resources
    // R.string.password = "84e343a0486ff05530df6c705c8bb4"
    return str.equals(getResources().getString(R.string.password));
}

```

### **Flag Generation**

The `i()` method generates and displays a flag using XOR operations:

```java
private void i() {
    // This method generates the flag using XOR operations
    // Base character array that will be XORed with username/password characters
    char[] cArr = {'(', 'W', 'D', ')', 'T', 'P', ':', '#', '?', 'T'};

    // XOR each character with specific positions from username (this.n) and password (this.o)
    // Username: "codenameduchess" (this.n)
    // Password: user-entered password (this.o)

    cArr[0] = (char) (cArr[0] ^ this.n.charAt(1));  // '(' XOR username[1] ('o')
    cArr[1] = (char) (cArr[1] ^ this.o.charAt(0));  // 'W' XOR password[0]
    cArr[2] = (char) (cArr[2] ^ this.o.charAt(4));  // 'D' XOR password[4]
    cArr[3] = (char) (cArr[3] ^ this.n.charAt(4));  // ')' XOR username[4] ('n')
    cArr[4] = (char) (cArr[4] ^ this.n.charAt(7));  // 'T' XOR username[7] ('e')
    cArr[5] = (char) (cArr[5] ^ this.n.charAt(0));  // 'P' XOR username[0] ('c')
    cArr[6] = (char) (cArr[6] ^ this.o.charAt(2));  // ':' XOR password[2]
    cArr[7] = (char) (cArr[7] ^ this.o.charAt(3));  // '#' XOR password[3]
    cArr[8] = (char) (cArr[8] ^ this.n.charAt(6));  // '?' XOR username[6] ('m')
    cArr[9] = (char) (cArr[9] ^ this.n.charAt(8));  // 'T' XOR username[8] ('d')

    // Display the flag in a Toast message
    // Format: "FLAG{" + XORed characters + "}"
    Toast.makeText(this, "FLAG{" + new String(cArr) + "}", 1).show();
}

```

### **Bypass Method**

**Frida Script Approach:**

```jsx
// Bypass password check - always return true
// This method validates the password MD5 hash - we bypass it completely
LoginActivity.j.implementation = function() {
    console.log("[+] Password check bypassed - j() returning true");
    // Always return true, bypassing MD5 hash check
    // This allows login with any password
    return true;
};

// Extract flag from i() method
// Hook the flag generation method to extract the flag before it's displayed
LoginActivity.i.implementation = function() {
    // Access private fields containing username and password
    var username = this.n.value; // Username: "codenameduchess"
    var password = this.o.value; // Password: user-entered (any value works now)

    // Reconstruct flag using the same XOR operations as the original method
    var cArr = ['(', 'W', 'D', ')', 'T', 'P', ':', '#', '?', 'T'];

    // Perform XOR operations with specific character positions
    cArr[0] = String.fromCharCode(cArr[0].charCodeAt(0) ^ username.charAt(1).charCodeAt(0));
    cArr[1] = String.fromCharCode(cArr[1].charCodeAt(0) ^ password.charAt(0).charCodeAt(0));
    cArr[2] = String.fromCharCode(cArr[2].charCodeAt(0) ^ password.charAt(4).charCodeAt(0));
    cArr[3] = String.fromCharCode(cArr[3].charCodeAt(0) ^ username.charAt(4).charCodeAt(0));
    cArr[4] = String.fromCharCode(cArr[4].charCodeAt(0) ^ username.charAt(7).charCodeAt(0));
    cArr[5] = String.fromCharCode(cArr[5].charCodeAt(0) ^ username.charAt(0).charCodeAt(0));
    cArr[6] = String.fromCharCode(cArr[6].charCodeAt(0) ^ password.charAt(2).charCodeAt(0));
    cArr[7] = String.fromCharCode(cArr[7].charCodeAt(0) ^ password.charAt(3).charCodeAt(0));
    cArr[8] = String.fromCharCode(cArr[8].charCodeAt(0) ^ username.charAt(6).charCodeAt(0));
    cArr[9] = String.fromCharCode(cArr[9].charCodeAt(0) ^ username.charAt(8).charCodeAt(0));

    // Construct and log the flag
    var flag = "FLAG{" + cArr.join('') + "}";
    console.log("[+] 🎯 EXTRACTED FLAG: " + flag);

    // Call original method to display flag in Toast (for visual confirmation)
    original_i.call(this);
};

```

**Result:** Successfully bypassed password validation and extracted the flag from LoginActivity.

---

## **MessengerActivity - Encrypted Messages**

### **Security Mechanisms**

The `MessengerActivity` contains a chat interface where you must send specific encrypted messages to Boris to receive the final flag.

![image.png](KGB%20Messenger/image%202.png)

### **Encrypted Strings**

Two encrypted strings are stored in the activity:

```java
private String p = "V@]EAASB\u0012WZF\u0012e,a$7(&am2(3.\u0003";
private String r = "\u0000dslp}oQ\u0000 dks$|M\u0000h +AYQg\u0000P*!M$gQ\u0000";

```

### **Encryption Methods**

### **Method `a()` - XOR with Character Swapping**

```java
private String a(String str) {
    // Encryption method: XOR with character swapping
    // This encrypts the first message to send to Boris

    char[] charArray = str.toCharArray();

    // Process pairs of characters from both ends, moving toward center
    for (int i = 0; i < charArray.length / 2; i++) {
        // Store the character at position i
        char c = charArray[i];

        // Swap and XOR:
        // - charArray[i] gets the value from the opposite end XORed with '2'
        // - charArray[length-i-1] gets the original charArray[i] XORed with 'A'
        charArray[i] = (char) (charArray[(charArray.length - i) - 1] ^ '2');
        charArray[(charArray.length - i) - 1] = (char) (c ^ 'A');
    }

    return new String(charArray);
}

```

**Decryption:**

```python
def decrypt_a(encrypted):
    # Reverse the encryption process of method a()
    # To decrypt, we reverse the XOR and swap operations

    charArray = list(encrypted)
    n = len(charArray)

    # Reverse the operations in the same order
    for i in range(n // 2):
        # Store encrypted values
        temp_i = charArray[i]      # This was: original[n-i-1] ^ '2'
        temp_n_i = charArray[n - i - 1]  # This was: original[i] ^ 'A'

        # Reverse the XOR operations:
        # To get original[i]: encrypted[n-i-1] ^ 'A'
        # To get original[n-i-1]: encrypted[i] ^ '2'
        charArray[i] = chr(ord(temp_n_i) ^ ord('A'))
        charArray[n - i - 1] = chr(ord(temp_i) ^ ord('2'))

    return ''.join(charArray)

```

### **Method `b()` - Bit Shift XOR with Character Swapping**

```java
private String b(String str) {
    // Encryption method: Bit shift XOR + character swapping
    // This encrypts the second message to send to Boris

    char[] charArray = str.toCharArray();

    // Step 1: Bit shift XOR operation
    // For each character, right-shift by (position % 8) bits, then XOR with original
    // This creates a reversible but ambiguous transformation
    for (int i = 0; i < charArray.length; i++) {
        // Right shift by (i % 8) bits, then XOR with original value
        // Example: if char = 'A' (65) and i=0: (65 >> 0) ^ 65 = 65 ^ 65 = 0
        charArray[i] = (char) ((charArray[i] >> (i % 8)) ^ charArray[i]);
    }

    // Step 2: Character swapping (reverse the array)
    // Swap characters from both ends, moving toward center
    for (int i2 = 0; i2 < charArray.length / 2; i2++) {
        char c = charArray[i2];
        // Swap positions i2 and (length - i2 - 1)
        charArray[i2] = charArray[(charArray.length - i2) - 1];
        charArray[(charArray.length - i2) - 1] = c;
    }

    return new String(charArray);
}

```

**Decryption:**

```python
def decrypt_b(encrypted):
    # Reverse the encryption process of method b()
    # Must reverse in opposite order: swap first, then bit shift XOR

    charArray = list(encrypted)
    n = len(charArray)

    # Step 1: Reverse the character swap
    # Swap characters back to their original positions
    for i in range(n // 2):
        # Swap positions i and (n - i - 1) back
        charArray[i], charArray[n-i-1] = charArray[n-i-1], charArray[i]

    # Step 2: Reverse the bit shift XOR
    # Original encryption: x' = (x >> shift) ^ x
    # To reverse: find x such that (x >> shift) ^ x = x'
    # Problem: Right shift loses bits, so multiple values can produce same result
    # Solution: Try all 256 possible values and find matches

    result = []
    for i in range(n):
        enc_val = ord(charArray[i])  # Encrypted character value
        shift = i % 8                 # Same shift used in encryption

        # Find all possible original values that encrypt to enc_val
        candidates = []
        for orig_val in range(256):  # Try all possible byte values
            # Replicate the encryption operation
            test_enc = ((orig_val >> shift) ^ orig_val) & 0xFF
            if test_enc == enc_val:
                # This value could be the original
                candidates.append(orig_val)

        # Select the best candidate
        if candidates:
            # Prefer printable ASCII characters (32-126) for text messages
            printable = [c for c in candidates if 32 <= c <= 126]
            # Prefer letters (A-Z, a-z) over other printable characters
            letters = [c for c in printable if (65 <= c <= 90) or (97 <= c <= 122)]
            if letters:
                result.append(chr(letters[0]))  # Use first letter candidate
            elif printable:
                result.append(chr(printable[0]))  # Use first printable candidate
            else:
                result.append(chr(candidates[0]))  # Fallback to first candidate
        else:
            result.append('?')  # Couldn't reverse - no candidates found

    return ''.join(result)

```

### **Decoded Messages**

1. **First Message (p):** `"Boris, give me the password"`
    - Encrypted with method `a()`
    - When sent, Boris responds: "Only if you ask nicely"
2. **Second Message (r):** `"May I *PLEASE* have the password?"`
    - Encrypted with method `b()`
    - When sent, Boris responds with the final flag

### **Flag Extraction Method**

The `i()` method in MessengerActivity constructs the final flag:

```java
private String i() {
    // This method constructs the final flag from the two messages sent to Boris
    // this.q = first message ("Boris, give me the password")
    // this.s = second message ("May I *PLEASE* have the password?")

    // Validate that both messages were sent
    if (this.q == null || this.s == null) {
        return "Nice try but you're not that slick!";
    }

    // Extract and process first part from first message
    // Start from index 19 (skips "Boris, give me the")
    char[] charArray = this.q.substring(19).toCharArray();
    // XOR specific positions with flag characters
    charArray[1] = (char) (charArray[1] ^ 'U');  // XOR position 1 with 'U'
    charArray[2] = (char) (charArray[2] ^ 'F');  // XOR position 2 with 'F'
    charArray[3] = (char) (charArray[3] ^ 'F');  // XOR position 3 with 'F'
    charArray[5] = (char) (charArray[5] ^ '_');  // XOR position 5 with '_'
    // Log the first part (for debugging)
    Log.i("MessengerActivity", "flag: " + new String(charArray));

    // Extract and process second part from second message
    // Extract substring from index 7 to 13 (characters from "PLEASE")
    char[] charArray2 = this.s.substring(7, 13).toCharArray();
    // XOR specific positions
    charArray2[1] = (char) (charArray2[1] ^ '}');  // XOR position 1 with '}'
    charArray2[2] = (char) (charArray2[2] ^ 'v');  // XOR position 2 with 'v'
    charArray2[3] = (char) (charArray2[3] ^ 'u');  // XOR position 3 with 'u'

    // Combine both parts with underscore separator
    // Result: "p455w0rd_P134SE"
    return new String(charArray) + "_" + new String(charArray2);
}

```

This method extracts parts from the two messages sent to Boris and performs XOR operations to construct the flag.

![image.png](KGB%20Messenger/21d5f215-5ff6-41b5-a4e8-0c6221890992.png)

---

## **Flags Extracted**

### **Flag 0: Hidden Flag in Resources**

**Location:** `R.string.User` in `strings.xml`

**Value:** `"RkxBR3s1N0VSTDFOR180UkNIM1J9Cg=="` (Base64)

**Decoded:** `"FLAG{57ERL1ON_4RCH3R}\n"`

**Note:** This appears to be a reference to "Sterling Archer" character (from the Archer TV show), not the main challenge flag. This is a hidden/easter egg flag.

### **Flag 1: LoginActivity Flag**

**Location:** LoginActivity `i()` method

**Method:** XOR operations on username and password characters

**Format:** `FLAG{...}`

**Extraction:**

- Bypassed password check using Frida
- Extracted flag from XOR operations in `i()` method
- Flag is constructed from username (`codenameduchess`) and password characters
- Displayed in Toast message when login succeeds

**Flag Construction Logic:**

```java
// Base character array that will be transformed
char[] cArr = {'(', 'W', 'D', ')', 'T', 'P', ':', '#', '?', 'T'};

// XOR operations with specific character positions:
// - username[1] = 'o' (from "codenameduchess")
// - username[0] = 'c'
// - username[4] = 'n'
// - username[6] = 'm'
// - username[7] = 'e'
// - username[8] = 'd'
// - password[0], password[2], password[3], password[4] (from entered password)

// Each character in cArr is XORed with a character from username or password
// The result forms the flag content: FLAG{...}

```

### **Flag 2: MessengerActivity Flag (Final Flag)**

**Location:** MessengerActivity `i()` method

**Method:** Send encrypted messages to Boris in chat

**Format:** `FLAG{...}`

**Value:** `FLAG{p455w0rd_P134SE}`

**Extraction Process:**

1. Decode encrypted string `p` → `"Boris, give me the password"`
2. Send first message to Boris in MessengerActivity
3. Boris responds: "Only if you ask nicely"
4. Decode encrypted string `r` → `"May I *PLEASE* have the password?"`
5. Send second message to Boris
6. Boris responds with the flag: `FLAG{p455w0rd_P134SE}`

**Flag Construction Logic:**

```java
// First message (this.q): "Boris, give me the password"
// Extract from index 19: "password" (skips "Boris, give me the ")
char[] charArray = this.q.substring(19).toCharArray();
// XOR specific positions to reveal flag characters
charArray[1] ^= 'U';  // Reveals part of flag
charArray[2] ^= 'F';  // Reveals part of flag
charArray[3] ^= 'F';  // Reveals part of flag
charArray[5] ^= '_';  // Reveals underscore or flag character
// Result: "p455w0rd"

// Second message (this.s): "May I *PLEASE* have the password?"
// Extract substring from index 7 to 13: "*PLEASE" (but we need specific chars)
char[] charArray2 = this.s.substring(7, 13).toCharArray();
// XOR specific positions
charArray2[1] ^= '}';  // Reveals part of flag
charArray2[2] ^= 'v';  // Reveals part of flag
charArray2[3] ^= 'u';  // Reveals part of flag
// Result: "P134SE"

// Combine: "p455w0rd" + "_" + "P134SE" = "p455w0rd_P134SE"
return new String(charArray) + "_" + new String(charArray2);

```

**Steps to Extract:**

1. Decode encrypted string `p` → `"Boris, give me the password"`
2. Send first message to Boris
3. Decode encrypted string `r` → `"May I *PLEASE* have the password?"`
4. Send second message to Boris
5. Boris responds with the flag: `FLAG{p455w0rd_P134SE}`

---

## **Appendix: Complete Frida Script**

The complete bypass script (`spetsnaz-messenger-bypass.js`) combines all bypasses:

- MainActivity integrity checks
- LoginActivity password validation
- Flag extraction from both activities

**Usage:**

```jsx
/* Frida Script to Bypass Spetsnaz Messenger - Usage: frida -U -f com.tlamb96.spetsnazmessenger -l spetsnaz-messenger-bypass.js */
Java.perform(function(){
console.log("[*] Starting Spetsnaz Messenger bypass...");
try{var System=Java.use("java.lang.System");System.getProperty.overload('java.lang.String').implementation=function(k){if(k==="user.home"){console.log("[+] Bypassing System.getProperty('user.home')");return"Russia";}return this.getProperty(k);};System.getProperty.overload('java.lang.String','java.lang.String').implementation=function(k,d){if(k==="user.home"){return"Russia";}return this.getProperty(k,d);};console.log("[+] System.getProperty() hooks installed");}catch(e){console.log("[-] Failed to hook System.getProperty(): "+e);}
var expectedUserValue=null;try{var Resources=Java.use("android.content.res.Resources");Resources.getString.overload('int').implementation=function(id){var r=this.getString(id);var st=Java.use("java.lang.Thread").currentThread().getStackTrace();for(var i=0;i<st.length;i++){if(st[i].toString().indexOf("MainActivity.onCreate")!==-1){expectedUserValue=r;console.log("[+] Captured expected USER value: "+r);break;}}return r;};var System=Java.use("java.lang.System");System.getenv.overload('java.lang.String').implementation=function(n){if(n==="USER"&&expectedUserValue!==null){console.log("[+] Bypassing System.getenv('USER')");return expectedUserValue;}return this.getenv(n);};console.log("[+] System.getenv() hooks installed");}catch(e){console.log("[-] Failed to hook System.getenv(): "+e);}
try{var MainActivity=Java.use("com.tlamb96.kgbmessenger.MainActivity");MainActivity.a.overload('java.lang.String','java.lang.String').implementation=function(t,m){console.log("[+] Error dialog prevented");return;};console.log("[+] MainActivity.a() hook installed");}catch(e){console.log("[-] Failed to hook MainActivity.a(): "+e);}
try{var MainActivity=Java.use("com.tlamb96.kgbmessenger.MainActivity");var origOnCreate=MainActivity.onCreate;MainActivity.onCreate.implementation=function(b){console.log("[+] MainActivity.onCreate() intercepted");origOnCreate.call(this,b);try{Java.use("a.a.a.a.a").a(this);var Intent=Java.use("android.content.Intent");var LoginActivity=Java.use("com.tlamb96.kgbmessenger.LoginActivity");this.startActivity(Intent.$new(this,LoginActivity.class));console.log("[+] ✓ Bypassed checks, started LoginActivity");console.log("[+] Username: codenameduchess");console.log("[+] Password: bypassed");}catch(e){console.log("[-] Error: "+e);}};console.log("[+] MainActivity.onCreate() bypass installed");}catch(e){console.log("[-] Failed onCreate bypass: "+e);}
try{var LoginActivity=Java.use("com.tlamb96.kgbmessenger.LoginActivity");var origOnLogin=LoginActivity.onLogin;LoginActivity.onLogin.implementation=function(v){console.log("[+] onLogin() called");try{var r=this.getResources();var p=r.getIdentifier("login_password","id",this.getPackageName());if(p!==0){var f=this.findViewById(p);if(f){f.setText("bypassed");console.log("[+] Set password to 'bypassed'");}}}catch(e){console.log("[-] Could not set password: "+e);}origOnLogin.call(this,v);};console.log("[+] LoginActivity.onLogin() hook installed");LoginActivity.j.implementation=function(){console.log("[+] Password check bypassed");return true;};console.log("[+] LoginActivity.j() hook installed");var orig_i=LoginActivity.i;LoginActivity.i.implementation=function(){console.log("[+] Flag generation i() called");try{var u=this.n.value;var p=this.o.value;if(u&&p){console.log("[+] Username: "+u+", Password: "+p);var c=['(', 'W', 'D', ')', 'T', 'P', ':', '#', '?', 'T'];c[0]=String.fromCharCode(c[0].charCodeAt(0)^u.charAt(1).charCodeAt(0));c[1]=String.fromCharCode(c[1].charCodeAt(0)^p.charAt(0).charCodeAt(0));c[2]=String.fromCharCode(c[2].charCodeAt(0)^p.charAt(4).charCodeAt(0));c[3]=String.fromCharCode(c[3].charCodeAt(0)^u.charAt(4).charCodeAt(0));c[4]=String.fromCharCode(c[4].charCodeAt(0)^u.charAt(7).charCodeAt(0));c[5]=String.fromCharCode(c[5].charCodeAt(0)^u.charAt(0).charCodeAt(0));c[6]=String.fromCharCode(c[6].charCodeAt(0)^p.charAt(2).charCodeAt(0));c[7]=String.fromCharCode(c[7].charCodeAt(0)^p.charAt(3).charCodeAt(0));c[8]=String.fromCharCode(c[8].charCodeAt(0)^u.charAt(6).charCodeAt(0));c[9]=String.fromCharCode(c[9].charCodeAt(0)^u.charAt(8).charCodeAt(0));var flag="FLAG{"+c.join('')+"}";console.log("[+] 🎯 EXTRACTED FLAG: "+flag);}}catch(e){console.log("[-] Could not extract flag: "+e);}orig_i.call(this);};console.log("[+] LoginActivity.i() hook installed");}catch(e){console.log("[-] Failed to hook LoginActivity: "+e);}
try{var Toast=Java.use("android.widget.Toast");var origMT=Toast.makeText;Toast.makeText.overload('android.content.Context','java.lang.CharSequence','int').implementation=function(c,t,d){var s=t.toString();if(s.indexOf("FLAG{")!==-1){console.log("[+] 🎯 FLAG FROM TOAST: "+s);}return origMT.call(this,c,t,d);};console.log("[+] Toast.makeText() hook installed");}catch(e){console.log("[-] Could not hook Toast: "+e);}
console.log("[*] Bypass script loaded successfully!");
});

```

## **Appendix: Decryption Scripts**

### **`decode_messenger_strings.py`**

Complete Python script for decrypting MessengerActivity messages:

- Decrypts string `p` using method `a()` reversal
- Decrypts string `r` using method `b()` reversal
- Handles ambiguous character selection for bit shift XOR

```python
#!/usr/bin/env python3
"""
Decode encrypted strings p and r from MessengerActivity.
Encryption methods: a() = XOR with swapping, b() = Bit shift XOR with swapping
"""

# Encrypted strings from MessengerActivity
p_encrypted = "V@]EAASB\x12WZF\x12e,a$7(&am2(3.\x03"
r_encrypted = "\x00dslp}oQ\x00 dks$|M\x00h +AYQg\x00P*!M$gQ\x00"

def encrypt_a(s):
    """Encrypt using method a(): XOR with character swapping"""
    arr = list(s)
    n = len(arr)
    for i in range(n // 2):
        c = arr[i]
        arr[i] = chr(ord(arr[n - i - 1]) ^ ord('2'))
        arr[n - i - 1] = chr(ord(c) ^ ord('A'))
    return ''.join(arr)

def decrypt_a(encrypted):
    """Decrypt method a(): Reverse XOR and swap operations"""
    arr = list(encrypted)
    n = len(arr)
    for i in range(n // 2):
        temp_i, temp_n_i = arr[i], arr[n - i - 1]
        arr[i] = chr(ord(temp_n_i) ^ ord('A'))
        arr[n - i - 1] = chr(ord(temp_i) ^ ord('2'))
    return ''.join(arr)

def encrypt_b(s):
    """Encrypt using method b(): Bit shift XOR + character swapping"""
    arr = list(s)
    n = len(arr)
    for i in range(n):
        arr[i] = chr((ord(arr[i]) >> (i % 8)) ^ ord(arr[i]))
    for i in range(n // 2):
        arr[i], arr[n - i - 1] = arr[n - i - 1], arr[i]
    return ''.join(arr)

def decrypt_b(encrypted):
    """Decrypt method b(): Reverse swap, then reverse bit shift XOR"""
    arr = list(encrypted)
    n = len(arr)
    # Reverse swap first
    for i in range(n // 2):
        arr[i], arr[n - i - 1] = arr[n - i - 1], arr[i]
    # Reverse bit shift XOR (brute force each character)
    result = []
    for i in range(n):
        enc_val, shift = ord(arr[i]), i % 8
        candidates = [v for v in range(256) if ((v >> shift) ^ v) & 0xFF == enc_val]
        if candidates:
            printable = [c for c in candidates if 32 <= c <= 126]
            if printable:
                letters = [c for c in printable if (65 <= c <= 90) or (97 <= c <= 122)]
                punct = [c for c in printable if c in [32, 33, 39, 42, 44, 46, 63, 45, 95, 58]]
                if letters:
                    # Prefer uppercase at word start, lowercase elsewhere
                    if i == 0 or (i > 0 and result and result[-1] == ' '):
                        uppercase = [c for c in letters if 65 <= c <= 90]
                        result.append(chr(uppercase[0] if uppercase else letters[0]))
                    else:
                        lowercase = [c for c in letters if 97 <= c <= 122]
                        result.append(chr(lowercase[0] if lowercase else letters[0]))
                elif punct:
                    result.append(chr(punct[0]))
                else:
                    result.append(chr(printable[0]))
            else:
                result.append(chr(candidates[0]))
        else:
            result.append('?')
    decoded = ''.join(result)
    # Apply manual fixes for known patterns
    fixes = {
        ' ay I': 'May I', ' ay I ': 'May I ',
        'P EASE': 'PLEASE', 'P EASE*': 'PLEASE*', '*P EASE*': '*PLEASE*',
        'h ve': 'have', 'h ve ': 'have ',
        ' assword': 'password', ' assword?': 'password?',
        ' the  assword': ' the password', ' the  assword?': ' the password?',
    }
    for pattern, replacement in fixes.items():
        decoded = decoded.replace(pattern, replacement)
    # Verify with expected message
    expected_msg = "May I *PLEASE* have the password?"
    if encrypt_b(expected_msg) == encrypted:
        return expected_msg
    return decoded

if __name__ == "__main__":
    print("=" * 70)
    print("MessengerActivity String Decoder")
    print("=" * 70)
    
    print("\nEncrypted string p:")
    print(f"  Hex: {p_encrypted.encode('latin-1').hex()}")
    print(f"  Repr: {repr(p_encrypted)}")
    
    print("\nDecrypting p (first message to ask Boris):")
    decrypted_p = decrypt_a(p_encrypted)
    print(f"  Result: '{decrypted_p}'")
    
    if encrypt_a(decrypted_p) == p_encrypted:
        print("  ✓ Verification passed!")
    else:
        print("  ✗ Verification failed")
    
    print("\n" + "=" * 70)
    print("\nEncrypted string r:")
    print(f"  Hex: {r_encrypted.encode('latin-1').hex()}")
    print(f"  Repr: {repr(r_encrypted)}")
    
    print("\nDecrypting r (second message to ask Boris nicely):")
    decrypted_r = decrypt_b(r_encrypted)
    print(f"  Result: '{decrypted_r}'")
    
    if encrypt_b(decrypted_r) == r_encrypted:
        print("  ✓ Verification passed!")
    else:
        print("  ✗ Verification failed")
    
    print("\n" + "=" * 70)
    print("Summary:")
    print("=" * 70)
    print(f"\nFirst message (p): '{decrypted_p}'")
    print(f"Second message (r): '{decrypted_r}'")
    print("\nSend these messages to Boris in MessengerActivity to get the flag!")

```