from django.db.models import QuerySet

from apps.factory.models import Product, ProductMaterial, Warehouse, Material
from math import ceil, floor


class FactoryService:
    def __init__(self, ):
        self.product = Product
        self.product_material = ProductMaterial
        self.warehouse = Warehouse
        self.material_list: list = []
        self.mat_result: list = []
        self.result: list = []

    @property
    def active_w_materials(self) -> QuerySet[Warehouse]:
        """
        :return: QuerySet[Warehouse]
        Return active materials from warehouse
        """
        return self.warehouse.objects.filter(remainder__gt=0, is_active=True)

    def get_product(self, product_id):
        """
        :param product_id: int
        Return product by id
        """
        return self.product.objects.get(id=product_id)

    def get_product_material(self, product_id) -> QuerySet[ProductMaterial]:
        """
        :param product_id: int
        Return product materials by product id
        """
        return self.product_material.objects.filter(product_id=product_id)

    def get_materials_from_w(self, material_id) -> QuerySet[Warehouse]:
        """
        :param material_id: int
        Return materials from warehouse by material id
        """
        return self.active_w_materials.filter(material_id=material_id)

    def data_json(self, warehouse_id: int | None, material_name: str,
                  remainder: float, price: float | None, *args, **kwargs) -> dict:
        return {
            'warehouse_id': warehouse_id,
            'material_name': material_name,
            'remainder': remainder,
            'price': price
        }

    def obj_2_json(self, obj: Warehouse, remainder: float) -> dict:
        return self.data_json(obj.id, obj.material.name, remainder, obj.price)

    def get_prod_json(self, product: Product, product_qty: int, data_list: list) -> dict:
        return {
            'name': product.name,
            'product_qty': product_qty,
            'product_materials': data_list
        }

    def mat_query_2_json(self, obj: Material, query: QuerySet[Warehouse]) -> dict:
        return {
            'id': obj.id,
            'obj_list': list(query)
        }

    def get_same_materials(self, material_id) -> dict:
        """
        :param material_id: int
        Return materials from warehouse by material id
        """
        w_materials = self.get_materials_from_w(material_id)
        return self.mat_query_2_json(getattr(w_materials.first(), 'material', None), w_materials)

    def set_usable_materials(self, product_id):
        """
        :param product_id: int
        Set usable materials for product
        """
        prod_mats = self.get_product_material(product_id)
        for pm in prod_mats:
            material = self.search_materials_from_list(pm.material_id)
            if material.get('id', -1) != pm.material_id:
                self.material_list.append(self.get_same_materials(pm.material_id))

    def search_materials_from_list(self, material_id) -> dict:
        """
        :param material_id: int
        Search material from list by material id and return it if it exists or return empty dict.
        """
        for material in self.material_list:
            if material['id'] == material_id:
                return material
        return {}

    def separate_materials(self, product_id, quantity: int) -> None:
        """
        :param product_id: int
        :param quantity: int
        Separate materials for product by product id and quantity
        """
        prod_materials = self.get_product_material(product_id)
        _quantity = quantity
        _list = []
        for pm in prod_materials:
            self.mat_result = []
            available_materials = self.search_materials_from_list(pm.material_id)
            for available_mat in available_materials['obj_list']:
                if available_mat.remainder >= pm.quantity * quantity:
                    available_mat.remainder -= pm.quantity * quantity
                    self.mat_result.append(self.obj_2_json(available_mat,
                                                           pm.quantity * quantity))
                    quantity = 0
                    break
                elif available_mat.remainder > 0:
                    quantity -= floor(available_mat.remainder / pm.quantity)
                    self.mat_result.append(self.obj_2_json(available_mat,
                                                           available_mat.remainder))
                    available_mat.remainder = 0
            if quantity > 0:
                self.mat_result.append(self.data_json(None,
                                                      pm.material.name,
                                                      pm.quantity * quantity,
                                                      None))
            _list.append(self.mat_result)
            quantity = _quantity
        self.result.append(self.get_prod_json(self.get_product(product_id),
                                              _quantity,
                                              _list))

    def clear_data(self) -> None:
        """
        Clear service temp data
        """
        self.material_list = []
        self.mat_result = []
        self.result = []

    def get_data(self, product_list) -> list:
        """
        :param product_list: list
        Return list of products with materials
        """
        self.clear_data()
        for product in product_list:
            self.set_usable_materials(product.get('id'))
            self.separate_materials(product.get('id'), product.get('product_qty'))
        return self.result
