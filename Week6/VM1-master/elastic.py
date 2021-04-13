from elasticsearch import Elasticsearch

es_conn = Elasticsearch('https://elastic:8DqL02F2hbFCBkg1GdVa@172.10.0.1:9200', ca_certs=False, verify_certs=False)

INDEX_NAME = ["book_details", "author_details", "publishing_company_details"]


for i in range(0,3):
 res = es_conn.indices.create(index=INDEX_NAME[i],body={
    'settings' : {
          'index' : {
               'number_of_shards':3
                    }
                 }
 }, ignore=400)
 print ("==res===", res)

 res = es_conn.indices.get(index=INDEX_NAME[i])


es_conn.indices.get_alias("*")

print ("====================================================done with adding indices=================================================")
print ("\n")
print ("\n")
print ("====================================================adding docuents to indexes===========================================")

for j in range(1,11):
 es_conn.index(index=INDEX_NAME[2], doc_type="companies", id= j, body={"doc":{"company":"bloomsbary"}})
