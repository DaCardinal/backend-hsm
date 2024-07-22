# import pytest
# from typing import Any, Dict
# from httpx import AsyncClient


# class TestContractAssignments:
#     default_contract_assignment: Dict[str, Any] = {}

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(name="create_contract_assignment")
#     async def test_create_contract_assignment(self, client: AsyncClient):
#         response = await client.post(
#             "/assign_contracts/",
#             json={
#                 "contract_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "employee_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "contract_status": "active",
#                 "property_unit_assoc": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
#             },
#         )
#         assert response.status_code == 200

#         TestContractAssignments.default_contract_assignment = response.json()["data"]

#     @pytest.mark.asyncio(scope="session")
#     async def test_get_all_contract_assignments(self, client: AsyncClient):
#         response = await client.get("/assign_contracts/", params={"limit": 10, "offset": 0})
#         assert response.status_code == 200
#         assert isinstance(response.json(), dict)

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["create_contract_assignment"], name="get_contract_assignment_by_id")
#     async def test_get_contract_assignment_by_id(self, client: AsyncClient):
#         contract_assignment_id = self.default_contract_assignment["contract_assignment_id"]

#         response = await client.get(f"/assign_contracts/{contract_assignment_id}")

#         assert response.status_code == 200
#         assert response.json()["data"]["contract_assignment_id"] == contract_assignment_id

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["get_contract_assignment_by_id"], name="update_contract_assignment_by_id")
#     async def test_update_contract_assignment(self, client: AsyncClient):
#         contract_assignment_id = self.default_contract_assignment["contract_assignment_id"]

#         response = await client.put(
#             f"/assign_contracts/{contract_assignment_id}",
#             json={
#                 "contract_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "employee_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "contract_status": "inactive",
#                 "property_unit_assoc": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
#             },
#         )
#         assert response.status_code == 200
#         assert response.json()["data"]["contract_status"] == "inactive"

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["update_contract_assignment_by_id"], name="delete_contract_assignment_by_id")
#     async def test_delete_contract_assignment(self, client: AsyncClient):
#         contract_assignment_id = self.default_contract_assignment["contract_assignment_id"]

#         response = await client.delete(f"/assign_contracts/{contract_assignment_id}")
#         assert response.status_code == 204

#         # Verify the contract assignment is deleted
#         response = await client.get(f"/assign_contracts/{contract_assignment_id}")
#         assert response.status_code == 404
