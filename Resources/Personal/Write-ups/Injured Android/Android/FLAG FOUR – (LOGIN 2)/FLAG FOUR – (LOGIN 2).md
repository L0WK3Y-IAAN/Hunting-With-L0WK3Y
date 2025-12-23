# FLAG FOUR – (LOGIN 2)


In FlagFour I am presented with another login prompt.

![image.png](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/raw/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20FOUR%20%E2%80%93%20(LOGIN%202)/FLAG%20FOUR%20%E2%80%93%20(LOGIN%202)/image.png)

This time I see the string “`decoder.getData()`” which tells me that there is some form of decoding going on.  The line “`byte[] a2 = new g().a();`” creates a new byte array with the returned data from the class and method `g.a`.

```java
public final void submitFlag(View view) {
    // Look up the EditText where the user types the flag (id: editText2)
    EditText editText = (EditText) findViewById(R.id.editText2);
    // Kotlin null-check helper: throws if editText is null, with "editText2" as the label
    d.s.d.g.d(editText, "editText2");

    // Read the user input from the EditText as a String (this is the candidate flag)
    String obj = editText.getText().toString();

    // Create a new decoder (class g) and get its internal byte[] value
    // g.f1468a is Base64‑decoded from "NF9vdmVyZG9uZV9vbWVsZXRz"
    // which is the Base64 for the actual flag string stored as bytes
    byte[] a2 = new g().a();
    // Null-check helper again: ensure the decoded data is not null
    d.s.d.g.d(a2, "decoder.getData()");

    // Convert the decoder’s byte[] to a String using the app’s charset (effectively UTF‑8),
    // then compare it with the user input using Kotlin’s equals helper d.s.d.g.a(...)
    if (d.s.d.g.a(obj, new String(a2, d.w.c.f2418a))) {

        // If the user input matches the decoded flag string:

        // 1) Prepare an Intent to open the success screen activity
        Intent intent = new Intent(this, (Class<?>) FlagOneSuccess.class);

        // 2) Mark the corresponding flag as solved in the overview state
        new FlagsOverview().I(true);

        // 3) Persist a UI change (e.g., change the button color for this flag to “solved”)
        new j().b(this, "flagFourButtonColor", true);

        // 4) Navigate to the FlagOneSuccess activity
        startActivity(intent);
    }
}
```

Heading over to the `g.a` method, you’ll see a Base64 string being decoded, decoding this string gives us the value `4_overdone_omelets`.

```java
package b3nac.injuredandroid;

import android.util.Base64;

/* loaded from: classes.dex */
public class g {

    /* renamed from: a, reason: collision with root package name */
    private byte[] f1468a = Base64.decode("NF9vdmVyZG9uZV9vbWVsZXRz", 0);

    public byte[] a() {
        return this.f1468a;
    }
}
```

![image.png](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/raw/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20FOUR%20%E2%80%93%20(LOGIN%202)/FLAG%20FOUR%20%E2%80%93%20(LOGIN%202)/image%201.png)