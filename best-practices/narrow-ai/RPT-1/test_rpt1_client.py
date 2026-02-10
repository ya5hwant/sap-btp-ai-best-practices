import pathlib
import sys
import unittest
from unittest.mock import Mock

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from rpt1_client import (  # noqa: E402
    RPT1AuthError,
    RPT1Client,
    RPT1RequestError,
    RPT1ValidationError,
)


class DummyResponse:
    def __init__(self, status_code: int, json_body: dict | None = None) -> None:
        self.status_code = status_code
        self._json_body = json_body or {}
        self.text = str(self._json_body)
        self.ok = 200 <= status_code < 300

    def json(self) -> dict:
        return self._json_body


class RPT1ClientTests(unittest.TestCase):
    def _new_client(self, **kwargs) -> RPT1Client:
        return RPT1Client(
            aicore_base_url="https://api.example.com/v2",
            aicore_auth_url="https://auth.example.com",
            client_id="client-id",
            client_secret="client-secret",
            resource_group="default",
            deployment_url="https://deployment.example.com",
            timeout_seconds=30,
            max_retries=3,
            retry_backoff_seconds=0.0,
            **kwargs,
        )

    def test_fit_predict_happy_path_classification(self) -> None:
        context_df = pd.DataFrame(
            [
                {
                    "PRODUCT": "Office Chair",
                    "PRICE": 150.8,
                    "ORDERDATE": "02-11-2025",
                    "ID": "44",
                    "COSTCENTER": "Office Furniture",
                },
                {
                    "PRODUCT": "Server Rack",
                    "PRICE": 2200.0,
                    "ORDERDATE": "01-11-2025",
                    "ID": "104",
                    "COSTCENTER": "Data Infrastructure",
                },
            ]
        )
        query_df = pd.DataFrame(
            [
                {
                    "PRODUCT": "Couch",
                    "PRICE": 999.99,
                    "ORDERDATE": "28-11-2025",
                    "ID": "35",
                }
            ]
        )

        client = self._new_client().fit(
            context_df,
            target_columns=["COSTCENTER"],
            index_column="ID",
            task_types={"COSTCENTER": "classification"},
        )

        captured: dict = {}

        def fake_request(method: str, url: str, *, payload=None, params=None):
            captured["method"] = method
            captured["url"] = url
            captured["payload"] = payload
            return {
                "id": "req-123",
                "status": {"code": 0, "message": "ok"},
                "predictions": [
                    {
                        "ID": "35",
                        "COSTCENTER": [
                            {"prediction": "Office Furniture", "confidence": 0.96}
                        ],
                    }
                ],
                "metadata": {
                    "num_columns": 5,
                    "num_rows": 3,
                    "num_predictions": 1,
                    "num_query_rows": 1,
                },
            }

        client._request = fake_request  # type: ignore[method-assign]
        result = client.predict(query_df)

        self.assertEqual(captured["method"], "POST")
        self.assertTrue(captured["url"].endswith("/predict"))
        self.assertEqual(
            captured["payload"]["rows"][-1]["COSTCENTER"],
            "[PREDICT]",
        )
        self.assertEqual(result.status_code, 0)
        self.assertEqual(result.predictions_df.loc[0, "COSTCENTER"], "Office Furniture")
        self.assertAlmostEqual(result.predictions_df.loc[0, "COSTCENTER__confidence"], 0.96)

    def test_deployment_resolution_from_url_and_id(self) -> None:
        url_client = self._new_client(deployment_url="https://dep.from.url")
        self.assertEqual(url_client._resolve_deployment_url(), "https://dep.from.url")

        id_client = self._new_client(deployment_url=None, deployment_id="dep-001")
        id_client._request = Mock(return_value={"deploymentUrl": "https://dep.from.id"})  # type: ignore[method-assign]
        self.assertEqual(id_client._resolve_deployment_url(), "https://dep.from.id")

    def test_validation_failures(self) -> None:
        client = self._new_client()
        context_df = pd.DataFrame([{"A": 1, "B": 2}])

        with self.assertRaises(RPT1ValidationError):
            client.fit(context_df, target_columns=["MISSING"])

        with self.assertRaises(RPT1ValidationError):
            client.fit(pd.DataFrame(columns=["A", "B"]), target_columns=["A"])

        with self.assertRaises(RPT1ValidationError):
            client.fit(
                context_df,
                target_columns=["A"],
                task_types={"A": "unsupported"},
            )

        fitted = client.fit(context_df, target_columns=["A"])
        with self.assertRaises(RPT1ValidationError):
            fitted.predict(pd.DataFrame([{"A": 3}]))

    def test_schema_inference_and_explicit_override(self) -> None:
        context_df = pd.DataFrame(
            [
                {
                    "PRODUCT": "Office Chair",
                    "PRICE": 150.8,
                    "ORDERDATE": pd.Timestamp("2025-11-02"),
                    "ID": "44",
                    "COSTCENTER": "Office Furniture",
                }
            ]
        )
        query_df = pd.DataFrame(
            [
                {
                    "PRODUCT": "Couch",
                    "PRICE": 999.99,
                    "ORDERDATE": pd.Timestamp("2025-11-28"),
                    "ID": "35",
                }
            ]
        )

        client = self._new_client().fit(context_df, target_columns=["COSTCENTER"])
        inferred_payload, _ = client._build_prediction_payload(query_df)
        inferred_schema = inferred_payload["data_schema"]
        self.assertEqual(inferred_schema["PRODUCT"]["dtype"], "string")
        self.assertEqual(inferred_schema["PRICE"]["dtype"], "numeric")
        self.assertEqual(inferred_schema["ORDERDATE"]["dtype"], "date")

        explicit_schema = {
            "PRODUCT": {"dtype": "string"},
            "PRICE": {"dtype": "numeric"},
            "ORDERDATE": {"dtype": "date"},
            "ID": {"dtype": "string"},
            "COSTCENTER": {"dtype": "string"},
        }
        explicit_client = self._new_client().fit(
            context_df,
            target_columns=["COSTCENTER"],
            data_schema=explicit_schema,
        )
        explicit_payload, _ = explicit_client._build_prediction_payload(query_df)
        self.assertEqual(explicit_payload["data_schema"], explicit_schema)

    def test_multi_target_parsing_and_confidence(self) -> None:
        context_df = pd.DataFrame(
            [
                {"ID": "1", "FEATURE": 10, "TARGET_A": "x", "TARGET_B": 100.0},
                {"ID": "2", "FEATURE": 20, "TARGET_A": "y", "TARGET_B": 120.0},
            ]
        )
        query_df = pd.DataFrame([{"ID": "3", "FEATURE": 15}])

        client = self._new_client().fit(
            context_df,
            target_columns=["TARGET_A", "TARGET_B"],
            index_column="ID",
            task_types={"TARGET_A": "classification", "TARGET_B": "regression"},
        )
        client._request = Mock(  # type: ignore[method-assign]
            return_value={
                "id": "req-2",
                "status": {"code": 0, "message": "ok"},
                "predictions": [
                    {
                        "ID": "3",
                        "TARGET_A": [{"prediction": "x", "confidence": 0.9}],
                        "TARGET_B": [{"prediction": 111.4, "confidence": None}],
                    }
                ],
                "metadata": {"num_query_rows": 1},
            }
        )

        result = client.predict(query_df)
        self.assertEqual(result.predictions_df.loc[0, "TARGET_A"], "x")
        self.assertAlmostEqual(result.predictions_df.loc[0, "TARGET_A__confidence"], 0.9)
        self.assertAlmostEqual(result.predictions_df.loc[0, "TARGET_B"], 111.4)
        self.assertIsNone(result.predictions_df.loc[0, "TARGET_B__confidence"])

    def test_predict_raises_on_api_level_error_status(self) -> None:
        context_df = pd.DataFrame([{"A": 1, "TARGET": "x"}])
        query_df = pd.DataFrame([{"A": 2}])
        client = self._new_client().fit(context_df, target_columns=["TARGET"])
        client._request = Mock(  # type: ignore[method-assign]
            return_value={
                "id": "req-error",
                "status": {"code": 2, "message": "Invalid input"},
                "predictions": [],
            }
        )
        with self.assertRaises(RPT1RequestError):
            client.predict(query_df)

    def test_auth_failure_and_http_retry_behavior(self) -> None:
        auth_client = self._new_client()
        auth_client.session = Mock()
        auth_client.session.post.return_value = DummyResponse(
            401, {"error": "invalid_client"}
        )
        with self.assertRaises(RPT1AuthError):
            auth_client._get_access_token()

        retry_client = self._new_client(max_retries=2, retry_backoff_seconds=0.0)
        retry_client._build_headers = Mock(return_value={})  # type: ignore[method-assign]
        retry_client.session = Mock()
        retry_client.session.request.side_effect = [
            DummyResponse(503, {"error": "temporary"}),
            DummyResponse(200, {"status": {"code": 0}}),
        ]

        response = retry_client._request(
            "POST",
            "https://deployment.example.com/predict",
            payload={"test": 1},
        )
        self.assertEqual(response["status"]["code"], 0)
        self.assertEqual(retry_client.session.request.call_count, 2)

        bad_request_client = self._new_client()
        bad_request_client._build_headers = Mock(return_value={})  # type: ignore[method-assign]
        bad_request_client.session = Mock()
        bad_request_client.session.request.return_value = DummyResponse(
            422, {"detail": "invalid payload"}
        )
        with self.assertRaises(RPT1RequestError):
            bad_request_client._request(
                "POST",
                "https://deployment.example.com/predict",
                payload={"bad": "payload"},
            )


if __name__ == "__main__":
    unittest.main()
