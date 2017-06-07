CREATE TABLE company1(
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

CREATE INDEX ON company1(id);

/* full row duplicates */
DELETE FROM company1
WHERE id IN 
 ( SELECT id FROM
  ( SELECT id, ROW_NUMBER() OVER
   ( partition BY id, zip, industry_sic_code, number_of_employees, yearly_sales,latitude, longitude, company_name_cleaned, city, state, county ORDER BY id) AS rnum FROM company1) t
 WHERE t.rnum > 1);


/* id duplicates */
select * from company ou where ( select count(*) from company inr where inr.id = ou.id) > 1;
