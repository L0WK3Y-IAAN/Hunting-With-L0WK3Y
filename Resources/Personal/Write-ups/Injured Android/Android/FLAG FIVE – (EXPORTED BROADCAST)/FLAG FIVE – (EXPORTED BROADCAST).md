# FLAG FIVE – (EXPORTED BROADCAST)

Since there isn’t much to show as far as UI in the actual application for the challenge, I’ll start with breaking down the `FlagFiveActivity`.

### Broadcast Receiver Registration

```java
// Instance variable: FlagFiveReceiver object that will handle the broadcast
private FlagFiveReceiver x = new FlagFiveReceiver();

// Method F: Sends a broadcast with the custom intent action
// This will trigger any registered receiver listening for this action
public void F() {
    sendBroadcast(new Intent("com.b3nac.injuredandroid.intent.action.CUSTOM_INTENT"));
}

// onCreate method snippet - sets up the receiver and button
// Find and reference the button with ID button9 from the layout
Button button = (Button) findViewById(R.id.button9);

// Register the BroadcastReceiver (this.x) with LocalBroadcastManager
// to listen for the custom intent action "com.b3nac.injuredandroid.intent.action.CUSTOM_INTENT"
// a.m.a.a.b(this) returns the LocalBroadcastManager instance
// .c() is the obfuscated registerReceiver method that maps the receiver to the intent filter
a.m.a.a.b(this).c(this.x, new IntentFilter("com.b3nac.injuredandroid.intent.action.CUSTOM_INTENT"));

// Set up a click listener for button9
// When the button is clicked, it will call the H() method which triggers F()
button.setOnClickListener(new View.OnClickListener() { 

    // from class: b3nac.injuredandroid.b
    @Override // android.view.View.OnClickListener
    public final void onClick(View view) {
    
        // Call the H() method which triggers F() to send the custom broadcast
        // This broadcast will be received by this.x (FlagFiveReceiver) since it's registered
        FlagFiveActivity.this.H(view);
    }
});

```

### FlagFiveReceiver

```java
package b3nac.injuredandroid;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.widget.Toast;

/* loaded from: classes.dex */
// BroadcastReceiver that handles the custom intent action from FlagFiveActivity
// Uses a state counter to progress through multiple stages before revealing the flag
public final class FlagFiveReceiver extends BroadcastReceiver {

    /* renamed from: a, reason: collision with root package name */
    // Static counter to track how many times the broadcast has been received
    // Determines which stage/message to show (0=debug info, 1=hint, 2=flag)
    private static int f1454a;

    @Override // android.content.BroadcastReceiver
    // Called when the receiver gets the broadcast with action "com.b3nac.injuredandroid.intent.action.CUSTOM_INTENT"
    public void onReceive(Context context, Intent intent) {
        String str;
        int i;
        String e;
        String e2;
        ...
        
        // Get current stage from the static counter
        int i2 = f1454a;
        
        // Stage 0: First broadcast - log debug information about the intent
        if (i2 == 0) {
        
            StringBuilder sb = new StringBuilder();
            // Build debug string showing the action and URI of the received intent
            e = d.w.h.e("\n    Action: " + intent.getAction() + "\n\n    ");
            sb.append(e);
            e2 = d.w.h.e("\n    URI: " + intent.toUri(1) + "\n\n    ");
            sb.append(e2);
            str = sb.toString();
            d.s.d.g.d(str, "sb.toString()");
            
            // Log the intent details for debugging/reverse engineering
            Log.d("DUDE!:", str);
            
        } else {
            // Default message for intermediate stages
            str = "Keep trying!";
            
            // Stage 1: Second broadcast - show "Keep trying!" hint
            if (i2 != 1) {
            
                // Stage 2: Third broadcast - decode and reveal the flag!
                if (i2 != 2) {
                
                    // Stage 3+: Beyond expected stages, just show hint
                    Toast.makeText(context, "Keep trying!", 1).show();
                    return;
                }
                // SUCCESS: Decode the base64 flag value and display it
                String str2 = "You are a winner " + k.a("Zkdlt0WwtLQ=");
                
                // Mark flag as captured in the app's overview/progress tracking
                new FlagsOverview().H(true);
                
                // Store completion state in shared preferences
                new j().b(context, "flagFiveButtonColor", true);
                
                // Show the victory message with the decoded flag
                Toast.makeText(context, str2, 1).show();
                
                // Reset counter back to 0 for next attempt
                i = 0;
                f1454a = i;
            }
        }
        
        // Display the current stage message as a Toast
        Toast.makeText(context, str, 1).show();
        
        // Increment the counter for the next broadcast reception
        i = f1454a + 1;
        f1454a = i;
    }
}

```

![Here is what is being shown in logcat.](FLAG%20FIVE%20%E2%80%93%20(EXPORTED%20BROADCAST)/image.png)

Here is what is being shown in logcat.

### Flag Decryption

```java
public class k {

    // DES encryption keys retrieved from class h (base64 encoded key bytes)
    // f1472a = "Captur3Th1s" (used by method a)
    private static final byte[] f1472a = h.b();
...
    // Decrypt base64 string using DES with key from f1472a
    public static String a(String str) {
        if (c(str)) {
            try {
            
                // Generate DES secret key from the hardcoded key bytes
                SecretKey generateSecret = SecretKeyFactory.getInstance("DES").generateSecret(new DESKeySpec(f1472a));
                
                // Decode the base64 input string to bytes
                byte[] decode = Base64.decode(str, 0);
                
                // Initialize cipher in DECRYPT mode (2) with the secret key
                Cipher cipher = Cipher.getInstance("DES");
                cipher.init(2, generateSecret);
                
                // Decrypt and return as plaintext string
                return new String(cipher.doFinal(decode));
            } catch (InvalidKeyException | NoSuchAlgorithmException | InvalidKeySpecException | BadPaddingException | IllegalBlockSizeException | NoSuchPaddingException e) {
                e.printStackTrace();
            }
        } else {
            System.out.println("Not a string!");
        }
        return str;
    }
```

```java
public class h {

    // Base64 encoded DES keys used for decryption
    // Decodes to: "Captur3Th1s"
    private static byte[] f1469a = Base64.decode("Q2FwdHVyM1RoMXM=", 0);
    ...
    
        // Returns the first DES key "Captur3Th1s"
    static byte[] b() {
        return f1469a;
    }
```

### Cyberchef Decryption

![Remove the last 3 bytes for proper key size](FLAG%20FIVE%20%E2%80%93%20(EXPORTED%20BROADCAST)/image%201.png)

Remove the last 3 bytes for proper key size

![Change key from `Q2FwdHVyM1RoMXM=` to `Q2FwdHVyM1R=`.](FLAG%20FIVE%20%E2%80%93%20(EXPORTED%20BROADCAST)/image%202.png)

Change key from `Q2FwdHVyM1RoMXM=` to `Q2FwdHVyM1R=`.

![Final toast message with flag displayed ](FLAG%20FIVE%20%E2%80%93%20(EXPORTED%20BROADCAST)/image%203.png)

Final toast message with flag displayed