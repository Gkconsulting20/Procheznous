---
name: Cloudflare migration safety
description: Preserve production data and avoid cutting over before Cloudflare is verified.
---

For PRO CHEZ NOUS, use a fresh Cloudflare database; the user says the existing app has seen little use and does not need its production records migrated. Keep PythonAnywhere active until the Cloudflare version and domain routing are tested and validated.

**Why:** the user chose to start with an empty database instead of transferring existing records.

**How to apply:** do not import the old PythonAnywhere or local Replit database; validate registration, login, booking, and payments before changing DNS or closing the old host.
