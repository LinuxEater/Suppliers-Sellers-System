# Vendedores-Fornecedores System

This is a Django-based system designed for managing products, suppliers, vendors, and sales. It provides a comprehensive platform for tracking inventory, sales performance, and vendor/supplier relationships.

## Features

The system includes the following key features:

*   **Product Management**: Comprehensive management of products, including details like product code, name, description, pricing, stock levels, and images.
*   **Supplier Management**: Track and manage information about product suppliers.
*   **Vendor Management**: Manage vendor profiles, including contact details and associated sales.
*   **Sales Tracking**: Record and monitor sales transactions, linking them to products and vendors.
*   **Stock History**: Detailed logging of all stock changes for each product.
*   **Low Stock Notifications**: Automated email notifications when product stock falls below a predefined threshold.
*   **Bulk Import/Export for Products**: Easily import and export product data via the Django admin panel using `django-import-export`.
*   **Vendor-Specific Dashboards**: Dedicated dashboards for each vendor, providing insights into their sales performance.
*   **Supplier Performance Tracking**: Dedicated dashboards for each supplier, showing their product and sales performance.
*   **REST API**: A robust RESTful API built with Django REST Framework for programmatic access to Product, Supplier, Vendor, and Sale data, including advanced filtering.
*   **Advanced Search & Filtering**: Enhanced search and filtering capabilities for API endpoints using `django-filter`.
*   **AI Chatbot**: An integrated AI chatbot, powered by Google Gemini, to assist users with system-related queries, accessible as a floating widget across the application.

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/LinuxEater/vendedores-fornecedores.git
    cd vendedores-fornecedores
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv env
    # On Windows
    .\env\Scripts\activate
    # On macOS/Linux
    source env/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000/`.

## Usage

*   **Admin Panel**: Access the Django administration interface at `http://127.0.0.1:8000/admin/` to manage products, suppliers, vendors, and sales.
*   **Dashboard**: View the main dashboard at `http://127.0.0.1:8000/dashboard/`.
*   **Vendor/Supplier Dashboards**: Access specific dashboards from the respective admin lists.
*   **REST API**: Interact with the API endpoints at `http://127.0.0.1:8000/api/`.
*   **Chatbot**: The AI chatbot is available as a floating icon on all pages. Click it to open the chat interface.

## API Endpoints

The following API endpoints are available:

*   `/api/products/`: List and create products.
*   `/api/products/<uuid:pk>/`: Retrieve, update, and delete a specific product.
*   `/api/suppliers/`: List and create suppliers.
*   `/api/suppliers/<int:pk>/`: Retrieve, update, and delete a specific supplier.
*   `/api/vendors/`: List and create vendors.
*   `/api/vendors/<int:pk>/`: Retrieve, update, and delete a specific vendor.
*   `/api/sales/`: List and create sales.
*   `/api/sales/<int:pk>/`: Retrieve, update, and delete a specific sale.

All API endpoints support advanced filtering using query parameters (e.g., `/api/products/?name=example&min_stock=5`).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact Moisés Souza Santos:
*   Email: [moisessouzasantos001gmail.com](mailto:moisessouzasantos001gmail.com)
*   WhatsApp: +55 38 99818-9765