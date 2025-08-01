# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains the GA4GH Data Repository Service (DRS) API schema definitions. DRS provides a generic interface to data repositories, allowing data consumers to access data in a standardized way regardless of where it's stored. The API defines a system for mapping logical IDs to means for physically retrieving data.

## Development Commands

### Documentation Building
```bash
# Install required tools
npm install -g @redocly/openapi-cli redoc-cli
npm install -g @ga4gh/gh-openapi-docs@0.2.2-rc3

# Build documentation (used in CI)
gh-openapi-docs
```

### OpenAPI Validation
```bash
# Validate OpenAPI specification
openapi-cli validate openapi/data_repository_service.openapi.yaml
```

## Architecture & Structure

### Core Components

- **`openapi/data_repository_service.openapi.yaml`**: Main OpenAPI 3.0.3 specification file
- **`openapi/components/`**: Reusable OpenAPI components organized by type:
  - `schemas/`: Core data models (DrsObject, AccessMethod, AccessURL, etc.)
  - `responses/`: Standard HTTP response definitions
  - `parameters/`: Reusable path/query parameters
  - `paths/`: API endpoint definitions
- **`openapi/tags/`**: Markdown documentation files for API sections

### Key Data Models

- **DrsObject**: Core entity representing a data object with metadata, checksums, and access methods
- **AccessMethod**: Defines how to access data (s3, gs, https, file, etc.) with URLs or access IDs
- **AccessURL**: Contains the actual URL and optional headers for data retrieval
- **Checksum**: Data integrity verification information

### API Endpoints Structure

- `/objects/{object_id}`: GET/POST/OPTIONS for object metadata
- `/objects/{object_id}/access/{access_id}`: GET/POST for access URLs
- `/bulkobjects/{object_id}`: Bulk operations for multiple objects
- `/service-info`: Service metadata endpoint

## Development Workflow

### Branch Strategy (HubFlow)

- **`master`**: Production releases only
- **`develop`**: Stable development branch (all PRs target this)
- **Feature branches**: `feature/issue-<number>-<description>`
- **Release branches**: `release/<version>` or `release/drs-<version>`

### Making Changes

1. Create issue in GitHub to track work
2. Create feature branch from `develop` following naming convention
3. Make changes to OpenAPI YAML files
4. Travis CI will automatically build and validate on push
5. Submit PR to `develop` branch
6. PRs require review and driver project voting for approval

### File Organization

- OpenAPI components are split into separate YAML files for maintainability
- Documentation is embedded in markdown files referenced from the main spec
- All schema changes must include proper documentation updates

## CI/CD Pipeline

- **Travis CI** builds documentation and validates OpenAPI spec
- **GitHub Pages** deployment for documentation hosting
- Preview builds available for all feature branches at: `ga4gh.github.io/data-repository-service-schemas/preview/<branch-name>/`
- Production docs at: `ga4gh.github.io/data-repository-service-schemas/docs/`

## Validation & Standards

- OpenAPI 3.0.3 specification compliance required
- Two-space indentation, no tabs
- 80-character line limit
- All new schemas require normative documentation
- Security considerations must be documented for any auth-related changes