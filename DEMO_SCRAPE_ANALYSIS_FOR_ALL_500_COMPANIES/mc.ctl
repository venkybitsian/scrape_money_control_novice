OPTIONS(skip=1)
LOAD DATA
INFILE './moneycontrol_after_cleaning_analyze_forsql.csv'
REPLACE
INTO TABLE TableName
FIELDS TERMINATED BY ','
optionally enclosed by '"'
TRAILING NULLCOLS
(
MARKETCAP_RS_CR,
	P_BY_E,
	BOOK_VALUE_RS,
	DIV_PERCENT,
	MARKET_LOT,
	INDUSTRY_P_BY_E	,
	EPS_TTM	P_BY_C,
	PRICE_BY_BOOK,
	DIV_YIELD_PERCENT,
	FACE_VALUE	,
	sector,
	company_code,
	company_name
)

        





