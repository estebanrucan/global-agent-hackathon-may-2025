import subprocess
import sys
from app import create_app

def run_tests():
    """Runs pytest and returns the exit code."""
    print("Ejecutando pruebas...")
    # Note: Adjust the command if your pytest is not directly on PATH
    # or if you need to activate a virtual environment first in a shell script.
    # For direct Python execution, ensure pytest is installed in the environment.
    try:
        # We use sys.executable to ensure we run pytest with the same python interpreter
        result = subprocess.run([sys.executable, "-m", "pytest", "--cov=app"], capture_output=True, text=True, check=False)
        print(result.stdout)
        if result.stderr:
            print("Errores de Pytest:")
            print(result.stderr)
        return result.returncode
    except FileNotFoundError:
        print("Error: pytest no encontrado. Asegúrate de que esté instalado y en tu PATH.")
        print("Puedes instalarlo con: pip install pytest pytest-cov")
        return -1 # Indicate a setup error
    except Exception as e:
        print(f"Ocurrió un error inesperado al ejecutar pytest: {e}")
        return -1 # Indicate an unexpected error

app = create_app()

if __name__ == '__main__':
    test_exit_code = run_tests()
    if test_exit_code == 0:
        print("Todas las pruebas pasaron. Iniciando la aplicación...")
        app.run(debug=app.config.get('DEBUG', False))
    elif test_exit_code == 5: # pytest specific exit code: no tests collected
        print("Advertencia: No se recolectaron pruebas por pytest. Iniciando la aplicación de todas formas...")
        print("Asegúrate de que tus pruebas estén correctamente configuradas.")
        app.run(debug=app.config.get('DEBUG', False))
    else:
        print("Las pruebas fallaron o ocurrió un error. La aplicación no se iniciará.")
        print(f"Pytest finalizó con el código de salida: {test_exit_code}")
        sys.exit(test_exit_code) # Exit with pytest's error code 