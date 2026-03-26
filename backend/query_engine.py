def execute_query(query_json):
    entity = query_json.get("entity")

    # 🔥 Route based on entity
    if entity == "Order":
        from query import high_value_orders
        return high_value_orders()

    elif entity == "Delivery":
        from query import orders_not_invoiced
        return orders_not_invoiced()

    elif entity == "Invoice":
        # If you don’t have invoice logic yet
        return []

    return []