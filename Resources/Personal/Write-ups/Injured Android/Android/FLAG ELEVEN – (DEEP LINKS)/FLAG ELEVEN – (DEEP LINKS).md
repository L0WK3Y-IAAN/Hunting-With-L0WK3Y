# FLAG ELEVEN – (DEEP LINKS)

**Flag 11** tests your ability to identify entry points in the `AndroidManifest.xml` (Deep Links) and correlate them with data stored in a backend database (Firebase). The challenge is to find the correct scheme to launch the activity and then identify the specific database key hint.

---

## Reconnaissance: The Manifest

The `AndroidManifest.xml` reveals that the `DeepLinkActivity` is not accessible via the standard UI flow but has a "backdoor" open via a Deep Link.

```xml
<activity android:label="@string/title_activity_deep_link" android:name="b3nac.injuredandroid.DeepLinkActivity">
    <intent-filter ...>
        ...
        <data android:scheme="flag11"/>
    </intent-filter>
</activity>
```

- **Finding:** The activity listens for the URI scheme `flag11://`.

## Source Code Analysis

Inside `DeepLinkActivity.java`, we see how the app verifies the flag.

## The Hint

```java
private final String z = "/binary";
```

The variable `z` is set to `/binary`. This is the "compiled treasure" the hint refers to—not a literal compiled file, but a reference to a specific location in the database.

## The Validation

```java
*// Sets up a reference to the "/binary" path in Firebase*
this.B = d2.h(this.z); 

*// Submits the text from the EditText to the Listener 'c'*
this.B.b(new c(editText.getText().toString()));
```

The app compares your input directly against the value stored at `injuredandroid.firebaseio.com/binary`.

## Exploitation

## Step 1: Trigger the Deep Link

Since you cannot navigate to this screen easily from the main menu, you must force it open using the scheme found in the manifest.

**Command:**

```bash
adb shell am start -W -a android.intent.action.VIEW -d "flag11://"
```

This launches the `DeepLinkActivity` on your device/emulator.

## Step 2: Retrieve the Flag (The "Treasure")

The code tells us the answer is stored at the `/binary` endpoint. Since the database rules allow public read access, we can query it directly via the REST API.

**URL:**

`https://injuredandroid.firebaseio.com/binary.json`

**Result:**

```json
"HIIMASTRING"
```

## Step 3: Solve

1. Go to the screen you opened in Step 1.
2. Enter the value `HIIMASTRING`.
3. Press Submit.

![image.png](FLAG%20ELEVEN%20%E2%80%93%20(DEEP%20LINKS)/image.png)