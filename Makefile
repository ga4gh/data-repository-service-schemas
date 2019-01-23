SWAGGER_PATH = openapi/data_repository_service.swagger.yaml
OPENAPI3_PATH = openapi/data_repository_service.openapi.yaml
SMARTAPI_PATH = openapi/data_repository_service.smartapi.yaml
SMARTAPI_PART_PATH = openapi/data_repository_service.smartapi.yaml.part
SWAGGER2OPENAPI_PATH = swagger2openapi

REPO_URL ?= "https://github.com/$(TRAVIS_REPO_SLUG)"
BRANCH_NAME ?= $(echo "$(TRAVIS_BRANCH)" | awk '{print tolower($0)}')
DOCS_STAGING_PATH = deploy

# Make docs available at / for master and at /preview/{branch} for all others.
# We don't need to check if `branch == gh-pages` since Travis will skip it by default.
ifeq "$(BRANCH_NAME)" "master"
	DOCS_ROOT = "$(DOCS_STAGING_PATH)"
else
	DOCS_ROOT = "$(DOCS_STAGING_PATH)/preview/$(BRANCH_NAME)"
endif

$(OPENAPI3_PATH) : $(SWAGGER_PATH)
	$(SWAGGER2OPENAPI_PATH) -y $(SWAGGER_PATH) --outfile $(OPENAPI3_PATH)

$(SMARTAPI_PATH) : $(OPENAPI3_PATH)
	python merge_yaml.py $(OPENAPI3_PATH) $(SMARTAPI_PART_PATH) > $(SMARTAPI_PATH)

schemas : $(OPENAPI3_PATH) $(SMARTAPI_PATH)
	true

stage_docs : clean_docs
	# First, make a shallow clone of our existing gh-pages docs
	git clone --depth=1 --branch=gh-pages $(REPO_URL) $(DOCS_STAGING_PATH)
	# Set up and populate documentation directories
	mkdir -p "$(DOCS_ROOT)/docs/" "$(DOCS_ROOT)/swagger-ui/"
	cp docs/html5/index.html docs/pdf/index.pdf "$(DOCS_ROOT)/docs/"
	cp "$(SWAGGER_PATH)" "$(DOCS_ROOT)/swagger.yaml"
	cp docs/_swagger-ui-template.html "$(DOCS_ROOT)/swagger-ui/index.html"
	# Vendor swagger-ui
	npm install swagger-ui-dist@3.20.5
	mv "$$(node -e 'console.log(path.dirname(require.resolve("swagger-ui-dist")));')" "$(DOCS_STAGING_PATH)/_swagger-ui/"

clean_docs :
	rm -rf $(DOCS_STAGING_PATH)

.PHONY : schemas stage_docs
