from sqlalchemy import create_engine, text
from extract_transform import proccesing

database_url = "postgresql+psycopg2://postgres:Qwe.123*@localhost:5432/prueba_desempeno"

engine = create_engine(database_url)

with engine.connect() as connection :
    connection.execute(text(
        '''
        CREATE TABLE IF NOT EXISTS dim_customers(
            customer_id INT PRIMARY KEY,
            customer_country VARCHAR(80)
        );
        
        CREATE TABLE IF NOT EXISTS dim_products(
            product_id INT PRIMARY KEY,
            product_category VARCHAR(50)
        );
        
        CREATE TABLE IF NOT EXISTS dim_payment_methods(
            payment_method_id INT PRIMARY KEY,
            payment_method VARCHAR(40)
        );
        
        CREATE TABLE IF NOT EXISTS dim_traffic_sources(
            traffic_source_id INT PRIMARY KEY,
            traffic_source VARCHAR(40)
        );
        
        CREATE TABLE IF NOT EXISTS fact_orders(
            order_id INT PRIMARY KEY,
            year INT,
            month INT,
            day INT,
            customer_id INT,
            product_id INT,
            product_price DECIMAL(10,2),
            discount_percent INT,
            is_returned INT,
            rating DECIMAL (2,1),
            shipping_cost DECIMAL(10,2),
            payment_method_id INT,
            traffic_source_id INT,
            revenue DECIMAL(10,2),
            profit DECIMAL(10,2),
            
            FOREIGN KEY(customer_id)
                REFERENCES dim_customers(customer_id),
            FOREIGN KEY(product_id)
                REFERENCES dim_products(product_id),
            FOREIGN KEY(payment_method_id)
                REFERENCES dim_payment_methods(payment_method_id),
            FOREIGN KEY(traffic_source_id)
                REFERENCES dim_traffic_sources(traffic_source_id)
        );
        '''))
    connection.commit()
    
    #Load data from gold folder to postgres
    (dim_customers, 
    dim_products, 
    dim_traffic_sources, 
    dim_payment_methods, 
    fact_orders) = proccesing()

    dim_customers.to_sql(
        'dim_customers',
        if_exists = 'append',
        con=engine,
        index = False
    )
    dim_products.to_sql(
        'dim_products',
        if_exists = 'append',
        con=engine,
        index = False
    )
    dim_traffic_sources.to_sql(
    'dim_traffic_sources',
    if_exists = 'append',
    con=engine,
    index = False
    )
    dim_payment_methods.to_sql(
    'dim_payment_methods',
    if_exists = 'append',
    con=engine,
    index = False
    )
    fact_orders.to_sql(
    'fact_orders',
    if_exists = 'append',
    con=engine,
    index = False
    )
    
    connection.close()








