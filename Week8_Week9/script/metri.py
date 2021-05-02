from time import sleep
import psutil
import os, popen2, sys
from riemann_client.transport import TCPTransport
from riemann_client.client import QueuedClient
from elasticsearch import Elasticsearch


def alert(Service, State, Metric, Description):
    with QueuedClient(TCPTransport("192.168.1.11", 5555)) as client:
    	client.event(service=Service, state=State, metric_f=Metric, description=Description)
        client.flush()

def cores():
    return psutil.cpu_count()

def cpu_report():
    r, w, e = popen2.popen3('ps -eo pcpu,pid,args | sort -nrb -k1 | head -10')
    return r.readlines()    

def cpu(warning=0.80, critical=0.90):
    c = psutil.cpu_times()
    used = c.user + c.system + c.nice
    total = used + c.idle
    f = used/total
    state = "ok"
    if f > warning: state="warning"
    if f > critical: state="critical"
    alert("cpu", state, f, "%.2f %% user+nice+sytem\n\n%s" % (f * 100, cpu_report()))

def disk(warning=0.80, critical=0.90):
    for p in psutil.disk_partitions():
        u = psutil.disk_usage(p.mountpoint)
        perc = u.percent
        f = perc/100.0
        state = "ok"
        if f > warning: state="warning"
        if f > critical: state="critical"
        alert("disk %s" % p.mountpoint, state, f, "%s used" % perc)

def load(warning=3, critical=8):
    l = os.getloadavg()
    f = l[2]/cores()
    state = "ok"
    if f > critical: state="critical"
    if f > warning: state="warning"
    alert("load", state, l[2], "15-minute load average/core is %f" % l[2])


def memory(warning = 0.80, critical=0.95):
    vm = psutil.virtual_memory()
    sf = sv = "ok"
    fv = vm.percent / 100.0
    if fv > warning: sv = "warning"
    if fv > critical: sv = "critical"
    alert("virtual memory", sv, fv, "%.2f%% used\n\n%s" % (fv * 100, memory_report()))

def memory_report():
    r, w, e = popen2.popen3('ps -eo pmem,pid,args | sort -nrb -k1 | head -10')
    return r.readlines()

es = Elasticsearch('http://172.10.0.1:9200', ca_certs=False, verify_certs=False)
def elastic_search():
    health = es.cluster.health()
    stats = es.cluster.stats()
    nodes = health['number_of_nodes']
    status = health['status']
    docs_count = stats['indices']['docs']['count']
    nodes_mem_used = stats['nodes']['os']['mem']['used_percent']

    jvm_mem_used = stats['nodes']['jvm']['mem']['heap_used_in_bytes']
    jvm_mem_max = stats['nodes']['jvm']['mem']['heap_max_in_bytes']
    nodes_mem_free = stats['nodes']['os']['mem']['free_percent']
    with QueuedClient(TCPTransport("192.168.1.11", 5555)) as client:
        client.event(service="nodes", metric_f=nodes)
        if status == 'yellow':
            client.event(service="status", metric_f = 1, state="warning")
        elif status == 'green':
            client.event(service="status",  metric_f = 1, state="ok")
        else:
            client.event(service="status", metric_f = 1, state="critical")        

        client.event(service='document count',state='ok',metric_f=docs_count, description='number of documentse')
        client.event(service='memory used by node', state='warning', metric_f=nodes_mem_used)
        client.event(service='jvm memory max',state='critical', metric_f=jvm_mem_max/1024)
        client.event(service='jvm memory use', metric_f=jvm_mem_used/1024)
        client.flush()        

def tick():
    try:
        cpu()
        memory()
        load()
        disk()
        elastic_search()
    except Exception, e:
        print "Exception: %s" % e
def run():
    while True:
        tick()
        sleep(10)

if __name__ == "__main__":
    run()
