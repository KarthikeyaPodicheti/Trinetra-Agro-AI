-- ============================================================
-- Trinetra Agro AI — Initial Schema
-- PostgreSQL 17 (Supabase)
-- All UUIDs stored as TEXT to match existing SQLAlchemy String(36) models
-- ============================================================

-- Enable useful extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- 1. users
-- ============================================================
CREATE TABLE IF NOT EXISTS public.users (
    id          TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    email       VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name   VARCHAR(255),
    phone       VARCHAR(20),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT users_email_unique UNIQUE (email)
);

CREATE INDEX IF NOT EXISTS idx_users_email ON public.users (email);

-- ============================================================
-- 2. farmers
-- ============================================================
CREATE TABLE IF NOT EXISTS public.farmers (
    id                  TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    user_id             TEXT NOT NULL,
    soil_type           VARCHAR(50),
    land_size_acres     FLOAT,
    budget_inr          FLOAT,
    location            VARCHAR(255),
    crops               JSONB,
    irrigation_type     VARCHAR(50),
    experience_years    INTEGER,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT farmers_user_id_unique UNIQUE (user_id),
    CONSTRAINT farmers_user_id_fk FOREIGN KEY (user_id)
        REFERENCES public.users (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_farmers_user_id ON public.farmers (user_id);

-- ============================================================
-- 3. disease_reports
-- ============================================================
CREATE TABLE IF NOT EXISTS public.disease_reports (
    id                  TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    farmer_id           TEXT,
    crop_type           VARCHAR(100) NOT NULL,
    disease_name        VARCHAR(255) NOT NULL,
    confidence          FLOAT NOT NULL,
    severity            VARCHAR(20),
    image_path          VARCHAR(500),
    treatment           TEXT,
    prevention_tips     JSONB,
    analysis_details    JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT disease_reports_farmer_id_fk FOREIGN KEY (farmer_id)
        REFERENCES public.farmers (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_disease_reports_farmer_id ON public.disease_reports (farmer_id);
CREATE INDEX IF NOT EXISTS idx_disease_reports_created_at ON public.disease_reports (created_at DESC);

-- ============================================================
-- 4. market_predictions
-- ============================================================
CREATE TABLE IF NOT EXISTS public.market_predictions (
    id                      TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    farmer_id               TEXT,
    crop                    VARCHAR(100) NOT NULL,
    location                VARCHAR(255),
    forecast_days           INTEGER NOT NULL,
    current_price           FLOAT,
    trend                   VARCHAR(20),
    recommendation_action   VARCHAR(20),
    predictions_json        JSONB,
    data_source             VARCHAR(100),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT market_predictions_farmer_id_fk FOREIGN KEY (farmer_id)
        REFERENCES public.farmers (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_market_predictions_farmer_id ON public.market_predictions (farmer_id);
CREATE INDEX IF NOT EXISTS idx_market_predictions_crop ON public.market_predictions (crop);

-- ============================================================
-- 5. risk_assessments
-- ============================================================
CREATE TABLE IF NOT EXISTS public.risk_assessments (
    id              TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    farmer_id       TEXT,
    crop            VARCHAR(100) NOT NULL,
    risk_score      FLOAT NOT NULL,
    risk_level      VARCHAR(20) NOT NULL,
    breakdown_json  JSONB,
    factors         JSONB,
    mitigations     JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT risk_assessments_farmer_id_fk FOREIGN KEY (farmer_id)
        REFERENCES public.farmers (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_risk_assessments_farmer_id ON public.risk_assessments (farmer_id);

-- ============================================================
-- 6. yield_predictions
-- ============================================================
CREATE TABLE IF NOT EXISTS public.yield_predictions (
    id                      TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    farmer_id               TEXT,
    crop                    VARCHAR(100) NOT NULL,
    land_size_acres         FLOAT NOT NULL,
    soil_type               VARCHAR(50),
    irrigation              BOOLEAN DEFAULT TRUE,
    estimate_conservative   FLOAT,
    estimate_moderate       FLOAT,
    estimate_optimistic     FLOAT,
    unit                    VARCHAR(20),
    multipliers_json        JSONB,
    season                  VARCHAR(20),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT yield_predictions_farmer_id_fk FOREIGN KEY (farmer_id)
        REFERENCES public.farmers (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_yield_predictions_farmer_id ON public.yield_predictions (farmer_id);

-- ============================================================
-- 7. irrigation_plans
-- ============================================================
CREATE TABLE IF NOT EXISTS public.irrigation_plans (
    id              TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    farmer_id       TEXT,
    crop            VARCHAR(100) NOT NULL,
    land_size_acres FLOAT NOT NULL,
    growth_stage    VARCHAR(50),
    daily_litres    FLOAT,
    weekly_litres   FLOAT,
    method          VARCHAR(100),
    schedule_json   JSONB,
    tips            JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT irrigation_plans_farmer_id_fk FOREIGN KEY (farmer_id)
        REFERENCES public.farmers (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_irrigation_plans_farmer_id ON public.irrigation_plans (farmer_id);

-- ============================================================
-- 8. profit_analyses
-- ============================================================
CREATE TABLE IF NOT EXISTS public.profit_analyses (
    id                      TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    farmer_id               TEXT,
    crop                    VARCHAR(100) NOT NULL,
    land_size_acres         FLOAT NOT NULL,
    irrigation              BOOLEAN DEFAULT TRUE,
    cost_total              FLOAT,
    cost_per_acre           FLOAT,
    cost_breakdown_json     JSONB,
    profit_conservative     FLOAT,
    profit_moderate         FLOAT,
    profit_optimistic       FLOAT,
    roi_conservative        FLOAT,
    roi_moderate            FLOAT,
    roi_optimistic          FLOAT,
    recommendation          TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT profit_analyses_farmer_id_fk FOREIGN KEY (farmer_id)
        REFERENCES public.farmers (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_profit_analyses_farmer_id ON public.profit_analyses (farmer_id);

-- ============================================================
-- 9. feedback
-- ============================================================
CREATE TABLE IF NOT EXISTS public.feedback (
    id          TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    user_id     TEXT,
    feature     VARCHAR(100) NOT NULL,
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment     TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT feedback_user_id_fk FOREIGN KEY (user_id)
        REFERENCES public.users (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON public.feedback (user_id);
CREATE INDEX IF NOT EXISTS idx_feedback_feature ON public.feedback (feature);

-- ============================================================
-- updated_at auto-update trigger for users and farmers
-- ============================================================
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE TRIGGER users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER farmers_updated_at
    BEFORE UPDATE ON public.farmers
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
