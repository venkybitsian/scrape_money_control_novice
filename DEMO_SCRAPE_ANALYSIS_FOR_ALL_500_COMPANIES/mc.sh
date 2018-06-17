#!/bin/ksh
#########################################################################################################
# Script        :       mc.sh                                                           #
# Purpose       :      For sqlldr the csv from money control scrape output into sql database     #
# Author        :      Venkatesh Mundada                                                                   #
# Date          :      16th June  2018                                                                  #
#                                                                                                       #
#########################################################################################################


# ConnectDB()                                                                                   #
# To connect to database.                                                                       #
#################################################################################################
ConnectDB()
{
        if [ "$DATABASE" = "" ]
        then
                echo "ERROR DATABASE environment variable should be set"
        exit
        fi
}

#THIS FUNC to DROP and recreate table using control file from csv()                                                                                      #
#To Create the Table for csv in the database                                       #
#################################################################################################

create_table_csv()
{
        echo "Trying to Drop the table if it is already there"
        echo $1
echo "hi"
echo $2
	sqlplus -S $DATABASE >> drop.log <<_END
        set pagesize 0 feedback off verify off heading off echo off;
        drop table $2;
_END
        sqlplus -S $DATABASE <<_END
        set pagesize 0 feedback off verify off heading off echo off;
        CREATE TABLE $2 (
company_code	varchar2(300)	,
company_category	varchar2(300)	,
company_name	varchar2(300)	,
BOOK_VALUE_RS	number(18,3)	,
DIV_PERCENT	number(18,3)	,
DIV_YIELD_PERCENT	number(18,3)	,
EPS_TTM	number(18,3)	,
FACE_VALUE	number(18,3)	,
INDUSTRY_P_BY_E	number(18,3)	,
MARKETCAP_RS_CR	number(18,3)	,
MARKET_LOT	number(18,3)	,
P_BY_C	number(18,3)	,
P_BY_E	number(18,3)	,
PRICE_BY_BOOK	number(18,3)	,
sector	varchar2(300)	
);
        commit;
        exit;
_END

        sed 's/TableName/'$2'/g' < ./mc.ctl > ./moneycontrol_input.ctl

        sqlldr $DATABASE control=./moneycontrol_input.ctl
        echo "Process Ended ...."
        rm ./moneycontrol_input.ctl
}







# Main()                                                                                        #
# Main functionality.                                                                           #
#################################################################################################
WorkingDir=`pwd`
count=0

Main()
{
       
        MENU=1
        clear
        DATE=`date`
        printf "\n\n"
        echo "Enter The Source Files Directory: "
        read Source
        echo "Enter The Table Name u Want"   #Give Table Name as mc ,For Further Convience
        read TableName
        echo "The Source Directory and TableName is :$Source $TableName "
        echo "Processing Started:"
        echo "$WorkingDir"
		ConnectDB
       create_table_csv $Source $TableName
}

Main

