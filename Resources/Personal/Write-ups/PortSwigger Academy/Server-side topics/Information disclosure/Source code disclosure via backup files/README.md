# Source code disclosure via backup files

<aside>
❓

This lab leaks its source code via backup files in a hidden directory. To solve the lab, identify and submit the database password, which is hard-coded in the leaked source code.

</aside>

This lab demonstrates a **source code disclosure vulnerability** caused by publicly accessible backup files in a `/backup` directory. Using tools like **Dirbuster** or **Gobuster**, we identified the `/backup` directory, which contains a backup file named `ProductTemplate.java.bak`.

Upon downloading and inspecting the file, we discovered sensitive hardcoded credentials within the Java source code, specifically a **database password** (`xlf0wurkoxlq7zmu55auymt1g2gvgvr4`). This password allows an attacker to directly connect to the database using the PostgreSQL driver and access the underlying data.

![image.png](Source%20code%20disclosure%20via%20backup%20files/1.png)

```java
package data.productcatalog;

import common.db.JdbcConnectionBuilder;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class ProductTemplate implements Serializable
{
    static final long serialVersionUID = 1L;

    private final String id;
    private transient Product product;

    public ProductTemplate(String id)
    {
        this.id = id;
    }

    private void readObject(ObjectInputStream inputStream) throws IOException, ClassNotFoundException
    {
        inputStream.defaultReadObject();

        ConnectionBuilder connectionBuilder = ConnectionBuilder.from(
                "org.postgresql.Driver",
                "postgresql",
                "localhost",
                5432,
                "postgres",
                "postgres",
                "xlf0wurkoxlq7zmu55auymt1g2gvgvr4"
        ).withAutoCommit();
        try
        {
            Connection connect = connectionBuilder.connect(30);
            String sql = String.format("SELECT * FROM products WHERE id = '%s' LIMIT 1", id);
            Statement statement = connect.createStatement();
            ResultSet resultSet = statement.executeQuery(sql);
            if (!resultSet.next())
            {
                return;
            }
            product = Product.from(resultSet);
        }
        catch (SQLException e)
        {
            throw new IOException(e);
        }
    }

    public String getId()
    {
        return id;
    }

    public Product getProduct()
    {
        return product;
    }
}
```

---

### **Why It’s Vulnerable**

1. **Exposed Backup Files**
    
    The `/backup` directory is publicly accessible and unprotected. This is a common misconfiguration, where developers or administrators unintentionally leave backup files, archives, or test data in a location accessible to anyone with knowledge of the directory structure.
    
    - File extensions like `.bak`, `.old`, `.tmp`, or `.zip` are often left behind during testing or development but are not cleaned up before deploying to production.
    - These files may contain sensitive information, such as source code, API keys, database credentials, or even hardcoded secrets.
2. **Hardcoded Credentials in Source Code**
    
    In the `ProductTemplate.java.bak` file, we find the database credentials hardcoded:
    
    ```java
    "xlf0wurkoxlq7zmu55auymt1g2gvgvr4"
    ```
    
    This is a serious security issue:
    
    - Anyone with access to the file can retrieve these credentials and connect to the database.
    - Hardcoding secrets in source code is an insecure practice because it increases the likelihood of accidental exposure.
3. **Directory Indexing Enabled**
    
    The `/backup` directory is not only accessible but also has directory indexing enabled, as evidenced by the HTML response. This allows attackers to easily enumerate and retrieve any files within the directory.
    
4. **Lack of Access Controls**
    
    No authentication or authorization is required to access the `/backup` directory or the sensitive files it contains. This makes it trivial for an attacker to exploit the vulnerability.
    ---
<div class="banner-container">
        <div class="left-panel">
            <div class="card">
                <h2>Let's Connect!</h2>
                <div class="social-links">
                    <a href="https://github.com/L0WK3Y-IAAN" target="_blank">
                        <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
                    </a>
                    <a href="https://www.linkedin.com/in/iaansec/" target="_blank">
                        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
                    </a>
                </div>
            </div>
        </div>
    </div>
