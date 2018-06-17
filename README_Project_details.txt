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

******************************************************

##########################NOTE::::
########################PLEASE READ BEFORE EXECUTION #################
"""
Assumptions :
    As assignment suggests, cursory analysis of stock companies, 
    that focus on understanding 2 params: MARKETCAP_RS_CR and P/E(P_BY_E) ratio
    and also various sectors based performance and distribution
   
   Thus I remove the cases where MARKETCAP_RS_CR and P/E(P_BY_E) ratio
    for CONSOLIDATED cases is absent.
   MEANS I consider only CONSOLIDATED based params and its values
   
   AS1: Basically we have 2 possible values. But I consider only CONSOLIDATED
  
   AS2: Remove NAN cases
   
   AS3: Consider MARKETCAP_RS_CR based ranking for only those sectors who have > 4 companies
   
   AS4: I dont write generic code for scrape. Code will impact, if website changes format
      and reduce or increase no of parameters
   
   AS5: in part 5 THERE ARE OUTLIERS in P/E meaning many cases where P/E > 70
        I dont worry, as its not asked in question. Although need to worry, if its real market data
        and need to find other resources to verify
    
STEP 1: DATA SCRAPE
Part 1 consists of web scraping of html links and list of 500 companies which appears
on :
    www.moneycontrol.com/india/stockpricequote
    When code is excuted, its necessary to either provide:
        www.moneycontrol.com/india/stockpricequote
        or
        provide list of companies=> COMPANY_CODE in list companybook
 links_moneycontrol_v5.csv willbe file composed of all 500 companies on part 1 
completion

example:
select option 2
enter:
www.moneycontrol.com/india/stockpricequote

ENTER quantity of companies:
40

ENTER THE NAMES LIKE:

GP08
GI25
NBV
HS
GC20
JKB
GSP02
KG01
OCL
CFH
PLN
CES
C13
KI01
AMP01
IHF01
HZ
CFC
BLC
IB04
TP14
SIB
VT10
RC
PGC
LIC
NTP
MGF01
SG
SCI
TSI
AI01
SJ01
M18
BPC
GIC
PJ
KB04
HDI
JA02



Part 2: DATA SCRAPE
This section contains all logic to extract the information of CONSOLIDATED Company
parameters for all 500 companies
This section will try to contact moneycontrol 500 times, thus may take time.
I didnt focus to optimize this time.
The web scraping takes 30 -40 mins
and finally we get the transpose file:       input_scrape_moneycontrol_500.csv

PART 3: Data Cleaning
CHECKING DUPLICATES, renaming columns, removing extra characters, datatype conversions
, fill NAN, drop NAN

PART 4: Data analysis and decide assumptions

PART 5:  Bucket P/E ratios in interval of 5, 11-15,16-20,21-25,...,66-70, then output list of
companies in each bucket
AS5: THERE ARE OUTLIERS in P/E meaning many cases where P/E > 70
I dont worry, as its not asked in question. Although need to worry, if its real market data
and need to find other resources to verify

PART 6: 3rd and 4th highest market cap companies sector wise.
ASSUMPTION: DO analysis for sectors having more than 3 companies
I try 3 methods to solve it. And 1 method successful
BUT pandasql method fails as rank or rownum feature not available in it 
Also method of groupby and then use rank fails, for few cases. Getting warning message 
which can be corrected. 

************************************************************
************************************************************

THE FINAL OUTPUTS OF FILES:

THE RAW FILE from website scrape, before pivot or transpose:
       example_moneycontrol_v5.csv
     
"BASE FILE THAT CONTAINS ALL SCRAPED INFO PRIOR TO CLEANING AND ANALYZE: \
    input_scrape_moneycontrol_500.csv\
    "

BASE FILE THAT CONTAINS ALL SCRAPED INFO AFTER CLEANING AND ANALYZE and SQL as well: \
    moneycontrol_after_cleaning_analyze_forsql.csv\


FOR Bucket P/E ratios in interval of 5, 11-15,16-20,21-25,...\
       KINDLY CHECK CONSOLE OUTPUT (JUPYTER/SPYDER)

FOR 3rd and 4th highest market cap companies sector wise \
       MARKETCAP_RS_CR_dessc_3_4.csv by method 1 \
       and MARKETCAP_RS_CR_dessc_3_4_v2.csv by method 2\

