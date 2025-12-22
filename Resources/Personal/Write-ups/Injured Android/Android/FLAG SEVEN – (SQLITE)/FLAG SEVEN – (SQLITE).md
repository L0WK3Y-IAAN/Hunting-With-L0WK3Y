# FLAG SEVEN – (SQLITE)

For FlagSeven an SQL database has data written to it consisting of Base64 subtitle, and an encoded string from the class and method `h.c`.

```jsx
public class h {
...

    /* renamed from: c, reason: collision with root package name */
    private static String f1471c = "9EEADi^^:?;FC652?5C@:5]7:C632D6:@]4@>^DB=:E6];D@?";
...

    static String c() {
        return f1471c;
    }
}
```

![image.png](FLAG%20SEVEN%20%E2%80%93%20(SQLITE)/image.png)

| **id** | **title** | **subtitle** |
| --- | --- | --- |
| 1 | The flag hash! | 2ab96390c7dbe3443de74d0c9b0b1767 |
| 2 | The flag is also a password! | 9EEADi^^:?;FC652?5C@:5]7:C632D6:@]4@>^DB=:E6];D@? |

We are also given a clue in the source, that doesn’t actually get displayed when clicking on the hint button in the app itself. With the current information i have now, I assume that the flag hash is a MD5 and the flag password text is ROT encoded text. We can see that ROT47 is used to encode the URL. (Use [https://dencode.com/en/cipher](https://dencode.com/en/cipher))

![image.png](FLAG%20SEVEN%20%E2%80%93%20(SQLITE)/2fd1ad06-658d-4e7c-8bad-5d529ae4bcef.png)

![Decoded ROT47 URL](FLAG%20SEVEN%20%E2%80%93%20(SQLITE)/image%201.png)

Decoded ROT47 URL

![image.png](FLAG%20SEVEN%20%E2%80%93%20(SQLITE)/bc478b8c-1c37-44b8-a0c5-98be591d694f.png)

I also cracked the MD5 hash and I now have both the password and flag needed to login.

![MD5 Hash cracked](FLAG%20SEVEN%20%E2%80%93%20(SQLITE)/image%202.png)

MD5 Hash cracked