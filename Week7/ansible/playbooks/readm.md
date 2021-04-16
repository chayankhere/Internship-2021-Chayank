1. execut installation_elaticsearh.yml
2. install: ansible-galaxy install elastic.elasticsearch,v7.12.0
   reference:
   -> Format for 7.5 or greater version got from here
   https://computingforgeeks.com/setup-elasticsearch-cluster-on-centos-ubuntu-with-ansible/
   -> General idea to write playbook for cluster from here
   https://www.digitalocean.com/community/tutorials/how-to-use-ansible-to-set-up-a-production-elasticsearch-cluster
3. generate certificates using generate.cert.yml
   reference:
   -> Generating certifica for ssl non interactively
   https://stackoverflow.com/questions/57495282/how-to-enable-tls-in-elasticsearch-non-interactively
4. now run node_set.ym
   reference:
   -> Documentayion for ssl for Elastic searc
   https://github.com/elastic/ansible-elasticsearch/blob/master/docs/ssl-tls-setup.md
   -> Various options for ssl using Elastic Searc
   https://github.com/elastic/ansible-elasticsearch/blob/master/defaults/main.yml
