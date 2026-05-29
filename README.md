# archify-backend

## Supabase Storage (required for images)

Image uploads use a **public** Storage bucket. The default name is `archify`.

If you see `{"error":"Bucket not found"}` when opening image URLs:

1. Open [Supabase Dashboard](https://supabase.com/dashboard) → your project → **SQL Editor**.
2. Run the script [`supabase/storage_bucket.sql`](./supabase/storage_bucket.sql).
3. Confirm under **Storage** that a bucket named `archify` exists and is **public**.
4. Restart the backend.
5. **Re-upload** images that were saved before the bucket existed (old URLs stay broken).

Uploads now store files under a UUID filename (no spaces). If an old URL contains `%20`, re-upload that image so a clean URL is saved.

### Private vs public bucket

- **Public bucket** (`SUPABASE_STORAGE_PUBLIC=true`): URLs use `/storage/v1/object/public/...` and never expire.
- **Private bucket** (default): URLs use `/storage/v1/object/sign/...?token=...` (same as Supabase “Copy URL”). Tokens expire after `SUPABASE_SIGNED_URL_EXPIRES` seconds; the API regenerates them on each `GET /images/{id}` and in `icon_url` on code languages.

To make the bucket public: run `supabase/storage_bucket.sql` or enable **Public bucket** in the Dashboard.

Optional: set a different bucket name in `.env`:

```env
SUPABASE_STORAGE_BUCKET=my-bucket-name
```

The bucket id in Supabase must match this value exactly.
