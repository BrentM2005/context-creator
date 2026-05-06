import re
import os
import platform
from pathlib import Path

def _get_app_data_dir():
    home = Path.home()
    system = platform.system()
    if system == "Windows":
        base = os.getenv("APPDATA", str(home / "AppData" / "Roaming"))
        return Path(base) / "ContextCreator"
    elif system == "Darwin":
        return home / "Library" / "Application Support" / "ContextCreator"
    else:
        base = os.getenv("XDG_CONFIG_HOME", str(home / ".config"))
        return Path(base) / "ContextCreator"

APP_DIR = _get_app_data_dir()
APP_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = str(APP_DIR / "codebase_context_config.json")

IGNORED_DIRS = {
    'node_modules', '.git', '.venv', 'venv', 'env', '__pycache__',
    'build', 'dist', '.idea', '.vscode', 'coverage', '.next', 'out',
    '.svelte-kit', '.nuxt', 'logs', 'tmp', 'temp', 'target', 'bin',
    '.cache', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    '.tox', '.nox', '.hypothesis', '.turbo', '.parcel-cache', 
    '.sass-cache', 'obj', '.terraform', '.serverless', '.aws-sam', 
    'vendor', '.history'
}

IGNORED_FILES = {
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'poetry.lock',
    'Pipfile.lock', 'project_lock.json', '.DS_Store', 'Thumbs.db',
    'bun.lockb', 'Cargo.lock', 'Gemfile.lock', 'composer.lock',
    '.gitignore', '.eslintignore', '.prettierignore', '.env', 
    '.env.local', '.env.production', '.env.development', '.env.test',
    '.coverage', 'coverage-final.json', 'npm-debug.log', 
    'yarn-error.log', 'pnpm-debug.log', '.ipynb_checkpoints'
}

IGNORED_EXTENSIONS = {
    '.json', '.yml', '.yaml', '.xml', '.csv', '.tsv', '.sql',
    '.sqlite', '.db', '.md', '.d', '.wasm', '.pyc', '.pyo', '.o', 
    '.obj', '.class', '.dll', '.so', '.exe', '.bin', '.a', '.lib', 
    '.jar', '.log', '.cache', '.pem', '.key', '.cert', '.crt', 
    '.p12', '.pfx', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
    '.webp', '.avif', '.bmp', '.tiff', '.pdf', '.docx', '.doc', 
    '.xlsx', '.xls', '.pptx', '.ppt', '.mp3', '.wav', '.ogg', 
    '.flac', '.mp4', '.mov', '.avi', '.mkv', '.webm', '.zip', 
    '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar', '.woff', '.woff2', 
    '.ttf', '.eot', '.otf', '.map'
}

EXT_TO_LANG = {
    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
    '.jsx': 'JavaScript (JSX)', '.tsx': 'TypeScript (TSX)',
    '.html': 'HTML', '.css': 'CSS', '.scss': 'Sass', '.less': 'Less',
    '.java': 'Java', '.cpp': 'C++', '.cc': 'C++', '.cxx': 'C++', '.c': 'C', '.h': 'C/C++ Header', '.hpp': 'C++ Header',
    '.cs': 'C#', '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby',
    '.php': 'PHP', '.swift': 'Swift', '.kt': 'Kotlin',
    '.sh': 'Shell/Bash', '.sql': 'SQL', '.vue': 'Vue', '.svelte': 'Svelte',
    '.dart': 'Dart', '.m': 'Objective-C', '.scala': 'Scala', '.r': 'R',
    '.lua': 'Lua', '.pl': 'Perl', '.asm': 'Assembly'
}

SECRET_PATTERNS =[
    re.compile(r'(?i)(?:api_key|apikey|secret|token|password|passwd|pwd)\s*[=:]\s*[\'"]?([a-zA-Z0-9_\-]{16,})[\'"]?'),
    re.compile(r'(?i)(?:bearer\s+)([a-zA-Z0-9_\-\.]{20,})'),
    re.compile(r'(?i)(?:ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59})')
]

ENTRYPOINT_NAMES = {
    'main.py', 'app.py', 'index.js', 'index.ts', 'server.js', 
    'server.ts', 'main.go', 'main.rs', 'program.cs'
}

PROMPT_PACK_TEMPLATES =[
    ("Explain Architecture", "Analyze the provided codebase context and provide a comprehensive explanation of its overall architecture. Identify the core architectural patterns, data flow, and how the major components interact."),
    ("Find Bugs & Vulnerabilities", "Review the provided codebase for potential bugs, edge cases, and security vulnerabilities. Highlight risky practices, unhandled exceptions, or potential performance bottlenecks."),
    ("Suggest Refactors", "Identify areas of the provided codebase that could benefit from refactoring. Suggest improvements for code readability, maintainability, and adherence to DRY/SOLID principles."),
    ("Add Tests", "Based on the codebase context, identify critical business logic or complex functions that lack coverage. Generate unit test templates for these components using the standard testing framework for the respective languages."),
    ("Improve Performance", "Analyze the codebase for performance inefficiencies. Suggest optimizations related to time complexity, memory management, database queries, or concurrent processing."),
    ("Security Review", "Conduct a security audit of the provided codebase. Look for hardcoded secrets, injection vulnerabilities, improper access controls, and suggest mitigations following OWASP guidelines.")
]

DOC_TEMPLATES = {
    "Professional README": """You are an expert technical writer and open-source maintainer. I will provide you with the codebase context for my project.

Please write an elite-level, highly polished README.md for this project. Use the following strict guidelines:

1. **Header & Badges**: Start with an eye-catching title. Directly below it, generate markdown for Shield.io badges (e.g., Build Status, Version, License, Main Frameworks/Languages).
2. **Elevator Pitch**: A concise, impactful paragraph explaining what the project does, why it exists, and the primary problem it solves.
3. **Features Matrix**: Use a bulleted list or markdown table to highlight the core capabilities. Use emojis appropriately to make it scannable.
4. **Tech Stack**: List the primary technologies, frameworks, and libraries used.
5. **Quick Start Guide**: Provide the exact commands needed to get this running locally (Clone, Install dependencies, Run/Build).
6. **Configuration / Environment**: List the required `.env` variables and what they do.
7. **Architecture Snippet**: A brief 2-3 sentence overview of how the codebase is structured.
8. **Testing**: How to run the automated tests.
9. **Contributing**: Clear, welcoming instructions for external contributors.
10. **License**: Mention the project's license.

Ensure the tone is highly professional, inspiring confidence in the software's stability and design.""",

    "Architecture Document": """You are a Principal Software Architect. I will provide you with the codebase context for my project.

Please draft a comprehensive High-Level Architecture (HLA) Document. Structure the document to be consumed by other senior engineers and stakeholders:

1. **Executive Summary**: The purpose of the system and its overarching architectural pattern (e.g., Event-Driven, Microservices, MVC, Hexagonal).
2. **System Context**: Describe the system's boundaries. Who are the users? What external systems does it interact with?
3. **Mermaid.js Diagram**: Generate a ````mermaid ... ```` code block illustrating the core data flow and component interactions.
4. **Core Components**: Break down the main directories/modules. For each component, define its:
   - **Responsibility**: What domain logic does it own?
   - **Dependencies**: What other internal components does it rely on?
5. **Data Management**: How is state managed? Describe databases, caches, and data schemas derived from the code.
6. **Cross-Cutting Concerns**: 
   - **Authentication/Authorization**: How is security handled?
   - **Error Handling & Logging**: What is the standard pattern used in the code?
7. **Trade-offs & Technical Debt**: Based on your code analysis, note any apparent architectural compromises or areas ripe for future refactoring.

Maintain a deeply technical, analytical, and authoritative tone.""",

    "API Reference": """You are a Senior Developer Relations (DevRel) Engineer. I will provide you with the codebase context for my API project.

Please generate an exhaustive, developer-friendly API Reference Document. Use standard OpenAPI/Swagger conceptual structuring:

1. **API Overview**: Base URL, content types (e.g., `application/json`), and general conventions.
2. **Authentication**: Explain the auth mechanism (e.g., Bearer tokens, API keys, OAuth) based on the code's middleware/security configuration.
3. **Rate Limiting & Pagination**: If applicable, explain how list endpoints are paginated and if rate limits are enforced.
4. **Endpoints**: For every distinct API route found in the codebase, provide:
   - **Endpoint**: e.g., `GET /api/v1/users/{id}`
   - **Description**: What it does.
   - **Request Headers / Parameters**: Required vs Optional parameters, with data types.
   - **cURL Example**: A realistic copy-pasteable cURL command.
   - **Success Response (200/201)**: A JSON payload example inferred from the codebase models/serializers.
   - **Error Responses (400, 401, 403, 404, 500)**: Common failure scenarios and their standard JSON error payloads.
5. **Webhooks / Events (If applicable)**: Document any outgoing payloads.

Ensure the documentation is clean, uses tables for parameters, and syntax-highlighted blocks for code.""",

    "Developer Onboarding Guide": """You are an Engineering Manager. I will provide you with the codebase context for my project.

Please create a "Zero to Hero" Developer Onboarding Guide meant for a new engineer joining the team today. Make it frictionless and encouraging:

1. **Welcome & Mission**: A brief welcome and the core philosophy of the project.
2. **Prerequisites**: A checklist of software to install (e.g., Docker, Node v18+, Python 3.11).
3. **Local Environment Setup**: 
   - Step-by-step terminal commands.
   - How to seed the database or mock third-party services.
4. **Project Structure 101**: A guided tour of the codebase. Explain *where* a new developer should look for models, controllers, UI components, and utilities.
5. **Development Workflow**:
   - Branching strategy (e.g., feature/branch-name).
   - Code formatting and linting commands.
   - How to run tests before committing.
6. **Common "Gotchas"**: Identify 2-3 complex or confusing parts of the codebase that a new developer might stumble over.
7. **Your First PR**: Suggestions for what a good first task looks like in the context of this architecture.

Use a supportive, clear, and structured format using checkboxes `- [ ]` where appropriate.""",

    "Testing & QA Strategy": """You are a QA Architect. I will provide you with the codebase context for my project.

Please draft a Comprehensive Testing Strategy and QA Guidelines document based on the existing test files, frameworks, and business logic:

1. **Testing Philosophy**: Summary of the project's approach to testing (e.g., TDD, BDD, Test Pyramid).
2. **Frameworks & Tools**: List the primary testing tools found in the code (e.g., PyTest, Jest, Cypress, Playwright).
3. **Unit Testing Guide**: 
   - Where tests are located.
   - Naming conventions.
   - How to mock dependencies/database calls based on current codebase patterns.
4. **Integration/E2E Testing**: How to test components working together.
5. **Running Tests**: 
   - Commands to run the full suite.
   - Commands to run specific test files or tags.
   - How to generate and view coverage reports.
6. **CI/CD Integration**: Explain how tests are expected to be run in the deployment pipeline.
7. **Missing Coverage**: Provide a brief analysis of critical files or modules that currently appear to lack sufficient testing.""",

    "Production Deployment Guide": """You are a Lead DevOps Engineer. I will provide you with the codebase context for my project.

Please write a highly secure and professional Production Deployment Guide/Runbook:

1. **Infrastructure Overview**: Summarize the deployment environment based on codebase artifacts (e.g., Dockerfiles, Terraform, Kubernetes manifests, AWS SAM).
2. **Build Process**: The exact steps/commands to compile, build, or bundle the application for production.
3. **Environment Variables**: A strict table of required production environment variables. DO NOT output actual secrets, but define what they represent.
4. **Database Migrations**: How to safely apply database schema changes in a production environment.
5. **Deployment Steps**: A step-by-step runbook for rolling out a new version with minimal downtime.
6. **Rollback Procedure**: Exactly what to do if the deployment fails.
7. **Health Checks & Monitoring**: How to verify the application is running smoothly post-deployment (referencing any health check endpoints in the code).

Tone should be rigorous, cautious, and exact, as expected in a high-stakes Ops environment.""",

    "User Guide": """You are an expert Technical Writer specializing in end-user documentation. I will provide you with the codebase context for my project.

Please create a comprehensive, easy-to-understand User Guide. Focus entirely on how an end-user interacts with the software, ignoring the underlying code. Structure it as follows:

1. **Introduction**: A non-technical overview of what the application does and the value it provides to the user.
2. **Core Concepts**: A glossary of terms or key concepts the user needs to understand to use the system effectively.
3. **Getting Started**: Initial setup, account creation, or first login steps.
4. **Key Workflows**: Break down the primary use cases into step-by-step instructions. Use bolding for UI elements (e.g., "Click the **Submit** button").
5. **FAQ & Troubleshooting**: Common user-facing errors (inferred from the codebase's error messages/UI) and how to resolve them.

Keep the tone helpful, highly professional, and perfectly accessible to non-developers.""",

    "Administrator Guide": """You are a Senior Systems Administrator and Technical Writer. I will provide you with the codebase context for my project.

Please generate an exhaustive Administrator Guide intended for IT, Ops, or SysAdmins who will manage and maintain the software. Structure it with these exact sections:

1. **System Overview**: High-level operational view of the platform.
2. **Configuration & Environment**: Detailed explanation of all configuration files, environment variables, and feature flags found in the codebase.
3. **User & Roles Management**: How permissions, RBAC (Role-Based Access Control), and user life-cycles are handled within the system.
4. **Data Management & Backups**: Where data is stored, cache clearing procedures, and backup/restore protocols based on the architecture.
5. **Monitoring & Logging**: Log file locations, log formatting, and key metrics to monitor (inferred from logging frameworks used in the code).
6. **Security & Compliance**: Audit logs, key rotation, and internal security mechanisms.
7. **Troubleshooting & Maintenance**: Known operational bottlenecks, health check endpoints, and recovery steps.

Use a highly technical, authoritative tone suitable for IT professionals.""",

    "GitHub Issue Creator": """You are a meticulous QA Engineer and Open Source Maintainer. I will provide you with the codebase context for my project, along with a custom description of a bug or feature.

**User Request:**[INSERT YOUR BUG OR FEATURE DESCRIPTION HERE]

Based on my request and the codebase context, draft a professional, ready-to-post GitHub Issue. Cross-reference my request with the code to provide deep technical insight. Use the following structure:

1. **Descriptive Title**: Clear and concise.
2. **Overview**: A summary of the issue or feature request.
3. **Steps to Reproduce (for bugs)** or **Use Case (for features)**.
4. **Expected vs. Actual Behavior** (if a bug).
5. **Technical Context**: Identify exactly which files, classes, or functions are likely responsible or need modification. Include brief code snippets or line references from the provided context.
6. **Proposed Solution**: Suggest a high-level technical fix or implementation strategy based on the existing architectural patterns in the codebase.
7. **Impact/Severity**: Assess how critical this is.

Ensure the issue is highly actionable for any developer picking it up.""",

    "Jira Ticket Creator": """You are an Agile Product Owner and Lead Engineer. I will provide you with the codebase context, plus a specific bug or feature request.

**User Request:**[INSERT YOUR TICKET DESCRIPTION HERE]

Please draft a comprehensive Jira ticket that perfectly bridges product requirements with technical implementation details. Structure it as follows:

1. **Summary**: A concise, standard Jira title (e.g., "Implement...", "Fix...").
2. **User Story**: "As a [role], I want [feature/fix] so that [benefit]."
3. **Background / Context**: Why this is needed, referencing existing system behavior.
4. **Acceptance Criteria**: Strict BDD format (Given / When / Then).
5. **Technical Details**:
   - **Affected Components**: List the specific files, database models, or API endpoints involved (derived from the codebase context).
   - **Implementation Notes**: Suggestions on *how* to build or fix this using the current tech stack and patterns.
   - **Out of Scope**: What should *not* be included in this ticket.
6. **Testing Requirements**: Specific unit, integration, or manual tests that must be written/performed.
7. **Estimated Effort / Story Points**: Provide a suggested Fibonacci point estimate (1, 2, 3, 5, 8) with a brief justification based on the codebase complexity."""
}