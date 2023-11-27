CREATE TYPE "order" AS ENUM (
  'in_order',
  'outof_order'
);

CREATE TABLE "tram_stops" (
  "osmid" integer,
  "name" varchar(50),
  "stop_number" integer,
  "geometry" varchar(50),
  PRIMARY KEY ("name", "stop_number")
);

CREATE TABLE "time_table" (
  "line" integer,
  "name" varchar(50),
  "stop_number" integer,
  "order" integer,
  PRIMARY KEY ("line", "name")
);

CREATE TABLE "departures" (
  "line" integer,
  "name" varchar(50) PRIMARY KEY,
  "direction" order,
  "hour" float64,
  "minute" float64
);

CREATE TABLE "vehicles_by_line" (
  "line" integer PRIMARY KEY,
  "geometria" multi_lines
);

CREATE TABLE "vehicles_by_ttss" (
  "line" integer,
  "last_seen" varchar(50),
  "latitude" float,
  "longitude" float,
  "direction" varchar(50),
  "tram_id" integer
);

CREATE TABLE "vehicles_by_type" (
  "tram_id" integer PRIMARY KEY,
  "tram_depo_code" varchar,
  "tram_code" varchar,
  "name" varchar(20)
);

CREATE TABLE "model_attributes" (
  "model" varchar(50) PRIMARY KEY,
  "wielkosc" varchar(50),
  "rodzaj" varchar(50),
  "dlugosc" float,
  "szerokosc" float,
  "wysokos_podloga_nadwozia" float,
  "rozstaw_czopow_pretu" float,
  "rozstaw_osi" float,
  "masa_integermasa_calkowita" integer,
  "miejsca_ogolem" integer,
  "miejsca_siedzace" integer,
  "wysokosc_podlogi_przy_wejsciu" float,
  "liczba_silnikow" integer,
  "moc_silnika" integer,
  "srednica_kol_tocznych" float
);

CREATE TABLE "latency" (
  "line" integer,
  "tram_direction" varchar(50),
  "estimated_time_of_arrival" varchar(50),
  "stop" varchar(50),
  "measurement_time" timestamp
);

ALTER TABLE "time_table" ADD FOREIGN KEY ("name") REFERENCES "tram_stops" ("name");

ALTER TABLE "time_table" ADD FOREIGN KEY ("stop_number") REFERENCES "tram_stops" ("stop_number");

ALTER TABLE "time_table" ADD FOREIGN KEY ("line") REFERENCES "vehicles_by_line" ("line");

ALTER TABLE "vehicles_by_ttss" ADD FOREIGN KEY ("line") REFERENCES "vehicles_by_line" ("line");

ALTER TABLE "vehicles_by_ttss" ADD FOREIGN KEY ("tram_id") REFERENCES "vehicles_by_type" ("tram_id");

ALTER TABLE "vehicles_by_type" ADD FOREIGN KEY ("name") REFERENCES "model_attributes" ("model");

ALTER TABLE "latency" ADD FOREIGN KEY ("line") REFERENCES "vehicles_by_line" ("line");

ALTER TABLE "latency" ADD FOREIGN KEY ("stop") REFERENCES "tram_stops" ("name");

ALTER TABLE "departures" ADD FOREIGN KEY ("line") REFERENCES "time_table" ("line");

ALTER TABLE "departures" ADD FOREIGN KEY ("name") REFERENCES "time_table" ("name");
