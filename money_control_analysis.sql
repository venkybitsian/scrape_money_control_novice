------AFTER SQLLDR the CSV file into DB, one can execute below queries to analyze the requirements:
------------------------------------------------------PROBLEM 1-------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
-- a:
--3rd and 4th highest market cap companies sector wise. 
 SELECT MARKETCAP_RS_CR  ,
         company_category sector,
         company_name     ,
         rnk
    FROM (select MARKETCAP_RS_CR,
                 company_category,
                 company_name,
                 rank() over(partition by company_category order by MARKETCAP_RS_CR DESC) as rnk
            from mc
           where company_category in
                 (SELECT company_category
                    from mc
                   group by company_category
                  having count(1) > 3)) VV
   where VV.rnk in (3, 4);
 ----------------------------------------------------PROBLEM 2---------------------------------------------------------  
 --------------------------------------------------------------------------------------------------------------
 --------------------------------------------------------------------------------------------------------------
   --b:
   -- Bucket P/E ratios in interval of 5, 11-15,16-20,21-25,...,66-70, then output list of companies in each bucket
   
  -- First understnad distribution of companies based on p/E
   
SELECT CASE 
         WHEN P_BY_E BETWEEN 0 AND 5 THEN '1-5' 
         WHEN P_BY_E  BETWEEN 5 AND 10 THEN '5-10' 
		 WHEN P_BY_E  BETWEEN 10 AND 15 THEN '10-15' 
		 WHEN P_BY_E  BETWEEN 15 AND 20 THEN '15-20' 
		 WHEN P_BY_E  BETWEEN 20 AND 25 THEN '20-25' 
		 WHEN P_BY_E  BETWEEN 25 AND 30 THEN '25-30' 
		 WHEN P_BY_E  BETWEEN 30 AND 35 THEN '30-35' 
		 WHEN P_BY_E  BETWEEN 35 AND 40 THEN '35-40' 
		 WHEN P_BY_E  BETWEEN 40 AND 45 THEN '40-45' 
         ELSE '45+' 
       END AS P_BY_E_category, 
       COUNT(distinct company_code) AS n
FROM mc
GROUP BY CASE 
        WHEN P_BY_E BETWEEN 0 AND 5 THEN '1-5' 
         WHEN P_BY_E  BETWEEN 5 AND 10 THEN '5-10' 
		 WHEN P_BY_E  BETWEEN 10 AND 15 THEN '10-15' 
		 WHEN P_BY_E  BETWEEN 15 AND 20 THEN '15-20' 
		 WHEN P_BY_E  BETWEEN 20 AND 25 THEN '20-25' 
		 WHEN P_BY_E  BETWEEN 25 AND 30 THEN '25-30' 
		 WHEN P_BY_E  BETWEEN 30 AND 35 THEN '30-35' 
		 WHEN P_BY_E  BETWEEN 35 AND 40 THEN '35-40' 
		 WHEN P_BY_E  BETWEEN 40 AND 45 THEN '40-45' 
         ELSE '45+' 
       END 
	   
	
------------------------------------------METHOD 1:::::::::::::::::::
--add new column bucket and checkout SQL results

alter table mc
add bucket varchar2(100);

	  


declare
  V_Sql varchar2(2000);
begin
  for i IN 0 .. 20 LOOP
    v_sql := 'merge into mc a
using (select company_name from mc where P_BY_E  BETWEEN ' || '5*' || i ||
             ' AND ' || '( ' || i || '+1)*5) vv
       on (a.company_name=vv.company_name)
       when matched then update
       set
       a.bucket=' || '''' || 5 * i || '_to_' || 5 * (i + 1) || '''';
    --dbms_output.put_line(v_sql);
	   execute immediate (v_sql);
    commit;
  end loop;
end;
update mc
set bucket='morethan_105'
where P_BY_E>105;
commit;

select company_name, p_by_e , bucket from mc order by bucket, p_by_e;



--------------------------------------------------METHOD 2:
-- execute sql statements
			 
	   declare
  V_Sql varchar2(2000);
begin
  for i IN 0 .. 20 LOOP
    v_sql := ' select company_name, P_BY_E from mc where P_BY_E  BETWEEN ' || '5*' || i ||
             ' AND ' || '( ' || i || '+1)*5';
    dbms_output.put_line('RANGE is: ' || 5 * i || ' to ' || 5 * (i + 1));
    dbms_output.put_line (v_sql);
  end loop;
end;

RANGE is: 0 to 5
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*0 AND ( 0+1)*5
RANGE is: 5 to 10
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*1 AND ( 1+1)*5
RANGE is: 10 to 15
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*2 AND ( 2+1)*5
RANGE is: 15 to 20
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*3 AND ( 3+1)*5
RANGE is: 20 to 25
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*4 AND ( 4+1)*5
RANGE is: 25 to 30
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*5 AND ( 5+1)*5
RANGE is: 30 to 35
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*6 AND ( 6+1)*5
RANGE is: 35 to 40
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*7 AND ( 7+1)*5
RANGE is: 40 to 45
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*8 AND ( 8+1)*5
RANGE is: 45 to 50
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*9 AND ( 9+1)*5
RANGE is: 50 to 55
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*10 AND ( 10+1)*5
RANGE is: 55 to 60
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*11 AND ( 11+1)*5
RANGE is: 60 to 65
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*12 AND ( 12+1)*5
RANGE is: 65 to 70
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*13 AND ( 13+1)*5
RANGE is: 70 to 75
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*14 AND ( 14+1)*5
RANGE is: 75 to 80
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*15 AND ( 15+1)*5
RANGE is: 80 to 85
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*16 AND ( 16+1)*5
RANGE is: 85 to 90
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*17 AND ( 17+1)*5
RANGE is: 90 to 95
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*18 AND ( 18+1)*5
RANGE is: 95 to 100
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*19 AND ( 19+1)*5
RANGE is: 100 to 105
 select company_name, P_BY_E from mc where P_BY_E  BETWEEN 5*20 AND ( 20+1)*5
