# Add a line for setting the controller "app" which matches the name of the
# module that hosts the controller functions.
sed -i 's/"operation/"x-swagger-router-controller": "ga4gh.dos.server", \n        "operation/g' data_objects_service.swagger.json
# Inject a base path
sed -i 's/"swagger"/  "basePath": "\/", "swagger"/g' data_objects_service.swagger.json
mv data_objects_service.swagger.json swagger/data_objects_service.swagger.json
cp swagger/data_objects_service.swagger.json python/ga4gh/dos/.
