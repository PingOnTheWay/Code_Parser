inventory = {
    1: 50,   
    2: 75,   
    3: 90,   
    4: 60,   
    5: 30    
}

product_map = {"apples": 1, "oranges": 2, "bananas": 3, "product4": 4, "product5": 5}
transaction_type_map = {"in": 1, "out": 0}  

for product_id in [1, 2, 3, 4, 5]:
    qty = 10  
    transaction_type = (product_id % 2) 
    
    if transaction_type == 1:  
        inventory[product_id] += qty
        print(f"Restocked {qty} units of product {product_id}. New inventory: {inventory[product_id]}")
    elif transaction_type == 0: 
        if inventory[product_id] >= qty:
            inventory[product_id] -= qty
            print(f"Sold {qty} units of product {product_id}. Remaining inventory: {inventory[product_id]}")
        else:
            print(f"Cannot sell {qty} units of product {product_id}. Insufficient inventory.")
