# import pytest
# from typing import Any, Dict
# from httpx import AsyncClient


# class TestInvoice:
#     default_invoice: Dict[str, Any] = {}

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(name="create_invoice")
#     async def test_create_invoice(self, client: AsyncClient):
#         response = await client.post(
#             "/invoice/",
#             json={
#                 "issued_by": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
#                 "issued_to": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
#                 "invoice_details": "Consulting services and utilities for the month of June 2024",
#                 "invoice_amount": 1700.00,
#                 "due_date": "2024-07-31T23:59:59",
#                 "date_paid": None,
#                 "status": "pending",
#                 "invoice_items": [
#                     {
#                         "description": "Consulting fee",
#                         "quantity": 10,
#                         "unit_price": 100.00,
#                         "total_price": 1000.00
#                     },
#                     {
#                         "description": "Development fee",
#                         "quantity": 5,
#                         "unit_price": 100.00,
#                         "total_price": 500.00
#                     },
#                     {
#                         "reference_id": "2bc5389b-98b2-4cdc-ac6f-7d41e76f6f23",
#                         "description": "Electricity utility charge",
#                         "quantity": 1,
#                         "unit_price": 100.00,
#                         "total_price": 100.00
#                     },
#                     {
#                         "reference_id": "9e134f25-528f-407a-85f7-9760118f8149",
#                         "description": "Water utility charge",
#                         "quantity": 1,
#                         "unit_price": 100.00,
#                         "total_price": 100.00
#                     }
#                 ]
#             },
#         )
#         assert response.status_code == 200

#         TestInvoice.default_invoice = response.json()["data"]

#     @pytest.mark.asyncio(scope="session")
#     async def test_get_all_invoices(self, client: AsyncClient):
#         response = await client.get("/invoice/", params={"limit": 10, "offset": 0})
#         assert response.status_code == 200
#         assert isinstance(response.json(), dict)

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["create_invoice"], name="get_invoice_by_id")
#     async def test_get_invoice_by_id(self, client: AsyncClient):
#         invoice_id = self.default_invoice["invoice_id"]

#         response = await client.get(f"/invoice/{invoice_id}")

#         assert response.status_code == 200
#         assert response.json()["data"]["invoice_id"] == invoice_id

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["get_invoice_by_id"], name="update_invoice_by_id")
#     async def test_update_invoice(self, client: AsyncClient):
#         invoice_id = self.default_invoice["invoice_id"]

#         response = await client.put(
#             f"/invoice/{invoice_id}",
#             json={
#                 "issued_by": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
#                 "issued_to": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
#                 "invoice_details": "Updated consulting services and utilities for the month of June 2024",
#                 "invoice_amount": 1800.00,
#                 "due_date": "2024-07-31T23:59:59",
#                 "date_paid": None,
#                 "status": "pending",
#                 "invoice_items": [
#                     {
#                         "description": "Consulting fee",
#                         "quantity": 10,
#                         "unit_price": 100.00,
#                         "total_price": 1000.00
#                     },
#                     {
#                         "description": "Development fee",
#                         "quantity": 6,
#                         "unit_price": 100.00,
#                         "total_price": 600.00
#                     },
#                     {
#                         "reference_id": "2bc5389b-98b2-4cdc-ac6f-7d41e76f6f23",
#                         "description": "Electricity utility charge",
#                         "quantity": 1,
#                         "unit_price": 100.00,
#                         "total_price": 100.00
#                     },
#                     {
#                         "reference_id": "9e134f25-528f-407a-85f7-9760118f8149",
#                         "description": "Water utility charge",
#                         "quantity": 1,
#                         "unit_price": 100.00,
#                         "total_price": 100.00
#                     }
#                 ]
#             },
#         )
#         assert response.status_code == 200
#         assert response.json()["data"]["invoice_details"] == "Updated consulting services and utilities for the month of June 2024"

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["update_invoice_by_id"], name="delete_invoice_by_id")
#     async def test_delete_invoice(self, client: AsyncClient):
#         invoice_id = self.default_invoice["invoice_id"]

#         response = await client.delete(f"/invoice/{invoice_id}")
#         assert response.status_code == 204

#         # Verify the invoice is deleted
#         response = await client.get(f"/invoice/{invoice_id}")
#         assert response.status_code == 404
