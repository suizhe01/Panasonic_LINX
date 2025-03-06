import json

file_path = "Json_Product.txt"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

products = data.get("value", [])
header = "Created On|Material|Model Code|Plant|Loading Group|Neg. stocks in plant|Storage Location|Standard price|Valuation Class|Sales Organization|Distribution Channel|Item category group|Delivering Plant|Warehouse Number|Storage Section Ind.|Stock placement|Loading equip. qty"
lines = [header]

def get_product_plant_details(product):
    product_plant = product.get("_ProductPlant", [{}])
    product_plant_sales = product.get("_ProductPlantSales", [{}])

    if isinstance(product_plant, list) and product_plant:
        first_plant = product_plant[0]
        plant = first_plant.get("Plant", "")
        neg_stocks_in_plant = first_plant.get("IsNegativeStockAllowed", "")

        loading_group = ""
        if isinstance(product_plant_sales, list) and product_plant_sales:
            loading_group_key = product_plant_sales[0].get("LoadingGroup", "")
            loading_group = first_plant.get(loading_group_key, "")

        return plant, neg_stocks_in_plant, loading_group

    return "", "", ""

def get_product_price_and_valuation(product):
    product_valuation = product.get("_ProductValuation", [])

    if isinstance(product_valuation, list) and product_valuation:
        first_item = product_valuation[0]
        return first_item.get("StandardPrice", ""), first_item.get("ValuationClass", "")

    return "", ""

def get_product_sales_delivery(product):
    product_sales_delivery = product.get("_ProductSalesDelivery", [])

    if isinstance(product_sales_delivery, list) and product_sales_delivery:
        first_item = product_sales_delivery[0]
        return (
            first_item.get("ProductSalesOrg", ""),
            first_item.get("ProductDistributionChnl", ""),
            first_item.get("ItemCategoryGroup", ""),
            first_item.get("SupplyingPlant", "")
        )

    return "", "", "", "" 

def get_ewm_warehouse_details(product):
    product_ewm_warehouse = product.get("ProductEWMWarehouse", [])

    if isinstance(product_ewm_warehouse, list) and product_ewm_warehouse:
        first_warehouse = product_ewm_warehouse[0]
        return first_warehouse.get("EWMWarehouse", ""), first_warehouse.get("EWMStorageSectionMethod", "")

    return "", ""

for product in products:
    created_on = product.get("CreationDate",'')
    material = product.get("Product",'')
    model_code = product.get("ProductDocumentNumber",'')

    # _ProductPlant
    plant, neg_stocks_in_plant, loading_group = get_product_plant_details(product)
    
    storage_location = '' # not exist in mapping file provided by sigar

    # _ProductValuation
    standard_price, valuation_class = get_product_price_and_valuation(product)

    # _ProductSalesDelivery
    sales_organization, distribution_channel, item_category_group, delivering_plant = get_product_sales_delivery(product)

    # ProductEWMWarehouse
    warehouse_number, storage_section = get_ewm_warehouse_details(product)

    stock_placement = '' # not exist in mapping file provided by sigar
    loading_equip_qty = '' # Still in development process

    # Format the line
    line = f"{created_on}|{material}|{model_code}|{plant}|{loading_group}|{neg_stocks_in_plant}|{storage_location}|{standard_price}|{valuation_class}|{sales_organization}|{distribution_channel}|{item_category_group}|{delivering_plant}|{warehouse_number}|{storage_section}|{stock_placement}|{loading_equip_qty}"
    
    # Append to lines list
    lines.append(line)

# Save the formatted data into a text file (ZLINX1_Result_.txt)
output_file = "ZLINX1_Result_Test.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(lines))
