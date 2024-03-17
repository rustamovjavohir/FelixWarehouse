# Felix WareHouse

Develop a combination of materials stored in the warehouse that will be needed to create products. Return information
about missing material.

## Documentation

[Documentation](https://felix-its.uz/media/Backend_st_Python.pdf)

## API Reference

#### Get need materials for create products

```http
  POST /api/factory/
```

    ```json
    {
        "product": [
            {
                "id": 1,
                "product_qty": 30
            },
            {
                "id": 2,
                "product_qty": 20
            }
        ]
    }
    ```




