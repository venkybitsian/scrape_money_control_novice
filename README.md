# scrape_money_control_novice

Data is ubiquitously scattered and web scraping plays critical role to fetch data in form of tables/dataframes,
so that data analysis can be initiated:

# PART 1:
EXTRACT the 500 companies and their dynamic links
The output of 500 companies and their links is in:
https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/links_moneycontrol_v6.csv

# PART 2:
Extract the basic parameters for stock related finnancial info on these 500 companies and create a final dataframe.
The output of final Dataframe as created (with no cleaning)
https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/input_scrape_moneycontrol_500_before_cleaning.csv


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
MARKET_LOT           ,
P_BY_C               ,
P_BY_E               ,
PRICE_BY_BOOK        ,
sector                ,
count_comp_cat         ,


'LINK': This is  http link of stock, which is assumed and observed as STATIC

'company_code': This is manually generated abbreviation for understanding company with company code
DERIVE LOGIC:
FOR EXAMPLE: http://www.moneycontrol.com/india/stockpricequote/banksprivatesector/yesbank/YB
has company_category banksprivatesector located as substring value only after immediate right  of http://www.moneycontrol.com/india/stockpricequote/
 which comes immediate after last occurance of '/' till end of string

'company_category': is nothing but comapny sector
DERIVE LOGIC:
FOR EXAMPLE: http://www.moneycontrol.com/india/stockpricequote/banksprivatesector/yesbank/YB
has company_category banksprivatesector located as substring value only after immediate right  of http://www.moneycontrol.com/india/stockpricequote/
 which comes at 50 th position and from that 50th position to next occurance of '/'    

'MARKETCAP_RS_CR'  and 'P_BY_E' are 2 params we re interested into

'sector' is same as company_category
Note: although this is derived from other part of same website

'count_comp_cat' is script generated column which helps to know the quantity of companies underneath a sector and will be defined for each company

******************************************************

##########################NOTE::::
####################### # PLEASE READ BEFORE EXECUTION #################
"""

# Assumptions :


    As assignment suggests, cursory analysis of stock companies, 
    that focus on understanding 2 params: MARKETCAP_RS_CR and P/E(P_BY_E) ratio
    and also various sectors based performance and distribution
   
   Thus I remove the cases where MARKETCAP_RS_CR and P/E(P_BY_E) ratio
    for CONSOLIDATED cases is absent.
   MEANS I consider only STANDALONE based params and its values
   
   # ASSUMPTION 1:
   Basically we have 2 possible values. But I consider only CONSOLIDATED. CHECK THE IMAGE
   https://github.com/venkybitsian/scrape_money_control_novice/blob/master/this_info_is_being_scraped_from_each_company.JPG
   
  
   # ASSUMPTION 2:
   Remove NAN cases pertaining to nonavailability of p_by_e ratio and marketcap values
   
   # ASSUMPTION 3: 
   Consider MARKETCAP_RS_CR based ranking for only those sectors who have > 4 companies
   
   # ASSUMPTION 4: 
   I dont write generic code for scrape. Code will impact, if website changes format
      and reduce or increase no of parameters
   
   # ASSUMPTION 5: 
   In part 5 THERE ARE OUTLIERS in P/E meaning many cases where P/E > 70
        I dont worry, as its not asked in question. Although need to worry, if its real market data
        and need to find other resources to verify. Or approach data analysis after normalization of data for multiple params
    
# STEP 1 EXECUTION: DATA COLLECTION
# Part 1 consists of web scraping of html links and list of 500 companiesis created. It also aims at creation of dictionary for companies that need to be analyzed
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
# NOTE:
The company codes value has to be entered and can be found in:
https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_LIST_OF_COMPANIES/links_moneycontrol_v6.csv

or:is derived from hyperlink in belowe "EM"
https://www.moneycontrol.com/india/stockpricequote/auto-lcvs-hcvs/eichermotors/EM

------->>>>>INPUT GIVEN IS BELOW FOR 40 companies

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



# Part 2: DATA SCRAPE
This section contains all logic to extract the information of CONSOLIDATED Company
parameters for all 500 companies
This section will try to contact moneycontrol 500 times, thus may take time.
I didnt focus to optimize this time.
The web scraping takes 30- 35 mins
and finally we get the transpose file:       input_scrape_moneycontrol_500.csv

# PART 3: Data Cleaning
CHECKING DUPLICATES, renaming columns, removing extra characters, datatype conversions
, fill NAN, drop NAN

# PART 4: Data analysis and decide assumptions
Check missing values, check deviations

# NOTE: AFTER PART 3 and PART 4: FILE WHICH WAS CREATED FOR 500 COMPANIES:
https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/input_scrape_moneycontrol_443_after_cleaning_analyze_v2.csv

# PART 5:  Bucket P/E ratios in interval of 5, 11-15,16-20,21-25,...,66-70, then output list of
  companies in each bucket
# ASSUMPTION 5: THERE ARE OUTLIERS in P/E meaning many cases where P/E > 70
I dont worry, as its not asked in question. Although need to worry, if its real market data
and need to find other resources to verify

# PART 6: 3rd and 4th highest market cap companies sector wise.
# ASSUMPTION 6: DO analysis for sectors having more than 3 companies
I try 3 methods to solve it. And 2 method successful
BUT pandasql method fails as rank or rownum feature not available in it 

************************************************************
************************************************************

# *************THE FINAL OUTPUTS OF FILES:************

THE RAW FILE from website scrape, before pivot or transpose:
       example_moneycontrol_v5.csv
     
"BASE FILE THAT CONTAINS ALL SCRAPED INFO PRIOR TO CLEANING AND ANALYZE: \
    input_scrape_moneycontrol_500_before_cleaning.csv\
    "

BASE FILE THAT CONTAINS ALL SCRAPED INFO AFTER CLEANING AND ANALYZE and SQL as well: \
    moneycontrol_after_cleaning_analyze_forsql.csv\


FOR Bucket P/E ratios in interval of 5, 11-15,16-20,21-25,...\
       KINDLY CHECK CONSOLE OUTPUT (JUPYTER/SPYDER)

FOR 3rd and 4th highest market cap companies sector wise \
       MARKETCAP_RS_CR_dessc_3_4.csv by method 1 \
       and MARKETCAP_RS_CR_dessc_3_4_v2.csv by method 2\
       
       
# ALSO BY SQL the same is solved: PLEASE READ FOR SQL STEPS

https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/README_EXECUTE_SQL.txt

 FOR SQL, (for 443/500 companies) CSV used is:
https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/moneycontrol_after_cleaning_analyze_forsql.csv
