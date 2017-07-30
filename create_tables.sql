CREATE TABLE company3(
       id bigint, /* PRIMARY KEY,*/
       zip bigint,
       industry_sic_code bigint,
       number_of_employees bigint,
       yearly_sales money,
       latitude float,
       longitude float,
       company_name_cleaned text,
       city text,
       state text,
       county text
);

/*CREATE TABLE company_dense(
       id bigint,
       zip bigint,
       industry_sic_code bigint,
       number_of_employees bigint,
       yearly_sales money
);
*/

/* delete duplicates */

CREATE INDEX ON company3(id);

/* full row duplicates */
DELETE FROM company3
WHERE id IN 
 ( SELECT id FROM
  ( SELECT id, ROW_NUMBER() OVER
   ( partition BY id, zip, industry_sic_code, number_of_employees, yearly_sales,latitude, longitude, company_name_cleaned, city, state, county ORDER BY id) AS rnum FROM company3) t
 WHERE t.rnum > 1);


/* id duplicates */
select * from company ou where ( select count(*) from company inr where inr.id = ou.id) > 1;


CREATE TABLE company_prediction (
       id bigint PRIMARY KEY,
       yearly_sales smallint,
       number_of_employees smallint,
       credit_score smallint,
       business_risk smallint
);
insert into company_prediction (id) (SELECT id FROM company1);


CREATE TABLE equifax (
       company_id bigint PRIMARY KEY,
       EFX_CREDITPERC smallint,
       EFX_FAILRATE smallint,
       EFX_FAILLEVEL smallint
);


create index on company1(county);
create index on company1 (city);
create index on company1 (state);
create index on company3 (county);
create index on company3 (city);
create index on company3 (state);
