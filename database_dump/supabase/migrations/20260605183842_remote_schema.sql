
  create policy "Authenticated users can use storage 1mnpmue_0"
  on "storage"."objects"
  as permissive
  for select
  to authenticated
using ((bucket_id = 'archify'::text));



  create policy "Authenticated users can use storage 1mnpmue_1"
  on "storage"."objects"
  as permissive
  for insert
  to authenticated
with check ((bucket_id = 'archify'::text));



  create policy "Authenticated users can use storage 1mnpmue_2"
  on "storage"."objects"
  as permissive
  for update
  to authenticated
using ((bucket_id = 'archify'::text));



  create policy "Authenticated users can use storage 1mnpmue_3"
  on "storage"."objects"
  as permissive
  for delete
  to authenticated
using ((bucket_id = 'archify'::text));



