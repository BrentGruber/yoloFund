-- upgrade --
ALTER TABLE "ticker" ADD "exchange_id" INT NOT NULL;
ALTER TABLE "ticker" ADD CONSTRAINT "fk_ticker_exchange_79dce303" FOREIGN KEY ("exchange_id") REFERENCES "exchange" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "ticker" DROP CONSTRAINT "fk_ticker_exchange_79dce303";
ALTER TABLE "ticker" DROP COLUMN "exchange_id";
