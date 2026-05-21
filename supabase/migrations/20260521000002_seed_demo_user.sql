-- ============================================================
-- Trinetra Agro AI — Seed: Demo user
-- demo@farm.com / demo123456
-- Bcrypt hash generated with passlib CryptContext (bcrypt rounds=12)
-- ============================================================

INSERT INTO public.users (
    id,
    email,
    hashed_password,
    full_name,
    phone,
    is_active,
    created_at,
    updated_at
) VALUES (
    'demo-user-0000-0000-000000000001',
    'demo@farm.com',
    '$2b$12$eq.zaYqzy384vsgja3R/IOieU8YcSFhtdW4UufKILC9RGlNGmt2rW',
    'Demo Farmer',
    '+91-9999999999',
    TRUE,
    NOW(),
    NOW()
) ON CONFLICT (email) DO NOTHING;
