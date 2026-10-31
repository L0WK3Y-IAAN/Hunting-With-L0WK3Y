---
title: "HackTheBox — Don't Overreact (Mobile) Walkthrough"
description: "Reversing a React Native Android app: the flag hides Base64-encoded in a config object inside the minified JavaScript bundle."
tags: [Android, React Native, Reverse Engineering, Base64]
difficulty: Very Easy
---
**Challenge:** Don't Overreact

**Category:** Mobile / Reverse Engineering

**Difficulty:** Very Easy

---

## Challenge Description

> Some web developers wrote this fancy new app! It's really cool, isn't it?

We're given a React Native Android application (`dont_overreact.zip`) and need to find the hidden flag.

---

## Initial Analysis

### 1. APK Extraction

First, I extracted the APK using standard Android reverse engineering tools:

```bash
# Extract APK structure
apktool d app-release.apk -o app-release_EXTRACTION
```

The extraction revealed:

- **Package Name:** `com.awesomeproject`
- **Main Activity:** `MainActivity.java` (standard React Native entry point)
- **React Native Bundle:** `assets/index.android.bundle` (410 lines of minified JavaScript)

### 2. Application Structure

The app follows a standard React Native structure:

- `MainActivity.java` - Entry point, registers the "AwesomeProject" component
- `MainApplication.java` - React Native host configuration
- `index.android.bundle` - Contains all the React Native JavaScript code (minified)

---

## The Hunt for the Flag

### Approach 1: Analyzing the Bundle

Since this is a React Native app, the JavaScript code is bundled into `index.android.bundle`. The file is minified but still readable. I searched for common CTF patterns:

```bash
# Search for flag patterns
grep -i "flag\|ctf\|secret\|password\|key\|api" index.android.bundle
```

### Approach 2: Manual Code Review

After examining the bundle file, I found an interesting configuration object near the end of the file (around line 406):

```javascript
__d(function (g, r, i, a, m, e, d) {
  Object.defineProperty(e, "__esModule", { value: !0 }),
  e.myConfig = void 0;
  var t = {
    importantData: "baNaNa".toLowerCase(),
    apiUrl: 'https://www.hackthebox.eu/',
    debug: 'SFRCe<REDACTED>='
  };
  e.myConfig = t
}, 400, []);
```

**Key findings:**

- `importantData`: `"baNaNa".toLowerCase()` → `"banana"` (red herring?)
- `apiUrl`: Points to the HackTheBox website
- `debug`: Contains a Base64-encoded string! 🎯

### Approach 3: Decoding the Flag

The `debug` field contains what appears to be a Base64-encoded string (note that `SFRC` is Base64 for `HTB`):

```txt
SFRCe<REDACTED>=
```

Let's decode it:

```bash
echo "<the debug value>" | base64 -d
```

**Result:**

```txt
HTB{REDACTED}
```

---

## Flag

```txt
HTB{REDACTED}
```

---

## Vulnerability Analysis

### Security Issues Identified

1. **Hardcoded secrets in client-side code**
   - The flag is embedded directly in the JavaScript bundle
   - Even though the code is minified, it's still readable
   - No obfuscation or server-side validation
2. **Debug information in a production build**
   - The `debug` field suggests this might be leftover from development
   - Production builds should not contain debug information or flags
3. **No code obfuscation**
   - The React Native bundle is minified but not obfuscated
   - Sensitive data can be easily extracted with basic reverse engineering

### Recommendations

1. **Never store secrets in client-side code** - Use environment variables or secure backend APIs
2. **Implement proper obfuscation** - Use tools like ProGuard/R8 for native code and JavaScript obfuscators
3. **Remove debug code** - Ensure production builds don't include development/debug information
4. **Use secure storage** - For any sensitive data, use Android Keystore or encrypted storage

---

## Tools Used

- **APKTool** - APK decompilation
- **JADX** - Java decompiler (for native Android code)
- **grep** - Pattern searching
- **base64** - Base64 decoding
- **Text editor** - Manual code review

---

## Lessons Learned

1. **React Native apps are not secure by default** - The JavaScript bundle is easily accessible
2. **Minification ≠ security** - Minified code is still readable
3. **Always check configuration objects** - Developers often leave debug/config data in bundles
4. **Base64 is not encryption** - It's encoding, easily reversible

---

## Conclusion

This challenge demonstrates a common mistake in mobile app development: storing sensitive information directly in the client-side code. The flag was hidden in plain sight within a configuration object in the React Native bundle, encoded with Base64 (which provides no security).

The challenge name "Don't Overreact" is a clever pun: it's a React Native app, and we shouldn't "overreact" to the minified code; the flag is right there waiting to be found!
