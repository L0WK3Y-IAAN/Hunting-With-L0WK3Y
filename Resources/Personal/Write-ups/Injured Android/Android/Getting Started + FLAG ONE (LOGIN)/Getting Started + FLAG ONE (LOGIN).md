# Getting Started + FLAG ONE (LOGIN)

## Getting Started

This CTF mobile challenge is based on the InjuredAndroid project, available here:

[**https://github.com/B3nac/InjuredAndroid**](https://github.com/B3nac/InjuredAndroid).

For this walkthrough, the application was tested on a **Google Pixel 9 XL** device running a compatible Android version, but any modern device should work as long as you can install unsigned APKs. You will also need to emulate an older version of Android for one of the older challenges, so using an emulator such as [**`Android Studio’s AVD (Android Virtual Device)`**](https://developer.android.com/studio/run/managing-avds) will allow you to complete said challenge (more on this when I get to the specified challenge).

To inspect the application internals, the APK was decompiled using [**`Jadx`**](https://github.com/skylot/jadx/releases/tag/v1.5.3), which provides a convenient GUI for viewing decompiled Java/Kotlin code and navigating through packages, classes, and methods. After obtaining the APK, simply open it in Jadx, locate the **`b3nac.injuredandroid`** package, and you can start examining activities, exported components, and any native or Firebase-related logic that will be referenced throughout the challenge.

![image.png](Getting%20Started%20+%20FLAG%20ONE%20(LOGIN)/c0a9089e-2897-4837-bc97-d91319156a9e.png)

---

## Flag 1 - (LOGIN)

![image.png](Getting%20Started%20+%20FLAG%20ONE%20(LOGIN)/image.png)

Let’s take a look at the `FlagOneLoginActivity` to see what the code is doing in JADX. I head on over to the `AndroidManifest.xml` under resources and navigate to the FlagOneLoginActivity class to obtain the flag.

![image.png](Getting%20Started%20+%20FLAG%20ONE%20(LOGIN)/image%201.png)

```java
public final void submitFlag(View view) {
        EditText editText = (EditText) findViewById(R.id.editText2);
        d.s.d.g.d(editText, "editText2");
        if (d.s.d.g.a(editText.getText().toString(), "F1ag_0n3")) //<-- basic string comparison 
        {
            Intent intent = new Intent(this, (Class<?>) FlagOneSuccess.class);
            new FlagsOverview().J(true);
            new j().b(this, "flagOneButtonColor", true);
            startActivity(intent);
        }
    }
```