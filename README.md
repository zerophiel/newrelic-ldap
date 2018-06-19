# newrelic-ldap
Run these commands to install newrelic infrastructure agent
  sudo yum -q makecache -y --disablerepo='*' --enablerepo='newrelic-infra

  sudo yum install newrelic-infra-integrations

Place ldapnewrelic.py, ldapnewrelic-definition.yml, and JSONData.json into:
          /var/db/newrelic-infra/custom-integrations/
Place ldapnewrelic-config into:
         /etc/newrelic-infra/integrations.d/
edit permission of JSONData.json:
         chmod 666 /var/db/newrelic-infra/custom-integrations/JSONData.json
edit ldapnewrelic.py password and event type:
         password='LDAPPASSWORD'
         "event_type" : "LDAP_NAME"
restart the infrastructure agent by:
         systemctl restart newrelic-infra
use NRQL to pull out metrics from python by following command by defined event type:
         SELECT * FROM LDAP_NAME

selectable metrics field:
Threads : Display Current Threads
add_operations : Display Total Add Operations since server up (referencing to uptime)
bind_operations: Display Total Bind Operations since server up (referencing to uptime)
compare_operations: Display Total compare Operations since server up (referencing to uptime)
core_count: Displays current core count
currentAddOps: Displays current Add Operations
currentBind: Displays current Bind Operations
currentCompOps: Displays current Compare Operations
currentCompletedOps: Displays current Completed Operations
currentDeleteOps: Displays current Delete Operations
currentInitiatedOps: Display current Initiated Operations
currentModOps: Display current Modify Operations
currentSearchOps: Display current Search Operations
currentUnbind: Display current Unbind Operations
current_connections: Display current connections
delete_operations: Display Total Delete Operations since server up (referencing to uptime)
initiated_operations: Display Total Initiated Operations since server up (referencing to uptime)
ldap_uptime: Display Total Uptime
modify_operations: Display modify Operations since server up (referencing to uptime)
piddiff: Display "1" if there is difference in PID
read_waiters: Display current read waiters
search_operations: Display Total Search_Operations since server up (referencing to uptime)
slapdpid: Display current slapd PID
unbind_operations: Display Total Unbind operations since server up (referencing to uptime)
write_waiters: Display current write waiters
