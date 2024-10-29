# Ship Database Application

This is a simple Flask application for managing a database of ships. The application allows users to view, add, edit, and delete ship records.

## Features

- **View Ships**: Display a list of ships with pagination and filtering options.
- **Add Ship**: Upload new ship records to the database.
- **Edit Ship**: Modify existing ship records.
- **Delete Ship**: Remove ship records from the database.
- **Error Handling**: Custom 404 error page.

## Technologies Used

- **Flask**: A micro web framework for Python.
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Flask-Migrate**: A Flask extension that handles SQLAlchemy database migrations.
- **SQLite**: A lightweight, disk-based database.

## Usage

### View Ships

- Navigate to the home page to view a list of ships.
- Use the search bar to filter ships by name or type.
- Pagination is available to navigate through the list of ships.

### Add Ship

- Click on the "Upload" link to add a new ship.
- Fill in the form with the ship's details and submit.

### Edit Ship

- Click on the "Edit" link next to a ship to modify its details.
- Update the form and submit to save changes.

### Delete Ship

- Click on the "Delete" link next to a ship to remove it from the database.
- Confirm the deletion on the confirmation page.

## Database Schema

The application uses a SQLite database with the following schema for the `Ship` model:

- `id`: Integer, primary key.
- `name`: String, unique and not null.
- `type`: String, not null.
- `year_built`: Integer, not null.
- `description`: String, not null.
- `image_url`: String, not null.
- `short_description`: String, not null.
- `is_active`: Boolean, default is True.
- `wikipedia_link`: String, not null.
- `country_of_origin`: String, not null.
