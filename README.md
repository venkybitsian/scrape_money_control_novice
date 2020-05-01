# scrape_money_control_novice
TECHNICAL:
    Python 3.6
    Libraries:
            bs4,  BeautifulSoup, requests, pandas, numpy, time, seaborn, matplotlib, traceback 
            
Data is ubiquitously scattered and web scraping plays critical role to fetch data in form of tables/dataframes,
so that data analysis can be initiated:
Final Results: https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/Revision2/extract_500.ipynb
Source of scrape:
# PART 1:
EXTRACT the 500 companies and their dynamic links
SOurce of scrape: https://www.moneycontrol.com/india/stockpricequote
FUNCTIONS USED: scrape_info() and  fn_input()  partially
FILES GENERATED: links_moneycontrol_v6.csv
# PART 2:
OBJECTIVE:  Creating input dictionary to faciliate the further scraping based on STDIN input
FUNCTIONS USED: fn_input() partially
INPUT SUPPLY:
    When code is excuted, its necessary to either provide:
        INPUT AS: 1 or 2
        1 will fetch all 500
        2 will fetch the list of companies provided
# PART 3: DATA SCRAPING
Extract the basic parameters for stock related finnancial info on these 500 companies and create a final dataframe.
The output of final Dataframe as created (with no cleaning)
https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/input_scrape_moneycontrol_500_before_cleaning.csv


I observe 9 input parameters:

LINK               ,   
company_code        ,  
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
sector                



'LINK': This is  http link of stock, which is assumed and observed as STATIC

'company_code': This is manually generated abbreviation for understanding company with company code
DERIVE LOGIC:
FOR EXAMPLE: http://www.moneycontrol.com/india/stockpricequote/banksprivatesector/yesbank/YB
has company_category banksprivatesector located as substring value only after immediate right  of http://www.moneycontrol.com/india/stockpricequote/
 which comes immediate after last occurance of '/' till end of string

 

'MARKETCAP_RS_CR'  and 'P_BY_E' are 2 params we re interested into

'sector' is same as company_category
DERIVE LOGIC:
FOR EXAMPLE: http://www.moneycontrol.com/india/stockpricequote/banksprivatesector/yesbank/YB
has company_category banksprivatesector located as substring value only after immediate right  of http://www.moneycontrol.com/india/stockpricequote/
 which comes at 50 th position and from that 50th position to next occurance of '/'   
'count_comp_cat' is script generated column which helps to know the quantity of companies underneath a sector and will be defined for each company



# PART 4: Data Cleaning
OBJECTIVE: CHECKING DUPLICATES, renaming columns, removing extra characters, datatype conversions,
fill NAN, drop NAN
FUNCTIONS USED: fn_clean()

# PART 5: 
OBJECTIVE: Data analysis and decide assumptions
FUNCTIONS USED:fn_analyze()
FILES GENERATED: input_scrape_moneycontrol_443_after_cleaning_analyze_v2.csv 
  and moneycontrol_after_cleaning_analyze_forsql.csv
  
 # PART 6: 
OBJECTIVE: Bucket P/E ratios in interval of 5, 11-15,16-20,21-25,...,66-70, then output list of
companies in each bucket
FUNCTIONS USED: fn_P_by_e()


# PART 7: 
OBJECTIVE: 3rd and 4th highest market cap companies sector wise.
ASSUMPTION: DO analysis for sectors having more than 3 companies
I try 2 methods to solve it.
FUNCTIONS USED: fn_marketcap()
##FILES GENERATED: MARKETCAP_RS_CR_dessc_3_4_v2.csv and MARKETCAP_RS_CR_dessc_3_4.csv

# PART 8:
OBJECTIVE: Visuals are generated for cursory info
ASSUMPTION: DO analysis for sectors having more than 3 companies   
FUNCTIONS USED: fn_visuals()
******************************************************

##########################NOTE::::
################# # PLEASE READ BEFORE EXECUTION #################
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
    
-----------------------CODE INFO----------------------
CODE:       
    For easy debug, I develop various functions and mentioning their objective below:
        
     scrape_info(requestsobject,tag): This will scape the information using "requests" for a particular tag
     
     fn_input(): 
         Objective1: is to formulate the basic information about  all 500 companies 
         mentioned on:
         https://www.moneycontrol.com/india/stockpricequote
         like their hyperlinks, company name, sector etc. and formaulate a dataframe
         #Here we are going to extract comapny name,code and sector from html liink
         #example  https://www.moneycontrol.com/india/stockpricequote/diversified/3mindia/MI42
         #then company_code is MI42,name is 3mindia, sector is diversified
         Objective 2: Based on STDIN from user 1 0r 2, a dictionary will be composed of list of companies we 
         aim to analyze
    
     fn_moneycontrol_scrape(self,test_df): 
     This is main step where the logic is written to scrape the STANDALONE params for all the companies
     we provided already in the fn_input implementation:
     MARKETCAP_RS_CR, P_BY_E, BOOK_VALUE_RS, DIV_PERCENT, MARKET_LOT, INDUSTRY_P_BY_E, EPS_TTM,
     P_BY_C, PRICE_BY_BOOK, DIV_YIELD_PERCENT
     FACE_VALUE, sector, company_code, company_name 
     This finally return the dataframe for the further analysis of case study.
         
     fn_clean(self,df_final): 
     This step cleans the dataframe of our interest according to observations that is observed in raw file
     composed from fn_moneycontrol_scrape()
     
     fn_analyze(self,df_input):
     This function analyze and make some changes in dataframe if required and returns modified dataframe for
     case study analysis 
     
     fn_P_by_e(self,df_input):
     Based on dataframe resulting from fn_analyze(), P/E distiribution is understood
     
     fn_marketcap(df_input):
     OBJECTIVE: 3rd and 4th highest market cap companies sector wise.
     ASSUMPTION: DO analysis for sectors having more than 3 companies.
     Else excpetion is thrown "NOT ENOUGH COMPANIES"
     
     fn_visual(self,df_input,df_rank):
     Try to plot basic graph to see P/E distribution or sectorwise company count or sectorwise top 3 and 4 Marketcap companies

# STEP 1 EXECUTION: DATA COLLECTION
on :
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




# *************THE FINAL OUTPUTS OF FILES:************


"BASE FILE THAT CONTAINS ALL SCRAPED INFO PRIOR TO CLEANING AND ANALYZE: \
    input_scrape_moneycontrol_500_before_cleaning.csv\
    "

BASE FILE THAT CONTAINS ALL SCRAPED INFO AFTER CLEANING AND ANALYZE and SQL as well: \
    moneycontrol_after_cleaning_analyze_forsql.csv\
https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/Revision2/input_scrape_moneycontrol_443_after_cleaning_analyze_v2.csv

FOR Bucket P/E ratios in interval of 5, 11-15,16-20,21-25,...\
       KINDLY CHECK CONSOLE OUTPUT (JUPYTER/SPYDER)

FOR 3rd and 4th highest market cap companies sector wise \
       MARKETCAP_RS_CR_dessc_3_4.csv by method 1 \
       and MARKETCAP_RS_CR_dessc_3_4_v2.csv by method 2\
 https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/Revision2/MARKETCAP_RS_CR_dessc_3_4_v2.csv      
       
# ALSO BY SQL the same is solved: PLEASE READ FOR SQL STEPS

https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/README_EXECUTE_SQL.txt

 FOR SQL, (for 443/500 companies) CSV used is:
https://github.com/venkybitsian/scrape_money_control_novice/blob/master/DEMO_SCRAPE_ANALYSIS_FOR_ALL_500_COMPANIES/moneycontrol_after_cleaning_analyze_forsql.csv


NOTE: This is mine first scraping assignment, thus can aim at optimize and write generic codes for future.
SUGGESTIONS are valuable and welcome
