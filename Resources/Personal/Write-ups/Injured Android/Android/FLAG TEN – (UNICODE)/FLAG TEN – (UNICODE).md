# FLAG TEN – (UNICODE)

This challenge was a bit tricky as it didn’t make much sense to me as to where to find the email and searching for “android unicode collision” mostly returns other writeup’s for this challenge, so instead I will breakdown the code and explain how it works for anyone that is curious. The email `John@Gıthub.com` works because of a **Unicode Collision**. The character `ı` (Latin Small Letter Dotless I) is distinct from the standard `i`, so it bypasses the "No Cheating" check. However, when converted to uppercase, both `ı` and `i` become the same character `I`, satisfying the validation check that unlocks the flag.

---

## Code Breakdown

Here is the step-by-step analysis of the code snippets you provided.

## 1. The Setup: Base64 Decoding

The app first determines where to look in the database.

```java
*// Decodes "dW5pY29kZS8=" to "unicode/"*
byte[] decode = Base64.decode("dW5pY29kZS8=", 0);
this.z = new String(decode, charset);

*// Sets up a listener on the "unicode/" path in Firebase*
com.google.firebase.database.d h = d2.h(this.z);
```

The app is listening for the correct "email" string stored at `unicode/` in the database.

## 2. The Trap: Direct Equality Check

When you press submit, the `b` class (a Listener) receives the data from Firebase (`str2`) and compares it with your input (`this.f1462b`).

```java
*// str2 = Value from Firebase (e.g., "John@Github.com")// this.f1462b = Your input (e.g., "John@Github.com")*

if (d.s.d.g.a(this.f1462b, str2)) {
    *// If they are EXACTLY the same:*
    flagTenUnicodeActivity = FlagTenUnicodeActivity.this;
    str = "No cheating. :]";
}
```

**What's happening:** The developer prevents you from just dumping the string from the database and pasting it in. If you type the standard "[John@Github.com](mailto:John@Github.com)", it matches `str2` exactly, triggering the "No cheating" message.

## 3. The Vulnerability: Uppercase Conversion

If the exact match fails, the code proceeds to a second check using `toUpperCase`.

```java
*// Converts your input to Uppercase*
String upperCase = str3.toUpperCase(locale);

*// Converts Firebase value to Uppercase*
String upperCase2 = str2.toUpperCase(locale2);

*// Checks if the UPPERCASE versions match*
if (d.s.d.g.a(upperCase, upperCase2)) {
    FlagTenUnicodeActivity.this.G(); *// Success! Flag unlocked.*
    return;
}
```

**What's happening:**

1. **Your Input:** `John@Gıthub.com` (with dotless `ı`).
2. **Database Value:** `John@Github.com` (with normal `i`).
3. **Normalization:**
    - `ı` (dotless) becomes `I` when uppercased.
    - `i` (dotted) also becomes `I` when uppercased.
4. **Result:** `JOHN@GITHUB.COM` == `JOHN@GITHUB.COM`.
    
    The strings are different enough to bypass the "No cheating" trap, but similar enough to pass the "Uppercase" validation.
    

![image.png](FLAG%20TEN%20%E2%80%93%20(UNICODE)/image.png)