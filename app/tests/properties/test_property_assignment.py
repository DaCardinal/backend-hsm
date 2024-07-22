# import pytest
# from typing import Any, Dict
# from httpx import AsyncClient


# class TestPropertyAssignment:
#     default_property_assignment: Dict[str, Any] = {}

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(name="create_property_assignment")
#     async def test_create_property_assignment(self, client: AsyncClient):
#         response = await client.post(
#             "/property_assignment/",
#             json={
#                 "property_unit_assoc_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "assignment_type": "other",
#                 "date_from": "2024-07-21T21:28:08.506Z",
#                 "date_to": "2024-07-21T21:28:08.506Z",
#                 "notes": "string"
#             },
#         )
#         assert response.status_code == 200

#         TestPropertyAssignment.default_property_assignment = response.json()["data"]

#     @pytest.mark.asyncio(scope="session")
#     async def test_get_all_property_assignments(self, client: AsyncClient):
#         response = await client.get("/property_assignment/", params={"limit": 10, "offset": 0})
#         assert response.status_code == 200
#         assert isinstance(response.json(), dict)

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["create_property_assignment"], name="get_property_assignment_by_id")
#     async def test_get_property_assignment_by_id(self, client: AsyncClient):
#         property_assignment_id = self.default_property_assignment["property_assignment_id"]

#         response = await client.get(f"/property_assignment/{property_assignment_id}")

#         assert response.status_code == 200
#         assert response.json()["data"]["property_assignment_id"] == property_assignment_id

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["get_property_assignment_by_id"], name="update_property_assignment_by_id")
#     async def test_update_property_assignment(self, client: AsyncClient):
#         property_assignment_id = self.default_property_assignment["property_assignment_id"]

#         response = await client.put(
#             f"/property_assignment/{property_assignment_id}",
#             json={
#                 "property_unit_assoc_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "assignment_type": "updated",
#                 "date_from": "2024-07-21T21:28:08.506Z",
#                 "date_to": "2024-07-21T21:28:08.506Z",
#                 "notes": "updated notes"
#             },
#         )
#         assert response.status_code == 200
#         assert response.json()["data"]["assignment_type"] == "updated"

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["update_property_assignment_by_id"], name="delete_property_assignment_by_id")
#     async def test_delete_property_assignment(self, client: AsyncClient):
#         property_assignment_id = self.default_property_assignment["property_assignment_id"]

#         response = await client.delete(f"/property_assignment/{property_assignment_id}")
#         assert response.status_code == 204

#         # Verify the property assignment is deleted
#         response = await client.get(f"/property_assignment/{property_assignment_id}")
#         assert response.status_code == 404
