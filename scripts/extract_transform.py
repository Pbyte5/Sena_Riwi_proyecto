import pandas as pd

def proccesing () :
    df = pd.read_csv('./data/01_bronce/dataset.csv')


    ##Text columns formatting 

    text_columns = [
        'product_category',
        'customer_country',
        'traffic_source',
        'payment_method'
    ]

    df[text_columns] = df[text_columns].apply(lambda x:x.str.lower())

    ##Value standarization 
    incosistent_values = {
        'usa' : 'United States',
        'uae' : 'Unitaed Arab Emirates',
        'uk'  : 'United Kingdom'    
    }

    df['customer_country'] = df['customer_country'].replace(incosistent_values)

    ##Date formating 
    df['order_date'] = pd.to_datetime(df['order_date'])

    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    df['day'] = df['order_date'].dt.day
    df = df.drop(columns='order_date')

    ##Drop duplicated id's
    df = df.drop_duplicates(subset=['order_id'])
    ##Fill NaN
    df = df.fillna('Unknow')

    ##Export clean dataset to silver folder
    silver_dataset = df.to_csv('./data/02_silver/formated_dataset.csv')


    # Tables Dimensions

    ## Customers
    dim_customer = (
        df[['customer_id', 'customer_country']]
        .drop_duplicates(subset=['customer_id'])
        .copy()
        .reset_index(drop=True)
        )

    ## Products
    dim_products = (
        df[['product_id', 'product_category']]
        .drop_duplicates(subset=['product_id'])
        .copy()
        .reset_index(drop=True)
    )

    ## Payment methods

    dim_payment_method = (
        df[['payment_method']]
        .drop_duplicates(subset='payment_method')
        .copy()
        .reset_index(drop=True)
    )

    dim_payment_method.insert(0, 'payment_method_id', range(1, len(dim_payment_method) + 1))

    ## Traffic sources
    dim_traffic_sources = (
        df[['traffic_source']]
        .drop_duplicates(subset=['traffic_source'])
        .copy()
        .reset_index(drop = True)
    )

    dim_traffic_sources.insert(0, 'traffic_source_id', range(1, len(dim_traffic_sources) + 1))

    ## Maps

    payment_map = (
        dim_payment_method
        .set_index('payment_method')['payment_method_id']
        .to_dict())

    traffic_map = (
        dim_traffic_sources
        .set_index('traffic_source')['traffic_source_id']
        .to_dict())

    # Fact Dimensio Orders

    fact_orders = (
        df[['year', 
            'month', 
            'day', 
            'customer_id', 
            'product_id'
            ,'product_price',
            'discount_percent',
            'is_returned',
            'rating',
            'shipping_cost',
            'payment_method',
            'traffic_source',
            'revenue',
            'profit'
            ]]
        .copy()
        )
    ###Rename columns to implement maps
    fact_orders = (
        fact_orders.rename(
            columns={'payment_method' : 'payment_method_id', 'traffic_source' : 'traffic_source_id'}))

    ###Mapping
    fact_orders['payment_method_id'] = fact_orders['payment_method_id'].map(payment_map)
    fact_orders['traffic_source_id'] = fact_orders['traffic_source_id'].map(traffic_map)

    fact_orders.insert(0, 'order_id', range(1, len(fact_orders) + 1))
    
    #Export copy to gold folder
    ex_dim_payment_method = dim_payment_method.to_csv('./data/03_gold/dim_payment_method.csv')
    ex_dim_traffic_sources = dim_traffic_sources.to_csv('./data/03_gold/dim_traffic_sources.csv')
    ex_dim_products = dim_products.to_csv('./data/03_gold/dim_products.csv')
    ex_dim_customer = dim_customer.to_csv('./data/03_gold/dim_customer.csv')
    ex_fact_orders = fact_orders.to_csv('./data/03_gold/fact_orders.csv')
        
    
    #Export data to load script
    return ( dim_customer,
        dim_products,
        dim_traffic_sources,
        dim_payment_method,
        fact_orders
    )

