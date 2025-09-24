'use strict';

// ========================================
// Enhanced Frida Crypto Detection Script
// Shows actual values and exact class locations
// ========================================

// Helper function to print clean stack trace with class focus
function printStackWithClasses() {
    var stack = Java.use("java.lang.Exception").$new().getStackTrace();
    console.log("    📍 Found in Classes:");
    for (var i = 1; i < Math.min(6, stack.length); i++) {
        var element = stack[i];
        var className = element.getClassName();
        var methodName = element.getMethodName();
        var fileName = element.getFileName();
        var lineNumber = element.getLineNumber();
        
        // Highlight app-specific classes (not Android framework)
        if (!className.startsWith('android.') && !className.startsWith('java.') && 
            !className.startsWith('javax.') && !className.startsWith('androidx.')) {
            console.log(`      🎯 ${className}.${methodName} (${fileName}:${lineNumber})`);
        } else {
            console.log(`         ${className}.${methodName} (${fileName}:${lineNumber})`);
        }
    }
}

// Enhanced detection logger with actual values
function logCryptoDetection(type, operation, actualValue, extraInfo) {
    console.log('\n╔═══════════════════════════════════════════════════════════╗');
    console.log('║                   🔍 CRYPTO DETECTED                     ║');
    console.log('╠═══════════════════════════════════════════════════════════╣');
    console.log(`║ Type: ${type.padEnd(50)} ║`);
    console.log(`║ Operation: ${operation.padEnd(43)} ║`);
    if (actualValue !== undefined && actualValue !== null) {
        var displayValue = actualValue.toString();
        if (displayValue.length > 45) {
            displayValue = displayValue.substring(0, 42) + "...";
        }
        console.log(`║ 🔑 Value: ${displayValue.padEnd(45)} ║`);
    }
    if (extraInfo) {
        console.log(`║ Info: ${extraInfo.padEnd(50)} ║`);
    }
    console.log('╚═══════════════════════════════════════════════════════════╝');
    printStackWithClasses();
    console.log('─'.repeat(60));
}

// Convert byte array to readable format
function bytesToReadable(bytes) {
    if (!bytes) return "null";
    
    // Try to convert to string first (if printable)
    var str = "";
    var isPrintable = true;
    for (var i = 0; i < Math.min(bytes.length, 50); i++) {
        var b = bytes[i] & 0xFF;
        if (b >= 32 && b <= 126) {
            str += String.fromCharCode(b);
        } else if (b === 0) {
            str += "\\0";
        } else {
            isPrintable = false;
            break;
        }
    }
    
    if (isPrintable && str.length > 0) {
        return `"${str}"${bytes.length > 50 ? '...' : ''} (${bytes.length} bytes)`;
    }
    
    // Otherwise show as hex
    var hex = "";
    for (var i = 0; i < Math.min(bytes.length, 16); i++) {
        hex += ("0" + (bytes[i] & 0xFF).toString(16)).slice(-2);
    }
    return `[${hex}${bytes.length > 16 ? '...' : ''}] (${bytes.length} bytes)`;
}

Java.perform(function () {
    console.log('\n🔍 Enhanced Crypto Detection Started');
    console.log('═'.repeat(60));

    // ========================================
    // BASE64 DETECTION WITH VALUES
    // ========================================
    try {
        var Base64 = Java.use('android.util.Base64');
        
        // Base64 Decode - Show the actual encoded string
        Base64.decode.overload('java.lang.String', 'int').implementation = function(str, flags) {
            logCryptoDetection(
                'Base64', 
                'Decode', 
                str, 
                `Flags: ${flags}, Length: ${str.length}`
            );
            
            var result = this.decode(str, flags);
            console.log(`    ✅ Decoded Result: ${bytesToReadable(result)}\n`);
            return result;
        };

        // Base64 Encode - Show the input bytes
        Base64.encodeToString.overload('[B', 'int').implementation = function(bytes, flags) {
            logCryptoDetection(
                'Base64', 
                'Encode', 
                bytesToReadable(bytes), 
                `Flags: ${flags}`
            );
            
            var result = this.encodeToString(bytes, flags);
            console.log(`    ✅ Encoded Result: "${result}"\n`);
            return result;
        };

        console.log('✅ Base64 hooks installed');
    } catch (e) {
        console.log('❌ Base64 hooks failed: ' + e.message);
    }

    // ========================================
    // AES/CIPHER DETECTION WITH VALUES
    // ========================================
    try {
        var Cipher = Java.use('javax.crypto.Cipher');
        
        // Cipher.getInstance()
        Cipher.getInstance.overload('java.lang.String').implementation = function(transformation) {
            logCryptoDetection(
                'Cipher', 
                'GetInstance', 
                transformation, 
                'Requesting crypto algorithm'
            );
            return this.getInstance(transformation);
        };

        // FIXED: Use AlgorithmParameterSpec (parent interface)
        Cipher.init.overload('int', 'java.security.Key', 'java.security.spec.AlgorithmParameterSpec').implementation = function(opmode, key, params) {
            var modeStr = (opmode === 1) ? 'ENCRYPT' : (opmode === 2) ? 'DECRYPT' : `MODE_${opmode}`;
            var keyBytes = key.getEncoded();
            
            // Get IV if it's IvParameterSpec
            var ivInfo = "Unknown params";
            try {
                var IvParameterSpec = Java.use('javax.crypto.spec.IvParameterSpec');
                if (Java.cast(params, IvParameterSpec)) {
                    var iv = Java.cast(params, IvParameterSpec).getIV();
                    ivInfo = `IV: ${bytesToReadable(iv)}`;
                }
            } catch (e) {
                ivInfo = "Non-IV params: " + params.toString();
            }
            
            logCryptoDetection(
                'AES Cipher', 
                `Init (${modeStr})`, 
                `Key: ${bytesToReadable(keyBytes)}`, 
                ivInfo
            );
            return this.init(opmode, key, params);
        };

        // Basic init without params
        Cipher.init.overload('int', 'java.security.Key').implementation = function(opmode, key) {
            var modeStr = (opmode === 1) ? 'ENCRYPT' : (opmode === 2) ? 'DECRYPT' : `MODE_${opmode}`;
            var keyBytes = key.getEncoded();
            
            logCryptoDetection(
                'Cipher', 
                `Init (${modeStr})`, 
                `Key: ${bytesToReadable(keyBytes)}`, 
                'No IV/params'
            );
            return this.init(opmode, key);
        };

        // Cipher.doFinal() - Show input and output
        Cipher.doFinal.overload('[B').implementation = function(data) {
            logCryptoDetection(
                'Cipher', 
                'doFinal (Process)', 
                `Input: ${bytesToReadable(data)}`, 
                `Processing ${data.length} bytes`
            );
            
            var result = this.doFinal(data);
            console.log(`    ✅ Output: ${bytesToReadable(result)}\n`);
            return result;
        };

        console.log('✅ Cipher hooks installed');
    } catch (e) {
        console.log('❌ Cipher hooks failed: ' + e.message);
    }

    // ========================================
    // SECRET KEY CREATION WITH ACTUAL KEYS
    // ========================================
    try {
        var SecretKeySpec = Java.use('javax.crypto.spec.SecretKeySpec');
        
        SecretKeySpec.$init.overload('[B', 'java.lang.String').implementation = function(keyBytes, algorithm) {
            logCryptoDetection(
                'SecretKey', 
                'Creation', 
                `${algorithm}: ${bytesToReadable(keyBytes)}`, 
                `Algorithm: ${algorithm}`
            );
            return this.$init(keyBytes, algorithm);
        };

        console.log('✅ SecretKeySpec hooks installed');
    } catch (e) {
        console.log('❌ SecretKeySpec hooks failed: ' + e.message);
    }

    // ========================================
    // IV CREATION WITH ACTUAL VALUES
    // ========================================
    try {
        var IvParameterSpec = Java.use('javax.crypto.spec.IvParameterSpec');
        
        IvParameterSpec.$init.overload('[B').implementation = function(iv) {
            logCryptoDetection(
                'IV', 
                'Creation', 
                bytesToReadable(iv), 
                `IV length: ${iv.length} bytes`
            );
            return this.$init(iv);
        };

        console.log('✅ IvParameterSpec hooks installed');
    } catch (e) {
        console.log('❌ IvParameterSpec hooks failed: ' + e.message);
    }

    // ========================================
    // KOTLIN STRING ENCODING (Your app uses this!)
    // ========================================
    try {
        var StringsKt = Java.use('kotlin.text.StringsKt');
        
        // This will catch your "uylcndhysjejgido" and "akzjgukaksburjtk" strings!
        StringsKt.encodeToByteArray.overload('java.lang.String').implementation = function(str) {
            logCryptoDetection(
                'Kotlin String', 
                'encodeToByteArray', 
                `"${str}"`, 
                `Converting string to bytes (likely key/IV)`
            );
            var result = this.encodeToByteArray(str);
            console.log(`    ✅ Byte Result: ${bytesToReadable(result)}\n`);
            return result;
        };

        // This will catch the decrypted result
        StringsKt.decodeToString.overload('[B').implementation = function(bytes) {
            logCryptoDetection(
                'Kotlin String', 
                'decodeToString', 
                bytesToReadable(bytes), 
                'Converting bytes back to string'
            );
            var result = this.decodeToString(bytes);
            console.log(`    ✅ String Result: "${result}"\n`);
            return result;
        };

        console.log('✅ Kotlin String hooks installed');
    } catch (e) {
        console.log('⚠️  Kotlin String hooks not available');
    }

    console.log('═'.repeat(60));
    console.log('🚀 All hooks ready! Values will be shown when detected...\n');
});