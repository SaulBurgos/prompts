# MCP Toolbox Setup Guide for AlloyDB in Cursor IDE

## Overview

This guide provides step-by-step instructions for configuring Google's MCP Toolbox to connect Cursor IDE with AlloyDB PostgreSQL databases using the Model Context Protocol (MCP). This setup eliminates the need for manual SSL certificate management and provides seamless AI-powered database interactions.

## What is MCP Toolbox?

MCP Toolbox for Databases is an open-source server that enables Large Language Model (LLM) applications to interact with databases through the Model Context Protocol. It acts as middleware between Cursor IDE and database systems, providing:

- **Automatic SSL/TLS Certificate Management** - No need to manually download or configure server certificates
- **Connection Pooling** - Efficient database connection management
- **Declarative Tool Definitions** - Predefined database operations
- **Authentication & Authorization** - Integrated Google Cloud IAM authentication
- **Observability** - Built-in telemetry and monitoring

## Prerequisites

Before starting, ensure you have the following:

### 1. Software Requirements
- **Cursor IDE** installed and running
- **Homebrew** package manager (macOS/Linux)
- **Google Cloud SDK (`gcloud`)** installed and configured

### 2. Google Cloud Resources
You need access to the following AlloyDB information:
- Project ID
- Region (e.g., `us-east4`)
- Cluster name
- Instance name
- Database name
- Database username
- Database password

### 3. Google Cloud Permissions
Your Google Cloud account must have:
- `alloydb.instances.get` permission
- `alloydb.instances.connect` permission
- Access to the target AlloyDB cluster

## Installation Steps

### Step 1: Install MCP Toolbox via Homebrew

```bash
brew install toolbox
```

**Verify installation:**
```bash
toolbox --version
```

**Find installation path:**
```bash
which toolbox
```

Expected output: `/opt/homebrew/bin/toolbox` or `/usr/local/bin/toolbox`

### Step 2: Authenticate with Google Cloud

The toolbox requires Application Default Credentials (ADC) to authenticate with AlloyDB.

```bash
gcloud auth application-default login
```

This command will:
1. Open your browser for authentication
2. Save credentials to `~/.config/gcloud/application_default_credentials.json`
3. Enable the toolbox to authenticate with Google Cloud services

**Verify authentication:**
```bash
gcloud auth application-default print-access-token > /dev/null 2>&1 && echo "✅ Authentication successful" || echo "❌ Authentication failed"
```

### Step 3: Gather AlloyDB Connection Information

Collect the following information from your Google Cloud Console or using `gcloud` commands:

**List AlloyDB instances:**
```bash
gcloud alloydb instances list \
  --cluster=<CLUSTER_NAME> \
  --region=<REGION> \
  --project=<PROJECT_ID> \
  --format="table(name,ipAddress,instanceType)"
```

**Get cluster details:**
```bash
gcloud alloydb clusters describe <CLUSTER_NAME> \
  --region=<REGION> \
  --project=<PROJECT_ID> \
  --format="value(databaseVersion,network)"
```

### Step 4: Configure Cursor MCP Settings

**Location of MCP configuration file:**
```
~/.cursor/mcp.json
```

**Add the following configuration to `mcp.json`:**

```json
{
  "mcpServers": {
    "mcp-alloydb-production": {
      "description": "AlloyDB PostgreSQL Production Database",
      "command": "/opt/homebrew/bin/toolbox",
      "args": ["--prebuilt", "alloydb-postgres", "--stdio"],
      "env": {
        "ALLOYDB_POSTGRES_PROJECT": "<PROJECT_ID>",
        "ALLOYDB_POSTGRES_REGION": "<REGION>",
        "ALLOYDB_POSTGRES_CLUSTER": "<CLUSTER_NAME>",
        "ALLOYDB_POSTGRES_INSTANCE": "<INSTANCE_NAME>",
        "ALLOYDB_POSTGRES_DATABASE": "<DATABASE_NAME>",
        "ALLOYDB_POSTGRES_USER": "<USERNAME>",
        "ALLOYDB_POSTGRES_PASSWORD": "<PASSWORD>"
      }
    }
  }
}
```

**Configuration Parameters:**

| Parameter | Description | Example |
|-----------|-------------|---------|
| `command` | Full path to toolbox binary | `/opt/homebrew/bin/toolbox` |
| `args` | Command arguments for toolbox | `["--prebuilt", "alloydb-postgres", "--stdio"]` |
| `ALLOYDB_POSTGRES_PROJECT` | Google Cloud Project ID | `production-468720` |
| `ALLOYDB_POSTGRES_REGION` | AlloyDB region | `us-east4` |
| `ALLOYDB_POSTGRES_CLUSTER` | AlloyDB cluster name | `my-cluster` |
| `ALLOYDB_POSTGRES_INSTANCE` | AlloyDB instance name | `my-cluster-primary` |
| `ALLOYDB_POSTGRES_DATABASE` | Target database name | `production` |
| `ALLOYDB_POSTGRES_USER` | Database username | `app_user` |
| `ALLOYDB_POSTGRES_PASSWORD` | Database password | `<secure_password>` |

**Important Notes:**
- Replace `<TOOLBOX_PATH>` with the actual path from `which toolbox`
- Replace all placeholder values (e.g., `<PROJECT_ID>`) with your actual values
- Keep credentials secure - do not commit this file to version control
- The server name (`mcp-alloydb-production`) can be customized to your preference

### Step 4.1: Understanding Access Modes (Read-Only vs Read-Write)

The toolbox provides three prebuilt AlloyDB configurations with different access levels. **Choose the appropriate one based on your security and operational requirements.**

#### Available Prebuilt Configurations

| Configuration | Access Level | Use Case | Available Operations |
|---------------|-------------|----------|---------------------|
| `alloydb-postgres` | **Full Read/Write** | Development, admin tasks, data management | SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP |
| `alloydb-postgres-observability` | **Read-Only** | Monitoring, reporting, analytics | SELECT only (queries and views) |
| `alloydb-postgres-admin` | **Full Admin** | Database administration, maintenance | All operations including VACUUM, REINDEX, pg_stat queries |

#### Default Configuration (Full Read-Write Access)

The configuration shown in Step 4 uses `alloydb-postgres`, which provides **full read-write access**:

```json
"args": ["--prebuilt", "alloydb-postgres", "--stdio"]
```

This means you can:
- ✅ Read data (`SELECT` queries)
- ✅ Insert data (`INSERT` statements)
- ✅ Update data (`UPDATE` statements)
- ✅ Delete data (`DELETE` statements)
- ✅ Execute DDL operations (`CREATE TABLE`, `ALTER TABLE`, etc.)

**Important:** The actual permissions are ultimately controlled by what privileges the database user (`ALLOYDB_POSTGRES_USER`) has been granted in AlloyDB.

#### Read-Only Configuration (Recommended for Production Monitoring)

For safer production access where you only need to query data, use the observability configuration:

```json
{
  "mcpServers": {
    "mcp-alloydb-production-readonly": {
      "description": "AlloyDB PostgreSQL Production Database (Read-Only)",
      "command": "/opt/homebrew/bin/toolbox",
      "args": ["--prebuilt", "alloydb-postgres-observability", "--stdio"],
      "env": {
        "ALLOYDB_POSTGRES_PROJECT": "<PROJECT_ID>",
        "ALLOYDB_POSTGRES_REGION": "<REGION>",
        "ALLOYDB_POSTGRES_CLUSTER": "<CLUSTER_NAME>",
        "ALLOYDB_POSTGRES_INSTANCE": "<INSTANCE_NAME>",
        "ALLOYDB_POSTGRES_DATABASE": "<DATABASE_NAME>",
        "ALLOYDB_POSTGRES_USER": "<USERNAME>",
        "ALLOYDB_POSTGRES_PASSWORD": "<PASSWORD>"
      }
    }
  }
}
```

This configuration:
- ✅ Allows `SELECT` queries
- ✅ Provides monitoring and observability tools
- ❌ Blocks `INSERT`, `UPDATE`, `DELETE`, and DDL operations
- 🔒 Safer for production environments where accidental data modification is a concern

#### Admin Configuration (For Database Maintenance)

For administrative tasks like vacuuming, reindexing, or analyzing database performance:

```json
"args": ["--prebuilt", "alloydb-postgres-admin", "--stdio"]
```

This provides administrative-level tools including:
- Database maintenance commands
- Performance analysis tools
- System catalog queries
- Statistics and monitoring functions

#### Choosing the Right Configuration

**Recommendations:**

| Scenario | Recommended Configuration | Rationale |
|----------|--------------------------|-----------|
| Production queries & reporting | `alloydb-postgres-observability` | Read-only access prevents accidental data changes |
| Development & testing | `alloydb-postgres` | Full access for development workflows |
| Data migrations & ETL | `alloydb-postgres` | Needs write permissions for data operations |
| Database administration | `alloydb-postgres-admin` | Requires admin-level tools |
| AI-assisted query writing | `alloydb-postgres-observability` | Safe exploration of production data |

**Security Best Practice:** For production databases, consider setting up multiple MCP servers:
- One read-only server for everyday queries and AI assistance
- One read-write server for authorized data operations (separate approval flow)

#### Switching Between Configurations

To change access modes:

1. Update the `args` field in your `mcp.json`
2. Restart Cursor IDE
3. Verify the new configuration is active

Example of having both read-only and read-write access:

```json
{
  "mcpServers": {
    "mcp-alloydb-prod-readonly": {
      "description": "Production Database (Read-Only)",
      "command": "/opt/homebrew/bin/toolbox",
      "args": ["--prebuilt", "alloydb-postgres-observability", "--stdio"],
      "env": { /* production config */ }
    },
    "mcp-alloydb-prod-admin": {
      "description": "Production Database (Admin - Use with Caution)",
      "command": "/opt/homebrew/bin/toolbox",
      "args": ["--prebuilt", "alloydb-postgres", "--stdio"],
      "env": { /* production config */ }
    }
  }
}
```

This allows you to choose the appropriate access level for each task.

### Step 5: Restart Cursor IDE

After updating the `mcp.json` file:

1. Save the file
2. Completely close Cursor IDE
3. Reopen Cursor IDE

Cursor will automatically:
- Read the updated `mcp.json` configuration
- Start the toolbox server in STDIO mode
- Establish connection to AlloyDB

## Verification and Testing

### Test Connection in Cursor

Once Cursor is restarted, you can test the connection by asking the AI assistant:

**Example queries:**
- "List all tables in the database"
- "Show me the schema for the users table"
- "How many records are in the customers table?"
- "What is the structure of the orders table?"

### Manual Testing (Optional)

You can also test the toolbox connection manually:

```bash
# Test toolbox with prebuilt configuration
toolbox --prebuilt alloydb-postgres --stdio
```

Press `Ctrl+C` to exit the test.

## How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────┐
│  Cursor IDE                                 │
│  └─ Reads ~/.cursor/mcp.json               │
│     └─ Auto-starts: toolbox                │
│        --prebuilt alloydb-postgres --stdio  │
│        └─ Passes environment variables      │
└─────────────────────────────────────────────┘
              ↓
         STDIO (JSON-RPC)
              ↓
┌─────────────────────────────────────────────┐
│  MCP Toolbox Server                         │
│  └─ Manages SSL/TLS certificates           │
│  └─ Connection pooling                      │
│  └─ Authenticates via Google Cloud IAM     │
└─────────────────────────────────────────────┘
              ↓
         Secure SSL/TLS
              ↓
┌─────────────────────────────────────────────┐
│  AlloyDB PostgreSQL                         │
│  └─ Verifies server certificate            │
│  └─ Establishes encrypted connection       │
└─────────────────────────────────────────────┘
```

### Why No Certificate Download?

Unlike traditional database connections that require manual SSL certificate downloads, MCP Toolbox:

1. **Automatically retrieves** the AlloyDB server certificate using Google Cloud APIs
2. **Manages certificate lifecycle** including renewal and validation
3. **Verifies server identity** to prevent man-in-the-middle attacks
4. **Establishes encrypted connections** with `verify-ca` or `verify-full` SSL mode

This is a **security best practice** - you get both encryption AND server identity verification without manual certificate management.

## Troubleshooting

### Issue: "Authentication failed" or "Permission denied"

**Symptoms:**
- Cannot connect to AlloyDB
- Error messages about authentication

**Solutions:**
1. Re-run Google Cloud authentication:
   ```bash
   gcloud auth application-default login
   ```

2. Verify your Google Cloud account has AlloyDB permissions:
   ```bash
   gcloud projects get-iam-policy <PROJECT_ID> \
     --flatten="bindings[].members" \
     --filter="bindings.members:<YOUR_EMAIL>"
   ```

3. Check that the database user has proper permissions in AlloyDB

### Issue: "Connection refused" or "Cannot connect to database"

**Symptoms:**
- Toolbox cannot reach AlloyDB instance
- Network timeout errors

**Solutions:**
1. Verify AlloyDB instance is running:
   ```bash
   gcloud alloydb instances describe <INSTANCE_NAME> \
     --cluster=<CLUSTER_NAME> \
     --region=<REGION> \
     --project=<PROJECT_ID>
   ```

2. Check network connectivity (VPC, firewall rules)
3. Verify the instance name and cluster name are correct

### Issue: "Toolbox not found" or "Command not found"

**Symptoms:**
- Cursor cannot start the toolbox server
- Error about missing executable

**Solutions:**
1. Verify toolbox is installed:
   ```bash
   which toolbox
   ```

2. Update the `command` path in `mcp.json` with the correct path

3. Reinstall toolbox if necessary:
   ```bash
   brew reinstall toolbox
   ```

### Issue: MCP server not appearing in Cursor

**Symptoms:**
- Configuration added but server not available
- No database tools available in AI chat

**Solutions:**
1. Verify `mcp.json` syntax is valid JSON (use a JSON validator)
2. Check for duplicate server names in `mcp.json`
3. Completely restart Cursor (not just reload window)
4. Check Cursor's MCP logs (if available in settings)

### Issue: "Invalid credentials" or "Password authentication failed"

**Symptoms:**
- Connection established but authentication fails
- Error about invalid password

**Solutions:**
1. Verify database username is correct
2. Verify database password is correct (check for special characters that need escaping)
3. Confirm the user exists in the database:
   ```bash
   gcloud alloydb users list \
     --cluster=<CLUSTER_NAME> \
     --region=<REGION> \
     --project=<PROJECT_ID>
   ```

## Security Best Practices

### Credential Management

1. **Never commit credentials to version control**
   - Add `.cursor/mcp.json` to `.gitignore`
   - Use separate configurations for development/staging/production

2. **Use environment variables for sensitive data** (alternative approach)
   - Store credentials in a secure location
   - Reference them in your shell profile

3. **Rotate passwords regularly**
   - Update passwords in both AlloyDB and `mcp.json`
   - Use strong, unique passwords for each environment

4. **Use IAM authentication when possible** (advanced)
   - Consider using Google Cloud IAM database authentication
   - Eliminates need for password in configuration

### Network Security

1. **Use Private IP when possible**
   - Add `"ALLOYDB_POSTGRES_IP_TYPE": "private"` to env vars
   - Requires VPC peering or VPN setup

2. **Restrict network access**
   - Use AlloyDB's authorized networks feature
   - Implement firewall rules

3. **Monitor access logs**
   - Enable AlloyDB audit logging
   - Review connection attempts regularly

## Additional Configuration Options

### Optional Environment Variables

```json
"env": {
  "ALLOYDB_POSTGRES_PROJECT": "<PROJECT_ID>",
  "ALLOYDB_POSTGRES_REGION": "<REGION>",
  "ALLOYDB_POSTGRES_CLUSTER": "<CLUSTER_NAME>",
  "ALLOYDB_POSTGRES_INSTANCE": "<INSTANCE_NAME>",
  "ALLOYDB_POSTGRES_DATABASE": "<DATABASE_NAME>",
  "ALLOYDB_POSTGRES_USER": "<USERNAME>",
  "ALLOYDB_POSTGRES_PASSWORD": "<PASSWORD>",
  "ALLOYDB_POSTGRES_IP_TYPE": "public"
}
```

| Variable | Values | Default | Description |
|----------|--------|---------|-------------|
| `ALLOYDB_POSTGRES_IP_TYPE` | `public`, `private` | `public` | IP address type to use for connection |

### Multiple Database Configurations

You can configure multiple AlloyDB databases in the same `mcp.json`:

```json
{
  "mcpServers": {
    "mcp-alloydb-production": {
      "description": "Production Database",
      "command": "/opt/homebrew/bin/toolbox",
      "args": ["--prebuilt", "alloydb-postgres", "--stdio"],
      "env": { /* production config */ }
    },
    "mcp-alloydb-staging": {
      "description": "Staging Database",
      "command": "/opt/homebrew/bin/toolbox",
      "args": ["--prebuilt", "alloydb-postgres", "--stdio"],
      "env": { /* staging config */ }
    },
    "mcp-alloydb-development": {
      "description": "Development Database",
      "command": "/opt/homebrew/bin/toolbox",
      "args": ["--prebuilt", "alloydb-postgres", "--stdio"],
      "env": { /* development config */ }
    }
  }
}
```

## References

### Official Documentation

#### MCP Toolbox Documentation
- [MCP Toolbox Official Documentation](https://deepwiki.com/googleapis/genai-toolbox) - Comprehensive guide to MCP Toolbox architecture, components, and configuration
- [MCP Toolbox GitHub Repository](https://github.com/googleapis/genai-toolbox) - Source code, issues, and community contributions
- [MCP Toolbox Release Notes](https://github.com/googleapis/genai-toolbox/blob/main/CHANGELOG.md) - Version history and updates
- [MCP Toolbox Prebuilt Configurations](https://github.com/googleapis/genai-toolbox/tree/main/internal/prebuiltconfigs) - Available prebuilt configuration options

#### Google Cloud AlloyDB Documentation
- [Connect to AlloyDB using MCP Toolbox](https://cloud.google.com/alloydb/docs/connect-ide-using-mcp-toolbox) - Official Google guide for AlloyDB + MCP integration
- [AlloyDB Overview](https://cloud.google.com/alloydb/docs) - General AlloyDB documentation
- [AlloyDB Authentication](https://cloud.google.com/alloydb/docs/connect-auth) - Authentication methods and IAM integration
- [AlloyDB Instances](https://cloud.google.com/alloydb/docs/instance-primary) - Managing AlloyDB instances
- [AlloyDB Security](https://cloud.google.com/alloydb/docs/security-overview) - Security best practices and SSL/TLS configuration

#### Model Context Protocol (MCP)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/) - Official MCP protocol documentation
- [MCP Protocol on GitHub](https://github.com/modelcontextprotocol) - MCP organization and repositories
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers) - Community MCP server implementations

#### Cursor IDE Integration
- [Cursor IDE Documentation](https://cursor.sh/docs) - General Cursor documentation
- [Cursor MCP Integration](https://docs.cursor.com/context/model-context-protocol) - How to configure MCP servers in Cursor

### Google Cloud SDK & Tools

#### gcloud CLI Documentation
- [gcloud auth application-default](https://cloud.google.com/sdk/gcloud/reference/auth/application-default) - Application Default Credentials commands
- [gcloud alloydb](https://cloud.google.com/sdk/gcloud/reference/alloydb) - AlloyDB gcloud commands reference
- [gcloud alloydb clusters](https://cloud.google.com/sdk/gcloud/reference/alloydb/clusters) - Cluster management commands
- [gcloud alloydb instances](https://cloud.google.com/sdk/gcloud/reference/alloydb/instances) - Instance management commands

#### Google Cloud IAM
- [IAM Roles for AlloyDB](https://cloud.google.com/alloydb/docs/iam-roles) - Available IAM roles and permissions
- [Service Accounts](https://cloud.google.com/iam/docs/service-accounts) - Using service accounts for authentication
- [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials) - How ADC works

### PostgreSQL Resources
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Official PostgreSQL documentation
- [PostgreSQL SSL Support](https://www.postgresql.org/docs/current/ssl-tcp.html) - Understanding PostgreSQL SSL/TLS
- [PostgreSQL Connection Strings](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING) - Connection string format and parameters

### Community & Support
- [MCP Toolbox Discussions](https://github.com/googleapis/genai-toolbox/discussions) - Community discussions and Q&A
- [Stack Overflow - AlloyDB](https://stackoverflow.com/questions/tagged/google-alloydb) - Community questions and answers
- [Google Cloud Community](https://www.googlecloudcommunity.com/) - Official Google Cloud community forum

## Appendix: Common gcloud Commands

### List AlloyDB Resources

```bash
# List all clusters
gcloud alloydb clusters list --project=<PROJECT_ID>

# List instances in a cluster
gcloud alloydb instances list \
  --cluster=<CLUSTER_NAME> \
  --region=<REGION> \
  --project=<PROJECT_ID>

# Describe a specific instance
gcloud alloydb instances describe <INSTANCE_NAME> \
  --cluster=<CLUSTER_NAME> \
  --region=<REGION> \
  --project=<PROJECT_ID>

# List database users
gcloud alloydb users list \
  --cluster=<CLUSTER_NAME> \
  --region=<REGION> \
  --project=<PROJECT_ID>
```

### Authentication Commands

```bash
# Login with application default credentials
gcloud auth application-default login

# Verify authentication
gcloud auth application-default print-access-token

# Revoke credentials (if needed)
gcloud auth application-default revoke

# Set default project
gcloud config set project <PROJECT_ID>
```

---

**Document Version:** 1.1  
**Last Updated:** 2025-10-24  
**Changes in v1.1:**
- Added comprehensive section on access modes (read-only vs read-write)
- Documented all three prebuilt configurations (standard, observability, admin)
- Expanded References section with detailed documentation links
- Added security best practices for choosing access modes

**Author:** Technical Documentation Team

