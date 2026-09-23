--
-- PostgreSQL database dump
--

\restrict 3fUZEdY6HZkc7TY2Kud6WClU8nLVcnUPIBM1ql59gJbV9jwjh72RwOfbNv1v2Jn

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chemical_management; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chemical_management (
    chemical_management_id integer NOT NULL,
    health_problem_id character varying(100) NOT NULL,
    treatment_type character varying(100),
    chemical_role character varying(100),
    active_ingredient text,
    chemical_class text,
    application_timing text,
    application_guidance text,
    resistance_management text,
    safety_notes text,
    source_id character varying(100)
);


--
-- Name: chemical_management_chemical_management_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.chemical_management_chemical_management_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: chemical_management_chemical_management_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.chemical_management_chemical_management_id_seq OWNED BY public.chemical_management.chemical_management_id;


--
-- Name: conditions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.conditions (
    condition_id text NOT NULL,
    health_problem_id text NOT NULL,
    factor text NOT NULL,
    value text,
    description text
);


--
-- Name: health_problems; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.health_problems (
    health_problem_id text NOT NULL,
    plant_id text NOT NULL,
    name text NOT NULL,
    type text NOT NULL,
    description text
);


--
-- Name: management; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.management (
    management_id text NOT NULL,
    health_problem_id text NOT NULL,
    category text NOT NULL,
    action text NOT NULL
);


--
-- Name: pathogens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pathogens (
    pathogen_id text NOT NULL,
    health_problem_id text NOT NULL,
    scientific_name text NOT NULL,
    type text NOT NULL,
    role text
);


--
-- Name: plants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plants (
    plant_id text NOT NULL,
    common_name text NOT NULL,
    genus text,
    family text
);


--
-- Name: sources; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sources (
    source_id text NOT NULL,
    health_problem_id text NOT NULL,
    organization text,
    title text,
    url text NOT NULL,
    accessed_date text
);


--
-- Name: species; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.species (
    species_id text NOT NULL,
    plant_id text NOT NULL,
    scientific_name text NOT NULL,
    common_name text
);


--
-- Name: symptoms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.symptoms (
    symptom_id text NOT NULL,
    health_problem_id text NOT NULL,
    category text,
    description text NOT NULL
);


--
-- Name: transmission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.transmission (
    transmission_id text NOT NULL,
    health_problem_id text NOT NULL,
    method text NOT NULL,
    description text
);


--
-- Name: chemical_management chemical_management_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chemical_management ALTER COLUMN chemical_management_id SET DEFAULT nextval('public.chemical_management_chemical_management_id_seq'::regclass);


--
-- Name: chemical_management chemical_management_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chemical_management
    ADD CONSTRAINT chemical_management_pkey PRIMARY KEY (chemical_management_id);


--
-- Name: conditions conditions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conditions
    ADD CONSTRAINT conditions_pkey PRIMARY KEY (condition_id);


--
-- Name: health_problems health_problems_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.health_problems
    ADD CONSTRAINT health_problems_pkey PRIMARY KEY (health_problem_id);


--
-- Name: health_problems health_problems_plant_id_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.health_problems
    ADD CONSTRAINT health_problems_plant_id_name_key UNIQUE (plant_id, name);


--
-- Name: management management_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.management
    ADD CONSTRAINT management_pkey PRIMARY KEY (management_id);


--
-- Name: pathogens pathogens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pathogens
    ADD CONSTRAINT pathogens_pkey PRIMARY KEY (pathogen_id);


--
-- Name: plants plants_common_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plants
    ADD CONSTRAINT plants_common_name_key UNIQUE (common_name);


--
-- Name: plants plants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plants
    ADD CONSTRAINT plants_pkey PRIMARY KEY (plant_id);


--
-- Name: sources sources_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT sources_pkey PRIMARY KEY (source_id);


--
-- Name: species species_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.species
    ADD CONSTRAINT species_pkey PRIMARY KEY (species_id);


--
-- Name: species species_plant_id_scientific_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.species
    ADD CONSTRAINT species_plant_id_scientific_name_key UNIQUE (plant_id, scientific_name);


--
-- Name: symptoms symptoms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.symptoms
    ADD CONSTRAINT symptoms_pkey PRIMARY KEY (symptom_id);


--
-- Name: transmission transmission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transmission
    ADD CONSTRAINT transmission_pkey PRIMARY KEY (transmission_id);


--
-- Name: idx_conditions_health_problem; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_conditions_health_problem ON public.conditions USING btree (health_problem_id);


--
-- Name: idx_health_problems_plant; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_health_problems_plant ON public.health_problems USING btree (plant_id);


--
-- Name: idx_management_health_problem; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_management_health_problem ON public.management USING btree (health_problem_id);


--
-- Name: idx_pathogens_health_problem; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pathogens_health_problem ON public.pathogens USING btree (health_problem_id);


--
-- Name: idx_sources_health_problem; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_sources_health_problem ON public.sources USING btree (health_problem_id);


--
-- Name: idx_species_plant; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_species_plant ON public.species USING btree (plant_id);


--
-- Name: idx_symptoms_health_problem; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_symptoms_health_problem ON public.symptoms USING btree (health_problem_id);


--
-- Name: idx_transmission_health_problem; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_transmission_health_problem ON public.transmission USING btree (health_problem_id);


--
-- Name: conditions conditions_health_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conditions
    ADD CONSTRAINT conditions_health_problem_id_fkey FOREIGN KEY (health_problem_id) REFERENCES public.health_problems(health_problem_id) ON DELETE CASCADE;


--
-- Name: chemical_management fk_chemical_health_problem; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chemical_management
    ADD CONSTRAINT fk_chemical_health_problem FOREIGN KEY (health_problem_id) REFERENCES public.health_problems(health_problem_id);


--
-- Name: health_problems health_problems_plant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.health_problems
    ADD CONSTRAINT health_problems_plant_id_fkey FOREIGN KEY (plant_id) REFERENCES public.plants(plant_id) ON DELETE CASCADE;


--
-- Name: management management_health_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.management
    ADD CONSTRAINT management_health_problem_id_fkey FOREIGN KEY (health_problem_id) REFERENCES public.health_problems(health_problem_id) ON DELETE CASCADE;


--
-- Name: pathogens pathogens_health_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pathogens
    ADD CONSTRAINT pathogens_health_problem_id_fkey FOREIGN KEY (health_problem_id) REFERENCES public.health_problems(health_problem_id) ON DELETE CASCADE;


--
-- Name: sources sources_health_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT sources_health_problem_id_fkey FOREIGN KEY (health_problem_id) REFERENCES public.health_problems(health_problem_id) ON DELETE CASCADE;


--
-- Name: species species_plant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.species
    ADD CONSTRAINT species_plant_id_fkey FOREIGN KEY (plant_id) REFERENCES public.plants(plant_id) ON DELETE CASCADE;


--
-- Name: symptoms symptoms_health_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.symptoms
    ADD CONSTRAINT symptoms_health_problem_id_fkey FOREIGN KEY (health_problem_id) REFERENCES public.health_problems(health_problem_id) ON DELETE CASCADE;


--
-- Name: transmission transmission_health_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transmission
    ADD CONSTRAINT transmission_health_problem_id_fkey FOREIGN KEY (health_problem_id) REFERENCES public.health_problems(health_problem_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 3fUZEdY6HZkc7TY2Kud6WClU8nLVcnUPIBM1ql59gJbV9jwjh72RwOfbNv1v2Jn

