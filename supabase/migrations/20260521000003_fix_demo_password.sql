-- ============================================================
-- Trinetra Agro AI — Fix: Correct demo user password hash
-- Generated directly with bcrypt (bypassing passlib __about__ bug)
-- demo@farm.com / demo123456
-- ============================================================

UPDATE public.users
SET hashed_password = '$2b$12$hrdLaTqPg9C7VI48x6atyOnBZ4arlbdHRL7ug3PwRYsYAeQ1LZiAa',
    updated_at      = NOW()
WHERE email = 'demo@farm.com';
