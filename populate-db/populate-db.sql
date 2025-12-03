
--
-- PostgreSQL database for astro-query
-- This SQL file includes the DDL (table definitions)
-- and the DML (insert queries for mock data)
--

-- User table

CREATE TABLE public.user (
    id integer DEFAULT nextval(('"user_id_seq"'::text)::regclass) NOT NULL,
    lastname text NOT NULL,
    firstname text NOT NULL,
    middlenames text,
    initials text,
    email text NOT NULL,
    institution text,
    city text NOT NULL,
    country text NOT NULL
);

CREATE SEQUENCE public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE ONLY public.user
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


CREATE INDEX user_firstname_inx ON public.user USING btree (firstname);

CREATE INDEX user_lastname_inx ON public.user USING btree (lastname);

CREATE UNIQUE INDEX user_email_inx ON public.user USING btree (email);

CREATE INDEX user_institution_inx ON public.user USING btree (institution);

CREATE INDEX user_city_inx ON public.user USING btree (city);

CREATE INDEX user_country_inx ON public.user USING btree (country);

-- User Data
-- id, lastname, firstname, middlenames, initials, email, institution, city, country, created

INSERT INTO public.user VALUES (1, 'Zhu', 'Ziyuan', NULL, 'ZZ', 'oz25@ic.ac.uk', 'Imperial College London', 'London', 'UK');
INSERT INTO public.user VALUES (2, 'Raghavan', 'Shreyas', NULL, 'SR', 'sr2025@ic.ac.uk', 'Imperial College London', 'London', 'UK');
INSERT INTO public.user VALUES (3, 'Hu', 'Yanglin', NULL, 'YL', 'yl14925@ic.ac.uk', 'Imperial College London', 'London', 'UK');


-- Telescope table

CREATE TABLE public.telescope (
    id integer DEFAULT nextval(('"student_id_seq"'::text)::regclass) NOT NULL,
    name text NOT NULL,
    manufacturer text,
    aperture int NOT NULL,
    magnitude float NOT NULL,
    focuslength int,
    fieldwidth float,
    fieldheight float,
    length int,
    weight float,
    purchasable BOOLEAN NOT NULL,
    imageurl text
);

CREATE SEQUENCE public.telescope_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE ONLY public.telescope
    ADD CONSTRAINT telescope_pkey PRIMARY KEY (id);


CREATE UNIQUE INDEX telescope_name_inx ON public.telescope USING btree (name);

CREATE INDEX telescope_aperture_inx ON public.telescope USING btree (aperture);

CREATE INDEX telescope_focuslength_inx ON public.telescope USING btree (focuslength);

CREATE INDEX telescope_purchasable_inx ON public.telescope USING btree (focuslength);


-- Telescope Data
-- id, name, manufacturer, aperture, magnitude, focuslength, fieldwidth, fieldheight, length, weight, purchasable, imageurl

INSERT INTO public.telescope VALUES (1, 'EQUINOX 2', 'Unistellar', 114, 18.2, 450, 34.2, 45.6, NULL, 7.0, true, 'https://shop.uk.unistellar.com/cdn/shop/files/EQ2-01.jpg');
INSERT INTO public.telescope VALUES (2, 'ODYSSEY PRO', 'Unistellar', 85, 17.2, 320, 33.6, 45.0, NULL, 4.0, true, 'https://shop.uk.unistellar.com/cdn/shop/files/ODP-00.jpg');
INSERT INTO public.telescope VALUES (3, 'Edge HD', 'Celestron', 279,  14.7, 2800, NULL, NULL, 610, 13.0, true, 'https://www.rothervalleyoptics.co.uk/user/templates/rothervalley-2019/2025bg1.jpg');
INSERT INTO public.telescope VALUES (4, 'NexStar 8SE', 'Celestron', 204,  14.0, 2032, NULL, NULL, 432, 5.4, true, 'https://www.celestron.com/cdn/shop/files/RS15946_11069_NexStar_8SE_Computerized_Telescope_1-hpr.jpg');
INSERT INTO public.telescope VALUES (5, 'OMC 200', 'Orion Optics UK', 200,  13.3, 4000, NULL, NULL, 600, 9.0, true, 'https://www.astroshop.eu/Produktbilder/big/57571_1.jpg');


-- Star table
CREATE TABLE public.star (
    id integer DEFAULT nextval(('"star_id_seq"'::text)::regclass) NOT NULL,
    starname text not NULL,
    startype text,
    coordra float,
    coorddec float,
    color text,
    appmagnitude float,
    measurefilter text
);


CREATE SEQUENCE public.star_id_seq
    START WITH 6
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

INSERT INTO public.star VALUES (1, '* alf Lyr', 'delSctV*', 279.234734787025, 38.783688956244, 'A0V', 0.029999999329447746, 'V');
INSERT INTO public.star VALUES (2, '* alf CMa', 'SB*', 101.28715533333335, -16.71611586111111, 'A0mA1Va', -1.4600000381469727, 'V');
INSERT INTO public.star VALUES (3, '* alf Car', 'Star', 95.98795782918306, -52.69566138386201, 'A9II', -0.7400000095367432, 'V');
INSERT INTO public.star VALUES (4, '* bet Ori', 'BlueSG', 78.63446706693006, -8.201638364722209, 'B8Ia', 0.12999999523162842, 'V');
INSERT INTO public.star VALUES (5, '* alf CMi', 'SB*', 114.82549790798149, 5.224987557059477, 'F5IV-V+DQZ', 0.3700000047683716, 'V');


-- Observation table
CREATE TABLE public.observation (
    id integer DEFAULT nextval(('"observation_id_seq"'::text)::regclass) NOT NULL,
    userid int,
    starid int,
    telescopeid int,
    time timestamptz DEFAULT now(),
    city text,
    country text
);

CREATE SEQUENCE public.observation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE ONLY public.observation
    ADD CONSTRAINT observation_pkey PRIMARY KEY (id);


CREATE UNIQUE INDEX observation_name_inx ON public.observation USING btree (name);

CREATE INDEX observation_userid_inx ON public.observation USING btree (aperture);

CREATE INDEX observation_starid_inx ON public.observation USING btree (focuslength);

CREATE INDEX observation_telescopeid_inx ON public.observation USING btree (focuslength);


-- Observation Data
-- id, userid, starid, telescope1d, time, city, country

INSERT INTO public.observation VALUES (1, 1, 3, 1, DEFAULT, 'London', 'UK');
INSERT INTO public.observation VALUES (2, 2, 2, 3, DEFAULT, 'London', 'UK');
INSERT INTO public.observation VALUES (3, 3, 1, 4, DEFAULT, 'London', 'UK');
