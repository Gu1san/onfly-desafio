
"""Testes adicionais de validação dos repositórios CSV."""

import csv
from decimal import Decimal

import pytest

from helpers import BASE, COLUMNS, PROJECT_ROOT
from onfly_report.exceptions import InputFileError
from onfly_report.repositories.csv_rate_repository import (
    CsvRateRepository,
)
from onfly_report.repositories.csv_reservation_repository import (
    CsvReservationRepository,
)


def write_reservations_csv(path, rows):
    """Cria um CSV de reservas usando a estrutura padrão dos testes."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=COLUMNS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows({**BASE, **row} for row in rows)


def test_rate_repository_reads_reference_rates():
    path = PROJECT_ROOT / "data" / "taxas_cambio.csv"

    rates = CsvRateRepository(path).read()

    assert rates == {
        "BRL": Decimal("1.000000"),
        "USD": Decimal("5.420000"),
        "EUR": Decimal("5.880000"),
    }


def test_rate_repository_rejects_missing_file(tmp_path):
    path = tmp_path / "inexistente.csv"

    with pytest.raises(InputFileError):
        CsvRateRepository(path).read()


def test_rate_repository_rejects_missing_columns(tmp_path):
    path = tmp_path / "rates.csv"
    path.write_text("currency\nBRL\n", encoding="utf-8")

    with pytest.raises(InputFileError):
        CsvRateRepository(path).read()


def test_rate_repository_rejects_empty_file(tmp_path):
    path = tmp_path / "rates.csv"
    path.write_text("", encoding="utf-8")

    with pytest.raises(InputFileError):
        CsvRateRepository(path).read()


def test_rate_repository_rejects_empty_table(tmp_path):
    path = tmp_path / "rates.csv"
    path.write_text(
        "currency,rate_to_brl\n",
        encoding="utf-8",
    )

    with pytest.raises(InputFileError):
        CsvRateRepository(path).read()


@pytest.mark.parametrize(
    "rate",
    [
        "NaN",
        "Infinity",
        "-Infinity",
        "0",
        "-1",
        "abc",
    ],
)
def test_rate_repository_rejects_invalid_rates(tmp_path, rate):
    path = tmp_path / "rates.csv"
    path.write_text(
        f"currency,rate_to_brl\nBRL,{rate}\n",
        encoding="utf-8",
    )

    with pytest.raises(InputFileError):
        CsvRateRepository(path).read()


def test_rate_repository_rejects_incomplete_row(tmp_path):
    path = tmp_path / "rates.csv"
    path.write_text(
        "currency,rate_to_brl\nBRL,\n",
        encoding="utf-8",
    )

    with pytest.raises(InputFileError):
        CsvRateRepository(path).read()


def test_rate_repository_rejects_invalid_encoding(tmp_path):
    path = tmp_path / "rates.csv"
    path.write_bytes(b"currency,rate_to_brl\nBRL,\xff\n")

    with pytest.raises(InputFileError):
        CsvRateRepository(path).read()


def test_reservation_repository_rejects_missing_file(tmp_path):
    path = tmp_path / "inexistente.csv"

    with pytest.raises(InputFileError):
        CsvReservationRepository(path).read()


def test_reservation_repository_rejects_missing_columns(tmp_path):
    path = tmp_path / "reservas.csv"
    path.write_text(
        "reservation_id,hotel_id\nR-1,H01\n",
        encoding="utf-8",
    )

    with pytest.raises(InputFileError):
        CsvReservationRepository(path).read()


def test_reservation_repository_rejects_empty_file(tmp_path):
    path = tmp_path / "reservas.csv"
    path.write_text("", encoding="utf-8")

    with pytest.raises(InputFileError):
        CsvReservationRepository(path).read()


def test_reservation_repository_rejects_invalid_encoding(tmp_path):
    path = tmp_path / "reservas.csv"
    path.write_bytes(b"reservation_id,traveler_name\nR-1,\xff")

    with pytest.raises(InputFileError):
        CsvReservationRepository(path).read()


def test_reservation_repository_reads_all_300_reference_reservations():
    path = PROJECT_ROOT / "data" / "reservas_hoteis.csv"

    reservations = CsvReservationRepository(path).read()

    assert len(reservations) == 300
    assert reservations[0].values["reservation_id"] == "RSV-0001"
    assert reservations[-1].values["reservation_id"] == "RSV-0300"


def test_reservation_repository_reads_validation_sample():
    path = PROJECT_ROOT / "data" / "exemplo-validacao.csv"

    reservations = CsvReservationRepository(path).read()

    assert len(reservations) == 12
    assert reservations[0].values["reservation_id"] == "EX-01"
    assert reservations[-1].values["reservation_id"] == "EX-12"
