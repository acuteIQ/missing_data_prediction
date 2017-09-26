CREATE TABLE company_tf_observation (
       id bigint PRIMARY KEY,

       yearly_sales smallint,
       number_of_employees smallint,
       credit_score smallint,
       business_risk smallint,

       industry_sic_code smallint,
       city_str text,
       city integer,
       state_str text,
       state smallint,
       county_str text,
       county smallint
);

CREATE TABLE city_codes (
       city text UNIQUE,
       id serial PRIMARY KEY
);

insert into city_codes (city) (select distinct city from company1);

CREATE TABLE county_codes (
       county text UNIQUE,
       id serial PRIMARY KEY
);

insert into county_codes (county) (select distinct county from company1);

CREATE TABLE state_codes (
       state text UNIQUE,
       id serial PRIMARY KEY
);

insert into state_codes (state) (select distinct state from company1);
