# FLAG SIX – (LOGIN 3)

This flag follows the same DES decryption process as flag five, all we have to do is keep the same Cyberchef recipe and replace the input value with the new Base64 input.

```java
public final void submitFlag(View view) {
        EditText editText = (EditText) findViewById(R.id.editText3);
        d.s.d.g.d(editText, "editText3");
        if (d.s.d.g.a(editText.getText().toString(), k.a("k3FElEG9lnoWbOateGhj5pX6QsXRNJKh///8Jxi8KXW7iDpk2xRxhQ=="))) // This line calls class and method k.a which uses the same DES decryption as FlagFive.
        
        
         {
            Intent intent = new Intent(this, (Class<?>) FlagOneSuccess.class);
            FlagsOverview.G = true;
            new j().b(this, "flagSixButtonColor", true);
            startActivity(intent);
        }
    }
```

![image.png](FLAG%20SIX%20%E2%80%93%20(LOGIN%203)/image.png)

```
{This_Isn't_Where_I_Parked_My_Car}
```