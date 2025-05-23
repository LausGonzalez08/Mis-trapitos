import schedule
import threading
import time
from datetime import datetime
from funciones import aplicar_descuentos


def aplicar_descuentos_periodicamente():
    """Aplica los descuentos cada día a medianoche"""
    def job():
        aplicar_descuentos()
        print(f"Descuentos aplicados el {datetime.now()}")

    # Programar la tarea
    schedule.every().day.at("00:00").do(job)

    # Ejecutar el scheduler en un hilo separado
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)

    thread = threading.Thread(target=run_scheduler)
    thread.daemon = True
    thread.start()
