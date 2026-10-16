---
name: Cloudflare migration safety
description: Preserve production data and avoid cutting over before Cloudflare is verified.
---

For PRO CHEZ NOUS, preserve the existing PythonAnywhere production data and uploaded verification documents. Keep PythonAnywhere active until the Cloudflare version and domain routing are tested and validated.

**Why:** the user chose to retain the existing accounts and data while moving hosting to Cloudflare.

**How to apply:** migrate from a current PythonAnywhere export, not the older local Replit database; validate important flows before changing DNS or closing the old host.
