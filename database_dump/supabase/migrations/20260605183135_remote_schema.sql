


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


COMMENT ON SCHEMA "public" IS 'standard public schema';



CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";






CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";






CREATE TYPE "public"."image_usage" AS ENUM (
    'project_logo',
    'avatar',
    'react_node',
    'code_logo',
    'pattern_graphic'
);


ALTER TYPE "public"."image_usage" OWNER TO "postgres";


COMMENT ON TYPE "public"."image_usage" IS 'Types of images uses in this app';



CREATE TYPE "public"."user_role" AS ENUM (
    'admin',
    'user'
);


ALTER TYPE "public"."user_role" OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_active_app_configs"() RETURNS TABLE("key" "text", "value" "text")
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
  RETURN QUERY
  SELECT c.key, c.value 
  FROM public.app_configs c
  WHERE c.enabled = true;
END;
$$;


ALTER FUNCTION "public"."get_active_app_configs"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."is_admin"() RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
  RETURN EXISTS (
    -- Importante: public.profiles
    SELECT 1 FROM public.profiles 
    WHERE id = auth.uid() 
    AND is_authorized = true
  );
END;
$$;


ALTER FUNCTION "public"."is_admin"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."rls_auto_enable"() RETURNS "event_trigger"
    LANGUAGE "plpgsql" SECURITY DEFINER
    SET "search_path" TO 'pg_catalog'
    AS $$
DECLARE
  cmd record;
BEGIN
  FOR cmd IN
    SELECT *
    FROM pg_event_trigger_ddl_commands()
    WHERE command_tag IN ('CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO')
      AND object_type IN ('table','partitioned table')
  LOOP
     IF cmd.schema_name IS NOT NULL AND cmd.schema_name IN ('public') AND cmd.schema_name NOT IN ('pg_catalog','information_schema') AND cmd.schema_name NOT LIKE 'pg_toast%' AND cmd.schema_name NOT LIKE 'pg_temp%' THEN
      BEGIN
        EXECUTE format('alter table if exists %s enable row level security', cmd.object_identity);
        RAISE LOG 'rls_auto_enable: enabled RLS on %', cmd.object_identity;
      EXCEPTION
        WHEN OTHERS THEN
          RAISE LOG 'rls_auto_enable: failed to enable RLS on %', cmd.object_identity;
      END;
     ELSE
        RAISE LOG 'rls_auto_enable: skip % (either system schema or not in enforced list: %.)', cmd.object_identity, cmd.schema_name;
     END IF;
  END LOOP;
END;
$$;


ALTER FUNCTION "public"."rls_auto_enable"() OWNER TO "postgres";

SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "public"."architectures" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "name" "text" NOT NULL,
    "description" "text" NOT NULL,
    "base_structure" "jsonb",
    "enabled" boolean DEFAULT false NOT NULL
);


ALTER TABLE "public"."architectures" OWNER TO "postgres";


COMMENT ON TABLE "public"."architectures" IS 'Master catalog of software architecture templates. This table defines the foundational directory structures and the initial React Flow graph layouts (nodes and edges). It serves as the read-only blueprint from which all user projects are initialized.';



CREATE TABLE IF NOT EXISTS "public"."code_languages" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "name" "text" NOT NULL,
    "file_extension" "text" NOT NULL,
    "icon" "uuid" NOT NULL
);


ALTER TABLE "public"."code_languages" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."images" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "file_name" "text" NOT NULL,
    "url" "text" NOT NULL,
    "user_id" "uuid" NOT NULL,
    "usage_type" "public"."image_usage" NOT NULL
);


ALTER TABLE "public"."images" OWNER TO "postgres";


COMMENT ON TABLE "public"."images" IS 'Centralized storage reference table for user and project-related imagery, managing file paths and metadata for consistent asset rendering across the platform.';



CREATE TABLE IF NOT EXISTS "public"."patterns" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "name" "text" NOT NULL,
    "description" "text" NOT NULL,
    "base_structure" "jsonb",
    "image_id" "uuid"
);


ALTER TABLE "public"."patterns" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."patterns_code" (
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "pattern_id" "uuid" NOT NULL,
    "code_id" "uuid" NOT NULL,
    "code_snippet" "jsonb" NOT NULL
);


ALTER TABLE "public"."patterns_code" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."profiles" (
    "id" "uuid" NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "email" "text" NOT NULL,
    "username" "text",
    "is_authorized" boolean DEFAULT false NOT NULL,
    "role" "public"."user_role" DEFAULT 'user'::"public"."user_role" NOT NULL,
    "first_name" "text" NOT NULL,
    "last_name" "text" NOT NULL,
    "avatar" "uuid"
);


ALTER TABLE "public"."profiles" OWNER TO "postgres";


COMMENT ON TABLE "public"."profiles" IS 'Extended user data for application logic, linked to auth.users via UUID';



CREATE TABLE IF NOT EXISTS "public"."projects" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "name" "text" NOT NULL,
    "description" "text",
    "user_id" "uuid" NOT NULL,
    "project_logo" "uuid",
    "architecture" "jsonb"
);


ALTER TABLE "public"."projects" OWNER TO "postgres";


COMMENT ON TABLE "public"."projects" IS 'Core relational table that instantiates architectures for end-users. It maps auth.users to public.architectures and serves as the parent record for folder customizations, project-specific images, and React Flow visual states.';



ALTER TABLE ONLY "public"."architectures"
    ADD CONSTRAINT "architectures_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."code_languages"
    ADD CONSTRAINT "code_languages_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."images"
    ADD CONSTRAINT "images_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."patterns_code"
    ADD CONSTRAINT "patterns_code_pkey" PRIMARY KEY ("pattern_id", "code_id");



ALTER TABLE ONLY "public"."patterns"
    ADD CONSTRAINT "patterns_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."profiles"
    ADD CONSTRAINT "profiles_email_key" UNIQUE ("email");



ALTER TABLE ONLY "public"."profiles"
    ADD CONSTRAINT "profiles_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."projects"
    ADD CONSTRAINT "projects_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."code_languages"
    ADD CONSTRAINT "code_languages_icon_fkey" FOREIGN KEY ("icon") REFERENCES "public"."images"("id") ON UPDATE CASCADE ON DELETE SET NULL;



ALTER TABLE ONLY "public"."images"
    ADD CONSTRAINT "images_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."profiles"("id") ON UPDATE CASCADE ON DELETE CASCADE;



ALTER TABLE ONLY "public"."patterns_code"
    ADD CONSTRAINT "patterns_code_code_id_fkey" FOREIGN KEY ("code_id") REFERENCES "public"."code_languages"("id") ON UPDATE CASCADE ON DELETE CASCADE;



ALTER TABLE ONLY "public"."patterns_code"
    ADD CONSTRAINT "patterns_code_pattern_id_fkey" FOREIGN KEY ("pattern_id") REFERENCES "public"."patterns"("id") ON UPDATE CASCADE ON DELETE CASCADE;



ALTER TABLE ONLY "public"."patterns"
    ADD CONSTRAINT "patterns_image_id_fkey" FOREIGN KEY ("image_id") REFERENCES "public"."images"("id") ON UPDATE CASCADE ON DELETE SET NULL;



ALTER TABLE ONLY "public"."profiles"
    ADD CONSTRAINT "profiles_avatar_fkey" FOREIGN KEY ("avatar") REFERENCES "public"."images"("id") ON UPDATE CASCADE ON DELETE SET NULL;



ALTER TABLE ONLY "public"."profiles"
    ADD CONSTRAINT "profiles_id_fkey" FOREIGN KEY ("id") REFERENCES "auth"."users"("id") ON UPDATE CASCADE ON DELETE CASCADE;



ALTER TABLE ONLY "public"."projects"
    ADD CONSTRAINT "projects_project_logo_fkey" FOREIGN KEY ("project_logo") REFERENCES "public"."images"("id") ON UPDATE CASCADE ON DELETE SET NULL;



ALTER TABLE ONLY "public"."projects"
    ADD CONSTRAINT "projects_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."profiles"("id") ON UPDATE CASCADE ON DELETE CASCADE;



CREATE POLICY "Admin can add code languages" ON "public"."code_languages" FOR INSERT TO "authenticated" WITH CHECK ("public"."is_admin"());



CREATE POLICY "Admin can create new architectures" ON "public"."architectures" FOR INSERT TO "authenticated" WITH CHECK ("public"."is_admin"());



CREATE POLICY "Admin can create patterns" ON "public"."patterns" FOR INSERT TO "authenticated" WITH CHECK ("public"."is_admin"());



CREATE POLICY "Admin can drop architectures" ON "public"."architectures" FOR DELETE TO "authenticated" USING ("public"."is_admin"());



CREATE POLICY "Admin can drop code languages" ON "public"."code_languages" FOR DELETE TO "authenticated" USING ("public"."is_admin"());



CREATE POLICY "Admin can drop pattern code" ON "public"."patterns_code" FOR DELETE TO "authenticated" USING ("public"."is_admin"());



CREATE POLICY "Admin can manage all projects" ON "public"."projects" USING ("public"."is_admin"()) WITH CHECK ("public"."is_admin"());



CREATE POLICY "Admin can manage all users" ON "public"."profiles" TO "authenticated" USING ("public"."is_admin"()) WITH CHECK ("public"."is_admin"());



CREATE POLICY "Admin can update all architectures" ON "public"."architectures" FOR UPDATE TO "authenticated" USING ("public"."is_admin"()) WITH CHECK ("public"."is_admin"());



CREATE POLICY "Admin can update code languages" ON "public"."code_languages" FOR UPDATE TO "authenticated" USING ("public"."is_admin"()) WITH CHECK ("public"."is_admin"());



CREATE POLICY "Admin can update patterns" ON "public"."patterns" FOR UPDATE TO "authenticated" USING ("public"."is_admin"()) WITH CHECK ("public"."is_admin"());



CREATE POLICY "Admin can update patterns code" ON "public"."patterns_code" FOR UPDATE TO "authenticated" USING ("public"."is_admin"()) WITH CHECK ("public"."is_admin"());



CREATE POLICY "Admins can add code to patterns" ON "public"."patterns_code" FOR INSERT TO "authenticated" WITH CHECK ("public"."is_admin"());



CREATE POLICY "Admins can drop patterns" ON "public"."patterns" FOR DELETE TO "authenticated" USING ("public"."is_admin"());



CREATE POLICY "Register policy" ON "public"."profiles" FOR INSERT WITH CHECK (("auth"."uid"() = "id"));



CREATE POLICY "Users can create their own projects" ON "public"."projects" FOR INSERT TO "authenticated" WITH CHECK (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can drop their images" ON "public"."images" FOR DELETE TO "authenticated" USING (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can drop their profiles" ON "public"."profiles" FOR SELECT TO "authenticated" USING (("auth"."uid"() = "id"));



CREATE POLICY "Users can drop their projects" ON "public"."projects" FOR DELETE TO "authenticated" USING (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can see architectures" ON "public"."architectures" FOR SELECT TO "authenticated" USING (true);



CREATE POLICY "Users can see code languages" ON "public"."code_languages" FOR SELECT USING (true);



CREATE POLICY "Users can see pattern code" ON "public"."patterns_code" FOR SELECT USING (true);



CREATE POLICY "Users can see patterns" ON "public"."patterns" FOR SELECT USING (true);



CREATE POLICY "Users can see their images and global" ON "public"."images" FOR SELECT USING (true);



CREATE POLICY "Users can see their profile" ON "public"."profiles" FOR SELECT TO "authenticated" USING (("auth"."uid"() = "id"));



CREATE POLICY "Users can see their projects" ON "public"."projects" FOR SELECT TO "authenticated" USING (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can update their profile" ON "public"."profiles" FOR UPDATE TO "authenticated" USING (("auth"."uid"() = "id"));



CREATE POLICY "Users can update their projects data" ON "public"."projects" FOR UPDATE TO "authenticated" USING (("auth"."uid"() = "user_id")) WITH CHECK (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can upload images" ON "public"."images" FOR INSERT TO "authenticated" WITH CHECK (("auth"."uid"() = "user_id"));



ALTER TABLE "public"."architectures" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."code_languages" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."images" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."patterns" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."patterns_code" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."profiles" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."projects" ENABLE ROW LEVEL SECURITY;




ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";


GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";






















































































































































GRANT ALL ON FUNCTION "public"."get_active_app_configs"() TO "anon";
GRANT ALL ON FUNCTION "public"."get_active_app_configs"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_active_app_configs"() TO "service_role";



REVOKE ALL ON FUNCTION "public"."is_admin"() FROM PUBLIC;
GRANT ALL ON FUNCTION "public"."is_admin"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."is_admin"() TO "service_role";
GRANT ALL ON FUNCTION "public"."is_admin"() TO "anon";



GRANT ALL ON FUNCTION "public"."rls_auto_enable"() TO "anon";
GRANT ALL ON FUNCTION "public"."rls_auto_enable"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."rls_auto_enable"() TO "service_role";


















GRANT ALL ON TABLE "public"."architectures" TO "anon";
GRANT ALL ON TABLE "public"."architectures" TO "authenticated";
GRANT ALL ON TABLE "public"."architectures" TO "service_role";



GRANT ALL ON TABLE "public"."code_languages" TO "anon";
GRANT ALL ON TABLE "public"."code_languages" TO "authenticated";
GRANT ALL ON TABLE "public"."code_languages" TO "service_role";



GRANT ALL ON TABLE "public"."images" TO "anon";
GRANT ALL ON TABLE "public"."images" TO "authenticated";
GRANT ALL ON TABLE "public"."images" TO "service_role";



GRANT ALL ON TABLE "public"."patterns" TO "anon";
GRANT ALL ON TABLE "public"."patterns" TO "authenticated";
GRANT ALL ON TABLE "public"."patterns" TO "service_role";



GRANT ALL ON TABLE "public"."patterns_code" TO "anon";
GRANT ALL ON TABLE "public"."patterns_code" TO "authenticated";
GRANT ALL ON TABLE "public"."patterns_code" TO "service_role";



GRANT ALL ON TABLE "public"."profiles" TO "anon";
GRANT ALL ON TABLE "public"."profiles" TO "authenticated";
GRANT ALL ON TABLE "public"."profiles" TO "service_role";



GRANT ALL ON TABLE "public"."projects" TO "anon";
GRANT ALL ON TABLE "public"."projects" TO "authenticated";
GRANT ALL ON TABLE "public"."projects" TO "service_role";









ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "service_role";



































