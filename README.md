# commonModel
Common methods that you can use in your project

Following are introduce of each *.py in dir of configs:

## configs.convertConfig.convertDictValueToList 
function: convert dict value to a list, return the list

## configs.convertConfig.convertToList
function: convert tuple, list to a list or an item(if the list has only one item)

## configs.timeConfig.timeConfig
function: format the date, create a date with the format you like

## configs.csvConfig.csvConfig
class: npack functions to create, write and save csv file

## configs.sqlConfig.sqlConfig
class: save and get sql model

## configs.sqlConfig.sqlConfigGetItem
function: get sql model from inside sqlConfig class

## configs.mysqlConfig.mysqlConfig
class: unpack MySQLdb functions to connect mysql, execute select_sql and \n 
close mysql connection. with fault tolerance

