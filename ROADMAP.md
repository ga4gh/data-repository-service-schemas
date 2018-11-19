Roadmap
-------

The Data Object Service has been implemented in multiple workflow execution engines 
and has helped to allow cloud agnostic data access. A small network of DOS servers 
is available from a resolver at dataguids.org.

Software for presenting Human Cell Atlas, NCI GDC, GTEx, and TOPMed data are all made 
available. Making it easier to discover, interact with, access, and publish new data 
using supporting software, documentation, and possible schema changes make up the 
bulk of this roadmap.

## Goal

### Short term - 6 months

Release version 1 and improve ease of use and adoption through supporting software. 
Provide a model for cloud agnostic data management and a network of resolving services.

### Long term

Interoperate with most major scientific data providers to enable a decentralized 
network of Data Object Services.

## Metrics of success

What data are available by DOS?

How easy is it to publish new data using a Data Object Service?

What supporting software uses the Data Object Service?

What is the support status of the various public DOS endpoints?

## Milestones

### Compliance Testing and Documentation

Develop a unified and extensible testing framework for evaluating the behavior of a DOS
instance. Develop a plan for extending and making it more useful. Document the various 
levels of compliance and what application use cases are served by each.

### Workflow Output and Provisioning

Develop solutions for handling the registration and management of workflow outputs into 
a DOS.

### Authentication Metadata

Add authentication metadata to DOS schemas as needed. Present practical solutions for
private and access controlled data.

### Visualization Components and Browser

Develop reusable components that interact with a DOS that can be assembled into a browser. 
Create examples of integating DOS into existing frontend software by presenting a minimal 
JavaScript library.

### Network Level Operations

Develop network level metadata entries into DOS schemas as needed. Present identifier 
resolution provenance in responses and improve error responses to support decentralized 
resolution. Develop plan for automating peer discovery.

## Timeline

### September 2018

Use existing compliance tests to improve testing status on existing DOS installations. Add test 
coverage to compliance tests to cover existing features. Add authentication metadata and tests 
in the demo server using HTTP basic auth for downloading a URL.

### October 2018

Document compliance tests and expose test results for public endpoints in a public place. Document
compliance levels. Integrate latest schemas/client work into DOS connect. Bring existing DOS 
installations to latest schemas.

Add network level metadata to responses.

### November 2018

Improve testing of dos_connect and demonstrate URL signing feature. Release DOS connect for 
workflow output handling. Create tests that demonstrate network resolution.

### December 2018

Maintain dos_connect release, improve supporting apps for indexing various cloud stores.

### January 2019

Develop basic components for rendering DOS responses. Begin integrating components into a frontend
webapp.

### February 2019

Wireframe frontend app for browsing DOS network. Develop a filterable table interface for 
objects and bundles.

### March 2019

Add documentation to schemas for creating namespaced resolution. Create dos_connect configuration 
for using namespaces. Create a demonstration network.

### April 2019

Integrate dos_connect and browser components to improve usability of network services and 
data management operations. Demonstrate replication and federated resolution.
