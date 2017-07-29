-- sudo -u postgres psql -d postgres -U postgres -a -f create_schema.sql

drop database pricedata;
create database pricedata;

\c pricedata;

create domain Price as decimal(12,6); 
create domain Code as varchar(20); 
create domain Name varchar(100); 
create domain Description varchar(300); 

-- yahoo finance, YF
create table DataSource (

	Id smallint primary key,

	Name Name
);

create table Instrument (

	Id smallint primary key,
	DataSourceId smallint references DataSource(Id),
	
	DataKey Code,

	Symbol Code,
	Name Name,
	Description Description,

	IsActive boolean,
	LastUpdated date,
	SequentialFailureCount smallint
);

-- equity, exchange rate, interest rate, commodity
-- index
create table Tag (

	Id smallint primary key,

	Name Name
);

create table InstrumentTag (

	Id serial primary key,
	InstrumentId smallint references Instrument(Id),
	TagId smallint references Tag(Id)
);

create table PriceQuantum (
    
    Id bigserial primary key,
    InstrumentId smallint references Instrument(Id),

	Date date not null,
	
	Open Price not null,
	High Price not null,
	Low Price not null,
	Close Price not null,
	AdjustedClose Price not null,

	Volume bigint not null
);