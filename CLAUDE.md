# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains the GA4GH Data Repository Service (DRS) API specification. DRS is an OpenAPI 3.0 specification that provides a generic interface to data repositories, enabling data consumers (including workflow systems) to access data in a standardized way regardless of storage location or management approach.

## Build and Validation Commands

```bash
# Install required tools
npm install -g @redocly/openapi-cli
npm install -g redoc-cli
npm install -g @ga4gh/gh-openapi-docs@0.2.2-rc3

# Validate OpenAPI specification
openapi-cli lint openapi/data_repository_service.openapi.yaml

# Build documentation locally
gh-openapi-docs

# Preview documentation
# After building, open public/docs/index.html in a browser
```

## OpenAPI Architecture

The OpenAPI specification is split across multiple files for maintainability:

### Main Specification File
- `openapi/data_repository_service.openapi.yaml` - Root OpenAPI spec (version 1.5.0)
  - Defines API metadata, servers, security schemes, and tags
  - Uses `$ref` to reference components and paths

### Component Organization
All reusable components are in `openapi/components/`:

- `schemas/` - Data models (DrsObject, AccessMethod, Checksum, etc.)
- `paths/` - Endpoint definitions (use `@` instead of `/` in filenames)
  - Example: `objects@{object_id}.yaml` = `/objects/{object_id}` endpoint
- `parameters/` - Reusable parameters (ObjectId, AccessId, etc.)
- `requestBodies/` - Request body definitions
- `responses/` - Response definitions (200OkDrsObject, 404NotFoundDrsObject, etc.)

### Documentation Tags
- `openapi/tags/` - Markdown files providing detailed documentation sections
  - Referenced in main spec via `$ref` in tag descriptions
  - Examples: Introduction.md, Auth.md, CompactIdentifierBasedURIs.md

## Key DRS Concepts

### DRS Objects
Two types of objects:
1. **Blobs** - Individual data files with access methods
2. **Bundles** - Collections of DrsObjects (may contain nested bundles)

### Core Operations
- **Read Operations**: GET/POST `/objects/{object_id}` - Retrieve object metadata and access methods
- **Access Methods**: GET/POST `/objects/{object_id}/access/{access_id}` - Get download URLs
- **Upload Operations** (optional): POST `/upload-request` + POST `/objects/register`
- **Update Operations** (optional): PATCH endpoints for access methods
- **Delete Operations** (optional): POST `/objects/{object_id}/delete` or bulk delete
- **Service Info**: GET `/service-info` - Standard GA4GH service info endpoint

### Bulk Operations
DRS 1.4.0+ supports bulk operations for performance:
- POST `/objects/access` - Bulk access URL retrieval
- POST `/objects/access-methods` - Bulk access method updates
- POST `/objects/delete` - Bulk deletion

## Branching and Development Workflow

This project follows **HubFlow** (Git Flow):

- `master` - Production releases only
- `develop` - Stable development branch (default target for PRs)
- `feature/issue-<number>-<description>` - Feature branches

**IMPORTANT**: Always create pull requests to `develop`, never to `master`.

### Feature Branch Workflow
1. Create GitHub issue to track work
2. Create feature branch: `feature/issue-<number>-<description>`
3. Travis CI automatically builds feature branches
4. Preview docs at: `https://ga4gh.github.io/data-repository-service-schemas/preview/<branch-name>/docs/`
5. Create PR to `develop` (not `master`)

## Documentation Build System

Documentation is automatically built and deployed via Travis CI using `gh-openapi-docs`:

- **Configuration**: `.spec-docs.json` defines build targets
- **Main docs**: Built from `openapi/data_repository_service.openapi.yaml`
- **Additional pages**: Built from `pages/` directory
- **Output**: HTML + OpenAPI YAML/JSON published to GitHub Pages

Preview URLs for non-master branches:
- Docs: `https://ga4gh.github.io/data-repository-service-schemas/preview/<branch>/docs/`
- Spec (YAML): `https://ga4gh.github.io/data-repository-service-schemas/preview/<branch>/openapi.yaml`
- Spec (JSON): `https://ga4gh.github.io/data-repository-service-schemas/preview/<branch>/openapi.json`

## Code Style Conventions

- Use 2-space indentation (no tabs)
- Hard-wrap code to 80 characters per line
- Follow OpenAPI 3.0 best practices
- Use `$ref` for reusable components
- Path filenames: Use `@` instead of `/` (e.g., `objects@{object_id}.yaml`)

## URI Schemes

DRS supports two URI schemes for identifying objects:
1. **Hostname-based**: `drs://drs.example.org/object_id`
2. **Compact identifier-based**: `drs://dg.4503:dg.4503/cc32d93d-a73c-4d2c-a061-26c0410e74fa`

See tags documentation for detailed URI resolution guidance.

## Version History

Current version: 1.5.0
- 1.5.0: Cold storage fields, explicit cloud locations, object count/size metadata, Data Connect integration
- 1.4.0: Bulk operations
- 1.3.0: OPTIONS method for auth issuer discovery
- 1.2.0: POST endpoints for large passport tokens, `/service-info` endpoint
- 1.1.0: Compact identifier URI convention
- 1.0.0: Approved GA4GH standard
