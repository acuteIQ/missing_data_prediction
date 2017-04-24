CREATE TABLE company(
       id bigint, /* PRIMARY KEY,*/
       zip bigint,
       industry_sic_code bigint,
       number_of_employees bigint,
       yearly_sales money
);

CREATE TABLE company_dense(
       id bigint, /* PRIMARY KEY,*/
       zip bigint,
       industry_sic_code bigint,
       number_of_employees bigint,
       yearly_sales money
);


/* delete duplicates */

/* full row duplicates */
DELETE FROM company
WHERE id IN 
 ( SELECT id FROM
  ( SELECT id, ROW_NUMBER() OVER
   ( partition BY id, zip, industry_sic_code, number_of_employees, yearly_sales ORDER BY id) AS rnum FROM company) t
 WHERE t.rnum > 1);


/* id duplicates */
select * from company ou where ( select count(*) from company inr where inr.id = ou.id) > 1;
