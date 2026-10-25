
import subprocess
import sys
import tempfile
from pathlib import Path


REQUIRED_ITEMS = [
    "Debugging_Test_STM32.ioc",
    ".mxproject",
    "Core",
    "Drivers",
    "MDK-ARM/Debugging_Test_STM32.uvprojx",
    "MDK-ARM/startup_stm32f103xb.s",
]


def evaluate_project(project):
    print("\nSTM32 Project Evaluation")
    print("=" * 40)

    passed = 0

    for item in REQUIRED_ITEMS:
        if (project / item).exists():
            print(f"[PASS] {item}")
            passed += 1
        else:
            print(f"[FAIL] {item}")

    print("=" * 40)
    print(f"Result: {passed}/{len(REQUIRED_ITEMS)} checks passed")

    success = passed == len(REQUIRED_ITEMS)
    print(f"Status: {'PASSED' if success else 'FAILED'}")
    return success


def main():
    if len(sys.argv) >= 2:
        repo_url = sys.argv[1].strip()
    else:
        repo_url = input(
            "Enter the public GitHub repository URL: "
        ).strip()

    prefix = "https://github.com/"

    if not repo_url.startswith(prefix):
        print("ERROR: Please enter a GitHub HTTPS URL.")
        return False

    with tempfile.TemporaryDirectory() as temp_dir:
        download_path = Path(temp_dir) / "student_repo"

        print("\nDownloading repository...")

        result = subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                repo_url,
                str(download_path),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("\nSTM32 Project Evaluation")
            print("=" * 40)
            print("[FAIL] Repository could not be downloaded.")
            print("Status: FAILED")
            print(result.stderr.strip())
            return False

        print("Repository downloaded successfully.")

        project_file = next(
            download_path.rglob("Debugging_Test_STM32.ioc"),
            None,
        )

        if project_file is None:
            print("\nSTM32 Project Evaluation")
            print("=" * 40)
            print("[FAIL] Expected STM32 project was not found.")
            print(f"Result: 0/{len(REQUIRED_ITEMS)} checks passed")
            print("Status: FAILED")
            return False

        return evaluate_project(project_file.parent)


if __name__ == "__main__":
    if not main():
        sys.exit(1)
