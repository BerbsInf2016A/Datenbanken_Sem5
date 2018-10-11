setwd("C:/Users/Andre/Downloads/Chicago-mvt-data-master")
install.packages("RPostgreSQL")
require("RPostgreSQL")
 
# create a connection
# save the password that we can "hide" it as best as we can by collapsing it
pw <- {
  "example"
}
 
# loads the PostgreSQL driver
drv <- dbDriver("PostgreSQL")
# creates a connection to the postgres database
# note that "con" will be used later in each connection to the database
con <- dbConnect(drv, dbname = "chicago_taxi",
                 host = "localhost", port = 5432,
                 user = "example", password = pw)
rm(pw) # removes the password

# query the data from postgreSQL 
df_postgres <- dbGetQuery(con, "SELECT long.longitude, lat.latitude
from raw_data as raw
join pickup_latitude as lat on lat.id = raw.pickup_latitude
join pickup_longitude as long on long.id = raw.pickup_longitude")

write.csv(df_postgres, file = "pickup.csv")

# close the connection
dbDisconnect(con)
dbUnloadDriver(drv)
 
