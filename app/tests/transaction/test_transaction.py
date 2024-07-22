# import pytest
# from typing import Any, Dict
# from httpx import AsyncClient


# class TestTransaction:
#     default_transaction: Dict[str, Any] = {}

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(name="create_transaction")
#     async def test_create_transaction(self, client: AsyncClient):
#         response = await client.post(
#             "/transaction/",
#             json={
#                 "payment_method": "credit_card",
#                 "client_offered": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "client_requested": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "transaction_date": "2024-07-21T21:27:32.557Z",
#                 "transaction_details": "Payment for services",
#                 "transaction_type_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "transaction_status": "pending",
#                 "invoice_number": "123456"
#             },
#         )
#         assert response.status_code == 200

#         TestTransaction.default_transaction = response.json()["data"]

#     @pytest.mark.asyncio(scope="session")
#     async def test_get_all_transactions(self, client: AsyncClient):
#         response = await client.get("/transaction/", params={"limit": 10, "offset": 0})
#         assert response.status_code == 200
#         assert isinstance(response.json(), dict)

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["create_transaction"], name="get_transaction_by_id")
#     async def test_get_transaction_by_id(self, client: AsyncClient):
#         transaction_id = self.default_transaction["transaction_id"]

#         response = await client.get(f"/transaction/{transaction_id}")

#         assert response.status_code == 200
#         assert response.json()["data"]["transaction_id"] == transaction_id

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["get_transaction_by_id"], name="update_transaction_by_id")
#     async def test_update_transaction(self, client: AsyncClient):
#         transaction_id = self.default_transaction["transaction_id"]

#         response = await client.put(
#             f"/transaction/{transaction_id}",
#             json={
#                 "payment_method": "paypal",
#                 "client_offered": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "client_requested": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "transaction_date": "2024-07-21T21:27:32.557Z",
#                 "transaction_details": "Updated payment for services",
#                 "transaction_type_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "transaction_status": "completed",
#                 "invoice_number": "123456"
#             },
#         )
#         assert response.status_code == 200
#         assert response.json()["data"]["payment_method"] == "paypal"

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["update_transaction_by_id"], name="delete_transaction_by_id")
#     async def test_delete_transaction(self, client: AsyncClient):
#         transaction_id = self.default_transaction["transaction_id"]

#         response = await client.delete(f"/transaction/{transaction_id}")
#         assert response.status_code == 204

#         # Verify the transaction is deleted
#         response = await client.get(f"/transaction/{transaction_id}")
#         assert response.status_code == 404
