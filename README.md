# Api endpoints and their parameters

  
  

## landing page

Displays current status in json format.

  

## symbol

- POST

	Returns historical data on a 15 min interval
	Takes the following parameters:
	 1. symbol


## tracker

- POST
	Adds valid entries to the tracking database and sends a buy order to the respective broker.
	Takes the following parameters:
	 1. symbol
	 2. amount
- DELETE
	Sends a sell order to respective brokers. Once confirmation is received, deletes/modifies the entry in the 	database
	 1. symbol
	
	
	
## wallet

- GET
	Gets current available amount.
- POST
	Adds or removes a specified amount to the wallet. Takes the following arguments:
	1. amount
	2. action (withdraw/deposit)

