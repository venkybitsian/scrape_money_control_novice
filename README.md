# scrape_money_control_novice
Data is ubiquitously scattered and web scraping plays critical role to fetch data in form of tables/dataframes, so that data analysis can be initiated:
PART 1:
EXTRACT the 500 companies and their dynamic links
PART 2:
Extract the basic parameters for stock related finnancial info on these 500 companies and create a final dataframe.
I observe 11 input parameters:
'LINK', 'company_code', 'company_category', 'company_name',
       'BOOK VALUE (Rs)', 'DIV (%)', 'DIV YIELD.(%)', 'EPS (TTM)',
       'FACE VALUE (Rs)', 'INDUSTRY P/E', 'MARKET CAP (Rs Cr)', 'Market Lot',
       'P/C', 'P/E', 'PRICE/BOOK', 'sector'
'LINK': This is dynamic link of stock
'company_code': This is manually generated abbreviation for understanding company with company code
'company_category':
