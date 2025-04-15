# Service Consolidation Plan

## Current Backend Structure
The backend is currently divided into many microservices:
- ai_assistant
- billing (already consolidated)
- calendar_dynamodb
- call_manager
- company_docs_s3
- messages_dynamodb
- patient_docs_s3
- payments (already consolidated)

## Proposed Consolidation
We can consolidate these services further into just 3-4 core modules:

1. **User Management Module**
   - Authentication
   - Authorization
   - User profiles
   - Role management

2. **Patient Records Module**
   - Patient information
   - Documents/files (combine patient_docs_s3 and company_docs_s3)
   - Visit history
   - Notes and transcriptions

3. **Clinical Operations Module**
   - Calendar and appointments (from calendar_dynamodb)
   - Messaging (from messages_dynamodb)
   - Call management (from call_manager)
   - AI Assistance (from ai_assistant)

4. **Financial Module** (already consolidated)
   - Payments
   - Billing
   - Insurance
   - Reporting

## Benefits
- Reduced code duplication
- Clearer module boundaries
- Simplified codebase structure
- Easier maintenance and development
- More efficient database operations

## Implementation Strategy
1. Create new module directories
2. Migrate functionality from existing services
3. Refactor database access to use shared utilities
4. Update API endpoints
5. Update frontend service calls
6. Remove redundant services
