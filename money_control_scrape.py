# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 18:27:21 2018

@author: vemu0615
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 14:56:26 2018

@author: vemu0615
"""

##########################NOTE::::
########################PLEASE READ BEFORE EXECUTION #################
"""
Assumptions :
    As assignment suggests, cursory analysis of stock companies, 
    that focus on understanding 2 params: MARKETCAP_RS_CR and P/E(P_BY_E) ratio
    and also various sectors based performance and distribution
    Thus I remove the cases where MARKETCAP_RS_CR and P/E(P_BY_E) ratio
    for CONSOLIDATED cases is absent.
    AS1: Basically we have 2 possible values. But I consider only CONSOLIDATED
    AS2: Remove NAN cases
    AS3: Consider MARKETCAP_RS_CR based ranking for only those sectors who have > 4 companies
    AS4: I dont write generic code for scrape. Code will impact, if website changes format
    and reduce or increase no of parameters
    AS5: in part 5 description below
    
STEP 1: DATA SCRAPE
Part 1 consists of web scraping of html links and list of 500 companies which appears
on :
    www.moneycontrol.com/india/stockpricequote
    When code is excuted, its necessary to either provide:
        www.moneycontrol.com/india/stockpricequote
        or
        provide list of companies in list companybook
 links_moneycontrol_v5.csv willbe file composed of all 500 companies on part 1 
completion

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

"""
 
#########################PART 1 ################################3   
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np  
import time  
    #---TRYING TO MAKE DICTIONARY
# Values will store the value of various params like p/e, marketcap, book value etc    
values = []
print ("Please mention what all companies you want to extract: PRESS 1 if you want all 500 companies. PRESS 2, if you want to provide list")
choice_input=input("ENTER THE VALUE:")
url = input("Enter a website to extract the URL's from !!!!NOTE!!!: ALWAYS copy from browser the link:: www.moneycontrol.com/india/stockpricequote:")
print (url)
r  = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data)
mydivs = soup.findAll("a", {"class": "bl_12"})

for link in mydivs:
     value=link.get('href')
     values.append(value)
     #print(link.get('href'))
    
    
    
#for link in soup.find_all('a'):
    #print(link.get('href'))#
test_df = pd.DataFrame({'LINK': values})
print(test_df.info())    
e='a'
test_df['company_code'] = e
test_df['company_category'] = e
test_df['company_name'] = e


#FILL company_code
# FOR EXAMPLE: http://www.moneycontrol.com/india/stockpricequote/banksprivatesector/yesbank/YB
#has company code located as substring value after rightmost appearence of /
# SIMILAR BEHAVIOR for every 500 companies on http://www.moneycontrol.com/india/stockpricequote
for index, row in test_df.iterrows():
    i= (row["LINK"])
    print (row.LINK)
    print(i[i.rfind('/')+1:])  
    test_df.loc[index, 'company_code'] =(i[i.rfind('/')+1:])
#FILL company_category 
# FOR EXAMPLE: http://www.moneycontrol.com/india/stockpricequote/banksprivatesector/yesbank/YB
#has company_category located as substring value only after immediate right  of http://www.moneycontrol.com/india/stockpricequote/
# which comes at 50 th position and from that 50th position to next occurance of '/'    
for index, row in test_df.iterrows():
    i= (row["LINK"])
    print(i[50:50+i[50:].find('/') ])
    test_df.loc[index, 'company_category'] =(i[50:50+i[50:].find('/') ])
#FILL company_name
#similarly this is automatically understood    
for index, row in test_df.iterrows():
    i= (row["LINK"])
    test_df.loc[index, 'company_name'] =(i[50+i[50:].find('/')+1: i.rfind('/')])

# deleting unwanted junk rows
test_df = test_df[test_df.LINK != 'javascript:;']
#MAKE dictionary
d= dict([(i,a) for i, a in zip( test_df.company_code, test_df.LINK)])
#print (d)    
for k,v in d.items():
            print(k, 'corresponds to', v)
            
            
test_df.to_csv('links_moneycontrol_v6.csv')    

##########################################################################
#final  dictionary
# based on initial input choice at stdin, the dictionary is created either for list of few companies to analyze or
# for all 500 companies
if choice_input == '2':
    
    input_flag=''
    while input_flag == '':
     codes=[]
     lim= int(input("HOW MANY COMPANY CODES TO ANALYZE?"))
     print ("Enter all codes in 1 go, same as quantity YOU EXPRESS ")
     codes = [str(x) for x in input().split()]
     if len(codes)!= lim:
        print("RE-ENTER THE COMPANY CODES AGAIN, SAME AS COMPANY CODES TO ANALYZE?" )
     else:
      companybook=dict((k, d[k]) for k in codes)
      input_flag='INPUT_FINISH_FROM_USER'
      print ("INPUT FINISH AND BELOW IS LIST FOR FURTHER DATA EXTRACTION AND ANALYSIS")
      print (companybook)  


#############THIS BLOCK will choose if we want to do analysis of all 500 companies
if choice_input == '1':
 companybook=d
 print ("INPUT FINISH AND all 500 companies processing begins FOR FURTHER DATA EXTRACTION AND ANALYSIS")
#############3


#########################PART 1 ends COMPANY LIST companybook  is created ################################


#########################PART 2: SCRAPING BASED ON COMPANY LIST companybook ################################3   
   
# Values will store the value of various params like p/e, marketcap, book value etc    
# names will store parameter names as recovered from beautiful soup objects
# url1 will store the hyperlinks lists corresponding to each company evaluation, which is appended
# sectors will store company sector as derived from sec beautiful soup object
# C_CODE is company code list
names = []
values = [] 
url1 = [] 
sectors= [] 
C_CODE= [] 
    #C_CODE = input("Enter COMPANY CODE")
for k,v in companybook.items():
            print(k, 'corresponds to', v)
            print ("***SCRAPING OF ABOVE COMPANY IN PROGRESS***")

            page = ''
            wait_param=0
            # This try catch necessary, coz server was observed refuse connection, if we try to 
            # approach moneycontrol more than threshold value
            #thus necessary to have some pause and retry and not quit as exception
            #although necessary to exit block, this page='a' is initialized, after 50 sec wait
            while page == '':
                    try:
                        response  = requests.get(v)
                        page = 'a'
                        break
                    except:
                        if wait_param<10:
                         print("Connection refused by the server..")
                         print("Let me sleep for 5 seconds")
                         print("ZZzzzz...")
                         time.sleep(5)
                         print("Was a nice sleep, now let me continue...")
                         wait_param=wait_param+1
                         continue
                        else:
                            page = 'a'
            #print(response.text[:500])
            html_soup = BeautifulSoup(response.text, 'html.parser')
        #"""
        #In HTML THIS IS WHAT WAS OBSERVED, And based on that,
        #necessary to identify appropriate tags like div, class, href, etc.
        #and use html soup
        #<div class="FL gL_10 UC">MARKET CAP (Rs Cr)</div>
        #<div class="FR gD_12">681,869.24</div>
        #<!-- Standalone data starts here -->
        #<div id="mktdet_1" name="mktdet_1" style="display:none;">
        #"""
        #CL
            #mc = html_soup.find_all('div', class_ = 'FL gL_10 UC')
            #vc = html_soup.find_all('div', class_ = 'FR gD_12')
            cc = html_soup.find_all("div",  {"class": ["FL gL_10 UC", "FR gD_12","mktdet_1"]})
            sec = html_soup.find_all('div', class_ = 'gry10')
            #sec[0].a
            #sec[0].a.text
            
            url2=k
            i=0
            for s in sec:
                if i==0:
                 sector=s.a.text
                 sectors.append(sector)
                 C_CODE.append(url2)
                i=i+1
            i=0    
        # Extract data from individual html code block: cc[0], cc[1], cc[2]...
            for container in cc:
                  
# If the container has got i value as even it is basically PARAMETER NAME: ex P/E, MARKETCAP
#  If the container has got i value as odd it is basically PARAMETER VALUE:
#i value 'even' and less than 22 corresponds to all rows of STANDALONE Situation of 
#particular company:
#These 22 rows divide: 11 for NAMES and 11 for VALUES
                    
                    # The name
                        if i%2 == 0 and i<=21:
                            name = container.text
                            names.append(name)
                            url1.append(url2)
                            
                        if i%2 > 0 and i<=21:
                    # The value
                            value=container.text
                            values.append(value)
                            #url1.append(url2)
                        i=i+1
                        #print(i)
                      
            
            
            test_df1 = pd.DataFrame({'parameter': names,
                                   'magnitude': values,
                                  'DETAIL': url1 })
            sectors_df=pd.DataFrame({'sector': sectors,
                                     'company_code':C_CODE})
            df_0=test_df1
            test_df1.to_csv('example_moneycontrol_v5.csv')
            #the below block df, only serves for debugging, but still kept, as it creates the final desired structure we aim for CSV
            df = pd.DataFrame({names[0]: [values[0]],
                                   names[1]: [values[1]],
                                   names[2]: [values[2]],
            					   names[3]: [values[3]],
            					   names[4]: [values[4]],
            					   names[5]: [values[5]],
            					   names[6]: [values[6]],
            					   names[7]: [values[7]],
            					   names[8]: [values[8]],
            					   names[9]: [values[9]],
            					   names[10]: [values[10]],
                                   'company_code':url1[0]})
            df2 = df
            len(values)/10
            df2=df2.truncate(before=5500, after=5500)
            # Here we have 11 parameters, thus below code helps to create a transpose which is desired csv for nice analyze
            for j in list(range(int(len(values)/11))):
                if (10*j)<len(values)-10:
                 df = pd.DataFrame({names[0]: [values[0+(10*j)+j]],
                                   names[1]: [values[1+(10*j)+j]],
                                   names[2]: [values[2+(10*j)+j]],
            					   names[3]: [values[3+(10*j)+j]],
            					   names[4]: [values[4+(10*j)+j]],
            					   names[5]: [values[5+(10*j)+j]],
            					   names[6]: [values[6+(10*j)+j]],
            					   names[7]: [values[7+(10*j)+j]],
            					   names[8]: [values[8+(10*j)+j]],
            					   names[9]: [values[9+(10*j)+j]],
            					   names[10]: [values[10+(10*j)+j]],
                                   'company_code':url1[10+(10*j)+j]
                                   })
                #print(df)
                df2 = df2.append(df)
            
            
            
df2.to_csv('example_moneycontrol_v5_transpose.csv')
result=pd.merge(test_df, df2, on="company_code")
result_f=pd.merge(result, sectors_df, on="company_code")
###NECESSARY merge to merge the sectors also
result_f.to_csv('input_scrape_moneycontrol_500.csv')
print ("$$$$$$$$$$$$$$$ SCRAPING IS COMPLETE, Plz check input_scrape_moneycontrol_500.csv $$$$$$$$$$$$$$$$")
print ("NOW CLEANING AND DATATYPE CONVERSIONS BEGINS..\
       ....")
#ABOVE FILE NEEDS CLEANING AND DATATYPE CONVERSIONS which is all in below PART 3
#########################PART 2 ends ################################

#########################PART 3  ################################3   

######################CLEANING############################

######################CLEANING############################
##REMOVE unwanted symbols
result_f['P/E'] = result_f['P/E'].str.replace(',', '')
result_f['DIV (%)'] = result_f['DIV (%)'].str.replace('%','')
result_f['DIV YIELD.(%)'] = result_f['DIV YIELD.(%)'].str.replace('%','')
result_f['MARKET CAP (Rs Cr)'] = result_f['MARKET CAP (Rs Cr)'].str.replace(',', '')

result_f=result_f.replace('-', np.NaN)
result_f = result_f.replace({
        'DIV YIELD.(%)': '',
        'P/E': '',
        'EPS (TTM)': ''
    }, np.nan)
result_f=result_f.replace('%', '')
# removing rows where company_code is null
result_f = result_f[result_f['company_code']!= '']

#rename columns for SQL as well ease
result_f = result_f.rename(columns={'LINK': 'LINK', 'BOOK VALUE (Rs)': 'BOOK_VALUE_RS'
                                    ,'DIV (%)': 'DIV_PERCENT', 'DIV YIELD.(%)': 'DIV_YIELD_PERCENT'
                                    ,'EPS (TTM)': 'EPS_TTM', 'FACE VALUE (Rs)': 'FACE_VALUE'
                                    ,'INDUSTRY P/E': 'INDUSTRY_P_BY_E', 'MARKET CAP (Rs Cr)': 'MARKETCAP_RS_CR'
                                    ,'P/C': 'P_BY_C', 'P/E': 'P_BY_E'
                                    ,'PRICE/BOOK': 'PRICE_BY_BOOK'
                                    ,'Market Lot': 'MARKET_LOT'}) 
result_f['EPS_TTM'] = result_f['EPS_TTM'].str.replace(',', '')  
result_f['P_BY_C'] = result_f['P_BY_C'].str.replace(',', '')    
  
#changing datatype

result_f['BOOK_VALUE_RS'] = result_f.BOOK_VALUE_RS.astype(float)
result_f['DIV_PERCENT'] = result_f.DIV_PERCENT.astype(float)
result_f['DIV_YIELD_PERCENT'] = result_f.DIV_YIELD_PERCENT.astype(float)
result_f['EPS_TTM'] = result_f.EPS_TTM.astype(float)
result_f['FACE_VALUE'] = result_f.FACE_VALUE.astype(float)
result_f['INDUSTRY_P_BY_E'] = result_f.INDUSTRY_P_BY_E.astype(float)
result_f['MARKETCAP_RS_CR'] = result_f.MARKETCAP_RS_CR.astype(float)
result_f['P_BY_C'] = result_f.P_BY_C.astype(float)
result_f['P_BY_E'] = result_f.P_BY_E.astype(float)
result_f['PRICE_BY_BOOK'] = result_f.PRICE_BY_BOOK.astype(float)
result_f.dtypes
#CHECKING DUPLICATES
result_f.head()
result_f.shape
result_f[result_f.company_code.duplicated()]
if result_f.company_code.duplicated().sum()==0:
    print  ('No DUPLICATE data of COMPANIES')
#result_f.to_csv('input_scrape_moneycontrol_443_after_cleaning.csv')

###FINAL FILE ABOVE FOR DATA ANALYSIS
 #########################PART 3 ends ################################

#########################PART 4  ################################3     
######################################################################
######################################################################
##############ANALYSIS#########################################3
result_f.head()
result_f.index
result_f.columns
result_f.describe(include='all')
#THERE ARE 90 SECTORS, 500 COMPANIES, PHARMACEUTICALS has max of 39 companies
result_f.describe(include=['object'])
result_f.describe()
#result_f['sector'].value_counts().plot(kind='bar')
result_f.groupby('company_category').size().plot(kind='bar',figsize=(13,9))
#List unique values in the df['name'] column
#checking the values and data we re interested into: MARKETCAP_RS_CR and P_BY_E
#NAN is observed, which must be removed, as no other way to calculate the values
result_f.isnull().sum()
result_f.loc[0:,['company_code','MARKETCAP_RS_CR','P_BY_E']]

# if 'any' values are missing in a row (considering only 'MARKETCAP_RS_CR' and 'P_BY_E'), then drop that row
result_f.dropna(subset=['MARKETCAP_RS_CR','P_BY_E'], how='any').shape
result_f['P_BY_E'].value_counts(dropna=False)
#result_f = result_f[np.isfinite(result_f['P_BY_E'])]
result_f=result_f.dropna(subset=['MARKETCAP_RS_CR','P_BY_E'], how='any')


result_f.to_csv('input_scrape_moneycontrol_443_after_cleaning_analyze_v2.csv')
print ("******************$$$ CLAENING IS COMPLETE, Plz check input_scrape_moneycontrol_443_after_cleaning_analyze_v2.csv $$$$$$$$$$$$$$$$")
print ("****************************************")
print ("NOW ANALYZE BEGINS FOR P/E..\
       .....")
###FINAL FILE ABOVE FOR questions and analysis and SQL

###443 companies available, as 57 companies didnt have P/E ratio

#########################PART 4 ends ################################3     



#########################PART 5 starts  ################################3     

# cleaning rows which has empty P/E ratio
#result_f = result[result['P/E']!= '-']

## we need P/E ranges basically and companies under those ranges 
#Bucket P/E ratios in interval of 5, 11-15,16-20,21-25,...,66-70, then output list of
#companies in each bucket
t=0.0
for x in range(0,15):
 print ("BUCKET IS:", t,"to:", t+5)   
 print(result_f[(result_f['P_BY_E']>=t) & (result_f['P_BY_E']<t+5) ].loc[0:,['company_code','MARKETCAP_RS_CR','P_BY_E']])
 t=t+5

###THERE ARE OUTLIERS in P/E
print ("OUTLIERS OF P/E, having more value of P/E than 70, which can either be fixed by reverify \
       or data can be normnalized using modifed log values. Latter wasnt expected and not done ")
print(result_f[(result_f['P_BY_E']>=70) & (result_f['P_BY_E']<20000) ].loc[0:,['company_code','MARKETCAP_RS_CR','P_BY_E']])


#########################PART 5 ends ################################3   


#########################PART 6 ################################3   
print ("****************************************")
print ("NOW ANALYZE BEGINS for 3rd and 4th highest market cap companies sector wise.\
       .....")
### a. 3rd and 4th highest market cap companies sector wise.

#How many sectors have more than 4 companies
print ("In analysis data-How many sectors have more than 4 companies")
print(result_f.company_category.value_counts())

# generate 'sector_companies_count' DF
sector_companies_count = pd.DataFrame(result_f.company_category.value_counts().reset_index())
sector_companies_count.columns = ['company_category', 'count_comp_cat']


# merge 'result_f' & 'sector_companies_count'
result_f = pd.merge(result_f, sector_companies_count, on='company_category')
#result_f.dtypes
df_cc=result_f[result_f.count_comp_cat >= 4]
#df_cc.shape
##our sectors of interest in which need to find 3rd and 4th top MARKETCAP_RS_CR
## df_cc is the dataframe which has count of companies per sector for each company and also only
#subset of companies that comes under sector which has more than 3 companies under them

############## METHOD 1:##################
df_cc.company_category.value_counts()
df_cc1=df_cc.sort_values('MARKETCAP_RS_CR',ascending = False).groupby('company_category').head(4)
df_cc2=df_cc1.sort_values('MARKETCAP_RS_CR',ascending = True).groupby('company_category').head(2)

#df_cc1.to_csv('MARKETCAP_RS_CR_dessc_.csv')
df_cc2.to_csv('MARKETCAP_RS_CR_dessc_3_4.csv')
print ("FOR 3rd and 4th highest market cap companies sector wise \
       MARKETCAP_RS_CR_dessc_3_4.csv by method 1 \
       ")
#print (df_cc2.head())


# =============================================================================
# ############## METHOD 2:##################
# 
# import pandasql
# 
# def complex_sql(df):
#     result_df=df
#    
#    q = 
#    """
# 	  	  SELECT MARKETCAP_RS_CR, company_category, company_name, rnk
#         FROM
#        (  	   
# 	select  MARKETCAP_RS_CR, company_category, company_name, rank() over (partition by company_category order by MARKETCAP_RS_CR DESC) as rnk
#        from result_df
#        where company_category in ( SELECT
#         company_category
#         from result_df 
#         group by 
#         company_category
#         having count(1) >3 )
# 		VV
#        where VV.rnk in (3,4)
#         """
#     
#     # Execute your SQL command against the pandas frame
#     sql_solution = pandasql.sqldf(q, locals(),drv = "SQLite")
#     return sql_solution  
# 
# pandas_df = complex_sql(result_f)
#
# =============================================================================
############## METHOD 3:##################

# =============================================================================
# 
# 
g=df_cc.groupby('company_category')
# df_cc['rank_company_category'] = g['MARKETCAP_RS_CR'].rank(method='max')
# df_cc[df_cc.rank_company_category.isin(['3','4'])]
# df_cc[df_cc.rank_company_category.isin(['3','4'])].to_csv('MARKETCAP_RS_CR_dessc_3_4_v2.csv')
# print ("FOR 3rd and 4th highest market cap companies sector wise \
#        MARKETCAP_RS_CR_dessc_3_4.csv by method 1 \
#        and MARKETCAP_RS_CR_dessc_3_4_v2.csv by method 2\
#       \
#         ")
#df_cc.loc[:, 'rank_company_category'] = g['MARKETCAP_RS_CR'].rank(method='max')
#p=g['MARKETCAP_RS_CR'].rank(method='max')
#df_cc.loc[:, 'rank_company_category']=p
#C:\Users\vemu0615\AppData\Local\Continuum\anaconda3\lib\site-packages\pandas\core\indexing.py:537: SettingWithCopyWarning: 
# #WARNING
# Try using .loc[row_indexer,col_indexer] = value instead
# 
# See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
#   self.obj[key] = _infer_fill_value(value)
# C:\Users\vemu0615\AppData\Local\Continuum\anaconda3\lib\site-packages\pandas\core\indexing.py:537: SettingWithCopyWarning: 
# A value is trying to be set on a copy of a slice from a DataFrame.
# Try using .loc[row_indexer,col_indexer] = value instead
# 
##THUS AFTER SOME GOOGLE, UNDERSTOOD ISSUE WITH PYTHON FOR CHAIN INDEXING
##SOLUTION LIES, MAKE PYTHON UNDERSTAND EXPLICITLY THAT WE WORK ON COPY
bf_cc = df_cc.copy()
bf_cc.loc[:, 'rk'] = g['MARKETCAP_RS_CR'].rank(method='max',  ascending=False)
bf_cc.loc[:,('company_code','sector','MARKETCAP_RS_CR','rk')]
bf_cc[bf_cc.rk.isin(['3','4'])].to_csv('MARKETCAP_RS_CR_dessc_3_4_v2.csv')
# =============================================================================
##########FINAL OUTPUTS:::

print ("*********************FINAL OUTPUT FILES************************* \
       ***************************************************************** \
      ")

print ("FOR FINAL OUTPUTS, PLEASE CHECK FILES BELOW GENERATED")
print ("*****************************************************************")
print ("*****************************************************************")

print ("THE RAW FILE from website scrape, before pivot or transpose:\
       example_moneycontrol_v5.csv\
       ")
print ("*****************************************************************")
print ("*****************************************************************")
print ("BASE FILE THAT CONTAINS ALL SCRAPED INFO PRIOR TO CLEANING AND ANALYZE: \
    input_scrape_moneycontrol_500.csv\
    ")
print ("*****************************************************************")
print ("*****************************************************************")
print ("BASE FILE THAT CONTAINS ALL SCRAPED INFO AFTER CLEANING AND ANALYZE and SQL as well: \
    input_scrape_moneycontrol_443_after_cleaning_analyze_v2.csv\
    ")
print ("*****************************************************************")
print ("*****************************************************************")
print ("FOR Bucket P/E ratios in interval of 5, 11-15,16-20,21-25,...\
       KINDLY CHECK CONSOLE OUTPUT\
       ")
print ("*****************************************************************")
print ("*****************************************************************")
print ("FOR 3rd and 4th highest market cap companies sector wise \
       MARKETCAP_RS_CR_dessc_3_4.csv by method 1 \
       and MARKETCAP_RS_CR_dessc_3_4_v2.csv by method 2\
       ")

print ("*****************************************************************")
print ("*****************************************************************")
print ("*****************************************************************")
print ("*****************************************************************")


#####VISUALS##############
print("SOME VISUALS AS BELOW:")
print ("P/E distribution and count of companies\
       ")
print ("*****************************************************************")
print ("*****************************************************************")
bin_values = np.arange(start=-30, stop=500, step=5)
result_f['P_BY_E'].hist(bins=bin_values, figsize=[18,9])

import matplotlib.pyplot as plt
import numpy as np
print ("*****************************************************************")
print ("*****************************************************************")
print ("MARKETCAP_RS_CR distribution and count of companies \
       ")
print ("*****************************************************************")
print ("*****************************************************************")
bin_values = np.arange(start=result_f.MARKETCAP_RS_CR.min()-100, stop=result_f.MARKETCAP_RS_CR.max()+1000, step=500)
result_f['MARKETCAP_RS_CR'].hist(bins=bin_values, figsize=[18,9])

print ("*****************************************************************")
print ("*****************************************************************")
print ("sectorwise 3rd and 4th and marketcap value on y axis \
       ")
print ("*****************************************************************")
print ("*****************************************************************")
fig, ax = plt.subplots()
fig.set_size_inches(28, 15)
ax.bar(left=df_cc2.sector, height=df_cc2['MARKETCAP_RS_CR'], width=0.3)
ax.set_xlabel("marketcap")
ax.set_ylabel("sectorwise 3rd and 4th postition")
ax.set_title("sectorwise 3rd and 4th postition marketcap distribution")
ax.grid(color='g', linestyle='--', linewidth=0.5)
plt.xticks(rotation='vertical')


print ("*****************************************************************")
print ("*****************************************************************")
print ("companywise 3rd and 4th and marketcap value on y axis \
       ")
print ("*****************************************************************")
print ("*****************************************************************")
fig, ax = plt.subplots()
fig.set_size_inches(40, 25)
ax.bar(left=df_cc2.company_name, height=df_cc2['MARKETCAP_RS_CR'], width=0.5)
plt.xlabel('xlabel', fontsize=45)
ax.set_xlabel("marketcap")
ax.set_ylabel("company wise 3rd and 4th postition")
ax.set_title("company wise  3rd and 4th postition marketcap distribution")
ax.xaxis.label.set_size(7)
ax.grid(color='g', linestyle='--', linewidth=0.5)
plt.xticks(rotation='vertical')
ax.tick_params(direction='out', length=7, width=7 )
###########################################EXTRA

# =============================================================================
# pd.read_csv('input_scrape_moneycontrol_500.csv')
# pd.read_csv('links_moneycontrol_v5.csv')
# result_f.MARKETCAP_RS_CR.min()
# result_f.MARKETCAP_RS_CR.max()
# result_f.dtypes
# =============================================================================

