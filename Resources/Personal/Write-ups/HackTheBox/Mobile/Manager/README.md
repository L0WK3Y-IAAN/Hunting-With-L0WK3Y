![banner](https://i.imgur.com/gp1Vr47.png)
![desc](https://i.imgur.com/q4MRikO.png)

# Code Review

Let’s start by taking a look at the application source code in [Jadx-GUI](https://github.com/skylot/jadx) to get an understanding of what the application is doing. Head over to the `AndroidManifest.xml` under the Resources tab. The **AndroidManifest.xml** is a **required configuration file** that serves as the central blueprint for every Android application. Think of it as the app's "birth certificate" that tells the Android system everything it needs to know about your app before it can run.

![image.png](https://github.com/L0WK3Y-IAAN/HackTheBox-Writeups/blob/main/Android/Manager/HackTheBox%20-%20Manager%20(Mobile)%20Walkthrough/image.png?raw=true)

There are a few focus points in the manifest to take note of, the first point being the minimum and target SDK Versions. These are the minimum and targeted Android versions the application was made to run on, anything above the target SDK version will work as well. For this walkthrough I am using Android 15.

For the second point of focus, we have 4 `activities`. Think of **activities** as the **individual screens** in your Android app - like different pages in a book. We have:

- Main
- Login
- Register
- Edit

### AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
...
    <uses-sdk
        android:minSdkVersion="21" 
        android:targetSdkVersion="31"/>
        <!--
        Min SDK Version = Android 5.0 (Lollipop)
        Targeted SDK Version = Android 12
        -->         

    <uses-permission android:name="android.permission.INTERNET"/>
...
        <activity
            android:name="com.example.manager.MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        <activity android:name="com.example.manager.LoginActivity"/>
        <activity android:name="com.example.manager.RegisterActivity"/>
        <activity android:name="com.example.manager.EditActivity"/>
...
</manifest>
```

## MainActivity Breakdown

```java
/* loaded from: classes.dex */
public class MainActivity extends AppCompatActivity {
    @Override // androidx.fragment.app.FragmentActivity, androidx.activity.ComponentActivity, androidx.core.app.ComponentActivity, android.app.Activity
    protected void onCreate(Bundle bundle) { //Entrypoint
        super.onCreate(bundle);
        setContentView(R.layout.activity_main);
        
        //Text inputs for HTB Challenge IP and Port
        final EditText editText = (EditText) findViewById(R.id.etIP);
        final EditText editText2 = (EditText) findViewById(R.id.etPort);
        
        
        //Button listener
        ((Button) findViewById(R.id.btnConnect)).setOnClickListener(new View.OnClickListener() { // from class: com.example.manager.MainActivity.1
            @Override // android.view.View.OnClickListener
            public void onClick(View view) {
                String str = "http://" + editText.getText().toString() + ":" + editText2.getText().toString() + "/";
                Intent intent = new Intent(MainActivity.this, (Class<?>) LoginActivity.class);
                intent.putExtra("url", str);
                MainActivity.this.startActivity(intent);
            }
        });
    }
}
```
![sidenote](https://i.imgur.com/Uf1uXy0.png)



- When the button (**`btnConnect`**) is clicked:
    1. **Reads input values** for IP and port.
    2. **Constructs a URL** in the form:
        
        **`http://<entered_ip>:<entered_port>/`**
        
    3. **Creates an Intent** to start **`LoginActivity`**, attaching the constructed URL as extra data.
    4. **Launches LoginActivity**.

After inputting the IP and port, the application redirects to the login screen, but since we have no credentials to work with we’ll need to register a user first.

## RegisterActivity Code Breakdown

This **RegisterActivity** Android code handles user registration by collecting username/password input and sending it to a server via HTTP POST request.

### Class Declaration & Variables

```java
public class RegisterActivity extends AppCompatActivity {
    EditText etUsername;  // Username input field
    EditText etPassword;  // Password input field
    String url = "";      // Base server URL

```

- Extends `AppCompatActivity` (makes it a screen/Activity).
- Three main variables to store UI elements and server URL.

### onCreate() Method - Screen Setup

```java
protected void onCreate(Bundle bundle) {
    super.onCreate(bundle);
    setContentView(R.layout.activity_register);  *// Load the UI layout*
    
    *// Connect Java variables to UI elements*
    this.etUsername = (EditText) findViewById(R.id.etUsername);
    this.etPassword = (EditText) findViewById(R.id.etPassword);
    
    *// Get server URL from previous screen*
    this.url = getIntent().getStringExtra("url");
    
    *// Set up register button click handler*
    ((Button) findViewById(R.id.btnRegister)).setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            try {
                RegisterActivity.this.register();  *// Call registration method*
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    });
}
```

## register() Method - The Core Registration Logic

### 1. HTTP Connection Setup

```java
String str = this.url + "register.php";  *// Build full URL*
HttpURLConnection httpURLConnection = (HttpURLConnection) new URL(str).openConnection();
httpURLConnection.setConnectTimeout(10000);  *// 10 second timeout*
httpURLConnection.setRequestMethod("POST");
httpURLConnection.setRequestProperty("User-Agent", "Mozilla/5.0");
```

### 2. Prepare Data to Send

```java
String str2 = "username=" + this.etUsername.getText().toString() + 
              "&password=" + this.etPassword.getText().toString();
```

Creates form data like: `username=john&password=mypass123`.

### 3. Send Data to Server

```java
httpURLConnection.setDoOutput(true);
dataOutputStream = new DataOutputStream(httpURLConnection.getOutputStream());
dataOutputStream.writeBytes(str2);  *// Send the username/password data*
dataOutputStream.flush();
dataOutputStream.close();
```

### 4. Handle Server Response

```java
BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream()));
*// Read response from server*
StringBuilder sb = new StringBuilder();
while (true) {
    String line = bufferedReader.readLine();
    if (line == null) break;
    sb.append(line);
}
```

### 5. Process Different Response Scenarios

```java
if (sb.toString().equals("Username already taken!")) {
    Toast.makeText(this, "Username already taken!", 1).show();
} else if (sb.toString().equals("Unable to register user!")) {
    Toast.makeText(this, "Unable to register user!", 1).show();
} else if (sb.toString().equals("An error occurred!")) {
    Toast.makeText(this, "An error occurred!", 1).show();
    *// Go back to login screen*
    Intent intent = new Intent(this, LoginActivity.class);
    intent.putExtra("url", this.url);
    startActivity(intent);
} else {
    *// Success! Registration worked*
    Toast.makeText(this, "User successfully created.", 1).show();
    *// Go to edit screen with user info*
    Intent intent2 = new Intent(this, EditActivity.class);
    intent2.putExtra("url", this.url);
    intent2.putExtra("info", sb.toString());  *// Pass user data*
    startActivity(intent2);
}
```

## User Flow

1. User enters username and password.
2. Clicks register button.
3. App sends data to `LAB_IP/register.php`.
4. Based on server response:
    - **Error**: Shows error message.
    - **Success**: Goes to EditActivity with user info.

---

## The Vulnerable Code

The `update` method contains a critical security flaw, it lacks authentication verification to confirm that the requesting user is authorized to modify the specified account. This results in an `IDOR` ([**Insecure Direct Object Reference**](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)) vulnerability, specifically a `BOLA` ([**Broken Object Level Authorization**)](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) issue. 

```java
public void update() throws IOException {
    String str = this.url + "manage.php";
    HttpURLConnection httpURLConnection = (HttpURLConnection) new URL(str).openConnection();
    httpURLConnection.setRequestMethod("POST");
    httpURLConnection.setRequestProperty("User-Agent", "Mozilla/5.0");
    httpURLConnection.setRequestProperty("Accept-Language", "en-US,en;q=0.5");
    
    // VULNERABLE CODE - Only sends username and password
    String str2 = "username=" + this.tvUsername.getText().toString() + "&password=" + this.etPassword.getText().toString();
    
    httpURLConnection.setDoOutput(true);
    DataOutputStream dataOutputStream = new DataOutputStream(httpURLConnection.getOutputStream());
    // ... rest of the method
}

```

---

# App Testing

Now that we have an understanding of the application, we can now start testing to validate our code review. Start by inputting the challenge IP and port then registering a user.

![](https://i.imgur.com/vpEi30z.png)

![image.png](https://res.cloudinary.com/dn8lr4uhb/image/upload/v1754041226/image_1_k7lsxk.png)

![image.png](https://res.cloudinary.com/dn8lr4uhb/image/upload/v1754041226/image_2_heerzs.png)

Now we’ve arrived at the vulnerable activity, the only input we can change is the password field. Let’s update the password and view the request in Burp Suite. 

![image.png](https://res.cloudinary.com/dn8lr4uhb/image/upload/v1754041226/image_3_twv9ux.png)

![image.png](https://res.cloudinary.com/dn8lr4uhb/image/upload/v1754041226/image_4_si3mmb.png)

Given our understanding of the vulnerability, we should be able to update the password of any registered user, but we need to figure out which users are already registered. We can achieve this by brute forcing the registration page with a user list. If a user is already registered, we should get the text `Username already taken!` just as we saw during our code review. After a few seconds, the `admin` user shows up as a taken username.

![image.png](https://res.cloudinary.com/dn8lr4uhb/image/upload/v1754041226/image_5_jec4t1.png)

Now, we can update the admin password by posting to the `/manage.php` endpoint and proceed to login to obtain the flag.

![image.png](https://res.cloudinary.com/dn8lr4uhb/image/upload/v1754041226/c67bfb89-6572-4a5b-b400-7a18e12877e3_afh2j6.png)

![htbimage.png](https://res.cloudinary.com/dn8lr4uhb/image/upload/v1754041226/htbimage_mdr4wx.png)



