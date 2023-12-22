## Card Status API Documentation

### Introduction

The Card Status API is designed to provide information about the current status of a user's card based on the phone number or card ID. It uses a SQLite database to store and manage card status data, and it exposes an endpoint (`/get_card_status`) to query this information.

### Endpoints

#### 1. `/get_card_status` (GET)

##### Request

- **Parameters:**
  - `identifier` (required): The user's phone number or card ID.

##### Response

- **Success (200 OK):**
  - Returns a JSON object with the card status:
    ```json
    {
      "status": "Delivered"
    }
    ```

- **Error (400 Bad Request):**
  - If the `identifier` parameter is missing:
    ```json
    {
      "error": "Identifier is required"
    }
    ```

- **Error (404 Not Found):**
  - If the card with the specified identifier is not found:
    ```json
    {
      "error": "Card not found"
    }
    ```

### Data Storage

#### 1. `card_status` Table

- **Columns:**
  - `id`: Unique identifier for the card (may contain alphanumeric values).
  - `card_id`: Card identifier.
  - `phone_number`: User's phone number.
  - `timestamp`: Timestamp of the card status update.
  - `status`: Current status of the card.

### Implementation Details

#### 1. Database Connection

- The SQLite database connection is managed using the Flask `g` object.
- Database connection is closed upon application context teardown.

#### 2. Initialization

- The database table (`card_status`) is created if it does not exist during application initialization.

#### 3. Data Population

- CSV files containing card status information are read and processed to populate the `card_status` table.
- Alphanumeric values are supported for the `id` column.
- Existing records are updated, and new records are inserted.

#### 4. Status Retrieval

- Card status can be retrieved based on either phone number or card ID using a case-insensitive `LIKE` query.

### Usage

1. Run the script to start the Flask application.
2. Access the `/get_card_status` endpoint with the appropriate `identifier` parameter to get the card status.

Example:

```bash
curl -X GET "http://localhost:5000/get_card_status?identifier=A883"
```

### Dependencies

- Flask: Web framework for building the API.
- SQLite: Lightweight relational database management system.
- Enum: Used for representing different card statuses.

### Notes

- Ensure that the required CSV files are stored in the "data" folder.
- Modify the CSV file format as needed based on the provided samples.
- Adjust the script for production use, considering security and scalability aspects.
