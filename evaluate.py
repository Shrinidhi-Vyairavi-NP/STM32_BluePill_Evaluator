
from pathlib import Path

def evaluate_project(project_path):
    project = Path(project_path)

    required_items = [
        "Debugging_Test_STM32.ioc",
        ".mxproject",
        "Core",
        "Drivers",
        "MDK-ARM/Debugging_Test_STM32.uvprojx",
        "MDK-ARM/startup_stm32f103xb.s",
    ]

    print("\nSTM32 Project Evaluation")
    print("=" * 30)

    if not project.is_dir():
        print(f"ERROR: Project folder not found: {project}")
        return

    passed = 0

    for item in required_items:
        item_path = project / item

        if item_path.exists():
            print(f"[PASS] {item}")
            passed += 1
        else:
            print(f"[FAIL] {item}")

    print("=" * 30)
    print(f"Result: {passed}/{len(required_items)} checks passed")


if __name__ == "__main__":
    submitted_project = input("Enter the path to the STM32 project folder: ").strip()
    evaluate_project(submitted_project)
