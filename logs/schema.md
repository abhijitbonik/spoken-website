# MongoDB validation schema for the website logs

The below is the MongoDB [validation schema](https://docs.mongodb.com/manual/core/schema-validation/) for the website event logs collection. This is to be entered in the mongo shell, after selecting the appropriate database. 

```
db.createCollection( "website_logs" , { 
   validator: { $jsonSchema: { 

      bsonType: "object", 

      required: [ "path_info", "browser_info", "method", "event_name", "visited_by","ip_address",      "country", "state_code", "city", "datetime", "first_time_visit" ], 
      properties: { 
         path_info: { 
            bsonType: "string", 
            pattern: "^/(.)*",
            description: "Webpage path. Required and must be a string beginning with /" }, 
         browser_info: { 
            bsonType: "string", 
            description: "Browser info. Required and must be a string" }, 
         method: { 
            enum: [ "GET", "POST", "HEAD", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH" ],
            description: "Required and must be a valid HTTP request method" }, 
         event_name: { 
            bsonType: "string", 
            pattern: "^event\.(.)+",
            description: "Event name. Required and must be of the form event.(...)" }, 
         visited_by: { 
            bsonType: "string", 
            description: "Username of visitor. Required and must be anonymous or a username" }, 
         ip_address: { 
            bsonType: "string",
            pattern: "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            description: "A valid IPv4 address. Required." },
         country: {
            bsonType: "string",
            description: "Country. Required and must be a country name or Unknown" },
         state_code: {
            bsonType: "string",
            description: "State. Required and must be a state name or Unknown" },
         city: {
            bsonType: "string",
            description: "City. Required and must be a city name or Unknown" },
         datetime: {
            bsonType: "date",
            description: "Datetime of log. Required." },
         first_time_visit: {
            bsonType: "bool",
            description: "Whether the visit was first time or returning. Required." },
         }
      }
   }
})
```