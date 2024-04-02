import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

from pysnmp.hlapi import *

class SNMPLogDisplay(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SNMP Log Display")
        self.setGeometry(100, 100, 600, 400)

        self.log_text = QTextEdit(self)
        self.log_text.setGeometry(10, 10, 580, 380)

    def add_log_entry(self, entry):
        self.log_text.append(entry)

# Define SNMP parameters
target_ip = 'localhost'
community_string = 'public'

# Threshold for CPU usage
cpu_threshold = 50

# SNMP GET operation
def snmp_get(oid, log_display):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData(community_string),
               UdpTransportTarget((target_ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )
    if error_indication:
        log_display.add_log_entry(str(error_indication))
    elif error_status:
        log_display.add_log_entry('%s at %s' % (error_status.prettyPrint(), var_binds[int(error_index)-1] if error_index else '?'))
    else:
        for varBind in var_binds:
            log_display.add_log_entry(' = '.join([x.prettyPrint() for x in varBind]))
            # Check if CPU usage exceeds threshold
            if oid == '.1.3.6.1.2.1.25.5.1.1.1' and int(varBind[-1]) >= cpu_threshold:
                # Trigger action (example: display notification)
                log_display.add_log_entry('CPU usage threshold exceeded!')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SNMPLogDisplay()
    window.show()

    # Perform SNMP GET operation for CPU usage
    snmp_get('1.3.6.1.2.1.25.5.1.1.1', window)

    sys.exit(app.exec_())
