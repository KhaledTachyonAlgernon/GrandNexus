import time
from grandnexus.nexuscore import NexusCore

if __name__ == "__main__":
    print("Initialisation du Grand Nexus...")
    nexus = NexusCore()
    print("Le Grand Nexus est initialisé.")

    nexus.start()
    print("Le Grand Nexus est démarré. Appuyez sur Ctrl+C pour arrêter.")

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nArrêt du Grand Nexus...")
    finally:
        nexus.stop()
        print("Nettoyage et fermeture.")
