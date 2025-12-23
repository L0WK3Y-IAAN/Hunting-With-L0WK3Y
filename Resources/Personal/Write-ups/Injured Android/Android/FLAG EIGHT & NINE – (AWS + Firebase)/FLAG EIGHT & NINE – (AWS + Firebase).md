# FLAG EIGHT & NINE – (AWS + Firebase)

### Eight

Flag eight references a Firebase Database, if you checked strings previously, there is a reference to a Firebase URL [`https://injuredandroid.firebaseio.com`](https://injuredandroid.firebaseio.com). In the `FlagEightLoginActivity`, there is a mention of an `/aws` node. If it is similar to the previous sqlite node in flag seven, then this should end in `.json` as well..

```jsx
    public FlagEightLoginActivity() {
        com.google.firebase.database.f fVarB = com.google.firebase.database.f.b();
        d.s.d.g.d(fVarB, "FirebaseDatabase.getInstance()");
        com.google.firebase.database.d dVarD = fVarB.d();
        d.s.d.g.d(dVarD, "FirebaseDatabase.getInstance().reference");
        this.x = dVarD;
        com.google.firebase.database.d dVarH = dVarD.h("/aws");
        d.s.d.g.d(dVarH, "database.child(\"/aws\")"); //aws node referenced.
        this.y = dVarH;
    }
```

![image.png](FLAG%20EIGHT%20&%20NINE%20%E2%80%93%20(AWS%20+%20Firebase)/image.png)

After heading to the url and appending “`/aws.json`” to the end I get the flag.

![image.png](FLAG%20EIGHT%20&%20NINE%20%E2%80%93%20(AWS%20+%20Firebase)/image%201.png)

---

### Nine

For flag nine, there is a Base64 encoded node `/flags` that can be appended to the end of the Firebase Database URL to get the flag.

```jsx
private final String x = "ZmxhZ3Mv";

...

public final void submitFlag(View view) {
        EditText editText = (EditText) findViewById(R.id.editText2);
        d.s.d.g.d(editText, "editText2");
        
        //Encode the flag in base64 as this line decodes the base64 back into plain text
        byte[] bArrDecode = Base64.decode(editText.getText().toString(), 0);
        d.s.d.g.d(bArrDecode, "decodedPost");
        Charset charset = StandardCharsets.UTF_8;
        d.s.d.g.d(charset, "StandardCharsets.UTF_8");
        this.B.b(new b(new String(bArrDecode, charset)));
    }
```

![image.png](FLAG%20EIGHT%20&%20NINE%20%E2%80%93%20(AWS%20+%20Firebase)/image%202.png)

![image.png](FLAG%20EIGHT%20&%20NINE%20%E2%80%93%20(AWS%20+%20Firebase)/image%203.png)