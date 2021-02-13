-- upgrade --
CREATE TABLE IF NOT EXISTS "exchange" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "code" VARCHAR(8) NOT NULL UNIQUE,
    "name" VARCHAR(128) NOT NULL,
    "mic" VARCHAR(16) NOT NULL,
    "timezone" VARCHAR(64) NOT NULL,
    "open_time" VARCHAR(32) NOT NULL,
    "country" VARCHAR(8) NOT NULL,
    "source" TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_exchange_name_26f1e2" ON "exchange" ("name");
CREATE INDEX IF NOT EXISTS "idx_exchange_timezon_d1298d" ON "exchange" ("timezone");
CREATE INDEX IF NOT EXISTS "idx_exchange_open_ti_c5b776" ON "exchange" ("open_time");
CREATE INDEX IF NOT EXISTS "idx_exchange_country_9f06bb" ON "exchange" ("country");
COMMENT ON TABLE "exchange" IS 'The Exchange model';
CREATE TABLE IF NOT EXISTS "ticker" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "currency" VARCHAR(8) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "displaySymbol" VARCHAR(16) NOT NULL,
    "figi" VARCHAR(32) NOT NULL,
    "mic" VARCHAR(32) NOT NULL,
    "symbol" VARCHAR(16) NOT NULL,
    "type" VARCHAR(64) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_ticker_currenc_f05153" ON "ticker" ("currency");
CREATE INDEX IF NOT EXISTS "idx_ticker_display_e10947" ON "ticker" ("displaySymbol");
CREATE INDEX IF NOT EXISTS "idx_ticker_symbol_d1124b" ON "ticker" ("symbol");
CREATE INDEX IF NOT EXISTS "idx_ticker_type_3a8257" ON "ticker" ("type");
COMMENT ON TABLE "ticker" IS 'The Ticker model';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
