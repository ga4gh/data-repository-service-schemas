SWAGGER_PATH = openapi/data_repository_service.swagger.yaml
OPENAPI3_PATH = openapi/data_repository_service.openapi.yaml
SMARTAPI_PATH = openapi/data_repository_service.smartapi.yaml
SMARTAPI_PART_PATH = openapi/data_repository_service.smartapi.yaml.part
SWAGGER2OPENAPI_PATH = swagger2openapi

$(OPENAPI3_PATH) : $(SWAGGER_PATH)
	$(SWAGGER2OPENAPI_PATH) -y $(SWAGGER_PATH) --outfile $(OPENAPI3_PATH)

$(SMARTAPI_PATH) : $(OPENAPI3_PATH)
	python merge_yaml.py $(OPENAPI3_PATH) $(SMARTAPI_PART_PATH) > $(SMARTAPI_PATH)

schemas : $(OPENAPI3_PATH) $(SMARTAPI_PATH)
	true

.PHONY: schemas
