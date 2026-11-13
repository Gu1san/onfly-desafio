
"""Testes adicionais das regras de negócio do relatório."""

from helpers import run_cli


def test_hotels_with_same_amount_are_sorted_by_id(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "hotel_id": "H03",
                "amount": "100.00",
            },
            {
                "reservation_id": "R-2",
                "hotel_id": "H01",
                "amount": "100.00",
            },
            {
                "reservation_id": "R-3",
                "hotel_id": "H02",
                "amount": "100.00",
            },
        ],
        top=3,
    )

    hotel_ids = [
        hotel["hotel_id"]
        for hotel in report["top_hotels"]
    ]

    assert hotel_ids == ["H01", "H02", "H03"]


def test_report_without_billable_reservations(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "status": "CANCELLED",
                "amount": "500.00",
            },
            {
                "reservation_id": "R-2",
                "status": "NO_SHOW",
                "amount": "300.00",
            },
        ],
    )

    summary = report["summary"]

    assert summary["total_reservations"] == 2
    assert summary["confirmed_reservations"] == 0
    assert summary["total_room_nights"] == 0
    assert summary["total_amount_brl"] == "0.00"
    assert summary["average_nightly_rate_brl"] == "0.00"

    assert report["by_month"] == []
    assert report["top_hotels"] == []


def test_more_than_200_reservations_are_processed(tmp_path):
    rows = [
        {
            "reservation_id": f"R-{index}",
            "amount": "10.00",
        }
        for index in range(201)
    ]

    report = run_cli(tmp_path, rows)

    assert report["summary"]["total_reservations"] == 201
    assert report["summary"]["confirmed_reservations"] == 201
    assert report["summary"]["total_amount_brl"] == "2010.00"


def test_top_limits_number_of_ranked_hotels(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H01", "amount": "300.00"},
            {"reservation_id": "R-2", "hotel_id": "H02", "amount": "200.00"},
            {"reservation_id": "R-3", "hotel_id": "H03", "amount": "100.00"},
        ],
        top=1,
    )

    assert len(report["top_hotels"]) == 1
    assert report["top_hotels"][0]["hotel_id"] == "H01"
