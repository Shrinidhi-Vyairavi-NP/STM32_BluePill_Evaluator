
import subprocess
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
        item_path = project / item

        if item_path.exists():
            print(f"[PASS] {item}")
            passed += 1
        else:
            print(f"[FAIL] {item}")

    print("=" * 40)
    print(f"Result: {passed}/{len(REQUIRED_ITEMS)} checks passed")

    if passed == len(REQUIRED_ITEMS):
        print("Status: PASSED")
        return True

    print("Status: FAILED")
    return False


def main():
    repo_url = input(
        "Enter the public GitHub repository URL: "
    ).strip()

    if not repo_url.startswith("https://github.com/"):
        print("ERROR: Please enter a GitHub HTTPS URL.")
        return

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
            print("\nGit error:")
            print(result.stderr.strip())
            return

        print("Repository downloaded successfully.")

        project_file = next(
            download_path.rglob("Debugging_Test_STM32.ioc"),
            None,
        )

        if project_file is None:
            print("\nSTM32 Project Evaluation")
            print("=" * 40)
            print("[FAIL] Debugging_Test_STM32.ioc")
            print("[FAIL] Expected STM32 project was not found.")
            print("=" * 40)
            print(f"Result: 0/{len(REQUIRED_ITEMS)} checks passed")
            print("Status: FAILED")
            return

        project_folder = project_file.parent
        evaluate_project(project_folder)


if __name__ == "__main__":
    main()
