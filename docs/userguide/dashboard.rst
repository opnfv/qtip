************************
Setting Up ElasticSearch
************************

Pull the elasticsearch docker container via the following command
::

	docker pull elasticsearch

Once the pull is complete, start container:
::

	docker run -d -p 9200:9200 --name esearch elasticsearch

*****************
Setting Up Kibana
*****************

Pull the Kibana docker container
::

	docker pull kibana

Now start Kibana. Make sure to link it to ElasticSearch
::

	docker run --link esearch:elasticsearch -p 5601:5601 --name kibana -d kibana

The Kibana Dashboard would now be accessible at http://{your_IP}:5601

***************
Pushing Results
***************

The results need to be pushed to ElasticSearch database first. It supports the input of
json files directly. This can be done via the RestAPI, i.e PUSH and PUT. Now in your
Qtip directory on container, forward the results,
::

	curl -X PUT http://{your_IP}:9200/index_name/type/id -d @/path/to/file/example.json

Here index_name refers to a database, dhrystone for example. Type is used to store different
data in the same database, in our case it could refer to the different compute nodes. ID should
be unique. PUT is used whenever one wants to specify the ID by himself.

In contrast, ID can also be dynamically allocated, for which we need POST.
::

	curl -X POST http://{your_IP}:9200/index_name/type/ -d @/path/to/file/example.json

*******************
Configure Kibana
*******************

In the Kibana Dashboard, under the Settings Tab,
1) Uncheck all the different options available.
2) Insert the index_name or pattern as specified in the above commands to push the data.
3) Click Create, and you'll observe that Kibana has found the database.

*******************
Viewing the Results
*******************

Now under the Visualize tab, perform the following steps:

1) Select Vertical Bar Graph.
2) Select From a new search. Now you'll observer a large rectangular box. This is Kibana default setup.
3) Under the Buckets, set X-Axis to Date Histogram. This would enable the results to be sorted according the timestamp.
4) Under the Metrics, set Y-AXIS to a suitable Aggregate, such as SUM, MIN, MAX etc.
