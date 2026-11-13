
"""Testes adicionais dos códigos de saída da CLI."""

import csv
import os
import subprocess
import sys

import pytest

from helpers import BASE, COLUMNS, PROJECT_ROOT, SRC_DIR


def prepare_input_files(tmp_path):
    """Cria arquivos CSV válidos para executar a CLI."""
    input_path = tmp_path / "reservas.csv"
    rates_path = tmp_path / "rates.csv"
    output_path = tmp_path / "report.json"

    with input_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=COLUMNS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerow(BASE)

    rates_path.write_text(
        "currency,rate_to_brl\n"
        "BRL,1.000000\n"
        "USD,5.420000\n"
        "EUR,5.880000\n",
        encoding="utf-8",
    )

    return input_path, rates_path, output_path


def execute_cli(input_path, rates_path, output_path, extra_args=None):
    """Executa a CLI e devolve o processo."""
    environment = os.environ.copy()

    for import_root in (SRC_DIR, PROJECT_ROOT):
        if (import_root / "onfly_report").is_dir():
            environment["PYTHONPATH"] = (
                str(import_root)
                + os.pathsep
                + environment.get("PYTHONPATH", "")
            )
            break

    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    command = [
        sys.executable,
        "-m",
        "onfly_report",
        "--input",
        str(input_path),
        "--rates",
        str(rates_path),
        "--output",
        str(output_path),
    ]

    if extra_args:
        command.extend(extra_args)

    return subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        env=environment,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_cli_returns_zero_on_success(tmp_path):
    input_path, rates_path, output_path = prepare_input_files(tmp_path)

    process = execute_cli(input_path, rates_path, output_path)

    assert process.returncode == 0
    assert output_path.exists()


@pytest.mark.parametrize("top", ["0", "-1", "abc"])
def test_cli_returns_two_for_invalid_top(tmp_path, top):
    input_path, rates_path, output_path = prepare_input_files(tmp_path)

    process = execute_cli(
        input_path,
        rates_path,
        output_path,
        ["--top", top],
    )

    assert process.returncode == 2


def test_cli_returns_two_when_input_file_does_not_exist(tmp_path):
    input_path, rates_path, output_path = prepare_input_files(tmp_path)
    input_path.unlink()

    process = execute_cli(input_path, rates_path, output_path)

    assert process.returncode == 2


def test_cli_returns_two_when_rates_file_does_not_exist(tmp_path):
    input_path, rates_path, output_path = prepare_input_files(tmp_path)
    rates_path.unlink()

    process = execute_cli(input_path, rates_path, output_path)

    assert process.returncode == 2


def test_cli_returns_one_when_output_cannot_be_written(tmp_path):
    input_path, rates_path, output_path = prepare_input_files(tmp_path)

    # Um diretório com o mesmo nome impede a criação do arquivo JSON.
    output_path.mkdir()

    process = execute_cli(input_path, rates_path, output_path)

    assert process.returncode == 1
