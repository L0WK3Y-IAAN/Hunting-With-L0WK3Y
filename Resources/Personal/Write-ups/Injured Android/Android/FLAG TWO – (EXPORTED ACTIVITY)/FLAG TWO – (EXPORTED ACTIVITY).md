# FLAG TWO – (EXPORTED ACTIVITY)

![image.png](FLAG%20TWO%20%E2%80%93%20(EXPORTED%20ACTIVITY)/image.png)

Looking at the code for `FlagTwoActivity` I come across two strings being referenced `"Key words Activity and exported."` and `"Exported Activities can be accessed with adb or Drozer."`. This is a clear indicator of what needs to be done next, I need to find the exported activity that is in reference to the FlagTwo activity.

```java
    public /* synthetic */ void F(View view) {
        int i = this.w;
        if (i == 0) {
            Snackbar X = Snackbar.X(view, "Key words Activity and exported.", 0);
            X.Y("Action", null);
            X.N();
            this.w++;
            return;
        }
        if (i == 1) {
            Snackbar X2 = Snackbar.X(view, "Exported Activities can be accessed with adb or Drozer.", 0);
            X2.Y("Action", null);
            X2.N();
            this.w = 0;
        }
    }
    ...
```

My next course of action is to look for any references to “FlagTwo” anywhere in the code. Doing so reveals an activity called `“b25lActivity”`

![ZAP 2025-10-03 16.48.29.png](FLAG%20TWO%20%E2%80%93%20(EXPORTED%20ACTIVITY)/ZAP_2025-10-03_16.48.29.png)

```java
package b3nac.injuredandroid;

import android.os.Bundle;

/* loaded from: classes.dex */
public final class b25lActivity extends androidx.appcompat.app.c {
    @Override // androidx.appcompat.app.c, androidx.fragment.app.d, androidx.activity.ComponentActivity, androidx.core.app.e, android.app.Activity
    protected void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        setContentView(R.layout.activity_b25l); // This line displays the flag
        j.j.a(this);
        new FlagsOverview().M(true);
        new j().b(this, "flagTwoButtonColor", true);
    }
}
```

```java
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <TextView
        android:textSize="24sp"
        android:id="@+id/textView6"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:layout_marginBottom="8dp"
        android:text="S3c0nd_F1ag" // <--
        android:layout_marginStart="8dp"
        android:layout_marginEnd="8dp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"/>
</androidx.constraintlayout.widget.ConstraintLayout>
```

```json
adb shell am start -n b3nac.injuredandroid/.b25lActivity
```

![image.png](FLAG%20TWO%20%E2%80%93%20(EXPORTED%20ACTIVITY)/image%201.png)