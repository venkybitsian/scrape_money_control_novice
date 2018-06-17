OPTIONS(skip=1)
LOAD DATA
INFILE './moneycontrol_after_cleaning_analyze_forsql.csv'
REPLACE
INTO TABLE TableName
FIELDS TERMINATED BY ','
optionally enclosed by '"'
TRAILING NULLCOLS
(
company_code	,
company_category	,
company_name	,
BOOK_VALUE_RS	,
DIV_PERCENT	,
DIV_YIELD_PERCENT	,
EPS_TTM	,
FACE_VALUE	,
INDUSTRY_P_BY_E	,
MARKETCAP_RS_CR	,
MARKET_LOT	,
P_BY_C	,
P_BY_E	,
PRICE_BY_BOOK	,
sector	
)

        





