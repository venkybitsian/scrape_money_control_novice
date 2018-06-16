# scrape_money_control_novice
Data is ubiquitously scattered and web scraping plays critical role to fetch data in form of tables/dataframes, so that data analysis can be initiated:

PART 1:
EXTRACT the 500 companies and their dynamic links

PART 2:
Extract the basic parameters for stock related finnancial info on these 500 companies and create a final dataframe.

I observe 11 input parameters:

LINK               ,   
company_code        ,  
company_category    ,  
company_name        ,  
BOOK_VALUE_RS       , 
DIV_PERCENT       ,   
DIV_YIELD_PERCENT    ,
EPS_TTM              ,
FACE_VALUE           ,
INDUSTRY_P_BY_E      ,
MARKETCAP_RS_CR      ,
MARKET_LOT            ,
P_BY_C               ,
P_BY_E               ,
PRICE_BY_BOOK        ,
sector                ,
count_comp_cat         ,


'LINK': This is  http link of stock, which is assumed and observed as STATIC

'company_code': This is manually generated abbreviation for understanding company with company code

'company_category': is nothing but comapny sector

'MARKETCAP_RS_CR'  and 'P_BY_E' are 2 params we re interested into

'sector' is same as company_category

'count_comp_cat' is script generated column which helps to know the quantity of companies underneath a sector and will be defined for each company

