
import ldap
import json
import logging
import os
from subprocess import check_output

def get_pid(name):
    return check_output(["pidof",name])

currentPID = get_pid("slapd")


class IntegrationData:
    def __init__(self, name, protocol_version, integration_version):
        self.name = name
        self.protocol_version = protocol_version
        self.integration_version = integration_version
        self.metrics = []


    def addMetric(self, metric_dict):
        self.metrics.append(metric_dict)

searchlist = {
        'write_waiters': ('cn=Write,cn=Waiters,cn=Monitor', 'monitorCounter'),
        'read_waiters': ('cn=Read,cn=Waiters,cn=Monitor', 'monitorCounter'),
        'Threads': ('cn=Active,cn=Threads,cn=Monitor', 'monitoredInfo'),
        'current_connections': ('cn=Current, cn=Connections, cn=Monitor','monitorCounter'),
        'completed_operations': ('cn=Operations,cn=Monitor', 'monitorOpCompleted'),
        'initiated_operations': ('cn=Operations,cn=Monitor', 'monitorOpInitiated'),
        'bind_operations': ('cn=Bind,cn=Operations,cn=Monitor', 'monitorOpCompleted'),
        'unbind_operations': ('cn=Unbind,cn=Operations,cn=Monitor', 'monitorOpCompleted'),
        'add_operations': ('cn=Add,cn=Operations,cn=Monitor', 'monitorOpInitiated'),
        'delete_operations': ('cn=Delete,cn=Operations,cn=Monitor', 'monitorOpCompleted'),
        'modify_operations': ('cn=Modify,cn=Operations,cn=Monitor', 'monitorOpCompleted'),
        'compare_operations': ('cn=Compare,cn=Operations,cn=Monitor', 'monitorOpCompleted'),
        'search_operations': ('cn=Search,cn=Operations,cn=Monitor', 'monitorOpCompleted'),
        'ldap_uptime':('cn=Uptime,cn=Time,cn=Monitor','monitoredInfo')
    }

readjson = json.loads(open("JSONData.json").read())

totalCompletedOps = int(readjson["metrics"][0]["completed_operations"])
totalInitiatedOps = int(readjson["metrics"][0]["initiated_operations"])
totalBind = int(readjson["metrics"][0]["bind_operations"])
totalUndbind = int(readjson["metrics"][0]["unbind_operations"])
totalAddOps = int(readjson["metrics"][0]["add_operations"])
totalDeleteOps = int(readjson["metrics"][0]["delete_operations"])
totalModOps = int(readjson["metrics"][0]["modify_operations"])
totalCompOps = int(readjson["metrics"][0]["compare_operations"])
totalSearchOps = int(readjson["metrics"][0]["search_operations"])
totalUptime = int(readjson["metrics"][0]["ldap_uptime"])
prevSlapdPid = int(readjson["metrics"][0]["slapdpid"])


if __name__ == "__main__":

    data = IntegrationData("com.ldap.newrelic", "1", "1.1.1")
    env = os.getenv("ENVIRONMENT")
    # connect LDAP
    summary = {"event_type": "LDAP_NAME",
               }
    username = 'cn=Manager,cn=config'
    password = 'PASSWORD'
    conn = ldap.initialize('ldap://%s:%s' % ('localhost', 389))
    conn.simple_bind_s(username, password)
    for key in searchlist.keys():
        b = searchlist[key][0]
        attr = searchlist[key][1]
        num = conn.search(b, ldap.SCOPE_BASE, 'objectClass=*', [attr, ])

        try:
            result_type, result_data = conn.result(num, 1)

            if result_type == 101:
                val = int(result_data[0][1].values()[0][0])
                summary[key] = val
        except:
            print "oops"

    summary["slapdpid"] = int(currentPID)
    data.addMetric(summary)
    newjson = json.dumps(data.__dict__)
    currentMetrics = json.loads(newjson)
    #create json for next previous
    with open('JSONData.json', 'w') as f:
        f.write(json.dumps(data.__dict__))
    currentUptime = int(currentMetrics["metrics"][0]["ldap_uptime"])
    if totalUptime < currentUptime:
        summary["currentCompletedOps"] = int(currentMetrics["metrics"][0]["completed_operations"]) - totalCompletedOps
        summary ["currentInitiatedOps"] = int(currentMetrics["metrics"][0]["initiated_operations"]) - totalInitiatedOps
        summary ["currentBind"] = int(currentMetrics["metrics"][0]["bind_operations"]) - totalBind
        summary ["currentUnbind"] = int(currentMetrics["metrics"][0]["unbind_operations"]) - totalUndbind
        summary ["currentAddOps"] = int(currentMetrics["metrics"][0]["add_operations"]) - totalAddOps
        summary ["currentDeleteOps"] = int(currentMetrics["metrics"][0]["delete_operations"]) - totalDeleteOps
        summary ["currentModOps"] = int(currentMetrics["metrics"][0]["modify_operations"]) - totalModOps
        summary ["currentCompOps"] = int(currentMetrics["metrics"][0]["compare_operations"]) - totalCompOps
        summary ["currentSearchOps"] = int(currentMetrics["metrics"][0]["search_operations"]) - totalSearchOps
        if prevSlapdPid != summary["slapdpid"]:
            summary ["piddiff"] = 1
    else:
        summary["currentCompletedOps"] = int(currentMetrics["metrics"][0]["completed_operations"])
        summary ["currentInitiatedOps"] = int(currentMetrics["metrics"][0]["initiated_operations"])
        summary ["currentBind"] = int(currentMetrics["metrics"][0]["bind_operations"])
        summary ["currentUnbind"] = int(currentMetrics["metrics"][0]["unbind_operations"])
        summary ["currentAddOps"] = int(currentMetrics["metrics"][0]["add_operations"])
        summary ["currentDeleteOps"] = int(currentMetrics["metrics"][0]["delete_operations"])
        summary ["currentModOps"] = int(currentMetrics["metrics"][0]["modify_operations"])
        summary ["currentCompOps"] = int(currentMetrics["metrics"][0]["compare_operations"])
        summary ["currentSearchOps"] = int(currentMetrics["metrics"][0]["search_operations"])
        if prevSlapdPid != summary["slapdpid"]:
            summary ["piddiff"] = 1

    print json.dumps(data.__dict__)
