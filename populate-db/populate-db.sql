
--
-- PostgreSQL database for astro-query
-- This SQL file includes the DDL (table definitions)
-- and the DML (insert queries for mock data)
--

-- User table

CREATE TABLE public.observer (
    id integer DEFAULT nextval(('"student_id_seq"'::text)::regclass) NOT NULL,
    lastname text NOT NULL,
    firstname text,
    middlenames text,
    initials text,
    email text,
    institution text,
    city text,
    country text
);

CREATE SEQUENCE public.observer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE ONLY public.observer
    ADD CONSTRAINT observer_pkey PRIMARY KEY (id);


CREATE INDEX observer_firstname_inx ON public.observer USING btree (firstname);

CREATE INDEX observer_lastname_inx ON public.observer USING btree (lastname);

CREATE UNIQUE INDEX observer_email_inx ON public.observer USING btree (email);

CREATE INDEX observer_institution_inx ON public.observer USING btree (institution);

CREATE INDEX observer_city_inx ON public.observer USING btree (city);

CREATE INDEX observer_country_inx ON public.observer USING btree (country);

-- User Data
-- id, lastname, firstname, middlenames, initials, email, institution, city, country, created

INSERT INTO public.observer VALUES (1, 'Zhu', 'Ziyuan', NULL, 'ZZ', 'oz25@ic.ac.uk', 'Imperial College London', 'London', 'UK');
INSERT INTO public.observer VALUES (2, 'Raghavan', 'Shreyas', NULL, 'SR', 'sr2025@ic.ac.uk', 'Imperial College London', 'London', 'UK');
INSERT INTO public.observer VALUES (3, 'Hu', 'Yanglin', NULL, 'YL', 'yl14925@ic.ac.uk', 'Imperial College London', 'London', 'UK');


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


-- Observation table
CREATE TABLE public.observation (
    id integer DEFAULT nextval(('"student_id_seq"'::text)::regclass) NOT NULL,
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