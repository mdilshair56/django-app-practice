## Updates – 30 October 2026

### 1. Polls API – Filtering, Search, Ordering and Pagination

Implemented filtering, searching, ordering and pagination functionality for the Polls API using Django REST Framework and `django-filter`.

**Filtering**
- Filter polls by status (`draft`, `in_progress`, `completed`).
- Filter by result visibility (`live`, `after_submission`, `polls_end`, `restricted`).
- Filter polls by creation, starting and ending dates/times.
- Date filters support ISO 8601 date/time values.

**Search**
- Search polls by name.
- Search polls by description.
- Uses DRF's built-in `SearchFilter`.

**Ordering**
- Order polls by name.
- Order by creation date.
- Order by starting date.
- Order by ending date.
- Supports ascending and descending ordering using the `-` prefix.

**Pagination**
- Implemented using DRF's built-in `PageNumberPagination`.
- Default page size: 10 polls.
- Supports custom page size using `page_size`.
- Maximum allowed page size: 100.
- Returns pagination metadata, including total count, current page, next page, previous page and total pages.

### 2. Generic ViewSet Implementation

Updated `PollViewSet` to use DRF's `GenericViewSet` with:
- `ListModelMixin` for retrieving all polls.
- `RetrieveModelMixin` for retrieving an individual poll.
- Existing custom `create()` action for creating polls.

Also configured:
- `DjangoFilterBackend`
- `SearchFilter`
- `OrderingFilter`
- `PollPagination`

Used `select_related()` and `prefetch_related()` to efficiently retrieve related poll creators, questions and answer options.

### 3. Common API Response Wrappers

Created reusable success-response functions inside the `common/api/` directory.

- `success_response()`: Provides a consistent success-response structure.
- `paginated_success_response()`: Provides a consistent response structure with pagination metadata.

These wrappers are currently connected to the Polls API.

### 4. Files Created

| File | Purpose |
|---|---|
| `common/api/__init__.py` | Exports common API response functions. |
| `common/api/responses.py` | Contains reusable success and paginated response wrappers. |
| `polls/filters.py` | Defines Poll-specific filtering parameters. |
| `polls/pagination.py` | Configures Poll pagination using DRF's built-in pagination class. |

### 5. Files Updated

| File | Changes |
|---|---|
| `core/settings.py` | Corrected `django-filters` to `django_filters` in `INSTALLED_APPS`. |
| `polls/views/poll.py` | Integrated GenericViewSet, filtering, search, ordering, pagination and common response wrappers. |

### 6. Available API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/polls/` | Create a poll. |
| GET | `/api/polls/` | Retrieve and paginate polls. |
| GET | `/api/polls/<id>/` | Retrieve a specific poll. |

### 7. Available Query Parameters

| Parameter | Purpose |
|---|---|
| `status` | Filter by poll status. |
| `result_visibility` | Filter by result visibility. |
| `created_after` | Filter by creation date (greater than or equal to). |
| `created_before` | Filter by creation date (less than or equal to). |
| `starts_after` | Filter by starting date (greater than or equal to). |
| `starts_before` | Filter by starting date (less than or equal to). |
| `ends_after` | Filter by ending date (greater than or equal to). |
| `ends_before` | Filter by ending date (less than or equal to). |
| `search` | Search poll names and descriptions. |
| `ordering` | Sort polls by supported fields. |
| `page` | Select the page number. |
| `page_size` | Specify the number of polls per page. |

**Example request:**

`GET /api/polls/?status=in_progress&result_visibility=live&search=election&ordering=-created_at&page=1&page_size=5`

### 8. Testing and Verification

The following checks were successfully performed:

- Django system check: Passed.
- Python compilation: Passed.
- Migration check: No changes detected.
- Poll list endpoint: HTTP 200.
- Poll detail endpoint: HTTP 200.
- Status and visibility filtering: Verified.
- Combined filtering, search and ordering: Verified.
- Pagination and custom page size: Verified.
- Invalid filter values: Correctly returned HTTP 400.
- Date/time filter validation: Passed.

No database model changes or migrations were required.

### 9. Current Scope

The work completed in this update focuses on Poll creation and retrieval, filtering, searching, ordering and pagination.

The voting workflow and poll ownership/visibility restrictions are separate tasks and are not included in this update.

No files inside the `auth/` application were modified.
