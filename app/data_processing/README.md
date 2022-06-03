# Data Processing Service
This service will read/pull from a csv formatted source, process the raw data, then store them in a SQL database.

## Data Processing Strategy
### Storing
For this project, I use a SQL database instead of No-SQL database mainly for two reasons.
- The given data is structured and comprehensive, which means that schema for the database will be relatively stable. The flexibility provided by No-SQL database may not benefit this project much.
- When using No-SQL database, typically we will store frequently accessed data together, and without normalization, the database will be larger than that of SQL database due to duplication. Also, considering Review record is relatively large, using SQL database can save a lot storage.  

For this project, I choose to use SQLite, because its simplicity and full support in Python.
Database schema can be found in [here](../simple_db/README.md)

### Sanitizing
Based on the observation aforementioned, there are a few issues needed to be addressed by sanitization. 
- encoding. Random characters, such as `â€˜`, indicate that the encoding for this file is not `ASCii`. The file will be encoded to UTF-8.
- a list of elements. Columns, such as Genres and Regions, contains a list of elements and they are represented as `{x...}`. Therefore, sanitization will remove the curly bracket.
- Escaping. Escaping string is important and necessary to prevent attacks, such as SQL injection. For this part, I will rely on the  Object Relational Mapper libary to handle it for me.

### Normalizing
To make data consistent among the whole file, I apply following steps:
- `created_at` and `updated_at` contain different timezone information, naming PST and PDT, both datetime data will be convert to `America/Los_Angeles`-based timezone.
- Empty cells will be replaced with empty string.
- All leading and trailing white space will be removed. This also applies to element for the list, for example `{US, AU, UK, JP}` will be normalized to `US,AU,UK,JP`.

### Indexing
Based on the usage of the database, I assume that there will be much more database accessing than database injection or database modification. Therefore, we can create a large number of index to improve the SELECT query performance. Due to the simplicity of the project, I only create a few indexes based on the api endpoints and accepted custom parameters.
- Review id
- Review created year
- Review score