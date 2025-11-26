
--
-- PostgreSQL database for Stars
-- This SQL file includes the DDL (table definitions)
-- and the DML (insert queries for mock data)
--



CREATE TABLE public.stars (
    id integer DEFAULT nextval(('"stars_id_seq"'::text)::regstars) NOT NULL,
    starname text,
    absmagnitude float,
    appmagnitude float,
    distance float,
)



CREATE SEQUENCE public.stars_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE ONLY public.stars
    ADD CONSTRAINT stars_pkey PRIMARY KEY (id);



CREATE INDEX stars_id_inx ON public.stars USING btree (id);

CREATE INDEX stars_starname_inx ON public.stars USING btree (starname);

CREATE INDEX stars_absmagnitude_inx ON public.stars USING btree (absmagnitude);

CREATE INDEX stars_appmagnitude_inx ON public.stars USING btree (appmagnitude);

CREATE INDEX stars_distance_inx ON public.stars USING btree (distance);


-- Data

INSERT INTO public.stars VALUES (1, 'Vega', 0.58, 0.03, 25)
INSERT INTO public.stars VALUES (2, 'Sirius', 1.42, -1.46, 8.6)
INSERT INTO public.stars VALUES (3, 'Canopus', -5.71, -0.74, 310)
INSERT INTO public.stars VALUES (4, 'Rigel', -6.7, 0.12, 860)
INSERT INTO public.stars VALUES (1, 'Procyon', 2.66, 0.40, 11.4)

