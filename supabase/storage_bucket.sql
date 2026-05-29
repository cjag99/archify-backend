-- Run once in Supabase Dashboard → SQL Editor
-- Creates the public bucket expected by archify-backend (default name: archify)

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'archify',
  'archify',
  true,
  10485760,
  array['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml']
)
on conflict (id) do update set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

-- Public read (required for get_public_url links in the frontend)
drop policy if exists "archify_public_read" on storage.objects;
create policy "archify_public_read"
on storage.objects for select
to public
using (bucket_id = 'archify');

-- Authenticated users can upload to their folder
drop policy if exists "archify_authenticated_insert" on storage.objects;
create policy "archify_authenticated_insert"
on storage.objects for insert
to authenticated
with check (bucket_id = 'archify');

drop policy if exists "archify_authenticated_update" on storage.objects;
create policy "archify_authenticated_update"
on storage.objects for update
to authenticated
using (bucket_id = 'archify');

drop policy if exists "archify_authenticated_delete" on storage.objects;
create policy "archify_authenticated_delete"
on storage.objects for delete
to authenticated
using (bucket_id = 'archify');
