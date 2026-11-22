-- ============================================================
--  TickTick — Database Schema
--  PostgreSQL 15+
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- USERS
CREATE TABLE users (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email            VARCHAR(255) NOT NULL UNIQUE,
    password_hash    VARCHAR(255) NOT NULL,
    display_name     VARCHAR(100),
    role             VARCHAR(20) NOT NULL DEFAULT 'user',
    is_email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at       TIMESTAMPTZ
);

-- REFRESH TOKENS
CREATE TABLE refresh_tokens (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash   TEXT NOT NULL UNIQUE,
    expires_at   TIMESTAMPTZ NOT NULL,
    revoked      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires ON refresh_tokens(expires_at) WHERE revoked = FALSE;

-- NOTES
CREATE TABLE notes (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id        UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title          VARCHAR(500) NOT NULL DEFAULT 'Без названия',
    content        TEXT NOT NULL DEFAULT '',
    tags           TEXT[] NOT NULL DEFAULT '{}',
    is_deleted     BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at     TIMESTAMPTZ,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    search_vector  TSVECTOR,
    version        INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX idx_notes_user_id       ON notes(user_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_notes_tags          ON notes USING GIN(tags);
CREATE INDEX idx_notes_search_vector ON notes USING GIN(search_vector);
CREATE INDEX idx_notes_updated_at    ON notes(user_id, updated_at DESC);

CREATE OR REPLACE FUNCTION notes_search_vector_update() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('russian', coalesce(NEW.title, '')),   'A') ||
        setweight(to_tsvector('russian', coalesce(NEW.content, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(NEW.title, '')),   'A') ||
        setweight(to_tsvector('english', coalesce(NEW.content, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trig_notes_search_vector
    BEFORE INSERT OR UPDATE OF title, content
    ON notes
    FOR EACH ROW EXECUTE FUNCTION notes_search_vector_update();

CREATE OR REPLACE FUNCTION set_updated_at() RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trig_notes_updated_at
    BEFORE UPDATE ON notes
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- NOTE LINKS
CREATE TABLE note_links (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_note_id UUID NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
    target_note_id UUID NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_note_link UNIQUE (source_note_id, target_note_id),
    CONSTRAINT no_self_link  CHECK  (source_note_id <> target_note_id)
);

CREATE INDEX idx_note_links_source ON note_links(source_note_id);
CREATE INDEX idx_note_links_target ON note_links(target_note_id);

-- NOTE ATTACHMENTS
CREATE TABLE note_attachments (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    note_id     UUID NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
    file_name   VARCHAR(500) NOT NULL,
    file_path   VARCHAR(1000) NOT NULL,
    mime_type   VARCHAR(100) NOT NULL,
    file_size   BIGINT NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_attachments_note_id ON note_attachments(note_id);

-- CALENDAR EVENTS
CREATE TABLE calendar_events (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    linked_note_id  UUID REFERENCES notes(id) ON DELETE SET NULL,
    title           VARCHAR(500) NOT NULL,
    description     TEXT,
    start_at        TIMESTAMPTZ NOT NULL,
    end_at          TIMESTAMPTZ NOT NULL,
    color           VARCHAR(20) NOT NULL DEFAULT '#4A90D9',
    all_day         BOOLEAN NOT NULL DEFAULT FALSE,
    is_deleted      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version         INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT chk_event_dates CHECK (end_at >= start_at)
);

CREATE INDEX idx_events_user_range ON calendar_events(user_id, start_at, end_at) WHERE is_deleted = FALSE;
CREATE INDEX idx_events_note ON calendar_events(linked_note_id) WHERE linked_note_id IS NOT NULL;

CREATE TRIGGER trig_events_updated_at
    BEFORE UPDATE ON calendar_events
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- TODOS
CREATE TABLE todos (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    linked_note_id  UUID REFERENCES notes(id) ON DELETE SET NULL,
    title           VARCHAR(500) NOT NULL,
    description     TEXT,
    is_done         BOOLEAN NOT NULL DEFAULT FALSE,
    priority        SMALLINT NOT NULL DEFAULT 2 CHECK (priority BETWEEN 1 AND 3),
    due_at          TIMESTAMPTZ,
    is_deleted      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version         INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX idx_todos_user_id ON todos(user_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_todos_due_at  ON todos(user_id, due_at) WHERE is_deleted = FALSE AND is_done = FALSE;

CREATE TRIGGER trig_todos_updated_at
    BEFORE UPDATE ON todos
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- SYNC CHECKPOINTS
CREATE TABLE sync_checkpoints (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id   VARCHAR(200) NOT NULL,
    last_sync   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_sync_device UNIQUE (user_id, device_id)
);

-- VIEWS
CREATE VIEW v_active_notes AS
SELECT id, user_id, title, content, tags, search_vector, created_at, updated_at
FROM notes WHERE is_deleted = FALSE AND deleted_at IS NULL;

CREATE VIEW v_trash AS
SELECT id, user_id, title, deleted_at
FROM notes WHERE is_deleted = TRUE
ORDER BY deleted_at DESC;

-- FULL TEXT SEARCH FUNCTION
CREATE OR REPLACE FUNCTION search_notes(query TEXT, p_user_id UUID)
RETURNS TABLE (id UUID, title VARCHAR, snippet TEXT, rank FLOAT4) AS $$
DECLARE tsq TSQUERY;
BEGIN
    tsq := websearch_to_tsquery('russian', query);
    RETURN QUERY
    SELECT n.id, n.title,
        ts_headline('russian', n.content, tsq, 'MaxWords=30, MinWords=10, MaxFragments=2') AS snippet,
        ts_rank_cd(n.search_vector, tsq) AS rank
    FROM notes n
    WHERE n.user_id = p_user_id AND n.is_deleted = FALSE AND n.search_vector @@ tsq
    ORDER BY rank DESC;
END;
$$ LANGUAGE plpgsql STABLE;
