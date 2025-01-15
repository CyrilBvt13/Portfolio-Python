import win32serviceutil
import win32service
import win32event
import servicemanager

class AppService(win32serviceutil.ServiceFramework):
    _svc_name_ = "EAI_Medical_Service"
    _svc_display_name_ = "EAI Medical Service"
    _svc_description_ = "Application EAI pour la gestion des fichiers HL7, HPRIM et CSV."

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ""))
        self.main()

    def main(self):
        # Lancer l'application Flask ou toute autre logique
        from app import app
        app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(AppService)