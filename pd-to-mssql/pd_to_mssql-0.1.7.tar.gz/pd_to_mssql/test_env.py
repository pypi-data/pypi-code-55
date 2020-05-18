import pandas as pd
import pyodbc
from pd_to_mssql import to_sql
import datetime

nav_cnxn_str = 'Driver={iSeries Access ODBC Driver};System=NAV400E;Uid=areis;Pwd=spring20;'
nav_cnxn = pyodbc.connect(nav_cnxn_str)

DS_cnxn_str = 'Driver={ODBC Driver 17 for SQL Server};Server=oh01msvsp64.workflowone.net\proddas1;Database=DataScience;Trusted_Connection=yes;'

start_date = datetime.date(year=2020, month=2, day=1)
end_date = datetime.date(year=2020, month=2, day=29)

full_query = """ /* Pull top line sales for Navitor companies, excludes freight, intercompany, coupons, serv sales, RAL / Pass Through */
DECLARE GLOBAL TEMPORARY TABLE SESSION.TP1 AS (
	SELECT h.sys, h.acct, billact#, mrktto#, h.ord#, ponum, h.invdat, c.name, c.prime, c.second, division, prddiv, d.item#, d.itemdsc, d.prdcls, d.invtyp, sum(d.itemamt) AS rev
	FROM NAVDTAWHS.DWORDHH AS h
	INNER JOIN NAVDTAWHS.DWORDDT AS d ON h.sys = d.sys AND h.acct = d.acct AND h.ord# = d.ord# AND h.seq# = d.seq# AND h.invdat = d.invdat
	INNER JOIN NAVDTAWHS.DWCUST AS c ON h.acct = c.acct AND h.sys = c.sys
	WHERE d.itemamt <> 0 AND h.invdat BETWEEN '<start_date>' AND '<end_date>' AND LEFT(c.prime, 2) NOT IN ('92', '91', '96', '93', '85') AND second NOT LIKE '582%' AND (division like '178%' or division like '80%' or ((h.prime in (12,31) or h.acct IN ('178000','178001','178002','177996','195791')) AND subsrc NOT LIKE 'IRG%' AND subsrc NOT LIKE 'NAVV%' AND srccde <> '148%')) AND LEFT(ordtyp, 1) NOT IN ('Y') AND LEFT(prdcls, 3) NOT IN ('XSS','XSH','ADR','970','NSF','XCO')
	GROUP BY h.sys, h.acct, billact#, mrktto#, h.ord#, ponum, h.invdat, c.name, c.prime, c.second, division, prddiv, d.item#, d.itemdsc, d.prdcls, d.invtyp
) DEFINITION ONLY;

INSERT INTO SESSION.TP1
SELECT h.sys, h.acct, billact#, mrktto#, h.ord#, ponum, h.invdat, c.name, c.prime, c.second, division, prddiv, d.item#, d.itemdsc, d.prdcls, d.invtyp, sum(d.itemamt) AS rev
	FROM NAVDTAWHS.DWORDHH AS h
	INNER JOIN NAVDTAWHS.DWORDDT AS d ON h.sys = d.sys AND h.acct = d.acct AND h.ord# = d.ord# AND h.seq# = d.seq# AND h.invdat = d.invdat
	INNER JOIN NAVDTAWHS.DWCUST AS c ON h.acct = c.acct AND h.sys = c.sys
	WHERE d.itemamt <> 0 AND h.invdat BETWEEN '<start_date>' AND '<end_date>' AND LEFT(c.prime, 2) NOT IN ('92', '91', '96', '93', '85') AND second NOT LIKE '582%' AND (division like '178%' or division like '80%' or ((h.prime in (12,31) or h.acct IN ('178000','178001','178002','177996','195791')) AND subsrc NOT LIKE 'IRG%' AND subsrc NOT LIKE 'NAVV%' AND srccde <> '148%')) AND LEFT(ordtyp, 1) NOT IN ('Y') AND LEFT(prdcls, 3) NOT IN ('XSS','XSH','ADR','970','NSF','XCO')
	GROUP BY h.sys, h.acct, billact#, mrktto#, h.ord#, ponum, h.invdat, c.name, c.prime, c.second, division, prddiv, d.item#, d.itemdsc, d.prdcls, d.invtyp
;


/* Add address from BillTo account - physical address rather than mailing */
DECLARE GLOBAL TEMPORARY TABLE SESSION.TP4 AS (
	SELECT tp1.sys, tp1.acct, tp1.billact#, tp1.mrktto#, tp1.ord#, ponum, tp1.invdat, item#, itemdsc, prdcls, invtyp, c.name, c.prime, c.second, padd1 AS add1, pcity AS city, pstate AS st, pzip AS zip, CASE WHEN (division LIKE '80%' OR division LIKE '178%') AND prddiv LIKE '%-%' THEN SUBSTR(prddiv, 1, LOCATE('-', prddiv)-1) WHEN division LIKE '80%' OR division LIKE '178%' THEN TRIM(prddiv) ELSE SUBSTR(division, 1, LOCATE('-', division)-1) END AS dv2, rev
	FROM SESSION.TP1 AS tp1
	LEFT OUTER JOIN NAVDTAWHS.DWCUST AS c ON tp1.sys = c.sys AND tp1.billact# = c.acct 
) DEFINITION ONLY;

INSERT INTO SESSION.TP4
	SELECT tp1.sys, tp1.acct, tp1.billact#, tp1.mrktto#, tp1.ord#, ponum, tp1.invdat, item#, itemdsc, prdcls, invtyp, c.name, c.prime, c.second, padd1 AS add1, pcity AS city, pstate AS st, pzip AS zip, CASE WHEN (division LIKE '80%' OR division LIKE '178%') AND prddiv LIKE '%-%' THEN SUBSTR(prddiv, 1, LOCATE('-', prddiv)-1) WHEN division LIKE '80%' OR division LIKE '178%' THEN TRIM(prddiv) ELSE SUBSTR(division, 1, LOCATE('-', division)-1) END AS dv2, rev
	FROM SESSION.TP1 AS tp1
	LEFT OUTER JOIN NAVDTAWHS.DWCUST AS c ON tp1.sys = c.sys AND tp1.billact# = c.acct 
;

DROP TABLE SESSION.TP1;

/* Update customer name if linked to related accounts */
DECLARE GLOBAL TEMPORARY TABLE SESSION.TP7 AS (
	SELECT tp4.sys, tp4.acct, tp4.billact#, tp4.mrktto#, tp4.ord#, ponum, tp4.invdat, item#, itemdsc, prdcls, invtyp, CASE WHEN tp4.mrktto# <> '' THEN c.name ELSE tp4.name END AS customer, tp4.name, tp4.prime, tp4.second, tp4.add1, tp4.city, tp4.st, tp4.zip, tp4.dv2, rev
	FROM SESSION.TP4 AS tp4
	LEFT OUTER JOIN NAVDTAWHS.DWCUST AS c ON tp4.sys = c.sys AND tp4.mrktto# = c.acct
) DEFINITION ONLY;

INSERT INTO SESSION.TP7
	SELECT tp4.sys, tp4.acct, tp4.billact#, tp4.mrktto#, tp4.ord#, ponum, tp4.invdat, item#, itemdsc, prdcls, invtyp, CASE WHEN tp4.mrktto# <> '' THEN c.name ELSE tp4.name END AS customer, tp4.name, tp4.prime, tp4.second, tp4.add1, tp4.city, tp4.st, tp4.zip, tp4.dv2, rev
	FROM SESSION.TP4 AS tp4
	LEFT OUTER JOIN NAVDTAWHS.DWCUST AS c ON tp4.sys = c.sys AND tp4.mrktto# = c.acct
;

DROP TABLE SESSION.TP4;

/* Add Division Name */
DECLARE GLOBAL TEMPORARY TABLE SESSION.TP8 AS (
	SELECT tp7.sys, tp7.acct, tp7.billact#, tp7.mrktto#, tp7.ord#, tp7.ponum, tp7.invdat, tp7.item#, tp7.itemdsc, tp7.prdcls, tp7.invtyp, tp7.customer, tp7.name, tp7.prime, tp7.second, tp7.add1, tp7.city, tp7.st, tp7.zip, tp7.dv2, TRIM(d.business) AS BU, TRIM(division) AS div, tp7.rev
	FROM SESSION.TP7 as tp7
	LEFT OUTER JOIN NAVDTAWHS.NAVDIV3 AS d ON dv2 = ICSMDIV
	WHERE TRIM(d.business) <> 'Other TSA'
) DEFINITION ONLY;

INSERT INTO SESSION.TP8
	SELECT tp7.sys, tp7.acct, tp7.billact#, tp7.mrktto#, tp7.ord#, tp7.ponum, tp7.invdat, tp7.item#, tp7.itemdsc, tp7.prdcls, tp7.invtyp, tp7.customer, tp7.name, tp7.prime, tp7.second, tp7.add1, tp7.city, tp7.st, tp7.zip, tp7.dv2, TRIM(d.business) AS BU, TRIM(division) AS div, tp7.rev
	FROM SESSION.TP7 as tp7
	LEFT OUTER JOIN NAVDTAWHS.NAVDIV3 AS d ON dv2 = ICSMDIV
	WHERE TRIM(d.business) <> 'Other TSA'
;

DROP TABLE SESSION.TP7;

UPDATE SESSION.TP8
SET BU = 'MCC', div = 'MCC'
WHERE BU in ('MCC', 'Artco / Tatex')
;

UPDATE SESSION.TP8
SET div = 'Folders'
WHERE div IN ('Accent')
;

/* Update product category / subcategory to most current definition, exclude corrected freight */
DECLARE GLOBAL TEMPORARY TABLE SESSION.TP9 AS (
	SELECT tp8.sys, tp8.acct, tp8.billact#, tp8.mrktto#, tp8.ord#, tp8.ponum, tp8.invdat, tp8.item#, CASE WHEN tp8.item# = cat.item# THEN cat.itemdsc ELSE tp8.itemdsc END AS itmdesc, CASE WHEN tp8.item#  = cat.item# THEN cat.prdcls ELSE tp8.prdcls END AS catg, CASE WHEN tp8.item# = cat.item# THEN cat.invtyp ELSE tp8.invtyp END AS subcat, tp8.customer, tp8.name, tp8.prime, tp8.second, tp8.add1, tp8.city, tp8.st, tp8.zip, tp8.dv2, tp8.bu, tp8.div, tp8.rev 
	FROM SESSION.TP8 AS tp8
	LEFT OUTER JOIN NAVDTAWHS.CATEGORY AS cat ON tp8.item# = cat.item# AND tp8.sys = cat.system
	WHERE CASE WHEN tp8.item#  = cat.item# THEN cat.prdcls ELSE tp8.prdcls END NOT LIKE 'XSH%'
) DEFINITION ONLY;

INSERT INTO SESSION.TP9
	SELECT tp8.sys, tp8.acct, tp8.billact#, tp8.mrktto#, tp8.ord#, tp8.ponum, tp8.invdat, tp8.item#, CASE WHEN tp8.item# = cat.item# THEN cat.itemdsc ELSE tp8.itemdsc END AS itmdesc, CASE WHEN tp8.item#  = cat.item# THEN cat.prdcls ELSE tp8.prdcls END catg, CASE WHEN tp8.item# = cat.item# THEN cat.invtyp ELSE tp8.invtyp END AS subcat, tp8.customer, tp8.name, tp8.prime, tp8.second, tp8.add1, tp8.city, tp8.st, tp8.zip, tp8.dv2, tp8.bu, tp8.div, tp8.rev 
	FROM SESSION.TP8 AS tp8
	LEFT OUTER JOIN NAVDTAWHS.CATEGORY AS cat ON tp8.item# = cat.item# AND tp8.sys = cat.system
	WHERE CASE WHEN tp8.item#  = cat.item# THEN cat.prdcls ELSE tp8.prdcls END NOT LIKE 'XSH%'
;

DROP TABLE SESSION.TP8;

/* Look up Taylor roll up revenue recognition category by Invtyp/subcat (defined exceptions), then prdcls/catg */
DECLARE GLOBAL TEMPORARY TABLE SESSION.TP10 AS (
	SELECT tp9.*, CASE WHEN catg LIKE '%-%' THEN SUBSTR(catg, 1, LOCATE('-', catg)-1) ELSE TRIM(catg) END AS prdcls, CASE WHEN subcat LIKE '%-%' THEN SUBSTR(subcat, 1, LOCATE('-', subcat)-1) ELSE TRIM(subcat) END AS invtyp
	FROM SESSION.TP9 AS tp9
) DEFINITION ONLY;

INSERT INTO SESSION.TP10
	SELECT tp9.*, CASE WHEN catg LIKE '%-%' THEN SUBSTR(catg, 1, LOCATE('-', catg)-1) ELSE TRIM(catg) END AS prdcls, CASE WHEN subcat LIKE '%-%' THEN SUBSTR(subcat, 1, LOCATE('-', subcat)-1) ELSE TRIM(subcat) END AS invtyp
	FROM SESSION.TP9 AS tp9
;

DROP TABLE SESSION.TP9;

DECLARE GLOBAL TEMPORARY TABLE SESSION.TP11 AS (
	SELECT tp10.*, CASE WHEN invtyp <> '' AND invtyp = cat2.prdcode THEN cat2.revrec WHEN prdcls=cat1.prdcode THEN cat1.revrec ELSE 'OTHER' END AS TAYCAT
	FROM SESSION.TP10 AS tp10
	LEFT OUTER JOIN NAVDTAWHS.CATROLLUP AS cat1 ON tp10.prdcls = cat1.prdcode
	LEFT OUTER JOIN NAVDTAWHS.CATROLLUP AS cat2 ON tp10.invtyp = cat2.prdcode
) DEFINITION ONLY;

INSERT INTO SESSION.TP11
	SELECT tp10.*, CASE WHEN invtyp <> '' AND invtyp = cat2.prdcode THEN cat2.revrec WHEN prdcls=cat1.prdcode THEN cat1.revrec ELSE 'OTHER' END AS TAYCAT
	FROM SESSION.TP10 AS tp10
	LEFT OUTER JOIN NAVDTAWHS.CATROLLUP AS cat1 ON tp10.prdcls = cat1.prdcode
	LEFT OUTER JOIN NAVDTAWHS.CATROLLUP AS cat2 ON tp10.invtyp = cat2.prdcode
;

DROP TABLE SESSION.TP10;

DECLARE GLOBAL TEMPORARY TABLE SESSION.TP12 AS (
	SELECT sys, acct, billact#, mrktto#, ord#, ponum, invdat, item#, itmdesc, taycat, catg, subcat, CASE WHEN LEFT(prime, 2) IN ('1_', '4_') THEN 'OFFICE DEPOT' WHEN LEFT(second, 3) in ('130', '141', '137') THEN 'QUILL' WHEN LEFT(prime, 2) IN ('2_', '5_') THEN 'STAPLES' WHEN (prime LIKE '10%' AND second NOT LIKE '380%') OR LEFT(second, 3) IN ('202', '208') THEN SUBSTR(second, LOCATE('_', second)+1, 50) ELSE customer END AS cust, CASE WHEN prime LIKE '10%' THEN 'BETH MARSTON' WHEN LEFT(prime, 2) IN ('1_', '2_', '4_', '5_', '77') THEN 'GREG MEERSMAN' WHEN LEFT(second, 3) IN ('446', '208') THEN 'SUE LUND' ELSE '' END AS SalesCon, name, prime, second, add1, city, st, zip, dv2, bu, div, rev
	FROM SESSION.TP11 as tp11
) DEFINITION ONLY;

INSERT INTO SESSION.TP12
	SELECT sys, acct, billact#, mrktto#, ord#, ponum, invdat, item#, itmdesc, taycat, catg, subcat, CASE WHEN LEFT(prime, 2) IN ('1_', '4_') THEN 'OFFICE DEPOT' WHEN LEFT(second, 3) in ('130', '141', '137') THEN 'QUILL' WHEN LEFT(prime, 2) IN ('2_', '5_') THEN 'STAPLES' WHEN (prime LIKE '10%' AND second NOT LIKE '380%') OR LEFT(second, 3) IN ('202', '208') THEN SUBSTR(second, LOCATE('_', second)+1, 50) ELSE customer END AS cust, CASE WHEN prime LIKE '10%' THEN 'BETH MARSTON' WHEN LEFT(prime, 2) IN ('1_', '2_', '4_', '5_', '77') THEN 'GREG MEERSMAN' WHEN LEFT(second, 3) IN ('446', '208') THEN 'SUE LUND' ELSE '' END AS SalesCon, name, prime, second, add1, city, st, zip, dv2, bu, div, rev
	FROM SESSION.TP11 as tp11
;

DROP TABLE SESSION.TP11;

/* Pull external sales for Cosco Enterprise */
DECLARE GLOBAL TEMPORARY TABLE SESSION.TP14 AS (
	SELECT sysx AS sys, '' AS acct, '' AS billact#, '' AS mrktto#, '' AS ord#, '' AS ponum, invdatx AS invdat, '' AS item#, '' AS itmdesc, 'CORP ID' AS taycat, '' AS catg, '' AS subcat, CASE WHEN primex in ('1', '4') THEN 'OFFICE DEPOT' WHEN primex IN ('2', '5') THEN 'STAPLES' ELSE 'EXCLUDE' END AS cust, 'GREG MEERSMAN' AS SalesCon, CASE WHEN primex in ('1', '4') THEN 'OFFICE DEPOT' WHEN primex IN ('2', '5') THEN 'STAPLES' ELSE 'EXCLUDE' END AS name, primex AS prime, '' AS second, '' AS add1, '' AS city, '' AS st, '' AS zip, divx AS dv2, 'COSCO' AS BU, 'COSCO' AS div, salex AS rev
	FROM NAVDTAWHS.DSRUPLOADX
	WHERE divnamex = 'Stock' AND primex IN ('2', '4', '5') AND salex <> 0 AND invdatx BETWEEN '<start_date>' AND '<end_date>'
) DEFINITION ONLY;

INSERT INTO SESSION.TP14
	SELECT sysx AS sys, '' AS acct, '' AS billact#, '' AS mrktto#, '' AS ord#, '' AS ponum, invdatx AS invdat, '' AS item#, '' AS itmdesc, 'CORP ID' AS taycat, '' AS catg, '' AS subcat, CASE WHEN primex in ('1', '4') THEN 'OFFICE DEPOT' WHEN primex IN ('2', '5') THEN 'STAPLES' ELSE 'EXCLUDE' END AS cust, 'GREG MEERSMAN' AS SalesCon, CASE WHEN primex in ('1', '4') THEN 'OFFICE DEPOT' WHEN primex IN ('2', '5') THEN 'STAPLES' ELSE 'EXCLUDE' END AS name, primex AS prime, '' AS second, '' AS add1, '' AS city, '' AS st, '' AS zip, divx AS dv2, 'COSCO' AS BU, 'COSCO' AS div, salex AS rev
	FROM NAVDTAWHS.DSRUPLOADX
	WHERE divnamex = 'Stock' AND primex IN ('2', '4', '5') AND salex <> 0 AND invdatx BETWEEN '<start_date>' AND '<end_date>'


<section>

SELECT * FROM SESSION.TP12 UNION ALL SELECT * FROM SESSION.TP14

<section>

DROP TABLE SESSION.TP12;
DROP TABLE SESSION.TP14

"""

full_query = full_query.replace('<start_date>', str(start_date))
full_query = full_query.replace('<end_date>', str(end_date))

sections = full_query.split('<section>')

crsr = nav_cnxn.cursor()

for s in sections[0].split(';'):
    crsr.execute(s)
    crsr.commit()

df_nav = pd.read_sql(sections[1], nav_cnxn)
df_nav.replace(r'^\s*$', pd.NA, inplace=True, regex=True)

for s in sections[2].split(';'):
    crsr.execute(s)
    crsr.commit()

to_sql(df_nav, 'stg_NAV', DS_cnxn_str, index=False)