# FLAG FOUR – (LOGIN 2)

In FlagFour I am presented with another login prompt.

![image.png](FLAG%20FOUR%20%E2%80%93%20(LOGIN%202)/image.png)

This time I see the string “`decoder.getData()`” which tells me that there is some form of decoding going on.  The line “`byte[] a2 = new g().a();`” creates a new byte array with the returned data from the class and method `g.a`.

```java
public final void submitFlag(View view) {
        EditText editText = (EditText) findViewById(R.id.editText2);
        d.s.d.g.d(editText, "editText2");
        String obj = editText.getText().toString();
        byte[] a2 = new g().a();
        d.s.d.g.d(a2, "decoder.getData()");
        if (d.s.d.g.a(obj, new String(a2, d.w.c.f2418a))) {
            Intent intent = new Intent(this, (Class<?>) FlagOneSuccess.class);
            new FlagsOverview().I(true);
            new j().b(this, "flagFourButtonColor", true);
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

![image.png](FLAG%20FOUR%20%E2%80%93%20(LOGIN%202)/image%201.png)