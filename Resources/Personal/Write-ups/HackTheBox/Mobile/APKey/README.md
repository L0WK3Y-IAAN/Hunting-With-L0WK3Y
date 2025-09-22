![banner](https://i.imgur.com/qIr832s.png)

## Challenge Description

### ***"This app contains some unique keys. Can you get one?"***


The Android app had several Java classes each holding small fragments of what eventually formed two critical pieces of data:

1. **The AES Decryption Key:** Built by concatenating individual characters selected from various string arrays.
2. **The Encrypted Flag:** Constructed by piecing together substrings from multiple arrays into one long Base64‑encoded ciphertext.

---

## MainActivity

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    android:versionCode="1"
    android:versionName="1.0"
    android:compileSdkVersion="30"
    android:compileSdkVersionCodename="11"
    package="com.example.apkey"
    platformBuildVersionCode="30"
    platformBuildVersionName="11">
    <uses-sdk
        android:minSdkVersion="16"
        android:targetSdkVersion="30"/>
    <application
        android:theme="@style/Theme.APKey"
        android:label="@string/app_name"
        android:icon="@mipmap/ic_launcher"
        android:allowBackup="true"
        android:supportsRtl="true"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:appComponentFactory="androidx.core.app.CoreComponentFactory">
        <activity android:name="com.example.apkey.MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
```

After taking a look at the AndroidManifest.xml, you’ll spot the MainActivity which we can navigate to for the core functionality.

## Main Activity

- **Handling User Input:**
    
    An inner class implementing `View.OnClickListener` is set on the button. When the button is clicked, the following steps occur:
    
    1. **Username Verification:**
        
        The code checks if the username equals `"admin"`.
        
    2. **Password Verification via MD5:**
        
        The entered password is hashed using MD5. Each byte of the hash is converted to a hexadecimal string, and the final hash is compared to a hardcoded value:
        
        ```java
        if (str.equals("a2a3d412e92d896134d9c9126d756f"))
        ```
        
    3. **Triggering Decryption:**
        
        If both the username and password match the expected values, the app calls:
        
        ```java
        b.a(g.a())
        ```
        
        This call first assembles a Base64‑encoded ciphertext using class `g` and then decrypts it using class `b`. The decrypted message (which turns out to be the flag) is then shown to the user via a Toast.
        
    4. **Error Handling:**
        
        If the credentials don’t match, the user sees a "Wrong Credentials!" message.
        

---

## Unpacking the Obfuscation Layers

Once you pass the authentication in MainActivity, the app calls the decryption function. Let’s explore how the decryption mechanism is structured across various classes.

### Fragmented String Storage

```kotlin
package c.b.a;

import android.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

/* loaded from: classes.dex */
public class b {
    public static String a(String str) {
        SecretKeySpec secretKeySpec = new SecretKeySpec((String.valueOf(h.a().charAt(0)) + String.valueOf(a.a().charAt(8)) + String.valueOf(e.a().charAt(5)) + String.valueOf(i.a().charAt(4)) + String.valueOf(h.a().charAt(1)).toLowerCase() + String.valueOf(h.a().charAt(4)) + String.valueOf(h.a().charAt(3)).toLowerCase() + String.valueOf(h.a().charAt(3)) + String.valueOf(h.a().charAt(0)) + String.valueOf(a.a().charAt(8)).toLowerCase() + String.valueOf(a.a().charAt(8)).toLowerCase() + String.valueOf(i.a().charAt(0)) + String.valueOf(c.a().charAt(3)).toLowerCase() + String.valueOf(f.a().charAt(3)) + String.valueOf(f.a().charAt(0)) + String.valueOf(c.a().charAt(0))).getBytes(), g.b());
        Cipher cipher = Cipher.getInstance(g.b());
        cipher.init(2, secretKeySpec);
        return new String(cipher.doFinal(Base64.decode(str, 0)), "utf-8");
    }
}
```

The decryption key and the ciphertext aren’t stored in one place. Instead, multiple classes such as `a`, `c`, `d`, `e`, `f`, `h`, and `i` each hold fragments of data. Each class has a method `a()` that returns a string extracted from an array. For instance:

```java
public class e {
    public static String a() {
        ArrayList arrayList = new ArrayList();
        arrayList.add("TG7ygj");
        arrayList.add("U8uu8i");
        arrayList.add("gGtT56");
        arrayList.add("84hYDG");
        arrayList.add("ejhHy6");
        arrayList.add("7ytr4E");
        arrayList.add("j5jU87");
        arrayList.add("HyeaX9"); // Key piece
        arrayList.add("jd9Idu");
        arrayList.add("kd546G");
        return (String) arrayList.get(7);
    }
}

//e.a(5) returns the 5th character from the 7th item in the array list.
```

This method of scattering the data makes it challenging to immediately see the whole picture.

### Assembling the AES Key in Class `b`

Class `b` is responsible for decrypting the ciphertext. It constructs the decryption key by concatenating specific characters from the outputs of the fragmented string methods. For example:

- `h.a().charAt(0)`
- `a.a().charAt(8)`
- `e.a().charAt(5)`
- `i.a().charAt(4)`
- Additional characters extracted from other classes with some converted to lowercase

When you follow the extraction sequence provided in class `b`, the resulting 16‑byte key is:

```
kV9qhuzZkvvrgW6F
```

### Constructing the Encrypted Data in Class `g`

```kotlin
package c.b.a;

import java.util.ArrayList;

/* loaded from: classes.dex */
public class g {
    public static String a() {
        StringBuilder sb = new StringBuilder();
        ArrayList arrayList = new ArrayList();
        arrayList.add("722gFc");
        arrayList.add("n778Hk");
        arrayList.add("jvC5bH");
        arrayList.add("lSu6G6");
        arrayList.add("HG36Hj");
        arrayList.add("97y43E");
        arrayList.add("kjHf5d");
        arrayList.add("85tR5d");
        arrayList.add("1UlBm2"); // Key piece
        arrayList.add("kI94fD");
        sb.append((String) arrayList.get(8));
        sb.append(h.a());
        sb.append(i.a());
        sb.append(f.a());
        sb.append(e.a());
        ArrayList arrayList2 = new ArrayList();
        arrayList2.add("ue7888");
        arrayList2.add("6HxWkw");
        arrayList2.add("gGhy77");
        arrayList2.add("837gtG");
        arrayList2.add("HyTg67");
        arrayList2.add("GHR673");
        arrayList2.add("ftr56r");
        arrayList2.add("kikoi9");
        arrayList2.add("kdoO0o");
        arrayList2.add("2DabnR");
        sb.append((String) arrayList2.get(9));
        sb.append(c.a());
        ArrayList arrayList3 = new ArrayList();
        arrayList3.add("jH67k8");
        arrayList3.add("8Huk89");
        arrayList3.add("fr5GtE");
        arrayList3.add("Hg5f6Y");
        arrayList3.add("o0J8G5");
        arrayList3.add("Wod2bk");
        arrayList3.add("Yuu7Y5");
        arrayList3.add("kI9ko0");
        arrayList3.add("dS4Er5");
        arrayList3.add("h93Fr5");
        sb.append((String) arrayList3.get(5));
        sb.append(d.a());
        sb.append(a.a());
        return sb.toString();
    }

    public static String b() {
        return String.valueOf(d.a().charAt(1)) + String.valueOf(i.a().charAt(2)) + String.valueOf(i.a().charAt(1));
    }
}
```

The ciphertext is pieced together in class `g`:

- It begins with a fragment from one array (for example, the element at index 8: `"1UlBm2"`).
- Then it appends results from `h.a()`, `i.a()`, `f.a()`, and `e.a()`.
- More segments from additional arrays and calls to `c.a()`, `d.a()`, and `a.a()` complete the ciphertext.

The final concatenated Base64‑encoded string is:

```
1UlBm2kHtZuVrSE6qY6HxWkwHyeaX92DabnRFlEGyLWod2bkwAxcoc85S94kFpV1
```

This string is what gets decrypted once the authentication in MainActivity passes.

---

## The Decryption Process

Inside class `b`, the following steps occur:

1. **Key Setup:**
    
    The 16‑byte key `"kV9qhuzZkvvrgW6F"` is used to create a `SecretKeySpec`.
    
2. **Cipher Configuration:**
    
    The cipher is initialized with:
    
    ```java
    Cipher.getInstance("AES")
    ```
    
    This typically means AES in ECB mode with PKCS5Padding in Java.
    
3. **Decoding and Decryption:**
    
    The Base64‑encoded string from `g.a()` is decoded into bytes. The cipher then decrypts these bytes with the key, removing the padding to reveal the plaintext. If successful, the plaintext is the flag:
    
    ```
    HTB{REDACTED}
    ```
    

---

## Bringing It All Together with a Python Script

For verification and to illustrate the process outside of the Android environment we can mimic the decryption with a Python script using [PyCryptodome](https://pycryptodome.readthedocs.io/). Here’s the complete script:

```python
#!/usr/bin/env python3
from Crypto.Cipher import AES
import base64

def unpad(data):
    """
    Remove PKCS#7 (or PKCS#5) padding.
    """
    pad_len = data[-1]
    return data[:-pad_len]

def decrypt_flag(ciphertext_base64, key):
    # Create an AES cipher in ECB mode.
    cipher = AES.new(key, AES.MODE_ECB)
    # Decode the Base64 string to bytes.
    ciphertext = base64.b64decode(ciphertext_base64)
    # Decrypt and remove padding.
    decrypted = cipher.decrypt(ciphertext)
    return unpad(decrypted)

if __name__ == '__main__':
    # The Base64 string generated by g.a()
    ciphertext_base64 = "1UlBm2kHtZuVrSE6qY6HxWkwHyeaX92DabnRFlEGyLWod2bkwAxcoc85S94kFpV1"

    # The decryption key constructed in b.a()
    key = b'kV9qhuzZkvvrgW6F'

    try:
        decrypted_flag = decrypt_flag(ciphertext_base64, key)
        print("Decrypted flag:", decrypted_flag.decode('utf-8'))
    except Exception as e:
        print("Decryption failed:", e)
```

Running this script reproduces the decryption process from the Java code and prints out the flag:

```
HTB{REDACTED}
```
