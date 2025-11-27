
--
-- PostgreSQL database for Star
-- This SQL file includes the DDL (table definitions)
-- and the DML (insert queries for mock data)
--



CREATE TABLE public.star (
    id integer DEFAULT nextval(('"star_id_seq"'::text)::regclass) NOT NULL,
    starname text not NULL,
    startype text,
    coordra float,
    coorddec float,
    color text,
    appmagnitude float,
    measurefilter text,
)



CREATE SEQUENCE public.star_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_pkey PRIMARY KEY (id);



CREATE INDEX star_id_inx ON public.star USING btree (id);

CREATE INDEX star_starname_inx ON public.star USING btree (starname);

CREATE INDEX star_startype_inx ON public.star USING btree (startype);

CREATE INDEX star_coordra_inx ON public.star USING btree (coordra);

CREATE INDEX star_coorddec_inx ON public.star USING btree (coorddec);

CREATE INDEX star_color_inx ON public.star USING btree (color);

CREATE INDEX star_appmagnitude_inx ON public.star USING btree (appmagnitude);

CREATE INDEX star_measurefilter_inx ON public.star USING btree (measurefilter);


-- Data

INSERT INTO public.star VALUES (1, '* alf Lyr', 'delSctV*', 279.234734787025, 38.783688956244, 'A0V', 0.029999999329447746, 'V')
INSERT INTO public.star VALUES (2, '* alf CMa', 'SB*', 101.28715533333335, -16.71611586111111, 'A0mA1Va', -1.4600000381469727, 'V')
INSERT INTO public.star VALUES (3, '* alf Car', 'Star', 95.98795782918306, -52.69566138386201, 'A9II', -0.7400000095367432, 'V')
INSERT INTO public.star VALUES (4, '* bet Ori', 'BlueSG', 78.63446706693006, -8.201638364722209, 'B8Ia', 0.12999999523162842, 'V')
INSERT INTO public.star VALUES (5, '* alf CMi', 'SB*', 114.82549790798149, 5.224987557059477, 'F5IV-V+DQZ', 0.3700000047683716, 'V')

