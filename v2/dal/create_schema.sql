--drop database pricedata;
create database pricedata;

\c pricedata;

create domain Price as decimal(12,6); 

create table Symbols (

	Id smallint primary key,
	
	Code varchar(10),
	Description varchar(100)	
);

create table DailyPrices (
    
    Id bigserial primary key,

    SymbolId smallint references Symbols(Id),

	Date date not null,
	
	Open Price not null,
	High Price not null,
	Low Price not null,
	Close Price not null,
	CloseAdjusted Price not null,

	Volume bigint not null
);