# FLAG THREE – (RESOURCES)

For FlagThree there is another string input comparison where the text given to `editText` is turned into a string and compared with the resource string `cmVzb3VyY2VzX3lv` to see if they match.

```java
public final void submitFlag(View view) {
        EditText editText = (EditText) findViewById(R.id.editText2);
        d.s.d.g.d(editText, "editText2");
        if (d.s.d.g.a(editText.getText().toString(), getString(R.string.cmVzb3VyY2VzX3lv))) //<--

{
            Intent intent = new Intent(this, (Class<?>) FlagOneSuccess.class);
            new FlagsOverview().L(true);
            new j().b(this, "flagThreeButtonColor", true);
            startActivity(intent);
        }
    }
```

If you head over to the `strings.xml` under `res/values` and look for the string variable `cmVzb3VyY2VzX3lv` you can find the flag there.

![image.png](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/raw/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20THREE%20%E2%80%93%20(RESOURCES)/FLAG%20THREE%20%E2%80%93%20(RESOURCES)/image.png)